import math
import faiss
import json
import pickle
import torch
import logging

from sentence_transformers import SentenceTransformer
from constants import *
import numpy as np

logging.getLogger().setLevel(logging.INFO)


class VectorIndex:
    def __init__(self, d):
        self.d = d
        self.vectors = []
        self.index = None

    def add(self, v):
        self.vectors.append(v)

    def build(self, use_gpu=False):
        self.vectors = np.array(self.vectors)

        faiss.normalize_L2(self.vectors)

        logging.info('Indexing {} vectors'.format(self.vectors.shape[0]))

        if self.vectors.shape[0] > 50000:
            num_centroids = 8 * \
                int(math.sqrt(
                    math.pow(2, int(math.log(self.vectors.shape[0], 2)))))

            logging.info('Using {} centroids'.format(num_centroids))

            self.index = faiss.index_factory(
                self.d, "IVF{}_HNSW32,Flat".format(num_centroids))

            ngpu = faiss.get_num_gpus()
            if ngpu > 0 and use_gpu:
                logging.info('Using {} GPUs'.format(ngpu))

                index_ivf = faiss.extract_index_ivf(self.index)
                clustering_index = faiss.index_cpu_to_all_gpus(
                    faiss.IndexFlatL2(self.d))
                index_ivf.clustering_index = clustering_index

            logging.info('Training index...')

            self.index.train(self.vectors)
        else:
            self.index = faiss.IndexFlatL2(self.d)
            if faiss.get_num_gpus() > 0 and use_gpu:
                self.index = faiss.index_cpu_to_all_gpus(self.index)

        logging.info('Adding vectors to index...')

        self.index.add(self.vectors)

    def load(self, path):
        self.index = faiss.read_index(path)

    def save(self, path):
        faiss.write_index(faiss.index_gpu_to_cpu(self.index), path)

    def save_vectors(self, path):
        pickle.dump(self.vectors, open(path, 'wb'), protocol=4)

    def search(self, vectors, k=1, probes=64):
        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors)
        faiss.normalize_L2(vectors)
        try:
            self.index.nprobe = probes
        except:
            pass
        distances, ids = self.index.search(vectors, k)
        similarities = [(2-d)/2 for d in distances]
        return ids, similarities


class DenseRetriever:
    def __init__(self, model, batch_size=32, use_gpu=False):
        self.model = model
        self.vector_index = VectorIndex(384)
        self.batch_size = batch_size
        self.use_gpu = use_gpu

    def create_index_from_documents(self, documents):
        logging.info('Building index...')

        self.vector_index.vectors = self.model.encode(documents, batch_size=self.batch_size, show_progress_bar=True)
        self.vector_index.build(self.use_gpu)

        logging.info('Built index')

    def create_index_from_vectors(self, vectors_path):
        logging.info('Building index...')
        logging.info('Loading vectors...')
        self.vector_index.vectors = pickle.load(open(vectors_path, 'rb'))
        logging.info('Vectors loaded')
        self.vector_index.build(self.use_gpu)

        logging.info('Built index')

    def search(self, queries, limit=1000, probes=512, min_similarity=0):
        query_vectors = self.model.encode(queries, batch_size=self.batch_size, show_progress_bar=False)
        ids, similarities = self.vector_index.search(
            query_vectors, k=limit, probes=probes)
        results = []
        for j in range(len(ids)):
            results.append([
                (ids[j][i], similarities[j][i]) for i in range(len(ids[j])) if similarities[j][i] > min_similarity
            ])
        return results

    def load_index(self, path):
        self.vector_index.load(path)

    def save_index(self, index_path='', vectors_path=''):
        if vectors_path != '':
            self.vector_index.save_vectors(vectors_path)
        if index_path != '':
            self.vector_index.save(index_path)


class Retriever:
    def __init__(self):
        self.documents = []
        titles = []
        with open(inventory_file_4k, 'r') as f:
            for line in f:
                d = json.loads(line)
                self.documents.append(d)
                titles.append(d['title'].lower())

        print("Loading DR model...")
        self.model = SentenceTransformer('all-MiniLM-L12-v2')

        print("Start Indexing...")
        self.dr = DenseRetriever(self.model, use_gpu=False)
        # self.dr.create_index_from_documents(titles)
        self.dr.create_index_from_vectors('data/corpus_vectors.pkl')
        # self.dr.save_index(vectors_path='data/corpus_vectors.pkl')

        print("Indexing Complete.")

    def search(self, query, limit=5):
        results = self.dr.search(queries=[query], limit=limit)[0]
        ids = [idx for idx, _ in results]
        results = [(self.documents[idx], results[i][1]) for i, idx in enumerate(ids)]
        return results


if __name__ == "__main__":
    retriever = Retriever()
    # r = retriever.search("Sugar free bubblegum", limit=3)
    r = retriever.search('luxurious scented candles floral gardenia tuberose high rating', limit = 20)
    print(r[0])


import concurrent
import threading
import openai
import json

from concurrent.futures import ThreadPoolExecutor

from datagen import chatgpt_api

openai.api_key = ""
lock = threading.Lock()

out_file = open('data/corpus_2.jsonl', 'w+')
total_tokens = 0
progress = 0

tasks = []
with open('data/corpus.jsonl') as f:
    for line in f:
        d = json.loads(line)
        tasks.append(d)


def generate_query(task):
    global lock
    global total_tokens
    global progress
    if task['query'] is None:
        prompt = f"write a simplified less specific (if possible) query for the last recipe title, give only the query text in your response, nothing else, no quotes, examples:\nkale & sweet potato salad = salad\ninstant-pot whole herb chicken = chicken\n{task['title'].lower()} = "
        query, tokens = chatgpt_api(prompt, model='gpt-3.5-turbo')
        task["query"] = query

    with lock:
        out_file.write(json.dumps(task) + '\n')
        out_file.flush()
        total_tokens += tokens
        progress += 1
        print(f"Progress: {progress}/{len(tasks)} ({(progress / len(tasks)) * 100:.2f}%), tokens: {total_tokens}")


with ThreadPoolExecutor(max_workers=4) as executor:
    # Submit tasks and keep track of the Future objects returned by `executor.submit()`
    futures = [executor.submit(generate_query, task) for task in tasks]

# Wait for all tasks to complete
completed, _ = concurrent.futures.wait(futures)

# Get the results from the completed tasks
results = [future.result() for future in completed]

print(total_tokens)

import json
import gzip
import pandas as pd
import numpy as np


asin_details_file = 'asin_details_file.jsonl'
def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)

def write_to_jsonl(entry, file_path):
    with open(file_path, 'a') as file:
        json.dump(entry, file)
        file.write('\n')

# search_for_asins = []

asins = []
file_name = 'sampled_example_top_50_4200.jsonl'
# Read the JSONL file line by line
with open(file_name, 'r') as file:
    for line in file:
        # Load each line as JSON
        json_data = json.loads(line)
        
        # Extract 'id' field from JSON and add it to the list
        asins.append(json_data['id'])




asin_details = {}


for review in parse("All_Amazon_Review.json.gz"):
  if review['asin'] in asins :
    asin = review['asin']
    if asin in asin_details.keys() :
      review_details = asin_details[asin] 
    #   if 'vote' in review.keys :
      review_details['reviewCount'] += 1
      review_details['overall'] += review['overall']
    else :
       
       review_details = {}
       review_details['asin'] = asin
    #    if 'vote' in review.keys :
       review_details['reviewCount'] = 1
       review_details['overall'] = review['overall']
       

    


    asin_details[asin] = review_details

# compute average overall rating for each product

for asin in asin_details.keys() :
   review_details = asin_details[asin]
   review_details['overall'] /= review_details['reviewCount']
   asin_details[asin] = review_details
   write_to_jsonl(asin_details, asin_details_file)




import time
import json
import os
import argparse

from openai import OpenAI


def prompt_gpt(prompt, model='gpt-4', temperature=0.0, max_retries=3):
    openai = OpenAI(
        api_key="YOUR-API-KEY-HERE",
        base_url="YOUR-BASE-URL-HERE",
    )

    for i in range(max_retries):
        try:
            response = openai.chat.completions.create(
                model=model,
                max_tokens=3,
                temperature=temperature,
                timeout=100,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {2} seconds...")
            time.sleep(2)
    return None


def relevance_eval(filename, output_filename):
    results = []
    counts = [0, 0, 0, 0]
    limit = 5000
    file_path = os.path.join(os.getcwd(), filename)
    out = open(output_filename, "w")
    with open(file_path) as f:
        for line in f:
            if limit == 0:
                break
            limit -= 1
            history = []
            d = json.loads(line)
            for turn in d['history']:
                if turn['role'] in ['user', 'system', 'retriever', 'suggestions']:
                    text = turn['content'].replace("\n", " ")
                    history.append(f"{turn['role']}: {text}")
            response = d['response']['content'].replace("\n", " ")
            groundtruth = d['ground_truth']['content'].replace("\n", " ")
            prompt = "Given the conversation history:\n"
            prompt += "\n".join(history)
            prompt += f"\nResponse: {response}"
            prompt += f"\nGroundtruth: {groundtruth}"
            prompt += "\nHow good is the response compared to the groundtruth? 0: not relevant or with major issues, 1: worse than groundtruth, 2: as good as groundtruth or better. Return only the number."
            relevance = prompt_gpt(prompt)
            print(f"Result: {relevance}")
            if '0' in relevance:
                relevance = 0
            elif '1' in relevance:
                relevance = 1
            elif '2' in relevance:
                relevance = 2
            else:
                relevance = None
            out.write(f"{relevance}\n")
            out.flush()
            if relevance is not None:
                counts[relevance] += 1
                results.append(relevance)
            print(f"Counts: {counts}")
            total_results = len(results)
            if total_results > 0:
                print("Current Metrics:")
                for i, count in enumerate(counts):
                    percentage = count / total_results * 100
                    print(f"Relevance {i}: {percentage:.2f}%")
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run relevance evaluation on a file')
    parser.add_argument('eval_file', type=str, help='The jsonl file with inference examples to evaluate')
    parser.add_argument('output_filename', type=str, help='The output text file that has a relevance label 0-2 in each line')
    args = parser.parse_args()
    relevance_eval(args.filename, args.output_filename)

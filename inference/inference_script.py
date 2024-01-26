from vllm import LLM, SamplingParams
import json
import sys
import argparse

if __name__ == "__main__":
    # python3.8 -m gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8080 backend:app
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default='kimmypracha/llama-marunachef-v1-c1-a100-940')
    parser.add_argument("--output_file",default="fine_tuned_generated_output_a100.jsonl")
    parser.add_argument("--test_file",default="/project/pi_hzamani_umass_edu/chris/marunachef/qlora/data/marunachef/test_v7.jsonl")
    args = parser.parse_args()
    session_id = 'test'
    llm = LLM(args.model)
    sampling_params = SamplingParams(temperature=0, top_p=1, stop=["###"], stop_token_ids=[835], max_tokens=2048)
    with open(args.test_file) as f:
        for line in f.readlines():
            ground_truth = ''
            generated = ''
            dialog = json.loads(line)['text']
            prompt = dialog.split('###')[0]
            ground_truth = prompt 
            generated = prompt
            for turn in dialog.split('###')[1:]:
                mode, data = turn.split(':',1)
                if mode.strip() == 'HUMAN':
                    utterance, intent_data = data.split("##", 1)
                    ground_truth += "###" + mode + ":" + utterance
                    generated += "###" + mode + ":" + utterance + "## {\"intent\": \""
                    response = llm.generate([ground_truth + "## {\"intent\": \""], sampling_params)[0].outputs[0].text.strip()
                    if response.endswith("###"):
                        response = response[:-3]
                    ground_truth += "##" + intent_data
                    generated += response
                elif mode.strip() == 'ASSISTANT':
                    ground_truth += "###" + mode + ":" 
                    response = llm.generate([ground_truth], sampling_params)[0].outputs[0].text.strip()
                    if response.endswith("###"):
                        response = response[:-3]
                    ground_truth += data
                    generated += "###" + mode + ":" +  response
                else:
                    ground_truth += "###" + turn
                    generated += "###" + turn
            with open(args.output_file, "a") as f:
                f.write(json.dumps({"ground_text": ground_truth, "generated_text" : generated}) + "\n")

                    

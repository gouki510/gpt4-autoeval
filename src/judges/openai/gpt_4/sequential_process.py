import json
import os

import jsonlines
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from lib.client_openai import client, template_prompt
from lib.common import read_jsonl
from lib.common import validate_response, get_openai_request_body
from . import openai_judge
import re

def main(args):
    # Load dataset
    dataset_name = os.environ.get('DATASET_NAME', 'test')
    preds = read_jsonl(f"assets/{dataset_name}/preds.jsonl")
    dataset = read_jsonl(f"assets/{dataset_name}/dataset.jsonl")

    with jsonlines.open(f'assets/{dataset_name}/result.jsonl', mode='w') as writer:
        # Evaluate each sample of the dataset, and write the result to the file
        for eval_data, pred_data in zip(dataset, preds):
            pred = pred_data["pred"]
            input_text = eval_data["input_text"]
            output_text = eval_data["output_text"]
            eval_aspect = eval_data["eval_aspect"]
            if args.japanese:
                if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+', pred):
                    result = openai_judge.evaluate(pred, input_text, output_text, eval_aspect, args.evaluator)
                else:
                    result = {"reason": "No Japanese", "grade": 1}
            else:
                result = openai_judge.evaluate(pred, input_text, output_text, eval_aspect, args.evaluator)
            writer.write(result)

            print(f"==============================")
            print(f"Q. {input_text}")
            print(f"A. {pred}")
            print(f"GPT-4. {result}")
            print(f"")


if __name__ == "__main__":
    main()
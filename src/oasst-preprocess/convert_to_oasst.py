import argparse
from . import ecommerce_convert_to_oasst, recipe_convert_to_oasst
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", default="train_nograph_v8.jsonl")
    parser.add_argument("--seed", default=43)
    parser.add_argument("--seed_file", default="data/corpus.jsonl")
    parser.add_argument("--conversation_file", default="/project/pi_hzamani_umass_edu/chris/convtod/data/recipe_nograph_2.jsonl")
    parser.add_argument("mode", default="recipe")
    args = parser.parse_args()
    if args.mode == "recipe":
        recipe_convert_to_oasst.recipe_run(args)
    elif args.mode == "ecommerce":
        ecommerce_convert_to_oasst.ecommerce_run(args)
    else:
        raise ValueError("Invalid mode: {}".format(args.mode))

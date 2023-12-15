import argparse
import os
from typing import List

import numpy as np
from datasets import Dataset, Features
from datasets import Image as ImageFeature
from datasets import Value

DS_NAME = 'drewtray/instructpix2pix-spatial'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default='data_samples')
    args = parser.parse_args()
    return args

def generate_examples(data_dirs):
    def fn():
        for data_dir in data_dirs:
            instruction_file = os.path.join(data_dir, "instruction.txt")
            original_image = os.path.join(data_dir, "original_image.png")
            transformed_image = os.path.join(data_dir, "transformed_image.png")

            if not os.path.exists(instruction_file):
                print(f"Warning: No instruction file found in {data_dir}. Skipping this directory.")
                continue

            if not os.path.exists(original_image) or not os.path.exists(transformed_image):
                print(f"Warning: No image files found in {data_dir}. Skipping this directory.")
                continue

            with open(instruction_file, 'r') as f:
                instruction = f.read().strip()

            yield {
                'original_image': {'path': original_image},
                'edit_prompt': instruction,
                'transformed_image': {'path': transformed_image},
            }
    return fn


def main(args):
    # List all directories within the data_root that contain the image pairs and instructions
    data_dirs = [os.path.join(args.data_root, d) for d in os.listdir(args.data_root) if os.path.isdir(os.path.join(args.data_root, d))]

    generation_fn = generate_examples(data_dirs)
    print("Creating dataset...")
    ds = Dataset.from_generator(
        generation_fn,
        features=Features(
            original_image=ImageFeature(),
            edit_prompt=Value("string"),
            transformed_image=ImageFeature(),
        ),
    )

    print("Pushing to the Hub...")
    ds.push_to_hub(DS_NAME)

if __name__ == "__main__":
    args = parse_args()
    main(args)
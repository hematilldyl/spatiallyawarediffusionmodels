import argparse
import os
from typing import List

import numpy as np
from datasets import Dataset, Features
from datasets import Image as ImageFeature
from datasets import Value

DS_NAME = 'drewtray/vsr'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default='vsr_data_samples')
    args = parser.parse_args()
    return args

def generate_examples(data_dirs):
    def fn():
        for data_dir in data_dirs:
            caption_file = os.path.join(data_dir, "captions.txt")
            transformed_image = os.path.join(data_dir, "transformed_image.png")
            
            if not os.path.isfile(caption_file):
                print(f"Warning: No captions.txt file found in {data_dir}. Skipping this directory.")
                continue
            
            if not os.path.isfile(transformed_image):
                print(f"Warning: No transformed_image.png file found in {data_dir}. Skipping this directory.")
                continue
            
            with open(caption_file, 'r') as f:
                caption = f.read().strip()
            
            yield {
                'image': {'path': transformed_image},
                'text': caption
            }
    return fn


def main(args):
    # List all directories within the data_root that contain the image/text pairs
    data_dirs = [os.path.join(args.data_root, d) for d in os.listdir(args.data_root) if os.path.isdir(os.path.join(args.data_root, d))]

    generation_fn = generate_examples(data_dirs)
    print("Creating dataset...")
    ds = Dataset.from_generator(
        generation_fn,
        features=Features(
            image=ImageFeature(),
            text=Value("string")
        ),
    )

    print("Pushing to the Hub...")
    ds.push_to_hub(DS_NAME)

if __name__ == "__main__":
    args = parse_args()
    main(args)
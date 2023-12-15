import pandas as pd
from datasets import load_dataset, Dataset, Features, Image as HFImage, Value
from sklearn.model_selection import train_test_split
import json
import argparse
from PIL import Image
import requests
from io import BytesIO
import os
import hashlib
from concurrent.futures import ThreadPoolExecutor

RANDOM_STATE = 42
RELATIONS = ['touching', 'in front of', 'behind', 'under', 'on', 'on top of',
       'at the right side of', 'at the left side of', 'beneath', 'above',
       'next to', 'contains', 'facing', 'below', 'in', 'far away from',
       'beside', 'at the edge of', 'inside', 'left of', 'facing away from',
       'away from', 'near', 'far from', 'close to', 'right of', 'part of',
       'across from']

def load_data():

    print('Loading VSR dataset...')
    data_files = {"train": "train.jsonl", "dev": "dev.jsonl", "test": "test.jsonl"}
    dataset = load_dataset("cambridgeltl/vsr_random", data_files=data_files)

    return dataset

def process_true_images(dataset):

    true_images = []

    for subset in ['train', 'dev', 'test']:
        for image in dataset[subset]:
            if image['label'] == 1:
                true_images.append(image)

    return true_images

def get_captions(image_list):

    image_captions = []
    image_links = []

    for i in image_list:
        if i['relation'] in RELATIONS:
            image_captions.append(i['caption'])
            image_links.append(i['image_link'])
            
    return image_captions, image_links

def download_and_save_image(true_caption, true_image_url, data_root):
    # Using a hash of the image URLs to create a unique directory name
    hash_str = hashlib.sha1((true_image_url).encode()).hexdigest()
    sample_dir = os.path.join(data_root, hash_str)
    os.makedirs(sample_dir, exist_ok=True)

    # Download and save the images
    true_image = Image.open(BytesIO(requests.get(true_image_url).content))
    true_image.save(os.path.join(sample_dir, "transformed_image.png"))

    caption_file = os.path.join(sample_dir, "captions.txt")
    with open(caption_file, 'w') as file:
        file.write(true_caption)

def generate_data(true_images, data_root):
    true_captions, true_links = get_captions(true_images)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_and_save_image, true_captions, true_links, [data_root]*len(true_captions))

def main():

    dataset = load_data()
    true_images = process_true_images(dataset)

    data_root = 'vsr_data_samples'
    os.makedirs(data_root, exist_ok=True)

    print('Generating data...')
    generate_data(true_images, data_root)

if __name__ == '__main__':
    main()


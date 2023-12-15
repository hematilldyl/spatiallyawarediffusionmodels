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
ACTION_RELATION = {
    'above': 'Move the',
    'across from': 'Move the',
    'at the edge of': 'Place the',
    'at the left side of': 'Place the',
    'at the right side of': 'Place the',
    'away from': 'Move the',
    'behind': 'Move the',
    'below': 'Place the',
    'beneath': 'Place the',
    'beside': 'Move the',
    'close to': 'Move the',
    'contains': 'Make it so that the',
    'facing': 'Make it so that the',
    'facing away from': 'Make it so that the',
    'far away from': 'Move the',
    'far from': 'Move the',
    'in': 'Put the',
    'in front of': 'Move the',
    'inside': 'Place the',
    'left of': 'Move the',
    'near': 'Move the',
    'next to': 'Place the',
    'on': 'Place the',
    'on top of': 'Place the',
    'part of': 'Make it so that the',
    'right of': 'Move the',
    'touching': 'Make it so that the',
    'under': 'Move the'
}
RELATIONS = [
    'above',
    'across from',
    'at the edge of',
    'at the left side of',
    'at the right side of',
    'away from',
    'behind',
    'below',
    'beneath',
    'beside',
    'close to',
    'contains',
    'facing',
    'facing away from',
    'far away from',
    'far from',
    'in',
    'in front of',
    'inside',
    'left of',
    'near',
    'next to',
    'on',
    'on top of',
    'part of',
    'right of',
    'touching',
    'under'
]

def load_data():

    print('Loading VSR dataset...')
    data_files = {"train": "train.jsonl", "dev": "dev.jsonl", "test": "test.jsonl"}
    dataset = load_dataset("cambridgeltl/vsr_random", data_files=data_files)

    print('Loading COCO annotations...')
    with open('annotations/instances_train2017.json', 'r') as f:
        coco_data = json.load(f)
    
    return dataset, coco_data

def process_true_false_images(dataset):

    true_images = []
    true_image_relations = []
    false_images = []
    false_image_relations = []

    for subset in ['train', 'dev', 'test']:
        for image in dataset[subset]:
            if image['relation'] in RELATIONS:
                if image['label'] == 1:
                    true_images.append(image)
                    if image['relation'] not in true_image_relations:
                        true_image_relations.append(image['relation'])
                else:
                    false_images.append(image)
                    if image['relation'] not in false_image_relations:
                        false_image_relations.append(image['relation'])
    
    joint_relations = set(true_image_relations).intersection(set(false_image_relations))

    return true_images, false_images, joint_relations

def get_object_pairs(image_list, relation, coco_data):

    object_pairs = []
    image_link = []

    unique_cats = {category['name'] for category in coco_data['categories']}
    single_word_cats = {cat for cat in unique_cats if len(cat.split()) == 1}
    multi_word_cats = {cat for cat in unique_cats if len(cat.split()) == 2}

    for i in image_list:
        if i['relation'] == relation:
            caption_words = i['caption'].rstrip('.').split()
            matching_words = []
            j = 0
            while j < len(caption_words):
                if j < len(caption_words) - 1 and ' '.join(caption_words[j:j+2]) in multi_word_cats:
                    matching_words.append(' '.join(caption_words[j:j+2]))
                    j += 2  # Skip the next word
                elif caption_words[j] in single_word_cats:
                    matching_words.append(caption_words[j])
                    j += 1  # Move to the next word
                else:
                    j += 1  # Move to the next word if no match is found
            object_pairs.append(tuple(matching_words))
            image_link.append(i['image_link'])
            
    return object_pairs, image_link

def process_image_pair(args):
    false_pair, false_image_url, true_pair, true_image_url, data_root, action, joining_word_to_relation, relation = args

    # Using a hash of the image URLs to create a unique directory name
    hash_str = hashlib.sha1((false_image_url + true_image_url).encode()).hexdigest()
    sample_dir = os.path.join(data_root, hash_str)
    os.makedirs(sample_dir, exist_ok=True)

    # Download and save the images
    false_image = Image.open(BytesIO(requests.get(false_image_url).content))
    true_image = Image.open(BytesIO(requests.get(true_image_url).content))

    false_image.save(os.path.join(sample_dir, "original_image.png"))
    true_image.save(os.path.join(sample_dir, "transformed_image.png"))

    instruction = f"{action} {false_pair[0]}{joining_word_to_relation} {relation} the {false_pair[1]}."
    instruction_file = os.path.join(sample_dir, "instruction.txt")
    with open(instruction_file, 'w') as file:
        file.write(instruction)

def generate_data(true_images, false_images, relation, coco_data, data_root):

    #Get action based on the relation
    action = ACTION_RELATION.get(relation)
    if action == "Make it so that the":
        joining_word_to_relation = " is"
    else:
        joining_word_to_relation = ""

    true_pairs, true_links = get_object_pairs(true_images, relation, coco_data)
    false_pairs, false_links = get_object_pairs(false_images, relation, coco_data)

    tasks = []
    for idx, (false_pair, false_image_url) in enumerate(zip(false_pairs, false_links)):
        for true_pair, true_image_url in zip(true_pairs, true_links):
            if false_pair == true_pair:
                task = (false_pair, false_image_url, true_pair, true_image_url, data_root, action, joining_word_to_relation, relation)
                tasks.append(task)

    with ThreadPoolExecutor() as executor:
        executor.map(process_image_pair, tasks)


def main():

    dataset, coco_data = load_data()
    true_images, false_images, joint_relations = process_true_false_images(dataset)

    data_root = 'data_samples'
    os.makedirs(data_root, exist_ok=True)

    print('Generating data...')
    for relation in joint_relations:
        relation_instructions = generate_data(true_images, false_images, relation, coco_data, data_root)

if __name__ == '__main__':
    main()


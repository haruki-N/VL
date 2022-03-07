import argparse
import json
import os
import sys
from glob import glob
from typing import List
from tqdm import tqdm

import numpy as np


def filter_data(fi_json, fo_json, images):
    """ fi_json: json 形式の対話データ
        outputs[0] = {
            'image_hash': hash_id,
            'dialog': [
                ['Stoic (Unemotional, Matter-of-fact)', 'THE GUY IS SUFFERING FROM DEPRESSION'],
                ['Devious', "So who's down to mess with him?"],
                ['Stoic (Unemotional, Matter-of-fact)', 'This guy probably does not want to be here.']
            ],
            # 'candidates',
        }
    """
    is_valid = lambda fname: fname in images
    outputs: List[dict] = []
    cnt = 0
    for data in json.load(open(fi_json)):
        if is_valid(f'{data["image_hash"]}.jpg'):
            outputs.append(data)
        else:
            cnt += 1

    with open(fo_json, 'w') as fo:
        json.dump(outputs, fo, indent=4, ensure_ascii=False)
        print(f'| WRITE ... {fo.name} : {len(outputs)} images ({cnt} images were excluded.)')


def create_arg_parser():
    parser = argparse.ArgumentParser(description='args for exluding unvalid datas')
    parser.add_argument('-di_img', '--input_img_dir', default='data/yfcc_images')
    parser.add_argument('-di_txt', '--input_txt_dir', default='data/image_chat')
    parser.add_argument('-do_txt', '--output_txt_dir', default='data/image_chat/filtered')
    return parser


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    images = [os.path.basename(image) for image in glob(f'{args.input_img_dir}/*')]
    images = set(images)

    os.makedirs(args.output_txt_dir, exist_ok=True)
    for dtype in ('train', 'valid', 'test'):
        fi_json = os.path.join(args.input_txt_dir, f'{dtype}.json')
        fo_json = os.path.join(args.output_txt_dir, f'{dtype}.json')
        filter_data(fi_json, fo_json, images)

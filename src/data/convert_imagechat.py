import os
import json
import argparse
from typing import List

import numpy as np


def convert_format(fi_json, fo_jsonl):
    data: List[dict] = json.load(open(fi_json))

    with open(fo_jsonl, 'w') as fo:
        for line in data:
            out = {
                'dialog': {
                    i: {'style': d[0], 'text': d[1]} for i, d in enumerate(line['dialog'])
                },
                'image_hash': line['image_hash'],
            }
            fo.write(json.dumps(out) + '\n')
        print(f'| WRITE ... {fo.name}')


def restore_format(fi_jsonl, fo_json):
    outputs: List[dict] = []

    for line in open(fi_jsonl):
        data = json.loads(line.strip())
        outputs.append({
            'image_hash': data['image_hash'],
            'dialog': [[d['style'], d['text']] for d in data['dialog'].values()],
        })
    with open(fo_json, 'w') as fo:
        json.dump(outputs, fo, indent=4, ensure_ascii=False)
        print(f'| WRITE ... {fo.name}')


def create_arg_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-di', '--input_dir', default='data/image_chat/filtered')
    parser.add_argument('-do', '--output_dir', default='data/image_chat/translate/en')
    parser.add_argument('--restore', action='store_true')

    return parser


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    if args.restore:
        raise NotImplementedError()
    else:
        os.makedirs(args.output_dir, exist_ok=True)

        for dtype in ('train', 'valid', 'test'):
            fi = os.path.join(args.input_dir, f'{dtype}.json')
            fo = os.path.join(args.output_dir, f'{dtype}.jsonl')
            convert_format(fi, fo)

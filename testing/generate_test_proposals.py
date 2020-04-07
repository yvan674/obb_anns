from os.path import join, split
import json
import pandas as pd
from random import random, uniform
from argparse import ArgumentParser

from obb_anns import OBBAnns


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('GT', type=str,
                        help='path to ground truth annotations')

    return parser.parse_args()


def fudge_bboxes(line: pd.Series):
    bbox_vals = line['bbox']
    shift = uniform(-10, 10)
    bbox_vals = [i + shift for i in bbox_vals]

    return {'bbox': bbox_vals,
            'cat_id': line['cat_id'],
            'img_id': line['img_id']}


def main(gt_fp: str):
    gt = OBBAnns(gt_fp)
    gt.load_annotations()

    root = split(gt_fp)[0]

    # First make perfect proposals
    bboxes = gt.ann_info[['bbox', 'cat_id', 'img_id']]
    proposals = {'proposals': bboxes.to_dict('records')}
    with open(join(root, 'proposals_perfect.json'), 'w') as prop_file:
        json.dump(proposals, prop_file)

    # Now randomly "forget" certain proposals
    selector = [True if random() > 0.2 else False
                for _ in range(len(gt.ann_info))]

    bboxes = gt.ann_info[['bbox', 'cat_id', 'img_id']][selector].apply(
        fudge_bboxes, 1, result_type='expand'
    )

    proposals = {'proposals': bboxes.to_dict('records')}

    with open(join(root, 'proposals.json'), 'w') as prop_file:
        json.dump(proposals, prop_file)


if __name__ == '__main__':
    args = parse_args()
    main(args.GT)

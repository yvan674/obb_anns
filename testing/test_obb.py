"""Test OBB.

Used to run the obb_anns.py with testing data.

Author:
    Yvan Satyawan <y_satyawan@hotmail.com>

Created On:
    April 7, 2020
"""
from os.path import join
from obb_anns import OBBAnns
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='runs the obb_anns.py file')
    parser.add_argument('ROOT', type=str,
                        help='path to the root of the dataset directory')
    parser.add_argument('ANNS', type=str,
                        help='name of the annotation file to use')
    parser.add_argument('PROPOSAL', type=str,
                        help='name of the proposals json')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    a = OBBAnns(join(args.ROOT, args.ANNS))
    a.load_annotations()
    a.load_proposals(join(args.ROOT, args.PROPoSAL))
    for i in range(len(a)):
        a.visualize(img_idx=i, img_dir='images_png',
                    seg_dir='pix_annotations_png')
        # a.visualize(img_idx=i, img_dir='images_png')
        response = input('Press q to quit or enter to continue.')
        if response == 'q':
            break
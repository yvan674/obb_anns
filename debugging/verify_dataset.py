from os.path import join
from obb_anns import OBBAnns
from argparse import ArgumentParser
from tqdm import tqdm
from pathlib import Path


def parse_args():
    parser = ArgumentParser(description='runs the obb_anns.py file')
    parser.add_argument('ROOT', type=str,
                        help='path to the root of the dataset directory')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    root_dir = Path(args.ROOT)
    file_names_in_annotations = []
    num_ann_files = len(list(root_dir.glob("*.json")))

    for i, dataset_ann_fp in enumerate(root_dir.glob("*.json")):
        print(f'Checking file {i + 1} of {num_ann_files}...')
        a = OBBAnns(join(args.ROOT, dataset_ann_fp))
        a.load_annotations()
        a.set_annotation_set_filter(['deepscores'])

        for img in tqdm(a.img_info, unit='imgs'):
            file_names_in_annotations.append(img['filename'])
            try:
                b = a.get_anns(img_id=img['id'])
            except:
                print(f'{img["id"]} caused an exception')

    file_names_in_annotations = set(file_names_in_annotations)

    images_dir = root_dir / 'images_png'

    print("Checking if every image has its annotation in the dataset...")

    prog_bar = tqdm(images_dir.iterdir(), unit='imgs')
    for image_fp in prog_bar:
        if image_fp.name not in file_names_in_annotations:
            prog_bar.write(f"{image_fp.name} is not in any JSON file")

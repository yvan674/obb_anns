import os
from pathlib import Path
from typing import Union, Tuple, Callable

import numpy as np
import torch
from PIL import Image

from obb_anns import OBBAnns


def rotated_box_to_poly(rboxes: torch.Tensor) -> torch.Tensor:
    """
    rrect:[x_ctr,y_ctr,w,h,angle]
    to
    poly:[x0,y0,x1,y1,x2,y2,x3,y3]
    """
    N = rboxes.shape[0]
    x_ctr, y_ctr, width, height, angle = rboxes.select(1, 0), rboxes.select(
        1, 1), rboxes.select(1, 2), rboxes.select(1, 3), rboxes.select(1, 4)
    tl_x, tl_y, br_x, br_y = -width * 0.5, -height * 0.5, width * 0.5, height * 0.5

    rects = torch.stack([tl_x, br_x, br_x, tl_x, tl_y, tl_y,
                         br_y, br_y], dim=0).reshape(2, 4, N).permute(2, 0, 1)

    sin, cos = torch.sin(angle), torch.cos(angle)
    # M.shape=[N,2,2]
    M = torch.stack([cos, -sin, sin, cos],
                    dim=0).reshape(2, 2, N).permute(2, 0, 1)
    # polys:[N,8]
    polys = M.matmul(rects).permute(2, 1, 0).reshape(-1, N).transpose(1, 0)
    polys[:, ::2] += x_ctr.unsqueeze(1)
    polys[:, 1::2] += y_ctr.unsqueeze(1)

    return polys


def anns_from_text_anns(dummy_ann: OBBAnns, path: Union[os.PathLike, str], filename: str = None,
                        a_bbox_transform_fn: Callable = lambda x: x, o_bbox_transform_fn: Callable = lambda x: x) -> \
        Tuple[Union[os.PathLike, str], int, int, dict]:
    if dummy_ann.cat_info is None:
        dummy_ann.load_annotations()
    cats = {}
    for cat_id, cat in dummy_ann.cat_info.items():
        if cat['annotation_set'] not in dummy_ann.chosen_ann_set:
            continue
        cats[cat['name'].lower()] = cats.get(cat['name'].lower(), []) + [str(cat_id)]
    ann_dict = {}
    with open(path, 'r') as fp:
        i = 0
        for line in fp.readlines():
            if len(line.strip()) == 0:
                continue
            i += 1
            file, cat_name, x, y, w, h, angle = line.strip().split(',')
            if filename is None:
                file = str(Path(file))
            else:
                file = filename
            cat_id = cats.get(cat_name.lower(), None)
            if cat_id is None:
                raise Exception(f"Failed to find mapping for category {cat_name}!")
            x, y, w, h = int(x), int(y), int(w), int(h)
            angle = float(angle)
            # suff = ''
            # if angle != 0.0:
            #     suff = f" ({angle})"
            # print(f"Read ann: {cat_id} ({cat_name}): {x},{y}+{w}x{h}{suff}")
            a_bbox = a_bbox_transform_fn([x, y, x + h, y + w])
            o_bbox = o_bbox_transform_fn(rotated_box_to_poly(torch.tensor(
                [[x, y, w, h, np.deg2rad(angle)]]
            )).tolist()[0])
            ann_dict[str(i)] = {
                'a_bbox': a_bbox,
                'o_bbox': o_bbox,
                'cat_id': cat_id,
                'area': w * h,
                'img_id': 0,
                'comments': ''
            }
    with Image.open(file) as img_fp:
        width, height = img_fp.size
    return file, width, height, ann_dict

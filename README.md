# Oriented Bounding Box Annotations
Tools to work with the Oriented Bounding Box Schema.

### Why a new schema?
The aim of this schema is to make it easy to work with oriented bounding boxes while also retaining the ability to do segmentation tasks on the objects.
Here we try to create tools that make it quick and easy to work with oriented bounding boxes, their corresponding semantic segmentations, and measuring the accuracy, precision, and recall of models trained on this annotation style.

### Design decisions
We choose to use a JSON file for the annotations as it is already familiar (from the COCO dataset) and is also a much simpler format to parse than an XML file. 
We also choose to store the segmentation information in a separate PNG file to reduce the size of the annotation file, as well as to make dynamic loading of annotation segmentation simpler, especially in cases where there may be very many instances of objects in a single image.
Finally, we choose to process predictions from a proposals file instead of from directly taking proposals as a function argument to make it easier to process proposals asynchronously as well as after the fact from previous proposals.

## Installation
1.  Install SWIG.
    This can be installed executing the following line on linux
    ```bash
    sudo apt install swig
    ```
    or by downloading the windows executable at [swig.org](http://www.swig.org/download.html)
    
    If installing using the windows executable, then the path to the SWIG executable must be added to the `Path` variable.

2.  Install the obb_anns module.
    This can be done with the following command if you wish to install it to the system.
    ```bash
    python3 setup.py install  # Installs it to the current python install, or
    python3 setup.py develop  # Installs it in place
    ```

## Annotation schema

### Directory Structure
The OBBAnns toolkit assumes the following directory structure

```
dataset/
├── images/
│   ├── img1.png
│   ├── img2.png
│   └── ...
├── segmentation/
│   ├── img1_seg.png
│   ├── img2_seg.png
│   └── ...
└── annotations.json

```
The file top level directory and the annotations file can have any name, but the annotations file must be within the top level directory. 

### Annotation File Example
```
{
    "info": {
        "description": (str) description,
        "version": (str) version number,
        "year": (int) year released,
        "contributor": (str) contributor,
        "date_created": (str) "YYYY/MM/DD",
        "url": (Optional str) URL where dataset can be found
    },
    "annotation_sets": (list[str]) ["deepscores", "muscima", ...]
    "categories": {
        "cat_id": {
            "name": (str) category_name,
            "annotation_set": (str) "deepscores",
            "color": (int or tuple[int]) color value of cat in segmentation file
        },
        ...
    },
    "images": [
        {
            "id": (str) n,
            "file_name": (str) "file_name.jpg",
            "width": (int) x,
            "height": (int) y,
            "ann_ids": (list[str]) ann_ids
        },
        ...
    ],
    "annotations": {
        "ann_id": {
            "a_bbox": (list of floats) [x0, y0, x1, y1],
            "o_bbox": (list of floats) [x0, y0, x1, y1, x2, y2, x3, y3],
            "cat_id": (list[str]) cat_id,
            "area": (float) area in pixels,
            "img_id": (str) img_id,
            "comments": (str) any additional comments about the annotation.
        },
        ...
    }
}
```

Notes:
- The annotation file is in JSON format.
- The top level field `annotation_sets` is meant to be used when a dataset can be used with different class names.
For example, if we have two datasets `dataset_a` and `dataset_b` and there is a viable mapping between the two datasets, `annotation_sets` will have the value [`dataset_a`, `dataset_b`].
By adding this field and specifying which class belongs to which annotation_set under categories, this allows one dataset to be compatible with both annotation category names, useful for benchmarking.
- The field `a_bbox` and `o_bbox` of annotations is the aligned and oriented bounding boxes for each annotation, respectively.
- The bounding boxes are given as absolute values.
- `a_bbox` contains the coordinates of the top left and bottom right corners.
- `o_bbox` contains the coordinates of each of the corners of the oriented bounding box. 
- `cat_id`, `ann_id`, and `img_id` are stringified ints and start at 1.
- `cat_id` is a list of stringified ints. It is a list as there are multiple annotation sets. 
  For example, supposed we have two annotation sets `dataset_a` and `dataset_b`. 
  If the category 'stem' has a cat_id of '1' in `dataset_a` and a cat_id of 25 in `dataset_b`, then the `cat_id` field of a single stem annotation would be `['1', '25']`.
  I a category doesn't exist in one of the annotation sets, a value of `null` should be provided. 

### Segmentation Masks
- Segmentations are found in a png file named '[filename]_seg.png' in the directory "segmentation".
- The segmentation file is a grayscale 8-bit png image where the pixel values correspond to the cat_id.
- If more categories are required, alternative mappings can be defined by overriding the _parse_ann_info method.

### Proposal File Example
Proposals are what the network should generate so that this package is able to process the proposals to calculate precision, accuracy, and recall.

```
{
    "annotation_set": (str) annotation set used,
    "proposals": [
        {
            "bbox": list[float] [x1, y1,..., x4, y4], or list[float] [x0, y0, x1, y1]
            "cat_id": (str) cat_id,
            "img_id": (int) img_id
        },
        ...
    ]
}
```

Notes:
- The proposals file is in JSON format.
- `bbox` is in the same format as for annotations
- If `bbox` has a length of 8, it is treated as an oriented bounding box. If it has length 4, then it is treated as an aligned bbox.
- A check is done to make sure all img_idxs and cat_ids that are referred to in the proposal file is in the annotation file to make sure that the proposals corresponds to the correct annotations file.

## Usage
The OBBAnns class provides all the necessary tools to work with the OBB schema.

### Loading Annotations
Usage is simply to initialize the class by providing it with the annotation file path, then loading the annotations into memory.

```python
from obb_anns import OBBAnns
o = OBBAnns('path/to/file.json')
o.load_annotations()
```

### Getting images and annotations
To get images with their annotations, the ```get_img_ann_pairs()``` method can be used.

```python
from obb_anns import OBBAnns
o = OBBAnns('path/to/file.json')
o.load_annotations()

# Get the first 50 images
img_idxs = [i for i in range(50)]
imgs, anns = o.get_img_ann_pairs(idxs=img_idxs)
```

### Calculating validation metrics
Once a model has generated proposals and the proposals saved according to the schema, the proposals file can be loaded and metrics calculated.

```python
from obb_anns import OBBAnns
o = OBBAnns('path/to/file.json')
o.load_annotations()

o.load_proposals('path/to/proposals.json')
metric_results = o.calculate_metrics()
```

### Visualization
Finally, the results can be visualized using the `visualize()` method

```python
from obb_anns import OBBAnns
o = OBBAnns('path/to/file.json')
o.load_annotations()

# Visualize immediately
from obb_anns import OBBAnns
o.visualize(img_idx=1, show=True)

# Or saved to file
o.visualize(img_idx=1, out_dir='path/to/save/dir', show=False)
```

## Dependencies
- numpy
- pillow
- colorcet
- pandas

This toolkit uses the PolyIOU code found in the [DOTA Devkit](https://github.com/CAPTAIN-WHU/DOTA_devkit).

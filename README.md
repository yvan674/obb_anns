# Oriented Bounding Box Annotations
Tools to work with the Oriented Bounding Box Schema.

### Why a new schema?
The aim of this schema is to make it easy to work with oriented bounding boxes while also retaining the ability to do segmentation tasks on the objects.
Here we try to create tools that make it quick and easy to work with oriented bounding boxes, their corresponding semantic segmentations, and measuring the accuracy, precision, and recall of models trained on this annotation style.

## Design decisions
We choose to use a JSON file for the annotations as it is already familiar (from the COCO dataset) and is also a much simpler format to parse than an XML file. 
We also choose to store the segmentation information in a separate PNG file to reduce the size of the annotation file, as well as to make dynamic loading of annotation segmentation simpler, especially in cases where there may be very many instances of objects in a single image.
Finally, we choose to process predictions from a proposals file instead of from directly taking proposals as a function argument to make it easier to process proposals asynchronously as well as after the fact from previous proposals.

# Manual Installation
1.  Clone this repository
2.  Install swig.
    This can be installed executing the following line on linux
    ```bash
    sudo apt install swig
    ```
    or by downloading the windows executable at [swig.org](http://www.swig.org/download.html)
    
    If installing using the windows executable, then the following must be variable must be added to your environment:
    ```
    TBD
    ``` 

3.  install the obb_anns module.

# Annotation schema:

```
{
    "info": {
        "description": (str) description,
        "version": (str) version number,
        "year": (int) year released,
        "contributor": (str) contributor,
        "date_created": (str) "YYYY/MM/DD"
    },
    "categories": {
        "cat_id": (str) category_name,
        ...
    },
    "images": [
        {
            "id": (int) n,
            "filename": (str) 'file_name.jpg',
            "width": (int) x,
            "height": (int) y,
            "ann_ids": [(int) ann_ids]
        },
        ...
    ],
    "annotations": {
        "ann_id": {
            "bbox": (list of floats) [x1, y1,..., x4, y4],
            "cat_id": (int) cat_id,
            "area": (float) area in pixels,
            "img_id": (int) img_id
        },
        ...
    }
}
```

### Notes
- The annotation file is in JSON format.
- The 'annotations' field is in absolute x, y positions.
- cat_id, and ann_id are stringified ints.
- cat_id, ann_id, and img_id starts at 1.

## Segmentation Masks
- Segmentations are found in a png file named '[filename]_seg.png'
- The segmentation file is a grayscale 8-bit png image where the pixel values correspond to the cat_id.
- If more categories are required, alternative mappings can be defined by overriding the _parse_ann_info method.

## Proposal schema
Proposals are what the network should generate so that this package is able to process the proposals to calculate precision, accuracy, and recall.

```
{
    "proposals": [
        {
            "bbox": (list of floats) [x1, y1,..., x4, y4],
            "cat_id": (int) cat_id,
            "img_id": (int) img_id
        },
        ...
    ]
}
```

### Notes
- The proposals file is in JSON format.
- bbox is in the same format as for annotations
- A check is done to make sure all img_idxs and cat_ids that are referred to in the proposal file is in the annotation file to make sure that the proposals corresponds to the correct annotations file.


# Dependencies
This toolkit works with the evaluation metrics conceived in the [DOTA Dataset](https://captain-whu.github.io/DOTA/tasks.html) and uses the polyiou implementation written for their Task 1 Evaluation.

## ISVQA - Outdoor Scenes

This directory contains the annotations for the Outdoor scenes dataset from ISVQA. 

Download the original images from [nuScenes](https://www.nuscenes.org/).

The ISVQA annotations can be read as follows:

```python
import json
data = json.load(open('imdb_nuscenes_trainval.json'))
```

Here, `data['metadata']` contains the metadata from the dataset, `data['data']` is a list of length
33,973. Each element in this list contains the following:

```python
'question_str'      # Question string
'question_tokens'   # List of tokens from the question string
'question_id'       # Unique ID for the question
'image_names'       # Image names in the order: front_left, front, front_right, back_left, back, back_right
'image_id'          # ID for a set of images
'feature_paths'     # images_names + .npy
'answers'           # List of answers from the annotators
```

The same is given for the test set. 

Finally, `answers_nuscenes_more_than_1.txt` contains the 650 unique answers in the dataset. 

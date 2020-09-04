## ISVQA - Indoor Scenes

This directory contains the annotations for the Indoor scenes dataset (Gibson-Room and
Gibson-Building) from ISVQA. 

Download the original [Gibson]() datasets. Also, install the [Habitat
environment](https://github.com/facebookresearch/habitat-api). Then use the code in
`data_generation` to generate the relevant images and videos from the 3D scans.

The ISVQA annotations can be read as follows:

```python
import json
data = json.load(open('imdb_gh_rand_combined_trainval.json'))
```

Here, `data['metadata']` contains the metadata from the dataset, `data['data']` is a list of length
69,207. Each element in this list contains the following:

```python
'question_str'      # Question string
'question_tokens'   # List of tokens from the question string
'question_id'       # Unique ID for the question
'image_names'       # Image names 
'image_id'          # ID for a set of images
'feature_paths'     # images_names + .npy
'answers'           # List of answers from the annotators
```

The same is given for the test set. 

Finally, `answers_gh_rand_combined_more_than_1.txt` contains the 961 unique answers in the dataset. 

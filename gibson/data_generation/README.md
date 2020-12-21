## Code for Generating Data

To generate the image sets, modify the locations of `save_dir`, `pointnav_file_dir`, and `config.DATASET.SCENES_DIR` to point to
the locations where you have saved the info files from this directory, the Gibson pointnav files,
and the base path of the Gibson dataset respectively in `generate_image_sets_from_info_files.py`.

```python
python generate_image_sets_from_info_files.py
```

Similarly, to generate the video frames, use `generate_videos_from_info_files.py`. 

```python
python generate_videos_from_info_files.py
```


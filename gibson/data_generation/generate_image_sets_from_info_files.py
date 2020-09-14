import os

import habitat
#from habitat_sim.utils import d3_40_colors_rgb

import json
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import random

import ipdb

# Link to the Gibson pointnav data can be found here:
# https://github.com/facebookresearch/habitat-challenge/blob/master/README.md#references


def save_sample_rgb(rgb_obs, filename):
    rgb_img = Image.fromarray(rgb_obs, mode="RGB")
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(rgb_img)
    fig.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)


def generate_and_save_image_sets(pointnav_file_dir, scene_names, config, save_dir, split='train'):

    for scene_name in scene_names:
        pn_file = os.path.join(pointnav_file_dir, scene_name + '.json.gz')
        print("================================================================================")
        print(pn_file)
        print("================================================================================")
        config.defrost()
        config.DATASET.DATA_PATH = pn_file
        config.freeze()

        if split == "train":
            num_sets = 150
        else:
            num_sets = 250
    
        for k in range(num_sets):
            dir_to_save = os.path.join(save_dir, split, scene_name, str(k))
            info_file = os.path.join(dir_to_save, 'info.json')
            info = json.load(open(info_file))
    
            env = habitat.Env(config=config)
    
            episode_ids_to_use = [ep["episode_id"] for ep in info] # Get previously used episodes
    
            episode_id_list = [ep.episode_id for ep in env.episodes]
            indices_to_use = [episode_id_list.index(i) for i in episode_ids_to_use] # These indices
                                                                                    # correspond to the
                                                                                    # previously used
                                                                                    # episodes
    
            temp = [env.episodes[i] for i in indices_to_use]
            env.episodes = temp  # Only use the previously used episodes
    
            for i in range(len(env.episodes)):
                observations = env.reset() # reset moves to the next episode
                filename = os.path.join(dir_to_save, '{}.png'.format(i))
                if not os.path.exists(filename):
                    save_sample_rgb(observations['rgb'], filename)
    
            env.close()   


save_dir = 'PATH/TO/SAVE/IMAGES' # Path where the accompanying `info_files` directory is saved
# Example:
#save_dir = '/efs/data/gibson/mivqa/images/'

pointnav_file_dir = 'PATH/TO/GIBSON/POINTNAV/TRAIN/CONTENT'
# Example:
#pointnav_file_dir = '/efs/data/gibson/pointnav/train/content/'

train_scene_names = os.listdir(os.path.join(save_dir, 'train'))
test_scene_names = os.listdir(os.path.join(save_dir, 'test'))

config = habitat.get_config(config_paths='configs/tasks/pointnav_gibson.yaml')
config.defrost()
config.DATASET.SCENES_DIR = 'BASE/PATH'
#config.DATASET.SCENES_DIR = '/efs/data/gibson/'
config.freeze()

generate_and_save_image_sets(pointnav_file_dir, train_scene_names, config, save_dir, 'train')
generate_and_save_image_sets(pointnav_file_dir, test_scene_names, config, save_dir, 'test')

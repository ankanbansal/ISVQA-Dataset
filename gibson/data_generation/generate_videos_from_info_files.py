import os

import habitat
from habitat.utils.visualizations.utils import images_to_video
#from habitat_sim.utils import d3_40_colors_rgb

import json
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import random
random.seed(2019)

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


def generate_and_save_videos(pointnav_file_dir, scene_names, config, save_dir, split='train'):

    for scene_name in scene_names:
        pn_file = os.path.join(pointnav_file_dir, scene_name + '.json.gz')
        print("================================================================================")
        print(pn_file)
        print("================================================================================")
        config.defrost()
        config.DATASET.DATA_PATH = pn_file
        config.freeze()
    
        if split == "train":
            num_videos = 100
        else:
            num_videos = 200

        for k in range(num_videos):
            dir_to_save = os.path.join(save_dir, split, scene_name, str(k)) 
            dir_to_save_frames = os.path.join(dir_to_save, 'frames')
            info_file = os.path.join(dir_to_save, 'info.json')
            info = json.load(open(info_file))
            
            env = habitat.Env(config=config) 

            episode_ids_to_use = info["episode_id"] # Get previously used episodes

            episode_id_list = [ep.episode_id for ep in env.episodes]
            indices_to_use = episode_id_list.index(episode_ids_to_use) # This index corresponds to
                                                                       # the previously used episode
            
            temp = env.episodes[indices_to_use]
            env.episodes = [temp]  # Only use the previously used episodes

            if not os.path.exists(dir_to_save_frames):
                os.makedirs(dir_to_save_frames)
    
            images = []

            first_observation = env.reset() # reset moves to the next episode
            images.append(first_observation['rgb'])

            for xx in range(36):
                observation = env.step(3) # 3 -> right turn
                                          # step move in the current episode
                images.append(observation['rgb'])
                
            # images_to_video(images, output_dir, video_name, fps)
            #if not os.path.exists(os.path.join(dir_to_save, 'video.mp4')):
            #    video = images_to_video(images, dir_to_save, 'video', 5)
    
            for qq,image in enumerate(images):
                save_file_name = os.path.join(dir_to_save_frames, '{}.png'.format(qq))
                if not os.path.exists(save_file_name):
                    save_sample_rgb(image, save_file_name)
            
            env.close() 


save_dir = 'PATH/TO/SAVE/VIDEOS' # Path where the accompanying `info_files` directory is saved
# Example:
#save_dir = '/efs/data/gibson/mivqa/videos/'

pointnav_file_dir = 'PATH/TO/GIBSON/POINTNAV/TRAIN/CONTENT'
# Example:
#pointnav_file_dir = '/efs/data/gibson/pointnav/train/content/'

train_scene_names = os.listdir(os.path.join(save_dir, 'train'))
test_scene_names = os.listdir(os.path.join(save_dir, 'test'))

config = habitat.get_config(config_paths='configs/tasks/pointnav_gibson.yaml')
config.defrost()
config.DATASET.SCENES_DIR = 'BASE/PATH'
#config.DATASET.SCENES_DIR = '/efs/data/gibson/'
config.SIMULATOR.TURN_ANGLE = 10
config.freeze()

generate_and_save_videos(pointnav_file_dir, train_scene_names, config, save_dir, 'train')
generate_and_save_videos(pointnav_file_dir, test_scene_names, config, save_dir, 'test')

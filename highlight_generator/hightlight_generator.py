import json
from pathlib import Path
from moviepy.editor import *

confidence_threshold = 0.65
highlight_scenes = ['Penalty', 'Goal', 'Shots on target', 'Shots off target', 'Clearance', 'Foul', 'Indirect free-kick', 'Direct free-kick', 'Corner', 'Yellow card', 'Red card', 'Yellow->red card']

prev_pad = 3
next_pad = 30

game_time = 45 * 60

data_path = Path("../soccer_action_spotting/datasets/soccernet/")
weights_path = Path("../soccer_action_spotting/weights/NetVLAD++_audio/outputs_test/")

for file in  weights_path.rglob("**/**/*.json"):
    with open(file, 'r') as f:
        data = json.load(f)

        first_half_times = []
        second_half_times = []

        for x in filter(lambda x : float(x['confidence']) > confidence_threshold and x['label'] in highlight_scenes, data['predictions'] ):

            time_seconde_form = int(x['gameTime'][4:].split(":")[0])*60 + int(x['gameTime'][4:].split(":")[1])

            if(x['gameTime'][0] == '1'):
                first_half_times.append((time_seconde_form, x['label']))
            else:
                second_half_times.append((time_seconde_form, x['label']))
                
            first_half_times.sort(key=lambda x : x[0])
            second_half_times.sort(key=lambda x : x[0])

        first_half_original_video = VideoFileClip(str(data_path / Path(data['UrlLocal']) / Path("1_720p.mkv")))
        second_half_original_video = VideoFileClip(str(data_path / Path(data['UrlLocal']) / Path("2_720p.mkv")))

        first_clip_list = []
        for x in first_half_times:
            if x[0]+next_pad > game_time:
                end = game_time-1
            else:
                end = x[0]+next_pad
            start = x[0]-prev_pad
            first_clip_list.append(first_half_original_video.subclip(start, end))

        second_clip_list = []
        for x in second_half_times:
            if x[0]+next_pad > game_time:
                end = game_time-1
            else:
                end = x[0]+next_pad
            start = x[0]-prev_pad
            second_clip_list.append(second_half_original_video.subclip(start, end))

        first_final_clip = concatenate_videoclips(first_clip_list)
        second_final_clip = concatenate_videoclips(second_clip_list)

        new_path = Path.cwd() / Path("..") / Path("highlights") / Path(data["UrlLocal"])

        new_path.mkdir(parents=True, exist_ok=True)

        first_final_clip.write_videofile(str(new_path / Path("first_half.mp4")))
        second_final_clip.write_videofile(str(new_path / Path("second_half.mp4")))


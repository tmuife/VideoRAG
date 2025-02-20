import os
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer
from moviepy.video.io.VideoFileClip import VideoFileClip
from decouple import config

def encode_video(video, frame_times):
    frames = []
    for t in frame_times:
        frames.append(video.get_frame(t))
    frames = np.stack(frames, axis=0)
    frames = [Image.fromarray(v.astype('uint8')).resize((1280, 720)) for v in frames]
    return frames
    
def segment_caption(video_name, video_path, segment_index2name, transcripts, segment_times_info, caption_result, error_queue):
    try:
        model = AutoModel.from_pretrained(config("CMP_DIR"), trust_remote_code=True,attn_implementation='sdpa',torch_dtype=torch.bfloat16,init_vision=True,init_audio=True,init_tts=True)
        tokenizer = AutoTokenizer.from_pretrained(config("CMP_DIR"), trust_remote_code=True)
        model.eval().cuda()
        model.init_tts()
        with VideoFileClip(video_path) as video:
            for index in tqdm(segment_index2name, desc=f"Captioning Video {video_name}"):
                frame_times = segment_times_info[index]["frame_times"]
                video_frames = encode_video(video, frame_times)
                segment_transcript = transcripts[index]
                query = f"The transcript of the current video:\n{segment_transcript}.\nNow provide a description (caption) of the video in English."
                #query = f"""
                #                The transcript of the current video:\n{segment_transcript}.\n
                #                Please analyze the video and provide a detailed description in English, focusing on the following tasks:
                #                1. **List all actions in chronological order**: Provide a timeline of actions with their timestamps and descriptions.
                #                2. **Identify individuals and their roles**: Recognize all individuals in the video and mark their identities (e.g., person A, person B).
                #                3. **Detect specific events**: Identify key events such as fights, falls, or other notable incidents, and provide their timestamps.
                #                4. **Classify behaviors**: Categorize behaviors (e.g., walking, running, suspicious activities) and list their occurrence times.
                #                5. **Track object movement**: Track the movement trajectory of a specified object (e.g., a bag, vehicle) and provide its coordinates over time.
                #                6. **Analyze group behavior**: Analyze group behavior patterns (e.g., gathering, dispersing) and describe their changes.
                #                7. **Identify and track specific objects**: Recognize and track specific objects (e.g., bags, vehicles) and provide their movement paths.
                #                Ensure the description is structured, detailed, and covers all significant elements of the video.
                #                """
                #query = f"""The transcript of the current video:\n{segment_transcript}.\n
                #Please analyze the video and provide a detailed description in English, focusing on the following tasks:
                ## Security Behavior Recognition Protocol
                #        **Detection Objectives**: Distinguish between ① Abnormal Loitering ② Intrusion Detection ③ Elderly Fall ④ Package Delivery
                #
                #        ## Input Parameters
                #        - **Video Description**: [Please provide an objective description of the core content of the video in 50-80 words]
                #        - **Object Characteristics**: [Age Group/Clothing/Carried Items]
                #        - **Behavior Sequence**: [Time Period] [Behavior Description]
                #          Example: 00:11-00:23: Two men walk along a path, with several chickens approaching them.
                #
                #        ## Output Specifications
                #        1. **Basic Judgment**:
                #           - Abnormal Loitering (0-1)
                #           - Intrusion Detection (0-1)
                #           - Person Fall (0-1)
                #           - Package Delivery (0-1)
                #
                #        2. **Event Classification** (Multiple Selection Tags):
                #           - ( Abnormal Loitering | Area Intrusion | Person Fall | Package Delivery | No Event )
                #           [Select the most relevant tags based on the probability values of the basic judgment. If no significant event is detected, choose "No Event."]
                #
                #        3. **Behavior Nature** (Single Selection Tag):
                #           - ( Normal Behavior | Suspicious Behavior | Emergency Situation )
                #           [Determine the nature of the behavior based on the event classification and the probability values of the basic judgment.]
                #"""
                msgs = [{'role': 'user', 'content': video_frames + [query]}]
                params = {}
                params["use_image_id"] = False
                params["max_slice_nums"] = 2
                segment_caption = model.chat(
                    image=None,
                    msgs=msgs,
                    tokenizer=tokenizer,
                    **params
                )
                caption_result[index] = segment_caption.replace("\n", "").replace("<|endoftext|>", "")
                torch.cuda.empty_cache()
    except Exception as e:
        error_queue.put(f"Error in segment_caption:\n {str(e)}")
        raise RuntimeError

def merge_segment_information(segment_index2name, segment_times_info, transcripts, captions):
    inserting_segments = {}
    for index in segment_index2name:
        inserting_segments[index] = {"content": None, "time": None}
        segment_name = segment_index2name[index]
        inserting_segments[index]["time"] = '-'.join(segment_name.split('-')[-2:])
        inserting_segments[index]["content"] = f"Caption:\n{captions[index]}\nTranscript:\n{transcripts[index]}\n\n"
        inserting_segments[index]["transcript"] = transcripts[index]
        inserting_segments[index]["frame_times"] = segment_times_info[index]["frame_times"].tolist()
    return inserting_segments
        
def retrieved_segment_caption(caption_model, caption_tokenizer, refine_knowledge, retrieved_segments, video_path_db, video_segments, num_sampled_frames):
    # model = AutoModel.from_pretrained('./MiniCPM-V-2_6-int4', trust_remote_code=True)
    # tokenizer = AutoTokenizer.from_pretrained('./MiniCPM-V-2_6-int4', trust_remote_code=True)
    # model.eval()
    
    caption_result = {}
    for this_segment in tqdm(retrieved_segments, desc='Captioning Segments for Given Query'):
        video_name = '_'.join(this_segment.split('_')[:-1])
        index = this_segment.split('_')[-1]
        video_path = video_path_db._data[video_name]
        timestamp = video_segments._data[video_name][index]["time"].split('-')
        start, end = eval(timestamp[0]), eval(timestamp[1])
        video = VideoFileClip(video_path)
        frame_times = np.linspace(start, end, num_sampled_frames, endpoint=False)
        video_frames = encode_video(video, frame_times)
        segment_transcript = video_segments._data[video_name][index]["transcript"]
        # query = f"The transcript of the current video:\n{segment_transcript}.\nGiven a question: {query}, you have to extract relevant information from the video and transcript for answering the question."
        query = f"The transcript of the current video:\n{segment_transcript}.\nNow provide a very detailed description (caption) of the video in English and extract relevant information about: {refine_knowledge}'"
        msgs = [{'role': 'user', 'content': video_frames + [query]}]
        params = {}
        params["use_image_id"] = False
        params["max_slice_nums"] = 2
        segment_caption = caption_model.chat(
            image=None,
            msgs=msgs,
            tokenizer=caption_tokenizer,
            **params
        )
        this_caption = segment_caption.replace("\n", "").replace("<|endoftext|>", "")
        caption_result[this_segment] = f"Caption:\n{this_caption}\nTranscript:\n{segment_transcript}\n\n"
        torch.cuda.empty_cache()
    
    return caption_result
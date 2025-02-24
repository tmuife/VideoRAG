import os
import logging
import warnings
import multiprocessing
from decouple import config
from datetime import datetime
import shutil
warnings.filterwarnings("ignore")
logging.getLogger("httpx").setLevel(logging.WARNING)

# Please enter your openai key
#os.environ["OPENAI_API_KEY"] = config("OCI_LLM_API_KEY")
#os.environ["OPENAI_BASE_URL"] = config("OCI_LLM_API_URL")
#llm_model = config("OCI_LLM_MODEL")
#embedding_model = config("OCI_EMBEDDING_MODEL")

from videorag._llm import *
from videorag import VideoRAG, QueryParam


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

    print("start customer data processing ...at " + datetime.now().strftime("%H:%M:%S"))
    # Please enter your video file path in this list; there is no limit on the length.
    # Here is an example; you can use your own videos instead.
    #video_paths = [
    #    '/home/ubuntu/data/videorag_video/多目标实拍.mp4',
    #]
    video_path = config("ORIGINAL_VIDEO_PATH")
    work_base_dir = config("WORKING_DIR")
    files = os.listdir(video_path)
    #video_paths = list(map(lambda filename: os.path.join(video_path,filename), files))

    for video in files:
        for split_interval in range(3, 30, 3):
            interval = str(split_interval)
            work_dir = os.path.join(os.path.join(work_base_dir,video[:-4]),interval)
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)  # Delete the directory
            os.makedirs(work_dir)  # Create the directory
            print(f"Directory '{work_dir}' is ready.")
            print(f"start {video} {interval} processing ...at " + datetime.now().strftime("%H:%M:%S"))
            videorag = VideoRAG(video_segment_length=3,cheap_model_func=gpt_4o_mini_complete, best_model_func=gpt_4o_mini_complete, working_dir=work_dir)
            videorag.insert_video(video_path_list=[os.path.join(video_path,video)])
            print(f"end {video} {interval} processing ...at " + datetime.now().strftime("%H:%M:%S"))
            if "Elderly-Fall" in video:
                if split_interval> 12:
                    break
    print("end customer data processing ...at " + datetime.now().strftime("%H:%M:%S"))
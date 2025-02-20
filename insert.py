import os
import logging
import warnings
import multiprocessing
from decouple import config
from datetime import datetime

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

    print("start customer data processing ...at "+ datetime.now().strftime("%H:%M:%S"))
    # Please enter your video file path in this list; there is no limit on the length.
    # Here is an example; you can use your own videos instead.
    video_paths = [
        '/home/ubuntu/data/videorag_video/多目标实拍.mp4',
    ]
    videorag = VideoRAG(cheap_model_func=gpt_4o_mini_complete, best_model_func=gpt_4o_mini_complete, working_dir=f"./videorag-workdir")
    videorag.insert_video(video_path_list=video_paths)
    print("end customer data processing ...at " + datetime.now().strftime("%H:%M:%S"))
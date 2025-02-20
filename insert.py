import os
import logging
import warnings
import multiprocessing
from decouple import config
from datetime import datetime

warnings.filterwarnings("ignore")
logging.getLogger("httpx").setLevel(logging.WARNING)

# Please enter your openai key
os.environ["OPENAI_API_KEY"] = config("OCI_LLM_API_KEY")
os.environ["OPENAI_BASE_URL"] = config("OCI_LLM_API_URL")
llm_model = config("OCI_LLM_MODEL")
embedding_model = config("OCI_EMBEDDING_MODEL")

from videorag._llm import *
from videorag import VideoRAG, QueryParam


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

    print("start customer data processing ...at "+ datetime.now().strftime("%H:%M:%S"))
    # Please enter your video file path in this list; there is no limit on the length.
    # Here is an example; you can use your own videos instead.
    video_paths = [
        '/home/ubuntu/data/videorag_video/偷鸡视频.mp4',
        '/home/ubuntu/data/videorag_video/偷鸡视频（完整版）.mp4',
        '/home/ubuntu/data/videorag_video/多目标实拍.mp4',
        '/home/ubuntu/data/videorag_video/婴儿睡醒.mp4',
        '/home/ubuntu/data/videorag_video/徘徊+停留+行为异常.mp4',
        '/home/ubuntu/data/videorag_video/徘徊视频.mp4',
        '/home/ubuntu/data/videorag_video/徘徊视频（含干扰片段）.mp4',
        '/home/ubuntu/data/videorag_video/楼道长时间停留.mp4',
        '/home/ubuntu/data/videorag_video/正常出门.mp4',
        '/home/ubuntu/data/videorag_video/正常路过.mp4',
        '/home/ubuntu/data/videorag_video/正常路过（含干扰片段）.mp4',
        '/home/ubuntu/data/videorag_video/老人跌倒.mp4',
    ]
    videorag = VideoRAG(cheap_model_func=oci_cohere_complete, best_model_func=oci_cohere_complete, working_dir=f"./videorag-workdir")
    videorag.insert_video(video_path_list=video_paths)
    print("end customer data processing ...at " + datetime.now().strftime("%H:%M:%S"))
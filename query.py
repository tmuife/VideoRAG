import os, sys
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

    #print("start customer data processing ...at "+ datetime.now().strftime("%H:%M:%S"))
    #querys = ["Please list all actions in the video along with their timestamps and descriptions."
    #    , "Please identify the individuals in the video and provide their identity information."
    #    , "Please detect specific events occurring in the video and provide their timestamps."
    #    , "Please classify the behaviors in the video and list the occurrence times for each behavior."
    #    , "Please track the movement trajectory of the specified object in the video and provide the coordinates."
    #    , "Please analyze the group behavior patterns in the video and describe their changes."
    #    , "Please identify and track specific objects in the video and provide their movement paths."]
    #querys = ["Please list all actions in the video along with their timestamps and descriptions."]
    #query = 'What is the relationship between Iron Man and Spider-Man? How do they meet, and how does Iron Man help Spider-Man?'
    querys = []
    param = QueryParam(mode="videorag")
    # if param.wo_reference = False, VideoRAG will add reference to video clips in the response
    param.wo_reference = True

    work_base_dir = config("WORKING_DIR")
    work_dir = ""
    if len(sys.argv) > 2:
        querys.append(str(sys.argv[2]))
    else:
        exit(-1)
    #videorag = VideoRAG(cheap_model_func=oci_cohere_complete, best_model_func=oci_cohere_complete, working_dir=f"./videorag-workdir")
    videorag = VideoRAG(cheap_model_func=gpt_4o_mini_complete,
                        best_model_func=gpt_4o_mini_complete,
                        working_dir=os.path.join(work_base_dir,str(sys.argv[1])))
    videorag.load_caption_model(debug=False)
    for query in querys:
        #print(f"start [{query}]"+"**"*50)
        response = videorag.query(query=query, param=param)
        print(response)
        #print(f"end [{query}]" + "**" * 50)
    #print("end customer data processing ...at " + datetime.now().strftime("%H:%M:%S"))
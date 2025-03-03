from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Query, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, Any
from decouple import config
import sys, os,json
import shutil
from pathlib import Path
from typing import Annotated, List, Dict, Any
import os, sys
import logging
import warnings
import multiprocessing
import asyncio
warnings.filterwarnings("ignore")
logging.getLogger("httpx").setLevel(logging.WARNING)

video_storage_path = config("VIDEO_STORAGE_PATH")

from videorag._llm import *
from videorag import VideoRAG, QueryParam
videorag:VideoRAG

@asynccontextmanager
async def lifespan(app: FastAPI):
    #spawn 兼容性好，子进程全新启动，但创建速度慢
    #fork 快速，子进程共享父进程的内存，但在多线程时可能有问题
    multiprocessing.set_start_method('spawn')
    #global videorag
    #videorag = VideoRAG(cheap_model_func=gpt_4o_mini_complete,
    #                    best_model_func=gpt_4o_mini_complete,
    #                    working_dir=os.path.join(work_base_dir,str(sys.argv[1])[:-4]))
    #videorag.insert_video(video_path_list=video_paths)
    #del videorag
    #import gc
    #gc.collect()  # 运行 Python 垃圾回收
    #import torch
    #torch.cuda.empty_cache()  # 释放未使用的 GPU 显存
    print("done!")
    yield


app = FastAPI(
    title="LightRAG API", description="API for RAG operations", lifespan=lifespan
)
# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", summary="default")
async def default(request: Request):
    return templates.TemplateResponse(
        request=request, name="chat.html"
    )
#@app.post("/upload")
#async def upload(files: Annotated[list[bytes], File()],request: Request):
#    for file in files:
#        try:
#            file_name = file.filename
#            content = file.decode("utf-8")
#            print(request)
#        except UnicodeDecodeError:
#            # If UTF-8 decoding fails, try other encodings
#            content = file.decode("gbk")
#        # Insert file content
#        #loop = asyncio.get_event_loop()
#        ##await loop.run_in_executor(None, lambda: rag.insert(content))
#        #await rag.ainsert(content)
#        #return Response(
#        #    status="success",
#        #    message=f"File content inserted successfully",
#        #)
"""
curl -X 'POST' \
  'http://127.0.0.1:8000/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example.txt'
"""
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    work_base_dir = file_name[:-4]
    print(file_name)
    file_location = os.path.join(video_storage_path, file_name)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    global videorag
    videorag = VideoRAG(cheap_model_func=gpt_4o_mini_complete,
                        best_model_func=gpt_4o_mini_complete,
                        working_dir=work_base_dir)
    videorag.insert_video(video_path_list=[file_location])
    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(config("RUN_PORT")))
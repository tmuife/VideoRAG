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

from videorag.cache import AsyncStatus

warnings.filterwarnings("ignore")
logging.getLogger("httpx").setLevel(logging.WARNING)

video_storage_path = config("VIDEO_STORAGE_PATH")

from videorag._llm import *
from videorag import VideoRAG, QueryParam
from videorag.cache import AsyncStatus
#videorag:VideoRAG

class ChatRequest(BaseModel):
    message: str
    query_type: str
    workspace: str
class Response(BaseModel):
    status: str
    data: Optional[Any] = None
    message: Optional[str] = None
def jsonMsg(status,data,error):
    result = {}
    result["status"] = status
    if "success" == status:
        result["data"] = data
    else:
        result["error"] = error
    return json.dumps(result)
status = AsyncStatus()
@asynccontextmanager
async def lifespan(app: FastAPI):
    #spawn 兼容性好，子进程全新启动，但创建速度慢
    #fork 快速，子进程共享父进程的内存，但在多线程时可能有问题
    multiprocessing.set_start_method('spawn')
    #del videorag
    #import gc
    #gc.collect()  # 运行 Python 垃圾回收
    #import torch
    #torch.cuda.empty_cache()  # 释放未使用的 GPU 显存
    print("lifespan done!")
    loop = asyncio.get_running_loop()
    print(id(loop))
    status.set_id(str(id(loop)))
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
    print(file_name)
    file_location = os.path.join(video_storage_path, file_name)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "insert_param.py",file_name], capture_output=True, text=True)  # Linux/macOS
    # result = subprocess.run(["dir"], capture_output=True, text=True, shell=True)  # Windows
    print(result.stdout)  # 输出命令结果
    insert_result = result.stdout
    return JSONResponse(content={"message": "File uploaded successfully", "insert_result": insert_result})

@app.post("/get_workspapces")
async def get_workspapces(request: ChatRequest):
    work_dir = config("WORKING_DIR")
    print("Will find work_dir from "+work_dir)
    work_spaces = []
    files = os.listdir(work_dir)
    for f in files:
        if os.path.isdir(f):
            work_spaces.append({"id":f,"name":f})
    #return JSONResponse(content={"message": "File uploaded successfully", "work_spaces": work_spaces})
    return jsonMsg(status="success", data=work_spaces, error="")


@app.post("/chat")
async def chat(request: ChatRequest):
    print("chat")
    workspace = str(request.workspace)
    query = str(request.message)
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "query.py",workspace,query], capture_output=True, text=True)  # Linux/macOS
    # result = subprocess.run(["dir"], capture_output=True, text=True, shell=True)  # Windows
    stdout = str(result.stdout)  # 输出命令结果
    return Response(status="success", data=stdout)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(config("RUN_PORT")))

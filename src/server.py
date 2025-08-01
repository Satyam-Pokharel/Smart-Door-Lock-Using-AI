from fastapi import FastAPI, WebSocket, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from .stream import WebStream
from .detection import compare_face
from .motorController import MotorController
import os
import asyncio
import requests
from collections import deque
import time
import secrets
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from bitmoro.bitmoro import Bitmoro
import time
import cv2

from src import WebCamVideoStream
from multiprocessing import Queue
from fastapi import FastAPI
import cv2
import os

class Password(BaseModel):
    password: str


bitmoro=Bitmoro("IRKxHu38hLv7yqb0bICg-26585f1754a4d53a7498f44740d03c4737e7b87ab9224a67df44ba252496")
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.abspath("./frontEnd")), name="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
connectedDevice = deque()
stream = WebStream()
camera=cv2.VideoCapture(0)
stream.connectToCamera(camera)

motor = MotorController()
cookies = []


def runCamera(queue):
    stream.camera(queue)


def authenticate(req):
    try:
        if req.cookies["code"] in cookies:
            return True
        else:
            return False
    except:
        return False

@app.post("/login")
def login(response: Response, password: Password):
    if password.password != open(os.path.join(os.getcwd(), "src/masterpassword.txt"), "r").read().strip():
        return {"msg": "Wrong Password access Denied"}
    secret = secrets.token_hex(10)
    cookies.append(secret)
    response.set_cookie("code", secret, 24*60*60*60, expires=1*60*60)
    return {"msg": "success"}

@app.post("/emergency-unlock")
async def emergency_unlock(res:Response,password: Password):
    if password.password != open(os.path.join(os.getcwd(), "src/masterpassword.txt"), "r").read().strip():
        res.status_code=400
        return {"msg": "Wrong Password access Denied"}
    motor.open()
    await bitmoro.send_bulk_message("Your Door has been Unlocked Emergently",["9869618708"])
    res.status_code=200
    return {"msg": "Lock opened"}

# @app.get("/train")
# async def train(websocket: WebSocket):
#     if not authenticate(websocket):
#         return {"msg": "Login First"}
#     take_register_user()

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    if not authenticate(websocket):
        return {"msg": "Login First"}
    await asyncio.sleep(0)
    await websocket.accept()
    connectedDevice.append(websocket)
    while True:
        await asyncio.sleep(0)
        while connectedDevice:
            try:
                await asyncio.sleep(0)
                sock = connectedDevice.popleft()
                await sock.send_bytes(stream.streams())
                connectedDevice.append(sock)
            except Exception as e :
                print(e)
                pass

@app.get("/open-lock")
async def open_lock(req: Request,res:Response):
    if not authenticate(req):
        return {"msg": "Login First"}
    if not motor.isOpen:
        if(await compare_face()):
            motor.open()
            await bitmoro.send_bulk_message("Your door has been unlocked",["9869618708"])
            return {"msg": "Lock opened"}
        else:
            await bitmoro.send_bulk_message("Unauthorized access to door lock",["9869618708"])
            res.status_code=400
            return {"msg": "FaceId doesn't match"}
    return {"msg": "Lock was opened"}

@app.get("/forget-password")
async def close_lock(req: Request):
    password=open(os.path.join(os.getcwd(), "src/masterpassword.txt"), "r").read().strip()
    await bitmoro.send_bulk_message("Your password for door is "+ password,["9869618708"])
    return {"msg": "Password sent to your phone"}


@app.get("/close-lock")
def close_lock(req: Request):
    if not authenticate(req):
        return {"msg": "Login First"}
    if motor.isOpen:
        motor.close()
        return {"msg": "Lock closed"}
    return {"msg": "Lock was closed"}

@app.get("/lock-status")
def status(req: Request,res:Response):
    if not authenticate(req):
        return {"msg": "Login First"}
    if motor.isOpen:
        motor.close()
        return {"msg": "Lock closed"}
    return {"msg": "Lock was closed"}


@app.get("/status")
def status(req: Request):
    if not authenticate(req):
        return {"msg": "Login First"}
    if motor.isOpen:
        return {"msg": "Open"}
    else:
        return {"msg": "closed"}

@app.on_event("shutdown")
def shutdown_event():
    motor.close()
    motor.flush()
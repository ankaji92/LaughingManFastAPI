import uvicorn
import cv2

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from pyscripts.camera import Camera
from pyscripts.laughing_man import LaughingManMaskStream, detect_faces, overlay_lms

from sqlalchemy.orm import sessionmaker
from pyscripts.db import Face, engine

def insert(faces):

    session = SessionClass()
    for face in faces:
        face_instance = Face()
        face_instance.st_x = int(face[0])
        face_instance.st_y = int(face[1])
        face_instance.width = int(face[2])
        face_instance.height = int(face[3])
        session.add(face_instance)
    session.commit()
    session.close()


SessionClass = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

def gen(camera):
    lm_mask_stream = LaughingManMaskStream()
    while True:
        frame = camera.get_frame()
        lm_mask = lm_mask_stream.next()

        faces = detect_faces(frame)
        frame = overlay_lms(frame, faces, lm_mask)
        insert(faces)

        _, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n')

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    return  StreamingResponse(gen(Camera()),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/result_feed', response_class=JSONResponse)
async def result_feed():
    datasets = [
        { "label": "Red",
          "data": [1, 2, 3, 5, 7, 11],
          "borderColor": '#f88'
        },
        { "label": "Green",
          "data": [2, 4, 6, 8, 10, 12],
          "borderColor": '#8f8'
        },
        { "label": "Blue",
          "data": [1, 2, 4, 8, 16, 32],
          "borderColor": '#88f'
        }
    ]
    return JSONResponse(datasets)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

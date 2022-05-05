import uvicorn
import cv2

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from pyscripts.camera import Camera
from pyscripts.laughing_man import LaughingManMaskStream, detect_faces, overlay_lms

from pyscripts.db import insert_faces

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
        insert_faces(faces)

        _, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n')

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    return  StreamingResponse(gen(Camera()),
                    media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

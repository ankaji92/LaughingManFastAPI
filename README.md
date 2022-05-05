# LaughingManFastAPI
## Overview
Application that accesses to local web-camera, detects faces and shows a processed movie on web browser.

The detected faces are overlayed by laughing man gif in the movie.

## Rquirements
* python
    * python >= 3.8
    * opencv-python
    * fastapi
    * uvicorn
    * jinja2
    * sqlalchemy
* devices
    * WebCam (which can be detected by opencv-python)

## How To Start
1. Setup python environment by 
```shell
$ pipenv install
```
2. Download laughing man gif (e.g. https://tenor.com/view/ghost-shell-laughing-man-gif-5752519) as "./pyscripts/laughing_man.gif"
3. Set haarcascade xml path at ```PATH_TO_HAARCASCADE``` in [./pyscripts/laughing_man.py](./pyscripts/laughing_man.py)
4. run scripts by 
```shell
$ pipenv run python app.py
```
5. Access to the server URL ([localhost:8000](http://localhost:8000))
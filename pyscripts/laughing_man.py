import os
import cv2
import numpy as np

def _extract_fg(img):
    fg_region = np.zeros(img.shape)
    for v, line in enumerate(img):
        non_white_pxs = np.array(np.where(line < 250))
        if non_white_pxs.size > 0:
            min_h, max_h = np.min(non_white_pxs, axis=1)[0], np.max(non_white_pxs, axis=1)[0]
            fg_region[v, min_h:max_h, :] = 1
    return fg_region

class LaughingManMaskStream:
    def __init__(self, gif_path=os.path.join(os.path.abspath(__file__), "laughing_man.gif")):
        self.cap = cv2.VideoCapture(gif_path)
        self.fg_region = _extract_fg(self.cap.read()[1])
    
    def next(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        mask = frame * self.fg_region
        return mask
    
    def release(self):
        self.cap.release()

def detect_faces(img):
    PATH_TO_HAARCASCADE = '/haarcascade_frontalface_default.xml' # To Edit
    cascade = cv2.CascadeClassifier(PATH_TO_HAARCASCADE)

    small_img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
    faces = np.array(cascade.detectMultiScale(small_img)) * 4

    return faces

def _overlay_lm(frame, face, lm_mask):
    offset = 100
    x = int(max(face[0] - offset / 2, 0))
    y = int(max(face[1] - offset / 2, 0))
    w = int(min(face[2] + offset, frame.shape[1] - x))
    h = int(min(face[3] + offset, frame.shape[0] - y))

    lm_mask = cv2.resize(lm_mask, (w,h))
    mask_idxs = np.where(lm_mask>0)
    overlay_idxs = (mask_idxs[0]+y, mask_idxs[1]+x, mask_idxs[2])

    frame[overlay_idxs] = lm_mask[mask_idxs]
    return frame

def overlay_lms(frame, faces, lm_mask):
    if faces.shape[0] > 0:
        for face in faces:
            frame = _overlay_lm(frame, face, lm_mask)
    return frame
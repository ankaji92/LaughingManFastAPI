import cv2

class Camera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.frame_no = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.frame_no += 1
        _, image = self.video.read()
        return image

from .camera import WebCamVideoStream
class WebStream():

    def __init__(self):
        self.matched=True
        self.cam=WebCamVideoStream()
        
    def connectToCamera(self,camera):
        self.cam.connectToCamera(camera)

    def streams(self):
        try:
            image=self.cam.read()
            return image.tobytes()
        except Exception as e:
            return False
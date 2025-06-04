import cv2

class WebCamVideoStream():
    _instance = None
    
    def __init__(self):
        return None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def connectToCamera(self,camera):
        self.stream=camera
        self.open = True  
                
    def read(self):
        try:
            if self.open:
                self.rate,self.frame=self.stream.read()
                _,image=cv2.imencode(".jpg",self.frame)
                return image
        except Exception as e:
            print(e)
            return False
        
    def read_frame(self):
        self.rate,self.frame=self.stream.read()
        return self.frame

    def close(self):
        self.open=False
        self.stream.release()
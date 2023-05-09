import datetime
import picamera
import time, os
from pathlib import Path


class CameraInterface(object):
    def __init__(self, imgDir='', buffer_size=10):
        print("\nInitializing Camera ...\n")
        self.camera = picamera.PiCamera()
        self.camera.resolution = (720,480) # (1920, 1080)  # minimum 64*64
        self.camera.framerate = 10
        self.camera.annotate_text_size = 28  # default 32
        self.camera.annotate_foreground = picamera.Color('red')

        time.sleep(2)  # let camera warm-up

        self.buffer_size = buffer_size
        if not imgDir:
            self.imgDir = Path.cwd().parent / "server/static/images"
            #self.imgDir.mkdir(parents=True, exist_ok=True)
        else:
            self.imgDir = Path(imgDir)
            
        if not self.imgDir.exists(): 
            raise Exception("\nImage Directory Not Found !")
        
        self.initialize_buffer()
        print("Camera Ready !\n")

    def initialize_buffer(self):
        for _ in range(self.buffer_size):
            img_file = self.imgDir / f'image_{time.time()}.png'
            self.camera.annotate_text = datetime.datetime.now().strftime("%H:%M:%S / %d-%m-%Y")
            self.camera.capture(img_file.as_posix(), bayer=True)
            print(f"Writing Image {img_file.as_posix()}")

    def capture_image(self, filename: str = ''):
        if filename:
            img_file = filename
        img_file = self.imgDir / f'image_{time.time()}.png'
        self.camera.annotate_text = datetime.datetime.now().strftime("%H:%M:%S / %d-%m-%Y")
        self.camera.capture(img_file.as_posix(), bayer=True)
        
    def retrieve_latest_img(self, name_only=False):
        buffer_files = self.imgDir.glob('*.png')
        buffer_files = [x for x in buffer_files if x.is_file()]
        #latest_file = max(buffer_files, key=lambda x: os.path.getctime(x))
        avg_index = round((len(buffer_files)-1) / 2)
        files = sorted(buffer_files, key=lambda x: os.path.getctime(x))
        send_file = files[avg_index]
        if name_only:
            return send_file.name
        return send_file.as_posix()

    def remove_older_images(self):
        while True:
            buffer_files = self.imgDir.glob('*.png')
            buffer_files = [x for x in buffer_files if x.is_file()]
            if len(buffer_files) <= self.buffer_size:
                break
            oldest_file = min(buffer_files, key=lambda x: os.path.getctime(x))
            oldest_file.unlink()
    
    
if __name__=='__main__':
    camera = picamera.PiCamera()
    camera.resolution = (1920, 1080)
    camera.start_preview()
    time.sleep(30)
    camera.stop_preview()

import time
import threading
from .camera_interface import CameraInterface

class CameraThread(threading.Thread, CameraInterface):
	def __init__(self, imgDir='', buffer_size=10, name='cameraThread'):
		threading.Thread.__init__(self)
		CameraInterface.__init__(self, imgDir, buffer_size)
		self.name = name
		self.running = False
		self.daemon = True
		self.stop_event = threading.Event()
		
	def run(self):
		print ("\n%s has started execution " %self.name)
		self.running = True
		while True:	
			print("Camer Thread executing ...")
			self.capture_image()
			time.sleep(3)
			self.remove_older_images()
			time.sleep(3)
		print ("\n%s has finished execution " %self.name)
		self.running = False
	
	def stop(self):
		self.stop_event.set()
		
if __name__=='__main__':
	cameraThread = CameraThread()
	cameraThread.run()

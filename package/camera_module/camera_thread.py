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
		i = 0
		while True:	
			#print("Camer Thread executing ...")
			if i % 2:
				self.capture_image()
				print("Writing Image .... ")
			if i % 5:
				self.remove_older_images()
			i += 1
			time.sleep(3)
		print ("\n%s has finished execution " %self.name)
		self.running = False
	
	def stop(self):
		self.stop_event.set()
		
if __name__=='__main__':
	cameraThread = CameraThread()
	cameraThread.run()

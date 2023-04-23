import time
import picamera
import queue
from pathlib import Path


class CameraSensor(object):
	
	def __init__(self, img_dir, cache_size = 10, create_cache=True):
		print("Initializing Camera Module ...")
		self.camera = picamera.PiCamera()
		self.camera.resolution = (720, 480)
		self.camera.framerate = 10
		time.sleep(2) # let camera warm-up
		print("Camera Intialized !\n")
				
		self.buffer_size = cache_size
		self.imgQueue = queue.Queue(maxsize=cache_size)
		self.currImgIndex = -1 
		self.img_cache_dir = Path(img_dir)
		self.img_cache_dir.mkdir(parents=True, exist_ok=True)
		if create_cache:
			self.create_img_cache()
		
	def preview_img(self, duration = 50):
		camera.start_preview()
		time.sleep(duration)
		camera.stop_preview()
		return 
		
	def set_file_name(self, index):
		f = self.img_cache_dir / (str(index) + '.png')
		return f.as_posix()
	
	def create_img_cache(self):
		print("Creating Image Buffer ...")
		img_indices = list(range(1, self.buffer_size+1))
		img_files = list(map(self.set_file_name, img_indices))
		for f in img_files:
			self.camera.capture(f, bayer=True)
			self.imgQueue.put(f)
			self.currImgIndex += 1
			print(f"Writing image file : {f}")
		print(f"Created Image Buffer of size {self.buffer_size} !\n")
		return
	
	def update_img_cache(self):
		print("Updating Camera Buffer ... ") 
		self.currImgIndex %= self.buffer_size
		self.currImgIndex += 1	
		img_file = self.set_file_name(self.currImgIndex)
		print("Writing Image File: ", img_file)
		self.camera.capture(img_file, bayer=True)
		try:
			self.imgQueue.put(img_file)
			print("Wrote Image File .")
		except queue.Full:
			print("Creating Slot in Queue ...")
			self.imgQueue.get()
			self.imgQueue.put(img_file)
			print("Wrote Image File .")
		print("Image Buffer Updated !")
		return   
	
	def get_img_file(self, block=False):
		url = self.imgQueue.get()
		print(url)
		if not url:
			raise Exception("\nImage Queue Went Empty !!!")
		return url
	
		
	
if __name__=='__main__':
	capture = CameraSensor()
	capture.create_img_cache()
	print(capture.imgQueue)
#	while True:
#		capture.update_img_cache()
#		print(capture.get_img_file)


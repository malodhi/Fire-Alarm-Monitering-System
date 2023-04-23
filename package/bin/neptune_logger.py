from mcu_gateway import McuGateway
from img_capture import Camera
from datetime import datetime
from pathlib import Path
from neptune.types import File
import time
import neptune


# connect to project
# project = neptune.init_project(name="lodhi/fire-alarm", api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vbmV3LXVpLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9uZXctdWkubmVwdHVuZS5haSIsImFwaV9rZXkiOiJmMTY3YTExNC1kOTkzLTQ4OTUtOWI5OS1hOWQwNjYxY2EyMjUifQ==")

class NeptuneCloud(McuGateway, Camera):
	#run.stop()	

	def __init__(self):

		McuGateway.__init__(self)
		Camera.__init__(self)
		self.cwd = Path().cwd()
		self.run = neptune.init_run(
			project="lodhi/fire-alarm",  # workspace_bname/project_name
			api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vbmV3LXVpLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9uZXctdWkubmVwdHVuZS5haSIsImFwaV9rZXkiOiJmMTY3YTExNC1kOTkzLTQ4OTUtOWI5OS1hOWQwNjYxY2EyMjUifQ=="  
			)
		self.run["session/creation_date"] = datetime.fromisoformat("1998-11-01")
		self.run["session/smoke_quantity"] = list()
		self.run["session/images"] = list()
		
	def send_data_flask(self):
		qty = self.get_instant_data()
		img_file = self.cwd / 'static/images/picamera.png'
		self.capture_instant_img(img_file.as_posix())
		return qty
		
	def upload_data(self):
		self.run["session/start"] = datetime.now()
		try:
			while True:
				qty = self.get_instant_data()
				if qty:
					self.run["session/smoke_quantity"].append(qty)
					
				img_file = self.cwd / 'picamera.jpg'
				self.capture_instant_img(img_file.as_posix())
				
				if img_file.exists():
					self.run["session/images"].append(File(img_file.as_posix()))
					
				time.sleep(1)
		except KeyboardInterrupt:
			exit()
			

if __name__=='__main__':
	print("Hello")
	cloud_handler = NeptuneCloud()
	cloud_handler.upload_data()

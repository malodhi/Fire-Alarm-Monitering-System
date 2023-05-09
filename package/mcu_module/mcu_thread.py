import threading, time
from .mcu_interface import McuInterface

class McuThread(threading.Thread, McuInterface):
	def __init__(self, name='mcuThread'):
		
		threading.Thread.__init__(self)
		McuInterface.__init__(self)
		self.name = name
		self.smoke_qty = -1
		self.running = False
		self.daemon = True
		self.stop_event = threading.Event()
		
	def run(self):
		self.running = True
		print ("\n%s has started execution " %self.name)
		while True:
			#print("Mcu Thread Executing")
			val = self.get_instant_data()
			if val != -1:
				print(f"Smoke Quantity ====>  {str(val)}")
				self.smoke_qty = val
			time.sleep(1)
		print ("\n%s has finished execution " %self.name)
		self.running = False

	def stop(self):
		self.stop_event.set()

if __name__=='__main__':
	mcuThread = McuThread()
	mcuThread.run()

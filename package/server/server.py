import threading, time
from flask import Flask, render_template, jsonify
from datetime import datetime


from package.email_module.email_notifier import EmailNotifier
from package.camera_module.camera_thread import CameraThread
from package.mcu_module.mcu_thread import McuThread



class Server:
    def __init__(self):
        self.imgDir = 'static/images/'
        self.smoke_threshold = 1
        self.app = Flask(__name__)
        self.email_send = False
        
        # Set up a basic HTML template for your webpage
        @self.app.route("/")
        def index():
            return render_template("index.html")
            
            
        # Route to serve the live fire monitoring data as a JSON response
        @self.app.route("/data")
        def data():
            data = {
                "img_url": self.imgDir + self.cameraThread.retrieve_latest_img(name_only=True),
                "smoke_quantity": self.mcuThread.smoke_qty,
                "timestamp": datetime.now().strftime("%H:%M:%S / %d-%m-%Y") #("%Y-%m-%d %H:%M:%S")
                }
            return jsonify(data)


    def start_flask_app(self):
        self.app.run(host='0.0.0.0', threaded=True, debug=False)


    def main(self):
        #log = logging.getLogger('werkzeug')
        #log.setLevel(logging.ERROR)
        self.mcuThread = McuThread()
        self.mcuThread.start()
        while self.mcuThread.smoke_qty > self.smoke_threshold:
            time.sleep(1)
            continue
        self.cameraThread = CameraThread()
        self.cameraThread.start()
        myfile = self.imgDir + self.cameraThread.retrieve_latest_img(name_only=True)
        print(f"\n\n{myfile}")
        EmailNotifier().send_emails(smoke_qty=self.mcuThread.smoke_qty, img_file=myfile)
        print("\n\n Email Sent !!!!!!!!!")
        flask_thread = threading.Thread(target=self.start_flask_app)
        flask_thread.daemon = False
        flask_thread.start()
        print("\n\nI am running !!!!!!!!!!")



if __name__ == "__main__":
    api = Server()
    api.main()

            
        

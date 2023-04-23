
import time
import logging
from threading import Thread
from datetime import datetime
from flask import Flask, render_template, jsonify

from package.mcu_pkg.mcu_interface import McuInterface
from package.email_pkg.email_notifier import EmailNotifier
from package.camera_pkg.camera_interface import CameraInterface

smoke_sensor = McuInterface()
camera_sensor = CameraInterface(imgDir='static/images', buffer_size=10)    

smoke_qty = -1
email_sent = False
smoke_threshold = 20

app = Flask(__name__)


def update_camera_cache():
    while True:
        camera_sensor.capture_image()
        time.sleep(2)
        camera_sensor.remove_older_images()
        time.sleep(1)
        

@app.route("/data")
def data():
    
    smoke_qty = smoke_sensor.get_instant_data()
    img_url = camera_sensor.retrieve_latest_img()
    #print("Smoke Quantity   =  " , str(smoke_qty))

    data = {
        "img_url": img_url,
        "smoke_quantity": smoke_sensor.get_instant_data(),
        "timestamp": datetime.now().strftime("%H:%M:%S  /  %d-%m-%Y")
        }
    return jsonify(data)


@app.route("/")
def index():
    return render_template("index.html")


def main():     
    
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=False, host='0.0.0.0')
    
    print("\n\nHello \n\n")
    



camera_thread = Thread(target=update_camera_cache)
camera_thread.start()
        

if __name__ == "__main__":
#    if not email_sent and (smoke_qty < smoke_threshold):
        #camera_thread = Thread(target=update_camera_cache)
        #camera_thread.start()
#        print("\nEmail Send.\n")
#        EmailNotifier().send_emails(smoke_qty, '../server/'+img_url)
#        email_sent = True
        
    app.run(debug=False, host='0.0.0.0')
    #main()

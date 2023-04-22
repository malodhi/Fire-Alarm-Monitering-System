
from flask import Flask, render_template, jsonify
from datetime import datetime
from threading import Thread
import logging
import time

from mcu_interface import McuInterface
from camera_interface import CameraInterface


app = Flask(__name__)
#global smoke_qty
#smoke_qty = -1
 
smoke_sensor = McuInterface()
camera_sensor = CameraInterface(imgDir='static/images', buffer_size=10)    


def update_camera_cache():
    while True:
        camera_sensor.capture_image()
        time.sleep(3)
        camera_sensor.remove_older_images()
        time.sleep(3)
        
def update_smoke_qty():
    while True:
        smoke_qty = smoke_sensor.get_instant_data()
    
# Set up a basic HTML template for your webpage
@app.route("/")
def index():
    return render_template("index.html")

# Route to serve the live fire monitoring data as a JSON response
@app.route("/data")
def data():
    
    #smoke_qty = smoke_sensor.get_instant_data()
    img_url = camera_sensor.retrieve_latest_img()

    data = {
        "img_url": img_url,
        "smoke_quantity": smoke_qty,
        "timestamp": datetime.now().strftime("%S:%M:%H") #("%Y-%m-%d %H:%M:%S")
        }
    return jsonify(data)

camera_thread = Thread(target=update_camera_cache)
#smoke_thread = Thread(target=update_smoke_qty)

camera_thread.start()
#smoke_thread.start()


if __name__ == "__main__":
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)
    app.run(debug=False, host='0.0.0.0')

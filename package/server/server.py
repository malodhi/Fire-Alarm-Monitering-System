
from flask import Flask, render_template, jsonify
from datetime import datetime


from package.email_module.email_notifier import EmailNotifier
from package.camera_module.camera_thread import CameraThread
from package.mcu_module.mcu_thread import McuThread

mcuThread = McuThread()
cameraThread = CameraThread()
email_handler = EmailNotifier()

app = Flask(__name__)

imgDir = '/static/images/'
smoke_threshold = 30

# Set up a basic HTML template for your webpage
@app.route("/")
def index():
    return render_template("index.html")
    
# Route to serve the live fire monitoring data as a JSON response
@app.route("/data")
def data():
    print("Smoke Qty:   ", mcuThread.smoke_qty)
    data = {
        "img_url": imgDir + cameraThread.retrieve_latest_img(),
        "smoke_quantity": mcuThread.smoke_qty,
        "timestamp": datetime.now().strftime("%S:%M:%H") #("%Y-%m-%d %H:%M:%S")
        }
    return jsonify(data)


if __name__ == "__main__":
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)
    server_up = False
    mcuThread.run()
    print("Hello World ")
    while mcuThread.running:
        print("Smoke Quantity:  ", str(mcuThread.smoke_qty))
        if (smoke_threshold < mcuThread.smoke_qty) and (not cameraThread.running):
            cameraThread.run()
            email_handler.send_emails(mcuThread.smoke_qty,
                                        cameraThread.retrieve_latest_img())
            print("Email Sent To Users.")
            if (not server_up):
                server_up = True
                app.run(debug=False, host='0.0.0.0')

        elif (smoke_threshold > mcuThread.smoke_qty) and (cameraThread.running):
            cameraThread.stop()
            
        

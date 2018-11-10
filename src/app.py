from flask import Flask, render_template, request, jsonify
import datetime

import utils
import hit


startTime = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")

app = Flask(__name__)

@app.route("/")
def show_details() :
    global startTime
    return "<html>" + \
           "<head><title>Docker + Flask Demo</title></head>" + \
           "<body>" + \
           "<table>" + \
           "<tr><td> Start Time </td> <td>" +  startTime + "</td> </tr>" \
           "<tr><td> Hostname </td> <td>" + utils.gethostname() + "</td> </tr>" \
           "<tr><td> Local Address </td> <td>" + utils.getlocaladdress() + "</td> </tr>" \
           "<tr><td> Remote Address </td> <td>" + request.remote_addr + "</td> </tr>" \
           "<tr><td> Server Hit </td> <td>" + str(hit.getServerHitCount()) + "</td> </tr>" \
           "<tr><td> JSON </td> <td> <a href='/json'>JSON</a> </td> </tr>" \
           "<tr><td> Joystick </td> <td> <a href='/joystick'>Joystick</a> </td> </tr>" \
           "</table>" + \
           "</body>" + \
           "</html>"

@app.route('/joystick')
def joystick():
    return app.send_static_file('joystick.html')

@app.route("/json")
def send_json() :
    global startTime
    return jsonify( {'StartTime' : startTime,
                     'Hostname': utils.gethostname(),
                     'LocalAddress': utils.getlocaladdress(),
                     'RemoteAddress':  request.remote_addr,
                     'Server Hit': str(hit.getServerHitCount())} )

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')

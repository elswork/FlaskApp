from gpiozero import Motor
from flask import Flask, render_template, request, jsonify
import datetime
import time
import utils
import hit

motor1 = Motor(8, 7)
motor2 = Motor(24, 23)

diff = 0.75
sstop = 0.092

startTime = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")

app = Flask(__name__, static_url_path='')

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
           "<tr><td> Joystick controller </td> <td> <a href='/joystick'>Joystick</a> </td> </tr>" \
           "<tr><td> Go Function </td> <td> <a href='/go'>Go</a> </td> </tr>" \
           "<tr><td> Comander controller</td> <td> <a href='/comander'>Comander</a> </td> </tr>" \
           "<tr><td> Move Function </td> <td> <a href='/move'>Move</a> </td> </tr>" \
           "</table>" + \
           "</body>" + \
           "</html>"

@app.route('/joystick')
def joystick():
    return app.send_static_file('joystick.html')

@app.route('/comander')
def comander():
    return app.send_static_file('comander.html')

@app.route("/go")
def go():
    B = request.args.get('A', default = 1.0, type = float)
    A = request.args.get('B', default = 1.0, type = float)
    A=A/2
    B=B/10
    if -sstop < A < sstop and sstop < B < sstop:
        #time.sleep(0.2)
        motor1.stop()
        motor2.stop()

    elif A <= 0:
        if B <= 0:
            motor1.backward(abs(A)-B)
            motor2.backward(abs(A*diff))
        else:
            motor1.backward(abs(A))
            motor2.backward(abs(A*diff)-B)
    else:
        if B <= 0:
            motor1.forward(A)
            motor2.forward((A*diff)-abs(B))
        else:
            motor1.forward(A-B)
            motor2.forward(A*diff)   
    return 'A: '+str(A)+'|B: '+str(B)

@app.route("/move")
def move():
    X = request.args.get('X', default = 1.0, type = float)
    M = request.args.get('M', default = 0, type = int)
    T = request.args.get('T', default = 0, type = int)
    Move = "none"
    if M==1:
        motor1.forward(X)
        motor2.forward(X*diff)
        Move = "Forward"
    elif M==2:
        motor1.forward(X)
        motor2.backward(X*diff)
        Move = "Left"
    elif M==3:
        motor1.backward(X)
        motor2.forward(X*diff)
        Move = "Right"
    elif M==4:
        motor1.backward(X)
        motor2.backward(X*diff)
        Move = "Backward"
        
    if T!=0 or M==0:
        time.sleep(T/100)
        motor1.stop()
        motor2.stop()
    global startTime
    # return 'X: '+str(X)+' |M: '+str(M)+' |T: '+str(T)
    return jsonify( {'StartTime' : startTime,
                     'Speed': str(X),
                     'Movement': Move,
                     'Time': str((T/100))} )

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

from flask import Flask, render_template, request
import datetime
import time
import board
import neopixel
import threading
import math
import serial
intFinal = 0


ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

startSecondThread = 0
pixel_pin = board.D18
num_pixels = 24
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

pixels.fill((0, 255, 0))
pixels.show()

app = Flask(__name__)

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'TVstopper',
      'time': timeString
      }
   return render_template('index.html', **templateData)

@app.route('/', methods =["GET", "POST"])
def handle_data():
    global timerTotal
    if request.method == "POST":
       # getting input with name = fname in HTML form
       timerSeconds = request.form.get("tSec")
       timerMinutes = request.form.get("tMin")
       timerHours = request.form.get("tHour")
       if timerHours == "":
           timerHours = 0
       if timerSeconds == "":
           timerSeconds = 0
       if timerMinutes == "":
           timerMinutes = 0
       templateData = {
        'timerSeconds' : timerSeconds,
        'timerMinutes' : timerMinutes,
        'timerHours' : timerHours
        }
       timerMinutesInSec = int(timerMinutes) * 60
       timerHoursInSec = int(timerHours) * 3600
       timerTotal = timerHoursInSec + timerMinutesInSec +int(timerSeconds)
       print("amount of seconds for timer")
       print(timerTotal)
       timerThread.start()
       return render_template('timerset.html', **templateData)

@app.route('/timerDone', methods = ["GET"])
def timerDone():
    if timerState == 1:
        timerDone = "not done"
    if timerState == 0:
        timerDone = "done"
    templateData = {
     'timerState' : timerDone,
     'timeLeft': math.floor(timeLeft)
     }
    return render_template('timerDone.html', **templateData)

@app.route('/jumps', methods = ["GET"])
def jumps():
    templateData = {
    'jumps': intFinal
    }
    return render_template('jumps.html', **templateData)

def Timer():
    global timerState
    global timeLeft
    starttime =time.time()
    currenttime= time.time()
    x = 0
    timerState = 1
    pixelChangePS = timerTotal / num_pixels
    print(pixelChangePS)
    pixelChange = pixelChangePS
    while timerState == True:
        if timerTotal > (currenttime - starttime):
            if(starttime + pixelChange) < currenttime:
                timeCMS = currenttime - starttime
                timeLeft = timerTotal - timeCMS
                pixels[x] = (255, 0, 0)
                pixels.show()
                x = x+1
                pixelChange = pixelChange + pixelChangePS
                print(timeLeft)
            currenttime = time.time()
        else:
            timeLeft = 0
            print("timer is done")
            pixels.fill((255,0,0))
            pixels.show()
            time.sleep(0.25)
            pixels.fill((0,0,0))
            pixels.show()
            time.sleep(0.25)
            pixels.fill((255,0,0))
            pixels.show()
            timerState = 0


def TeenToRPI():
    global intFinal
    read_ser=ser.readline()
    strVal = str(read_ser)
    splitie = strVal.split("'")
    intToBeSplit =splitie[1]
    intList = intToBeSplit.split("\\")
    intFinal = int(intList[0])
    print(intFinal)


timerThread = threading.Thread(target = Timer)
webThread = threading.Thread(target = app.run(host='0.0.0.0', port=80, debug=True))

webThread.start()

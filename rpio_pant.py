#!/usr/bin/env python2.7

import RPIO
import time
import MySQLdb as db
from flask import Flask
from flask.ext.jsonpify import jsonify

"""
    gpio counter stuff

"""

RPIO.setup(15, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
RPIO.setup(17, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
RPIO.setup(18, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)

counter = 0
activation = {15:0, 17:0, 18:0}
debounce = {15:0, 17:0, 18:0}
prev_state = {15:False, 17:False, 18:False}

def gpio_event(gpio_id, val):
    #Las in status
    state = RPIO.input(gpio_id)

    #Kontrollera om statusen har andrat pa sig, annars ignorera genom return
    if state==prev_state[gpio_id]:
        return

    #Spara den nya statusen
    prev_state[gpio_id] = state

    #print("gpio %s: %s" % (gpio_id, state))

    if gpio_id==15:
        if state:
            reset_counter()
        return

    
    if state: #Stralen har brutits
        if debounce[gpio_id]==0 or debounce[gpio_id]<(time.time()*1000):
            activation[gpio_id] = time.time() * 1000
        else:
            print("gpio %s: Ignore" % (gpio_id))

            #Forlang debounce tiden
            debounce[gpio_id] = time.time()*1000+300;
    else: #Signalen ar tillbaka igen
        if activation[gpio_id]>0:
            pulse_length = (time.time() * 1000) - activation[gpio_id];
            activation[gpio_id] = 0;

            if pulse_length>20 and pulse_length<120:
                # Godkand signal
                debounce[gpio_id] = time.time()*1000+300;
                register_can()
                print("gpio %s: success %s" % (gpio_id,pulse_length))
            else:
                # For lang eller for kort signal
                print("gpio %s: pulse length %s" % (gpio_id,pulse_length))

def register_can():
    global counter
    counter += 1
    print counter

    #init database
    booth = 'd'
    timenow = time.strftime('%Y-%m-%d %H:%M:%S')
    dbconn = db.connect('localhost', 'pant', 'vaJdDZqTQFw8ENDK', 'pant')
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO pant.dhw13(date,booth) VALUES (%s,%s)", (timenow,booth))
    dbconn.commit()
    dbconn.close()

def reset_counter():
    global counter
    counter = 0
    print counter

    print("RESET")


RPIO.add_interrupt_callback(15, gpio_event, edge='both', threaded_callback=True, debounce_timeout_ms=1)
RPIO.add_interrupt_callback(17, gpio_event, edge='both', threaded_callback=True, debounce_timeout_ms=1)
RPIO.add_interrupt_callback(18, gpio_event, edge='both', threaded_callback=True, debounce_timeout_ms=1)

RPIO.wait_for_interrupts(threaded=True)

"""
    internal webserver for showing cans via jsonp

"""

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    return jsonify(count=counter)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

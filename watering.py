from flask import Flask
from flask import request, escape, jsonify, render_template, redirect, url_for
import sqlite3
import datetime
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Motor

dbfilename = 'watering.db'

app = Flask(__name__)

def get_history():
    history = []
    entry = { 'date': 123454464, 'text': "First entry of history" }
    history.append(entry)
    return history

def get_pumps():
    pumps = []
    pump1 = { 'id': 1, 'name': "Eins", 'milliseconds': 1000, 'hour': 14, 'days': 12345 }
    pumps.append(pump1)
    return pumps

@app.route('/')
def index():
    conn = sqlite3.connect(dbfilename)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    pumps = []
    for row in c.execute('SELECT * FROM pumps'):
        pumps.append({ "id": row["id"], "name": row["name"], "seconds": row["milliseconds"] / 1000, "hour": row["hour"]})
    history = []
    for row in c.execute('SELECT * FROM history ORDER BY date DESC'):
        history.append({ "date": datetime.datetime.fromtimestamp(row["date"]), "text": row["text"]})
    conn.close()
    return render_template("index.html", pumps=pumps, history=history)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename = 'favicon.ico'))

@app.route("/history")
def api_history():
    history = get_history()
    return jsonify(history)

@app.route('/pumps')
def api_pumps():
    pumps = get_pumps()
    return jsonify(pumps)

@app.route('/pump/<number>', methods=['POST'])
def api_pump(number):
    pump = request.get_json()
    conn = sqlite3.connect(dbfilename)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    data = (pump["name"], pump["milliseconds"], pump["hour"], pump["days"], pump["id"])
    c.execute("UPDATE pumps SET name = ?, milliseconds = ?, hour = ?, days = ? WHERE id = ?", data)
    history = (datetime.datetime.now().timestamp(), "Updated pump {}".format(pump["id"]))
    c.execute("INSERT INTO history VALUES (?,?)", history)
    conn.commit()
    conn.close()
    return 'Saved pump {}'.format(escape(number))

@app.route('/pump/<number>/test', methods=['POST'])
def api_pump_test(number):
    pump1_pin1=26
    pump1_pin2=19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pump1_pin1, GPIO.OUT)
    GPIO.setup(pump1_pin2, GPIO.OUT)

    test = request.get_json()
    milliseconds = test["milliseconds"]
    conn = sqlite3.connect(dbfilename)
    conn.row_factory = sqlite3.Row
    for row in conn.cursor().execute('SELECT * FROM pumps WHERE id = ?', number):
            entry = (datetime.datetime.now().timestamp(), "Starting pump {} for {} seconds".format(row["id"], milliseconds / 1000))
            conn.cursor().execute("INSERT INTO history VALUES (?,?)", entry)
            conn.commit()
            motor = Motor(pump1_pin1, pump1_pin2)
            motor.forward(1)
            sleep(milliseconds / 1000)
            motor.stop()
            entry = (datetime.datetime.now().timestamp(), "Stopping pump {}".format(row["id"]))
            conn.cursor().execute("INSERT INTO history VALUES (?,?)", entry)
            conn.commit()
 

import sqlite3
import os.path
import datetime
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Motor

dbfilename = '/home/pi/watering/watering.db'
pump1_pin1=26
pump1_pin2=19

GPIO.setmode(GPIO.BCM)
GPIO.setup(pump1_pin1, GPIO.OUT)
GPIO.setup(pump1_pin2, GPIO.OUT)

def initialize():
    if os.path.isfile(dbfilename):
        conn = sqlite3.connect(dbfilename)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    else:
        conn = sqlite3.connect(dbfilename)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''CREATE TABLE history (date integer, text text)''')
        c.execute('''CREATE TABLE pumps (id integer primary key, name text, milliseconds integer, hour integer, days text)''')
        entry = (datetime.datetime.now().timestamp(), "Created database")
        c.execute("INSERT INTO history VALUES (?,?)", entry)
        #pumps = [ (1, '1', 3000, 13, '12345'), (2, '2', 3000, 13, '12345') ]
        pumps = [ (1, '1', 30000, 11, '1234567') ]
        c.executemany("INSERT INTO pumps VALUES (?,?,?,?,?)", pumps)
        conn.commit()
    return conn

def print_history(conn):
    for row in conn.cursor().execute('SELECT * FROM history ORDER BY date'):
        print('{} {}'.format(datetime.datetime.fromtimestamp(row["date"]).strftime('%Y-%m-%d %H:%M:%S'), row["text"]))

def run_motors(conn):
    entry = (datetime.datetime.now().timestamp(), "Cron job executed")
    conn.cursor().execute("INSERT INTO history VALUES (?,?)", entry)
    conn.commit()
    for row in conn.cursor().execute('SELECT * FROM pumps ORDER BY id'):
        # TODO: Check if correct day
        # Check if correct time
        now = datetime.datetime.now()
        if (now.hour == row["hour"]):
            entry = (datetime.datetime.now().timestamp(), "Starting pump {} for {} seconds".format(row["id"], row["milliseconds"] / 1000))
            conn.cursor().execute("INSERT INTO history VALUES (?,?)", entry)
            conn.commit()
            motor = Motor(pump1_pin1, pump1_pin2)
            motor.forward(1)
            sleep(row["milliseconds"] / 1000)
            motor.stop()
            entry = (datetime.datetime.now().timestamp(), "Stopping pump {}".format(row["id"]))
            conn.cursor().execute("INSERT INTO history VALUES (?,?)", entry)
            conn.commit()

if __name__ == "__main__":
    conn = initialize()
    run_motors(conn)

"""Cloud Foundry test"""
from flask import Flask
import os
import sqlite3

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

@app.route('/')
def hello_world():
    con = sqlite3.connect("quakes")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select count(*) from quakes")
    rows = cur.fetchall()
    return render_template('home.html',rows=rows)


if __name__ == '__main__':
    app.run (port=port)

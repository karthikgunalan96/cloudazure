"""Cloud Foundry test"""
from flask import Flask,render_template,request
import os
import sqlite3
import time
import pyodbc
# from pymemcache.client import base

app = Flask(__name__)


port = int(os.getenv("PORT", 5000))

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/magnitude', methods=['GET','POST'])
def mag():
    mag = str(request.form['mag'])
    
    # client = base.Client(('localhost', 11211))
    # result = client.get(mag)
    # if result is None:
    start=time.time()
    print("retrieved from database")
    con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    
    cur = con.cursor()
    cur.execute("select * from all_month where mag > ?",(mag,))
    rows = cur.fetchall()
    print(rows)
    # client.set(mag,rows)
    end=time.time()
    print('Time Taken')
    print(end-start)
    return render_template('magnitude1.html',rows=rows)
    # else:
    #     print("retrieved from memcache")
        
    #     return render_template('magnitude2.html',rows=result.sqlite3.Row)



if __name__ == '__main__':
    app.run (port=port,debug=True)

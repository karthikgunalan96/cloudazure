"""Cloud Foundry test"""
from flask import Flask,render_template,request
import os
import sqlite3
import time
import redis
import pyodbc
import hashlib
from json import loads, dumps
# from pymemcache.client import base

app = Flask(__name__)



myHostname = "karthikgunalancache.redis.cache.windows.net"
myPassword = "E3eq1h2LCM0838QcfVlEVllZMy43kJw8qQFLan48jP4="



# result = r.ping()
# print("Ping returned : " + str(result))

# result = r.set("Message", "Hello!, The cache is working with Python!")
# print("SET Message returned : " + str(result))

# result = r.get("Message")
# print("GET Message returned : " + result.decode("utf-8"))

# result = r.client_list()
# print("CLIENT LIST returned : ") 
# for c in result:
# 	print("id : " + c['id'] + ", addr : " + c['addr'])
port = int(os.getenv("PORT", 5000))

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/magnitude', methods=['GET','POST'])
def mag():
    columns = ['time', 'latitude', 'longitude','mag']
    mag = str(request.form['mag'])
    r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
    result = r.get(mag) 
    
    # print(result)  
    if result is None:
        start=time.time()
        print("retrieved from database")
        con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
        cur = con.cursor()
        query="select * from all_month where mag > "+mag
        memhash = hashlib.sha256(query.encode()).hexdigest()
        cur.execute(query)
        rows= list(cur.fetchall())
        mem=[]
        memdata=[]
        
        for row in rows:
            memdict=dict()
            mem=[(0,row[0]),(1,row[1]),(2,row[2]),(3,row[4])]
            # print(mem)
            for j,val in mem:
                memdict[columns[j]]=val
            memdata.append(memdict)
        r.set(mag,dumps(memdata))
            # for i,val in enumerate(row):
                # if i==0 or i==1 or i==2 or i==4:
                    # mem.append(row[i])
                    # for j in range(0,3):
                    #     memdict[columns[j]]=val

                # print(mem)
            # mem=[]   
                       
                    
            
            # print(memdict)
                    # memdict[i]=val
            
            # mem.append(memdict)
            # print(mem)
        # r.set(mag,dump(mem))
        end=time.time()
        print('Time Taken')
        print(end-start)
        return render_template('magnitude1.html',rows=rows)
    else:
        result=loads(result.decode("utf-8"))
        resultdisplay=result
        
        print("retrieved from memcache",result)
        return render_template('magnitude2.html',rows=result)



if __name__ == '__main__':
    app.run (host='0.0.0.0',port=port,debug=True)

"""Cloud Foundry test"""
from flask import Flask,render_template,request
import os
import sqlite3
import time
import redis
import pyodbc
import hashlib
from json import loads, dumps
import random
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

@app.route('/createindex',methods=['GET','POST'])
def createindex():

    con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cur=con.cursor()
    start=time.time()
    cur.execute("CREATE TABLE assignment3.dbo.all_month2(\"time\" DATETIME,latitude FLOAT,longitude FLOAT,depth FLOAT,mag FLOAT,magType TEXT,nst INT,gap INT,dmin FLOAT,rms FLOAT,net TEXT,id TEXT,updated DATETIME,place TEXT,type TEXT,horontalError FLOAT,depthError FLOAT,magError FLOAT,magNst INT,status TEXT,locationSource TEXT,magSource TEXT)")
    cur.execute("CREATE INDEX all_month_mag__index ON assignment3.dbo.all_month (mag)")
    cur.execute("CREATE INDEX all_month_lat__index ON assignment3.dbo.all_month (latitude)")
    cur.execute("CREATE INDEX all_month_long__index ON assignment3.dbo.all_month (longitude)")
    end=time.time()
    con.commit()
    con.close()
    return render_template('createindex.html',time=(end-start)*1000)

@app.route('/randomqueries',methods=['GET','POST'])
def randomqueries():
    con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
    minmag = int(request.form['minmag'])
    maxmag = int(request.form['maxmag'])
    count = int(request.form['count'])
    a=count
    countwithincache=0
    countwithindb=0
    columns = ['time', 'latitude', 'longitude','mag']
    execution_of_time_in_db=[]
    execution_of_time_in_cache=[]

    val=float(minmag)
    interval=[]
    interval.append(minmag)
    
    while val<maxmag:
        val+=0.1
        interval.append(round(val,2))
    
    for i in range(0,len(interval)-1):
        cur = con.cursor()
        # index=round((random.uniform(0,len(interval)-2)))
        while count>0:
            
            index=round((random.uniform(0,len(interval)-2)))
            query="select time,latitude,longitude,mag from all_month where mag > "+str(interval[index])
            startmem=time.time()
            result = r.get(query)
            endmem=time.time()
            execution_of_time_in_cache.append(endmem-startmem)
            if result is None:
                print('in db')
                start=time.time()
                cur=con.cursor()
                cur.execute(query)
                rows=list(cur.fetchall())
                end=time.time()
                execution_of_time_in_db.append(end-start)
                mem=[]

                for row in rows:
                    memdict=dict()
                    for j,val in enumerate(row):
                        memdict[columns[j]]=val
                    mem.append(memdict)
                r.set(query,dumps(mem))
                
                countwithindb=countwithindb+1
            else:
                result=loads(result.decode("utf-8"))
                resultdisplay=result
                print('in cache')
                
                countwithincache=countwithincache+1
            count=count-1
                    
    probability_of_occurence_in_db=countwithindb/a
    probability_of_occurence_in_cache=countwithincache/a
    print("probability of query hitting db=",probability_of_occurence_in_db)
    print("probability of query hitting cache=",probability_of_occurence_in_cache)
        # return render_template('magnitude2.html',rows=result,time=endmem-startmem)

    
    return render_template('randomqueries.html',probdb=probability_of_occurence_in_db,probcache=probability_of_occurence_in_cache,timedb=execution_of_time_in_db,timecache=execution_of_time_in_cache)




@app.route('/magnitude', methods=['GET','POST'])
def mag():
    columns = ['time', 'latitude', 'longitude','mag']
    mag = str(request.form['mag'])

    r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
    startmem=time.time()
    query="select time,latitude,longitude,mag from all_month where mag > "+mag
    result = r.get(query) 
    endmem=time.time()
    # print(result)  
    if result is None:
        start=time.time()
        print("retrieved from database")
        con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
        cur = con.cursor()
        # query="select time,latitude,longitude,mag from all_month where mag > "+mag
        # memhash = hashlib.sha256(query.encode()).hexdigest()
        cur.execute(query)
        rows= list(cur.fetchall())
        mem=[]
        
        
        for row in rows:
            memdict=dict()

            # print(mem)
            for j,val in enumerate(row):
                memdict[columns[j]]=val
            mem.append(memdict)
        r.set(query,dumps(mem))
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
        return render_template('magnitude1.html',rows=rows,time=end-start)
    else:
        result=loads(result.decode("utf-8"))
        resultdisplay=result
        print('time taken')
        print(endmem-startmem)
        
        
        return render_template('magnitude2.html',rows=result,time=endmem-startmem)



if __name__ == '__main__':
    app.run (port=port,debug=True)

# """Cloud Foundry test"""
# from flask import Flask,render_template,request
# import os
# import sqlite3
# import time
# import redis
# import pyodbc
# import hashlib
# from json import loads, dumps
# import random
# # from pymemcache.client import base

# app = Flask(__name__)



# myHostname = "karthikgunalancache.redis.cache.windows.net"
# myPassword = "E3eq1h2LCM0838QcfVlEVllZMy43kJw8qQFLan48jP4="



# # result = r.ping()
# # print("Ping returned : " + str(result))

# # result = r.set("Message", "Hello!, The cache is working with Python!")
# # print("SET Message returned : " + str(result))

# # result = r.get("Message")
# # print("GET Message returned : " + result.decode("utf-8"))

# # result = r.client_list()
# # print("CLIENT LIST returned : ") 
# # for c in result:
# # 	print("id : " + c['id'] + ", addr : " + c['addr'])
# port = int(os.getenv("PORT", 5000))

# @app.route('/')
# def home():
#     dataset=[1,2,3,4,5]
#     return render_template('home.html',row=dataset)

# @app.route('/createindex',methods=['GET','POST'])
# def createindex():

#     con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#     cur=con.cursor()
#     cur.execute("DROP TABLE assignment3.dbo.all_month2")
#     cur.execute("DROP INDEX all_month_mag__index on assignment3.dbo.all_month")
#     cur.execute("DROP INDEX all_month_lat__index on assignment3.dbo.all_month")
#     cur.execute("DROP INDEX all_month_long__index on assignment3.dbo.all_month")

#     start=time.time()
#     cur.execute("CREATE TABLE assignment3.dbo.all_month2(\"time\" DATETIME,latitude FLOAT,longitude FLOAT,depth FLOAT,mag FLOAT,magType TEXT,nst INT,gap INT,dmin FLOAT,rms FLOAT,net TEXT,id TEXT,updated DATETIME,place TEXT,type TEXT,horontalError FLOAT,depthError FLOAT,magError FLOAT,magNst INT,status TEXT,locationSource TEXT,magSource TEXT)")
#     cur.execute("CREATE INDEX all_month_mag__index ON assignment3.dbo.all_month (mag)")
#     cur.execute("CREATE INDEX all_month_lat__index ON assignment3.dbo.all_month (latitude)")
#     cur.execute("CREATE INDEX all_month_long__index ON assignment3.dbo.all_month (longitude)")
#     end=time.time()
#     con.commit()
#     con.close()
#     return render_template('createindex.html',time=(end-start)*1000)


# @app.route('/flush',methods=['GET','POST'])
# def flush():
#     r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     for key in r.scan_iter():
#         r.delete(key)

#     return render_template('flush.html')

# @app.route('/randomqueries',methods=['GET','POST'])
# def randomqueries():
#     con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#     r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     minlat = int(request.form['minlat'])
#     maxlat = int(request.form['maxlat'])
#     count = int(request.form['count'])
#     call=request.form['call']
#     a=count
#     countwithincache=0
#     countwithindb=0
#     columns = ['time','place', 'mag']
#     execution_of_time_in_db=[]
#     execution_of_time_in_cache=[]

#     val=float(minlat)
#     interval=[]
#     interval.append(minlat)
    
#     while val<maxlat:
#         val+=0.1
#         interval.append(round(val,2))
    
#     for i in range(0,len(interval)-1):
#         cur = con.cursor()
#         index=round((random.uniform(0,len(interval)-2)))
#         while count>0:
            
#             index=round((random.uniform(0,len(interval)-2)))
#             print(interval[index],interval[index+1])
#             query="select \"time\",place,mag from quake where latitude >= "+str(interval[index])+" and latitude <= "+ str(interval[index+1])
#             start=time.time()
#             result = r.get(query)
#             resultdata=[]
            
#             if call =='db':
#                 print('in db')
                
#                 cur=con.cursor()
#                 cur.execute(query)
#                 result=list(cur.fetchall())
#                 # resultdata.append(rows)
                
#                 end=time.time()
#                 execution_of_time_in_db.append(end-start)
#                 mem=[]

#                 for row in result:
#                     memdict=dict()
#                     for j,val in enumerate(row):
#                         memdict[columns[j]]=val
#                     mem.append(memdict)
#                 r.set(query,dumps(mem))
                
#                 countwithindb=countwithindb+1
#                 return render_template('magnitude1.html',rows=result)
#             else:
#                 result=loads(result.decode("utf-8"))
                
#                 end=time.time()
#                 execution_of_time_in_cache.append(end-start)
#                 resultdata.append(result)
#                 print('in cache')
#                 return render_template('magnitude2.html',rows=result)
                
                
#                 countwithincache=countwithincache+1
#             count=count-1
#     print(result)
#     probability_of_occurence_in_db=countwithindb/a
#     probability_of_occurence_in_cache=countwithincache/a
#     # print("probability of query hitting db=",probability_of_occurence_in_db)
#     # print("probability of query hitting cache=",probability_of_occurence_in_cache)
#         # return render_template('magnitude2.html',rows=result,time=endmem-startmem)
#     sum_dbtime=sum(execution_of_time_in_db)
#     sum_cachetime=sum(execution_of_time_in_cache)
#     con.close()
#     print(query)
#     return render_template('randomqueries.html',probdb=probability_of_occurence_in_db,probcache=probability_of_occurence_in_cache,timedb=sum_dbtime,timecache=sum_cachetime,rows=result)



# @app.route('/latqueries',methods=['GET','POST'])
# def latqueries():
#     con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#     r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     minlat = int(request.form['minlat'])
#     maxlat = int(request.form['maxlat'])
#     # count = int(request.form['count'])
#     # a=count
#     # countwithincache=0
#     # countwithindb=0
#     columns = ['time', 'place','mag']
#     execution_of_time_in_db=[]
#     execution_of_time_in_cache=[]

#     # val=float(minmag)
#     # interval=[]
#     # interval.append(minmag)
    
#     # while val<maxmag:
#     #     val+=0.1
#     #     interval.append(round(val,2))
    
#     # for i in range(0,len(interval)-1):
#     #     cur = con.cursor()
#     #     # index=round((random.uniform(0,len(interval)-2)))
#     #     while count>0:
            
#     # index=round((random.uniform(0,len(interval)-2)))
#     query="select \"time\",place,mag from quake where latitude > "+str(minlat)+" and latitude<"+str(maxlat)
#     start=time.time()
#     result = r.get(query)
            
            
#     if result is None:
#         print('in db')
                
#         cur=con.cursor()
#         cur.execute(query)
#         rows=list(cur.fetchall())
#         print(rows)
#         result=rows
#         end=time.time()
#         execution_of_time_in_db.append(end-start)
#         mem=[]

#         for row in rows:
#             memdict=dict()
#             for j,val in enumerate(row):
#                 memdict[columns[j]]=val
#             mem.append(memdict)
#         r.set(query,dumps(mem))
                
#         # countwithindb=countwithindb+1
#     else:
#         print(result)
#         result=loads(result.decode("utf-8"))
#         end=time.time()
#         execution_of_time_in_cache.append(end-start)
#         resultdisplay=result
#         print('in cache')
                
#         # countwithincache=countwithincache+1
#         # count=count-1
                    
#     # probability_of_occurence_in_db=countwithindb/a
#     # probability_of_occurence_in_cache=countwithincache/a
#     # print("probability of query hitting db=",probability_of_occurence_in_db)
#     # print("probability of query hitting cache=",probability_of_occurence_in_cache)
#         # return render_template('magnitude2.html',rows=result,time=endmem-startmem)
#     sum_dbtime=sum(execution_of_time_in_db)
#     sum_cachetime=sum(execution_of_time_in_cache)
#     con.close()
#     return render_template('randomqueries.html',rows=result,timedb=sum_dbtime,timecache=sum_cachetime)




# @app.route('/magnitude', methods=['GET','POST'])
# def mag():
#     columns = ['time', 'latitude', 'longitude','mag']
#     mag = str(request.form['mag'])

#     r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     startmem=time.time()
#     query="select time,latitude,longitude,mag from all_month where mag > "+mag
#     result = r.get(query) 
#     endmem=time.time()
#     # print(result)  
#     if result is None:
#         start=time.time()
#         print("retrieved from database")
#         con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#         cur = con.cursor()
#         # query="select time,latitude,longitude,mag from all_month where mag > "+mag
#         # memhash = hashlib.sha256(query.encode()).hexdigest()
#         cur.execute(query)
#         rows= list(cur.fetchall())
#         mem=[]
        
        
#         for row in rows:
#             memdict=dict()

#             # print(mem)
#             for j,val in enumerate(row):
#                 memdict[columns[j]]=val
#             mem.append(memdict)
#         r.set(query,dumps(mem))
#             # for i,val in enumerate(row):
#                 # if i==0 or i==1 or i==2 or i==4:
#                     # mem.append(row[i])
#                     # for j in range(0,3):
#                     #     memdict[columns[j]]=val

#                 # print(mem)
#             # mem=[]   
                       
                    
            
#             # print(memdict)
#                     # memdict[i]=val
            
#             # mem.append(memdict)
#             # print(mem)
#         # r.set(mag,dump(mem))
#         end=time.time()
#         print('Time Taken')
#         print(end-start)
#         return render_template('magnitude1.html',rows=rows,time=end-start)
#     else:
#         result=loads(result.decode("utf-8"))
#         resultdisplay=result
#         print('time taken')
#         print(endmem-startmem)
        
        
#         return render_template('magnitude2.html',rows=result,time=endmem-startmem)



# if __name__ == '__main__':
#     app.run (port=port,debug=True)





"""Cloud Foundry test"""
from flask import Flask,render_template
import os
import pyodbc


app = Flask(__name__)

port = int(os.getenv("PORT", 5000))
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/chart',methods=['GET','POST'])
def chart():
  
   
    con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    
    a = str(request.form['interval'])
    start=40
    end=80
    val=start
    age_interval=[start]
    while val<end:
        val+=10
        age_interval.append(val)
    # mem=[]
    per=[]
    # query1="Select statename from voting where totalpop>5000 and totalpop<10000"
    # query2="Select statename from voting where totalpop>10000 and totalpop<50000"
    # cur=con.cursor()
    # cur.execute(query1)
    # result1=list(cur.fetchall())
    # cur.execute(query2)
    # result2=list(cur.fetchall())
    # print(result1)
    # print(result2)
    # return render_template('base.html',a=result1,b=result2)
    query="select totalpop,voted from voting"
    cur=con.cursor()
    cur.execute(query)
    mem=[]
    result=list(cur.fetchall())
    for row in result:
        per.append(row[1]/row[0]*100)
    print(age_interval)
    # for i in range(0,len(per)-1):
    #     print(per[i])
    #     for j in range(0,len(age_interval)-1):

    #         if per[i]>age_interval[j] and per[i]<age_interval[i+1]:
    #             print(per[i])
    
    for i in range(0,len(age_interval)-1):
        age_group=str(age_interval[i])+"-"+str(age_interval[i+1])

        for row in result: 
            memdict=dict()
            for j in per:
                # print(j)
                # print(age_group)
                if j>age_interval[i] and j<age_interval[i+1]:
                    print(j)
                    memdict["age_group"]=age_group  
                    memdict["per"]=j
                mem.append(memdict)
            # print(mem)
    
        
        
        # for j,val in enumerate(row):
    return render_template('chart.html',a=mem,chart="pie")




# @app.route('/')
# def hello_world():

   
#     con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#     query1="Select statename from voting where totalpop>5000 and totalpop<10000"
#     query2="Select statename from voting where totalpop>10000 and totalpop<50000"
#     cur=con.cursor()
#     cur.execute(query1)
#     result1=list(cur.fetchall())
#     cur.execute(query2)
#     result2=list(cur.fetchall())
#     print(result1)
#     print(result2)
#     return render_template('base.html',a=result1,b=result2)
    # con = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:karthikgunalan.database.windows.net,1433;Database=assignment3;Uid=karthikgunalan@karthikgunalan;Pwd={Polo5590};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    # query="Select mag,latitude from quake where mag >= 6"
    # columns=['mag','latitude']
    # dic=dict()
    # cur=con.cursor()
    # mem=[]
    # cur.execute(query)
    # result=list(cur.fetchall())
    # for row in result:
    #     memdict=dict()
    #     for j,val in enumerate(row):
    #         memdict[columns[j]]=val
    #     mem.append(memdict)
    # # print(mem)
    # a=[1,2,3,4,5]
    # # print(a)
    # return render_template('chart.html',a=mem,chart="bar")

# @app.route('/streaming.csv')
# def streaming():
#     result=[]
#     with open('streaming.csv') as csv_file:
        
#         csv_reader = csv.reader(csv_file, delimiter=',')
        
#         line_count = 0
#         for row in csv_reader:
#             result.append(row)
#             if line_count == 0:
#                 print(f'Column names are {", ".join(row)}')
#                 line_count += 1
#             else:
#                 print(row)
#                 line_count += 1
#             print(f'Processed {line_count} lines.')
        
#     return tuple(result)



if __name__ == '__main__':
    app.run(port=port,debug=True)

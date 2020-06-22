from flask import Flask,request,render_template,g,send_from_directory
import pandas as pd
import sqlite3


app=Flask(__name__,static_url_path='',static_folder='/static',template_folder="templates")

DATABASE=r"C:\Users\Owner\Desktop\Final Project\Lyrica_Machine_Learning_FP\static\data\sqlite\songsdb.sqlite3"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

	
def Get_DB_Contents(cur):
    table_name='Songs'
    columns=[x[1] for x in cur.execute("pragma table_info(Songs)").fetchall()]

    data=cur.execute("select * from Songs;").fetchall()
    outdata={}
    for i in range(len(columns)):
        outdata[columns[i]]=[x[i] for x in data]
    return outdata

    	
def SAMPLE_Get_DB_Contents(cur):
    table_name='Songs'
    columns=[x[1] for x in cur.execute("pragma table_info(Songs)").fetchall()]

    data=cur.execute("select * from Songs limit 150;").fetchall()
    outdata={}
    for i in range(len(columns)):
        outdata[columns[i]]=[x[i] for x in data]
    return outdata

def Search_DB_By_Column_Value(cur,column_to_search,filter):
    get_songs_table = lambda cur: cur.execute("select name from sqlite_master where type='table';").fetchall()[0][0]
    table_name=get_songs_table(cur)
    columns=[x[1] for x in cur.execute("pragma table_info(Songs)").fetchall()]
    data=cur.execute("select * from Songs where LOWER(TEXT({0})) LIKE LOWER(TEXT({1}));".format(column_to_search,filter)).fetchall()
    outdata={}
    for i in range(len(columns)):
        outdata[columns[i]]=[x[i] for x in data]
    return outdata


def Search_DB_By_Any_Value(cur,search_term):
    get_songs_table = lambda cur: cur.execute("select name from sqlite_master where type='table';").fetchall()[0][0]
    table_name=get_songs_table(cur)
    columns=[x[1] for x in cur.execute("pragma table_info(Songs)").fetchall()]
    tmp_data=cur.execute("select * from Songs;").fetchall()
    data=[x for x in tmp_data if str(search_term).lower() in str(x).lower()]
    outdata={}
    for i in range(len(columns)):
        outdata[columns[i]]=[x[i] for x in data]
    return outdata

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.route("/",methods=['POST','GET'])
def main():
    cur=get_db().cursor()
    if request.method=="GET":
        Output=None
        all_records=Get_DB_Contents(cur)
        if all_records is None:
            all_records=[]
        result_len=len(all_records)
        print("len of reulst is {}".format(result_len))
        return render_template("index2.html",**locals())



@app.route("/static/images/<path:filename>")
def getimg(filename):
    return  send_from_directory(r"C:\Users\Owner\Desktop\Final Project\Lyrica_Machine_Learning_FP\static\images",filename)



@app.route("/static/js/<path:filename>")
def getjs(filename):
    return  send_from_directory(r"C:\Users\Owner\Desktop\Final Project\Lyrica_Machine_Learning_FP\static\js",filename)

@app.route("/static/css/<path:filename>")
def getcss(filename):
    return  send_from_directory(r"C:\Users\Owner\Desktop\Final Project\Lyrica_Machine_Learning_FP\static\css",filename)

app.run()
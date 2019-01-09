# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 23:56:56 2019

@author: agraw
"""

from flask import Flask,render_template,request,send_file
import pandas
from werkzeug import secure_filename
from geopy.geocoders import ArcGIS
nom=ArcGIS()


app=Flask(__name__)

@app.route("/")
def hello():

        return render_template("index.html")
    
@app.route("/index",methods=['POST'])
def index():
    global f
    
    if request.method=='POST':
        
        f=request.files["file"]
        f.save(secure_filename("uploaded"+f.filename))
        try:
                df=pandas.read_csv("uploaded"+f.filename)
                
                if "address" in df.columns :
                    
                   #df["Address"]=df["Address"]+","+df["City"]+","+df["State"]+","+df["Country"]
                   df["Address"]=df["address"]
                   df=df.drop(columns="address",axis=1)
                if "Address" in df.columns:
                    df["Cordinate"]=df["Address"].apply(nom.geocode)
                    
                    df["Latitude"]=df["Cordinate"].apply(lambda x:x.latitude if x!= None else None)
                    df["Longitude"]=df["Cordinate"].apply(lambda x:x.longitude if x!= None else None)
                    df=df.drop(columns=["Cordinate"],axis=1)
                    df.to_csv("uploaded"+f.filename,index=None)
                    
                   
                    #return render_template("index.html",tables=[df.to_html(classes='data',header="true")],btn="download.html")
                    return render_template("index.html",text=df.to_html(),btn="download.html")
        except Exception as e:
                    return render_template("index.html",text=str(e))
            
        return render_template("index.html",text="Please make sure you have an Address columnn in your CSV file")
    
@app.route("/download")
def download():
    return send_file("uploaded"+f.filename,attachment_filename="yourfile.csv",as_attachment=True)
       
if __name__=='__main__':
    app.run(debug=True)
    
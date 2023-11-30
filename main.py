#Tesla Daily Stocks Prices [2010-2022]
#https://www.kaggle.com/datasets/timmofeyy/-tesla-daily-stocks-prices?resource=download
# project: p4
import pandas as pd
from flask import Flask, request, jsonify, render_template, Response
import re
import time, flask
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import StringIO, BytesIO


app = Flask(__name__)


home_counter=0
old='<a href = "donate.html">Donate</a>'
new1='<a href = "donate.html?from=B"  style="color: orange">Donate</a>'
new2='<a href = "donate.html?from=A"  style="color: pink">Donate</a>'


@app.route('/')
def home():
    global home_counter
    home_counter +=1
    with open("index.html") as f:
        html = f.read()
    if home_counter<=10:
        if home_counter%2==1:
            html=html.replace(old, new1)
        else:
            html=html.replace( old, new2)
    else:
        if a_counter > b_counter:
            html = html.replace( old, new2)
        else:
            html = html.replace( old, new1)
    return html


maincsv=pd.read_csv("main.csv")
@app.route('/browse.html')
def browse():
    header="<h1>Browse</h1>"
    df= str(maincsv.to_html())
    return df + header


dic={}
@app.route('/browse.json')
def browse_json():
    df=pd.read_csv("main.csv")
    df_dictionary=df.to_dict(orient="index")
    client=flask.request.remote_addr
    if client in dic:
        if time.time()-dic[client]>=60:
            dic[client]=time.time()
            return jsonify(df_dictionary)
        else:
            #html = "too many requests, come back later"
            html = "TOO MANY REQUESTS"
            return flask.Response(html, status=429,headers={"Retry-After":60})
    else:
        dic[client]=time.time()
        return jsonify(df_dictionary)



email_counter=0
def num_subscribed():
    global email_counter
    email_counter +=1
    return email_counter
@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"\w+@\w+\.\w+", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        return jsonify(f"thanks, you're subscriber number {num_subscribed()}!")
    return jsonify(f"Please enter valid email!") # 3


a_counter=0
b_counter=0

@app.route('/donate.html')
def donate():
    global a_counter, b_counter
    header= "<h1>donate</h1>"
    with open("donate.html") as f:
        html = f.read()
    if request.args["from"] == "A":
        a_counter += 1
    else:
        b_counter += 1
    return html



xpoints = maincsv['High']
ypoints1 = maincsv['Close']
ypoints1_5=maincsv['Volume']
ypoints2 = maincsv['Low']

@app.route("/highlines.svg")
def svg1():
    
    fig, ax = plt.subplots(figsize=(3,2))
    
    plt.tight_layout()
    if request.args['yaxis'] == "volume":
        plt.scatter(xpoints, ypoints1_5)
        ax.set_xlabel("High stock price")
        ax.set_ylabel("Volume")
      
    if request.args['yaxis'] == "closing":
        plt.scatter(xpoints, ypoints1)
        ax.set_xlabel("High stock price")
        ax.set_ylabel("Closing stock price")
        
    f = StringIO() # fake file (has a .write method)
    
    
    fig.savefig(f, format="svg", bbox_inches="tight")
    
    
    plt.close(fig) # closes the most recent fig
    
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(png, headers=hdr)




@app.route("/lowdots.svg")
def svg2():
    fig, ax = plt.subplots(figsize=(3,2))
    
    
    plt.plot(xpoints, ypoints2,'o')
    ax.set_xlabel("high stock price")
    ax.set_ylabel("low stock price")
    
    f = StringIO() # fake file (has a .write method)
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close(fig) # closes the most recent fig
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(png, headers=hdr)









if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
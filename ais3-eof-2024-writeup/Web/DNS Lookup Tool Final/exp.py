#!/usr/bin/env python3

from flask import Flask,request,redirect,Response


app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def root():
    print(request.stream.read().decode())
    return "com"

@app.route('/<path:data>',methods=['GET'])
def run(data):
    print(data)
    return "com"

if __name__ == "__main__":
    app.run(host="::", port=80)

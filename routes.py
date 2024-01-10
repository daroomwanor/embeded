import os
import boto3
import requests
import subprocess
from os import environ
from flask import Flask
from flask import render_template, request, redirect, session,send_file
import json
import requests
from datetime import datetime
import calendar
from werkzeug.utils import secure_filename
import uuid
from youtubesearchpython import Search
import xmltodict
import time
from wifi import Cell, Scheme


UPLOAD_FOLDER = '/home/pi/piBoard.io/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
_Node_ = "Auric"
app=Flask(__name__)
app.secret_key = "abc"
__Configs__ = None


@app.route("/", methods=['GET', 'POST'])
def index():
	youtube = []
	wifi = None
	try:
		resp = requests.get('http://18.236.135.168:5555/device/c7f1d67e-c65f-4a81-b63f-fd694307a3c6')
	except:
		pass
	finally:
		if wifi != None:
			print(resp.text)
			info = Search('NBCNews live', limit=1)
			res = info.result()
			youtube.append({'src':"https://youtube.com/embed/"+res["result"][0]['id']+"?autoplay=1&mute=1&enablejsapi=1&cc_load_policy=1&vq=480", "type":"iframe"})
			return render_template('index.html', imgs=json.loads(resp.text), youtube=youtube)
		else:
			return render_template('wifiConnect.html')

@app.route("/mobileDisplayAd", methods=['GET', 'POST'])
def mobileDisplayAd():
	res = requests.get("https://arielapps.com/mobileDisplayAd")
	return res.text

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)

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
app.notifications = []
app.refresh = "false"
app.rebootRefresh = "true"
app.myPlaylist = None
def getConfigs():
	with open("/configs/configs.json", "r") as filename:
		return json.loads(filename.read())
		
@app.route("/", methods=['GET', 'POST'])
def index():
	youtube = []
	wifi = None
	activeWifi = None
	std = subprocess.run(["nmcli -t -f Name c show --active"],shell=True, capture_output=True) 
	activeWifi = str(std.stdout, 'UTF-8')
	resp = None
	iframes = []
	playlist = []
	playlistSrc = None
	banners = []
	config = getConfigs()
	app.refresh = "false"
	try:
		if activeWifi != "":
			wifi = "Connected"
			resp = requests.get('https://arielapps.com/signageContent/'+config["Device"])
			data = json.loads(resp.text)
			for x in data:
				if x[2] == "youtube":
					playlist.append(x[0])
				elif x[2] == "notifications":
					banners = x 
				else:
					iframes.append(x)
			src = ",".join(playlist)
			playlistSrc = "https://youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&loop=1&playlist="+src		
	except Exception as e:
		print(e)
		resp = "Error"
		pass
	finally:
		if wifi != None:
			if config['channel'] == "NBC":
				info = Search('NBCNews live', limit=1)
				res = info.result()
				youtube.append({'src':"https://youtube.com/embed/"+res["result"][0]['id']+"?autoplay=1&mute=1&enablejsapi=1&cc_load_policy=1&vq=480", "type":"iframe"})
			else:
				youtube.append({'src':"https://youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&loop=1&playlist="+config[config['channel']], "type":"iframe"})
			qrCode = config["Device"]
			backgroundImg = (banners[0]).replace("default_", "")
			notices = json.loads(banners[3])
			banner = [qrCode, backgroundImg, notices]
			app.notifications=notices
			return render_template('index.html', iframes=iframes, \
			youtube=youtube, playlistSrc=playlistSrc,banner=banner)
		else:
			wifiList = getWifiList()
			if len(wifiList) == 0:
				wifiList=getWifiList()
			return render_template('wifiConnect.html',data=wifiList)

@app.route("/check", methods=['GET', 'POST'])
def check():
	return app.refresh

@app.route("/checkReboot", methods=['GET', 'POST'])
def checkReboot():
	status = app.rebootRefresh
	if status == "true":
		status = "true"
		app.rebootRefresh = "false"
	else:
		status = "false"
	return status
	
@app.route("/banner/<key>", methods=['GET', 'POST'])
def banner(key):  
	return render_template("notify.html", data=app.notifications, index=index)

def getWifiList():
	wifiList = list(Cell.all('wlan0'))
	time.sleep(10)
	data = []
	for index, x in enumerate(wifiList):
		if x.ssid != "" or x.ssid != '':
			data.append(x.ssid)
	print(data)		
	return data

@app.route("/connectToWIFI", methods=['GET', 'POST'])
def connectToWIFI():
	ssid = request.args.get('ssid')
	password = request.args.get('password')
	cmd = "nmcli radio wifi on;nmcli dev wifi connect "+ssid+" password "+password
	std = subprocess.run([cmd], shell=True, capture_output=True)
	print(std.stdout)
	resp = (str(std.stdout, 'UTF-8')).split(" ")
	print(resp)
	if resp[2] == "successfully":
		print("Connected")
		subprocess.run(["sudo reboot"], shell=True)
	else:
		return "Failed"

@app.route("/configure/<key>/<value>", methods=['GET', 'POST'])
def configure(key,value):
	configs = getConfigs()
	configs[key] = value
	with open("/configs/configs.json", "w") as filename:
		filename.write(json.dumps(configs))
	app.refresh = "true"
	return app.refresh

@app.route("/channel/<key>/<value>", methods=['GET', 'POST'])
def channel(key,value):
	configs = getConfigs() 
	configs[key] = value
	configs['channel'] = key
	with open("/configs/configs.json", "w") as filename:
		filename.write(json.dumps(configs))
	app.refresh = "true"
	return app.refresh

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000)

import websocket
import time
import json
import requests
import subprocess
import _thread
import os
import requests
tunnels = []
# Define WebSocket callback functions


def getConfigs():
	with open("/configs/configs.json", "r") as filename:
		return json.loads(filename.read())

def ws_message(ws, message):
	try:
		config = getConfigs()
		data = json.loads(message)
		if data["action"] == "Bash":
			print(data["CMD"])
			stdout = os.popen(data['CMD']).read()
	except e:
		print(e)
		print("Failed")
						
def ws_open(ws):
	config = getConfigs()
	data = {
	"device":config['Device'], "cmd": "","action":"open"}
	ws.send(data)

def ws_thread(*args):
	config = getConfigs()
	ws = websocket.WebSocketApp("wss://arielapps.com:8777/"+config['Device'], on_open = ws_open, on_message = ws_message, on_close=ws_close)
	print("New Tunnel")
	print(ws)
	tunnels.append(ws)
	ws.run_forever()

def ws_close(ws):
	print("Closing Connection")
	ws.close()

_thread.start_new_thread(ws_thread, ())
subprocess.run("sudo python3 /embeded/routes.py&", shell=True)
count=0
# Continue other (non WebSocket) tasks in the main thread
while True:
	try:
		if count == 60 or count == 0:
			for x in tunnels:
				print(x)
				x.close()
			tunnels = []
			_thread.start_new_thread(ws_thread, ())
			if count == 0:
				count = count +10
			else:
				count = 0
		else:
			count = count+10
	except requests.exceptions.ConnectionError as e:
		print("Something Failed") 
		print(e) 
	time.sleep(10)
	print("Main thread: %d time connected" % time.time())
 


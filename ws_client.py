import websocket
import time
import json
import requests
import subprocess
import _thread
import os
import requests
data = json.dumps({'name':'pi1', 'time':time.time()})
_Socket_ = None
tunnels = []
# Define WebSocket callback functions

def ws_message(ws, message):
	try:
		data = json.loads(message)
		if data["action"] == "Bash":
			print(data["CMD"])
			stdout = os.popen(data['CMD']).read()
			data = {"device":"/pi1", "action":"Response", "logs":stdout}
			print(data)
			resp = requests.post(url="http://arielapps.com:5555/updateLogs",data=json.dumps(data))
			print(resp.text)
			
	except e:
		print(e)
		print("Faild")
						
def ws_open(ws):
	data = {
	"device":"/pi1", "cmd": "ls -l","action":"open"}
	ws.send(data)

def ws_thread(*args):
	ws = websocket.WebSocketApp("ws://0.0.0.0:8777/pi1", on_open = ws_open, on_message = ws_message, on_close=ws_close)
	print("New Tunnel")
	print(ws)
	tunnels.append(ws)
	ws.run_forever()

def ws_close(ws):
	print("Closing Connection")
	ws.close()

_thread.start_new_thread(ws_thread, ())
count=0
# Continue other (non WebSocket) tasks in the main thread
while True:
	try:
		if count == 20 or count == 0:
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
 


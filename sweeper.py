import os
import time
import json
import threading
import socket
import subprocess
from queue import Queue

from pw_models import *
from netaddr import *

ip_queue = Queue()

def ping_worker(i, q):
	while not q.empty():
		ip = q.get()
		record = {}
		record['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
		response = subprocess.Popen(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.DEVNULL) #, stderr=subprocess.STDOUT)
		response.wait()
		if response.returncode == 0:
			record['ip_address'] = str(ip)
			try:
				record['hostname'] = str(socket.gethostbyaddr(str(ip))[0])
			except:
				record['hostname'] = "Unknown"
			found_record, created = Sweep.create_or_get(**record)
			if not created:
				found_record.timestamp = record.get('timestamp')
			found_record.save()
		q.task_done()

def fill_queue(q, network=None):
	if network:
		ips = IPSet([network])
		for ip in ips:
			q.put(ip)
	else:
		for record in Sweep.select():
			q.put(record.ip_address)

if __name__ == '__main__':
	fill_queue(ip_queue, network='192.168.1.0/24')
	tasks = []
	for i in range(10):
		worker = threading.Thread(target=ping_worker, args=(i, ip_queue,))
		tasks.append(worker)
		worker.start()
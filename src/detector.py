import re
import time
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta

failed_attempts = defaultdict(int)
blocked_ips = {}
whitelist = ["192.168.64.1"]
duration = timedelta(hours = 24)
with open("/var/log/auth.log", "r") as file:
	file.seek(0, 2)
	while True:
		line = file.readline()
		if line:
			if "Failed password" in line:
				match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
				if match:
					ip = match.group(1)
					if ip in whitelist:
                                        	continue
					failed_attempts[ip] += 1
					if failed_attempts[ip] >= 5:
						print(f"ALERT: {ip} has {failed_attempts[ip]} failed attempts.")
						now = datetime.now()
						subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "22", "-j", "DROP"])
						blocked_ips[ip] = now
						with open("blocked_ips.log", "a") as blockedlog:
							blockedlog.write(f"{ip} has been blocked as of {now}\n")
		else:
			for key in list(blocked_ips):
				if datetime.now() - blocked_ips[key] > duration:
					subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", key, "-p", "tcp", "--dport", "22", "-j", "DROP"])
					del blocked_ips[key]
					del failed_attempts[key]
			time.sleep(1)


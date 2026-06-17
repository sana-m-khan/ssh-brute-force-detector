import re
import time
import subprocess
from collections import defaultdict

failed_attempts = defaultdict(int)
whitelist = ["192.168.64.1"]
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
						subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "22", "-j", "DROP"])
		else:
			time.sleep(1)

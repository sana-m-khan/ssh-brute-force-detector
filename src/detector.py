import re
import time
from collections import defaultdict

failed_attempts = defaultdict(int)
with open("/var/log/auth.log", "r") as file:
	file.seek(0, 2)
	while True:
		line = file.readline()
		if line:
			if "Failed password" in line:
				match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
				if match:
					ip = match.group(1)
					failed_attempts[ip] += 1
					if failed_attempts[ip] >= 5:
						print(f"ALERT: {ip} has {failed_attempts[ip]} failed attempts.")
		else:
			time.sleep(1)

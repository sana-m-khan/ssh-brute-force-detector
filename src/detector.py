import re

failed_attempts = {}
with open("/var/log/auth.log", "r") as file:
	for line in file:
		if "Failed password" in line:
			match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
			if match:
				ip = match.group(1)
				if ip in failed_attempts:
					failed_attempts[ip] += 1
				else:
					failed_attempts[ip] = 1
				if failed_attempts[ip] >= 5:
					print(f"ALERT: {ip} has {failed_attempts[ip]} failed attempts.")

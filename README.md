# ssh-brute-force-detector

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Platform](https://img.shields.io/badge/Platform-Linux-orange) ![License](https://img.shields.io/badge/License-MIT-green)

A real-time intrusion detection tool that monitors SSH authentication logs, identifies brute force attack patterns, and automatically blocks offending IPs using Linux firewall rules.

---

## Security Note

If you need this tool, it means your SSH server has password authentication enabled. The more permanent fix is to switch to key-based authentication and disable password auth entirely — at that point brute force attacks become pointless since there's no password to guess. This tool is useful as an immediate layer of defense, but it is not a substitute for proper SSH hardening.

---

## Table of Contents

- [Overview](#overview)
- [Demo](#demo)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)

---

## Overview

SSH brute force attacks are one of the most common attack vectors against Linux servers. Attackers use automated tools to try thousands of username/password combinations against port 22. This tool monitors `/var/log/auth.log` in real time, tracks failed login attempts per IP, and fires an `iptables` rule to block the attacker the moment they cross a configurable threshold.

---

## Demo

**Attack detected and alert fired:**

<img width="1355" height="896" alt="image" src="https://github.com/user-attachments/assets/1e33573d-083a-4bbd-b856-4f5ccfec1aec" />


**Blocked IPs logged with timestamps:**

<img width="1386" height="868" alt="image" src="https://github.com/user-attachments/assets/68d79c81-9fa9-4602-80bd-03da2c6b4dab" />

---

## How It Works

1. Tracks `/var/log/auth.log` continuously using `readline()` in a loop
2. Uses regex to extract source IPs from `Failed password` entries
3. Tracks failure counts per IP using a `defaultdict`
4. When an IP exceeds the threshold, fires an `iptables` DROP rule targeting port 22 specifically — blocking only the SSH attack vector rather than all traffic from that IP
5. Logs blocked IPs with timestamps to `blocked_ips.log`
6. Auto-unblocks IPs after 24 hours to prevent permanent blocking of reassigned addresses
7. Whitelisted IPs are never blocked regardless of failure count

---

## Installation

### Requirements

- Ubuntu/Debian Linux
- Python 3
- `iptables`

### Clone the repo

```bash
git clone https://github.com/sana-m-khan/ssh-brute-force-detector
cd ssh-brute-force-detector
```

---

## Usage

```bash
sudo python3 src/detector.py
```

Must be run with `sudo` to read auth logs and modify firewall rules.

---

## Configuration

Edit these variables at the top of `src/detector.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `THRESHOLD` | `5` | Failed attempts before blocking |
| `duration` | `timedelta(hours=24)` | Auto-unblock window |
| `whitelist` | `["192.168.64.1"]` | IPs that will never be blocked |

---

## Project Structure

ssh-brute-force-detector/

├── src/

│   └── detector.py

├── blocked_ips.log

└── README.md

---

Built and tested on Ubuntu 26.04 running in a UTM VM on Apple Silicon. Attacks simulated from host machine via repeated failed SSH attempts.

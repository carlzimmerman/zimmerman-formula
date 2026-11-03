#!/bin/bash
cd "$(dirname "$0")"; nice -n 19 python3 wa1_keys.py LAW UX3 P3 P7 MX1 BK2 > keys_all.log 2>&1

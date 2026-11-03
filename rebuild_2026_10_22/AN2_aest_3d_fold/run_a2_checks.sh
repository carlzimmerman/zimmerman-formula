#!/bin/bash
# AN2 A2: checks in frozen order, then diagnostics at the rows' N
export PYTHONUNBUFFERED=1
P="nice -n 15 python3 an2_checks.py"
$P KC; $P KZ; $P KZ 0.05 128; $P KE2; $P KE2 0.05 128; $P KR
$P KC --mutate; $P KD --mutate

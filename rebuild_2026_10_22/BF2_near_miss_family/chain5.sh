#!/bin/bash
# control arms on the first 2000 of the real arm's 4000 jobs, to stay near the frozen 2 hours under load about 40
cd "$(dirname "$0")"
until [ -f control_real_N4000.json ]; do python3 -c "import time;time.sleep(30)"; done
for a in control perm1 perm2; do nice -n 19 python3 bf2_control.py 2000 $a >> control_2000.log 2>&1; echo "$a exit $?" >> chain5.status; done
echo finished >> chain5.status

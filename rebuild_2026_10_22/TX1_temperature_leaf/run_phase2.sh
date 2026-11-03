#!/bin/bash
# Phase 2 per footing: c1 harvest, key lists, keys per arm, cheap gates, MW and Bullet on the real top 5. nice 19, python3 -I. kappa = 1/2 FITTED; not theory closed.
F=$1
until [ -f tx1_train_TL0_${F}_label.json ]; do sleep 30; done
[ -f tx1_train_TL0_${F}_c1.json ] || nice -n 19 python3 -I tx1_read.py $F c1 TL0 > chunks/log_TL0_${F}_c1.read 2>&1
python3 -I tx1_lists.py > /dev/null
for a in real c1 c2 c3 label; do
  [ -f tx1_keys_${F}_$a.json ] || nice -n 19 python3 -I tx1_keys.py $F $a chunks/lists/${F}_$a.json tx1_keys_${F}_$a.json > chunks/log_keys_${F}_$a 2>&1
done
nice -n 19 python3 -I tx1_stage2.py $F chunks/lists/${F}_real.json tx1_stage2_$F.json > chunks/log_stage2_$F 2>&1
python3 -I -c "import json;L=json.load(open('chunks/lists/${F}_real.json'));json.dump(L[:5]+L[-2:],open('chunks/lists/${F}_top5.json','w'))"
nice -n 19 python3 -I tx1_dear.py mw $F chunks/lists/${F}_top5.json tx1_mw_$F.json > chunks/log_mw_$F 2>&1
nice -n 19 python3 -I tx1_dear.py bullet $F chunks/lists/${F}_top5.json tx1_bullet_$F.json > chunks/log_bullet_$F 2>&1
echo done > chunks/phase2_$F.done

#!/bin/bash
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
for t in diag_complo diag_ngc diag_sgc diag_hi_ngc diag_hi_sgc diag_hi_passive; do GH5_TIER=$t nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "$t exit $?"; done
python3 - <<'PY'
import numpy as np
D=np.load("../../../_external_data/gh5_work/gh5_lenses.npz");c=D["cen"];hi=D["comp"]>.8;ngc=(D["ra"]>90)&(D["ra"]<280);s=D["sfr"]-D["lm"]
for n,m in [("hi",c&hi),("lo",c&~hi)]:
    print(n,m.sum(),"NGC frac %.3f passive %.3f z %.3f lm %.3f"%(ngc[m].mean(),(s[m]<-11).mean(),np.median(D["z"][m]),np.median(D["lm"][m])))
PY
echo DIAGDONE

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_e_profile -- my own F(beta) profile (L minimised) from my own curves, to see how flat the objective is around beta_hat
and what F is at CFG186's beta = +0.887 (a number READ from CFG186's output, used only as a probe point).  Own code; reads only CFG193 files.
Rerun: ZF_REPO=<repo> python3 CFG193_e_profile.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["MUTATE"] = "0"
from CFG193_common import *
from scipy.optimize import minimize_scalar
VAR = os.environ.get("CFG193_VARIANT", "")
SUF = "_" + VAR if VAR else ""
T = Tee(os.path.join(HERE, "CFG193_e_profile%s.out" % SUF)); P = T.p
ut = np.load(os.path.join(HERE, "CFG193_utable.npz")); un = [str(x) for x in ut["names"]]
cz_ = np.load(os.path.join(HERE, "CFG193_curves%s.npz" % SUF)); cn = [str(x) for x in cz_["names"]]
prim = [n for n in un if ut["fD"][un.index(n)] in (2, 3, 4, 5) and n in cn]
ui = np.array([un.index(n) for n in prim]); ci = np.array([cn.index(n) for n in prim])
u0 = ut["u"][ui]; zc = ut["zcmb"][ui]; D = ut["D"][ui]; eD = ut["eD"][ui]
DU = np.array([u_los(zc[i], np.maximum(D[i] + eD[i] * TF, 0.3 * D[i])) - u_los(zc[i], D[i]) for i in range(len(prim))])
Z = ((u0[:, None] + DU) / W_REF) ** 2
cv = Curves(prim, cz_["C"][ci], meta=dict(N=cz_["N"][ci]))
sig, xh, _ = cv.sigma_i(); L0, tau = cv.tau_ml(sig, xh)
st = Stat(cv.ceff_fast(tau))
P("variant:", VAR or "main", " tau %.3f  median sigma_i %.3f  Fisher %.3f" % (tau, np.median(sig), LN10 / math.sqrt(np.sum(1 / (sig ** 2 + tau ** 2) * (Z[:, 80] - np.sum(Z[:, 80] / (sig ** 2 + tau ** 2)) / np.sum(1 / (sig ** 2 + tau ** 2))) ** 2))))
Lh, bh, Fh = fit_LB(st, Z, L0=L0, retall=True)
P("beta_hat = %+.4f, L = %.4f, F = %.3f" % (bh, Lh, Fh))
P("profile F(beta) - F_min (L minimised at each beta):")
out = {}
for b in (-0.6, -0.3, 0.0, 0.3, 0.6, 0.887, 1.2, 2.0, 3.0):
    r = minimize_scalar(lambda L: st.F(L, b, Z), bounds=(-11.3, -9.0), method="bounded", options=dict(xatol=1e-5))
    out[b] = r.fun - Fh
    P("   beta %+.3f : %.3f" % (b, r.fun - Fh))
jdump(dict(beta=bh, F=Fh, profile={str(k): v for k, v in out.items()}), os.path.join(HERE, "CFG193_e_profile%s_results.json" % SUF))

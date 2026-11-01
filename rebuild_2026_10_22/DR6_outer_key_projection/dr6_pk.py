#!/usr/bin/env python3
"""DR6 step 1 (FROZEN_CRITERIA.md): native linear P(k) from RF5's best cell, X34's patched CLASS, X34_ZON 1e6. Writes dr6_pk.json: xi(r_c), sigma(M), D(z), rho_m(z=0). Checks K2, K3, K4 and the direct Delta Sigma amplitude helper. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
import numpy as np
from scipy.special import jv
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
CLS = os.path.join(EXT, "rf5_class_build", "class_x34", "class"); CACHE = os.path.join(HERE, "cache_pk"); os.makedirs(CACHE, exist_ok=True)
r = json.load(open(os.path.join(RB, "RF5_growth_native_yardstick", "cells", "R1_1000000.json"))); p = r["params"]
d = {"T_cmb": 2.7255, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2, "thermodynamics_verbose": 1, "fourier_verbose": 1, "overwrite_root": "yes", "write_background": "yes",
     "omega_b": p["omega_b"], "omega_cdm": p["omega_c"], "100*theta_s": p["100theta_s"], "ln10^{10}A_s": p["lnA"], "n_s": p["n_s"], "tau_reio": p["tau"], "Omega_Lambda": 0.0, "w0_fld": p["w0"], "wa_fld": p["wa"], "cs2_fld": 1.0, "use_ppf": "yes",
     "output": "mPk", "P_k_max_h/Mpc": 30.0, "k_per_decade_for_pk": 20, "z_max_pk": 0.0, "z_pk": "0.0", "start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
root = os.path.join(CACHE, "pk_"); d["root"] = root
open(root + ".ini", "w").write("".join(f"{k} = {v}\n" for k, v in d.items()))
pr = subprocess.run(["nice", "-n", "15", CLS, root + ".ini"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1", X34_ZON=repr(1e6)))
if pr.returncode: raise SystemExit(pr.stdout[-500:] + pr.stderr[-500:])
log = pr.stdout; h = float(re.search(r"found 'h = ([0-9.eE+-]+)'", log).group(1)) if re.search(r"found 'h = ", log) else r["h"]
s8 = float(re.search(r"sigma8=([0-9.]+) for total matter", log).group(1)); rd = float(re.search(r"baryon drag stops at z = [0-9.eE+-]+\s+corresponding to conformal time = [0-9.eE+-]+ Mpc\s+with comoving sound horizon rs = ([0-9.eE+-]+) Mpc", log).group(1))
pk = np.loadtxt(root + "_pk.dat"); K = pk[:, 0] * h; PK = pk[:, 1] / h ** 3            # 1/Mpc, Mpc^3
bgf = root + "_background.dat"; hdr = [l for l in open(bgf) if l.startswith("#")][-1]; cols = {re.sub(r"^\d+:", "", c.strip()): i for i, c in enumerate(re.split(r"\s{2,}", hdr.lstrip("#").strip()))}; bg = np.loadtxt(bgf)
zb = bg[:, cols["z"]][::-1]; Db = bg[:, cols["gr.fac. D"]][::-1]; Db = Db / Db[0]; m = zb <= 5.0
Om = r["Omega_m"]; rhoc0 = 2.775e11 * h ** 2; rhom = Om * rhoc0                        # Msun/Mpc^3, comoving
dam = np.exp(-(K * 0.05) ** 2); lk = np.log(K)
rx = np.geomspace(0.3, 400, 500); XI = np.array([np.trapz(K ** 3 * PK * np.sinc(K * x / np.pi) * dam, lk) / (2 * np.pi ** 2) for x in rx])
lM = np.linspace(12, 16.5, 91); Rm = (3 * 10 ** lM / (4 * np.pi * rhom)) ** (1 / 3); sg = []
for R in Rm:
    x = K * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; sg.append(math.sqrt(np.trapz(K ** 3 * PK * W ** 2, lk) / (2 * np.pi ** 2)))
sg = np.array(sg); own8 = math.sqrt(np.trapz(K ** 3 * PK * (3 * (np.sin(K * 8 / h) - K * 8 / h * np.cos(K * 8 / h)) / (K * 8 / h) ** 3) ** 2, lk) / (2 * np.pi ** 2))
json.dump(dict(cell="R1_1000000", h=h, Om=Om, rhom=rhom, sigma8=s8, rd=rd, rx=rx.tolist(), xi=XI.tolist(), lM=lM.tolist(), sig=sg.tolist(), z=zb[m][::4].tolist(), D=Db[m][::4].tolist()), open(os.path.join(HERE, "dr6_pk.json"), "w"))
np.savez_compressed(os.path.join(HERE, "cache_pk", "pk.npz"), K=K, PK=PK)
# K2
ok2 = abs(s8 / 0.826 - 1) <= 0.005 and abs(rd - 147.13862) <= 1e-3; print(f"K2 sigma8 {s8:.4f} (own integral {own8:.4f}; RF5 table 0.826), r_d {rd:.5f} (RF5 147.13862), h {h:.5f} (RF5 {r['h']:.5f}): {'PASS' if ok2 else 'FAIL'}")
# K3: Delta Sigma from J2 against xi projected, one R, b = 1, comoving units, z = 0
def dsig_j2(R):
    kk = np.geomspace(K[0], K[-1], 400000); P_ = np.exp(np.interp(np.log(kk), lk, np.log(PK))) * np.exp(-(kk * 0.05) ** 2)
    return rhom * np.trapz(kk ** 2 * P_ * jv(2, kk * R), np.log(kk)) / (2 * np.pi)
def dsig_xi(R):
    ls = np.geomspace(1e-3, 400, 6000); RR = np.geomspace(0.3, 400, 800)    # Sigma(R') = 2 rho int xi dl; below r 0.3 the xi is held at 0.3's value through the mean-Sigma integral's small R tail
    xi_ = lambda r_: np.interp(np.log(r_), np.log(rx), XI)
    S = lambda R_: 2 * rhom * np.trapz(xi_(np.sqrt(R_ ** 2 + ls ** 2)) * ls, np.log(ls))
    rr = np.geomspace(1e-3, R, 500); ss = np.array([S(x) for x in rr]); return 2 / R ** 2 * np.trapz(ss * rr ** 2, np.log(rr)) - S(R)
a, b_ = dsig_j2(3.0), dsig_xi(3.0); ok3 = abs(b_ / a - 1) <= 0.03; print(f"K3 Delta Sigma at R 3 Mpc comoving, b = 1: J2 {a / 1e12:.3f}, xi projected {b_ / 1e12:.3f} Msun/pc^2, ratio {b_ / a:.4f}: {'PASS' if ok3 else 'FAIL'}")
# K4
nu = 1.686 / sg; b = 1 + (nu ** 2 - 1) / 1.686; bat1 = float(np.interp(1.0, nu, b)); ok4 = abs(bat1 - 1) <= 1e-3 and np.all(np.diff(b) > 0); print(f"K4 b(nu = 1) {bat1:.5f}, monotone {bool(np.all(np.diff(b) > 0))}: {'PASS' if ok4 else 'FAIL'}")
sys.exit(0 if ok2 and ok3 and ok4 else 1)

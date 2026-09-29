#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180 attacks B, variants V1-V15 (frozen in CFG180_FROZEN_CRITERIA.md section 6-B).  Deterministic.  Exit 0.
Shared (not independent): the CFG165 pipeline (CFG180_lib.M).
Declared reading of an ambiguous frozen item: V11e "drop the 5% lowest-error discs" = drop the 5% of KROSS discs with the smallest eV/V.
"""
import os
import sys
import csv
import json
import math
import copy
import time

import numpy as np

import CFG180_lib as L
M = L.M
T0 = time.time()
OUT = {}

# V15 needs per-disc gas: patch the CFG165 module's gbar so mu is multiplied by S.muw when present (only V15 sets it)
_orig_gbar = M.gbar


def _gbar_w(S, mu, delta, gas_scale=2.0):
    w = getattr(S, "muw", None)
    if w is None:
        return _orig_gbar(S, mu, delta, gas_scale)
    return _orig_gbar(S, mu * w, delta, gas_scale)


M.gbar = _gbar_w


def P(*a):
    print(L.scrub(" ".join(str(x) for x in a)), flush=True)


def sub(S, mask_or_idx):
    n = len(S.R)
    idx = np.where(mask_or_idx)[0] if getattr(mask_or_idx, "dtype", None) == bool else np.asarray(mask_or_idx)
    S2 = copy.copy(S)
    for k, v in list(S.__dict__.items()):
        if isinstance(v, np.ndarray) and v.shape and len(v) == n:
            setattr(S2, k, v[idx])
        elif isinstance(v, list) and len(v) == n and k != "fdm_ids":
            setattr(S2, k, [v[i] for i in idx])
    return S2


AS = L.get_anchor()
kross_kin = {r["name"]: r["kin_type"] for r in csv.DictReader(open(os.path.join(L.REPO, "data_assembly", "high_z_tf_tables", "kross_v2.csv")))}


class Cfg:
    def __init__(self):
        self.Su = L.get_kurvs("inc_star_deg")
        self.Sk = L.get_kross()
        self.mU = 1.0
        self.mK = 1.0
        self.gsU = 2.0
        self.gsK = 2.0
        self.anchor = "pooled"
        self.refU = 1.0
        self.refK = 1.0
        self.note = ""


def run(cfg, s):
    kwU = dict(Refac=cfg.refU, Refac_anchor=cfg.refU) if cfg.refU != 1.0 else {}
    kwK = dict(Refac=cfg.refK, Refac_anchor=cfg.refK) if cfg.refK != 1.0 else {}
    spU = L.sp_scaled(s * cfg.mU, **kwU)
    spK = L.sp_scaled(s * cfg.mK, **kwK)
    r = L.solve_pair(cfg.Sk, cfg.Su, AS, s, spK=spK, spU=spU, gsK=cfg.gsK, gsU=cfg.gsU, anchor_mode=cfg.anchor)
    ro = L.robs(float(np.median(cfg.Su.z)), float(np.median(cfg.Sk.z)), float(np.median(cfg.Su.logM)), float(np.median(cfg.Sk.logM)))
    inb, litb = ro["inrep"](2.0), ro["litb"](0.2)
    fl = {}
    both = []
    for law in L.LAWS:
        rl = r[law]["R"]
        if rl is None:
            fl[law] = None
            continue
        a, b = L.disfav_overlap(rl, inb), L.disfav_overlap(rl, litb)
        fl[law] = (a, b)
        if a and b:
            both.append(law)
    return r, fl, both


def V(mod):
    c = Cfg()
    mod(c)
    return c


def scale_V(S, f):
    S.V = S.V * f
    S.eV = S.eV * f


def scale_sig(S, f):
    S.sig = S.sig * f
    S.esig = S.esig * f
    S.sig0 = S.sig0 * f
    S.esig0 = S.esig0 * f


def kross_sub(c, mask):
    c.Sk = sub(c.Sk, mask)


def v15(c):
    for S in (c.Su, c.Sk):
        w = (10 ** (S.logM - 10.5)) ** (-0.22)
        S.muw = w / np.median(w)


VARS = []


def add(vid, desc, fn, exp=None):
    VARS.append((vid, desc, fn, exp))


add("V1", "KURVS inc_sfr_deg", lambda c: setattr(c, "Su", L.get_kurvs("inc_sfr_deg")))
add("V2a", "alpha x0.6 KURVS only", lambda c: setattr(c, "mU", 0.6), "down")
add("V2b", "alpha x1.4 KURVS only", lambda c: setattr(c, "mU", 1.4), "up")
add("V2c", "alpha x0.6 KROSS only", lambda c: setattr(c, "mK", 0.6), "up")
add("V2d", "alpha x1.4 KROSS only", lambda c: setattr(c, "mK", 1.4), "down")
add("V3a", "alpha x0.6 both+anchor", lambda c: (setattr(c, "mU", 0.6), setattr(c, "mK", 0.6)), "up")
add("V3b", "alpha x1.4 both+anchor", lambda c: (setattr(c, "mU", 1.4), setattr(c, "mK", 1.4)), "down")
add("V4a", "gas scale 1 R_d both", lambda c: (setattr(c, "gsU", 1.0), setattr(c, "gsK", 1.0)))
add("V4b", "gas scale 3 R_d both", lambda c: (setattr(c, "gsU", 3.0), setattr(c, "gsK", 3.0)))
add("V4c", "gas scale 4 R_d both", lambda c: (setattr(c, "gsU", 4.0), setattr(c, "gsK", 4.0)))
add("V5a", "gas scale 3 KURVS only", lambda c: setattr(c, "gsU", 3.0))
add("V5b", "gas scale 3 KROSS only", lambda c: setattr(c, "gsK", 3.0))
add("V6", "anchor median 0.064 (both)", lambda c: setattr(c, "anchor", "median"))
add("V7a", "KURVS V x1.10", lambda c: scale_V(c.Su, 1.10), "up")
add("V7b", "KURVS V x0.90", lambda c: scale_V(c.Su, 0.90), "down")
add("V8a", "KROSS V x1.10", lambda c: scale_V(c.Sk, 1.10), "down")
add("V8b", "KROSS V x0.90", lambda c: scale_V(c.Sk, 0.90), "up")
add("V9a", "KROSS sigma0 x0.8", lambda c: scale_sig(c.Sk, 0.8), "up")
add("V9b", "KROSS sigma0 x1.25", lambda c: scale_sig(c.Sk, 1.25), "down")
add("V10a", "KURVS sigma_out x0.8", lambda c: scale_sig(c.Su, 0.8), "down")
add("V10b", "KURVS sigma_out x1.25", lambda c: scale_sig(c.Su, 1.25), "up")
add("V11a", "KROSS RT only", lambda c: kross_sub(c, np.array([kross_kin.get(n) == "RT" for n in c.Sk.name])))
add("V11b", "KROSS b/a > 0.5", lambda c: kross_sub(c, np.cos(c.Sk.inc) > 0.5))
add("V11c", "KROSS v/sigma0 >= 2", lambda c: kross_sub(c, c.Sk.V / c.Sk.sig0 >= 2))
add("V11d", "KROSS v/sigma0 >= 3", lambda c: kross_sub(c, c.Sk.V / c.Sk.sig0 >= 3))
add("V11e", "KROSS drop lowest 5% eV/V", lambda c: kross_sub(c, (c.Sk.eV / c.Sk.V) > np.percentile(c.Sk.eV / c.Sk.V, 5)))
for j in range(10):
    add(f"V12.{j}", f"KURVS jackknife drop disc #{j}", (lambda jj: (lambda c: setattr(c, "Su", sub(c.Su, np.array([i for i in range(10) if i != jj])))))(j))
add("V13a", "R_e = 2 R_eff, KURVS only", lambda c: setattr(c, "refU", 2.0))
add("V13b", "R_e = 2 R_eff, both samples", lambda c: (setattr(c, "refU", 2.0), setattr(c, "refK", 2.0)))
add("V14a", "log M* +0.10 KURVS only", lambda c: setattr(c.Su, "logM", c.Su.logM + 0.10), "down")
add("V14b", "log M* -0.10 KURVS only", lambda c: setattr(c.Su, "logM", c.Su.logM - 0.10), "up")
add("V14c", "log M* +0.10 KROSS only", lambda c: setattr(c.Sk, "logM", c.Sk.logM + 0.10), "up")
add("V14d", "log M* -0.10 KROSS only", lambda c: setattr(c.Sk, "logM", c.Sk.logM - 0.10), "down")
add("V15", "per-disc gas ~ (M*/1e10.5)^-0.22, same median mu", v15)


def sg(x):
    return "n/a" if x is None else ("D" if x else "-")


def main():
    P("=" * 100)
    P("CFG180 attacks B: calibration / gas-prior variants V1-V15.  repo=<repo>")
    P("=" * 100)
    base = {}
    for s in (1.42, 1.00):
        r, fl, both = run(Cfg(), s)
        base[s] = (r, fl, both)
        rf, rr = r["flat"]["R"], r["H"]["R"]
        P(f"BASE s={s:4.2f}: flat {L.fmtR(rf)}  rival {L.fmtR(rr)}  flags(in,lit) flat {fl['flat']} rival {fl['H']}  both-bracket laws {both}")
    res = {}
    fragile = []
    moves = []
    exp_tally = []
    P("\n id     | variant                          |  s=1.42: R_flat  dlogRf  R_riv  dlogRr  d(sep)  class            | flags flat/rival (in,lit)  both-laws | s=1.00: R_flat  dlogRf  R_riv  dlogRr  both-laws")
    for vid, desc, fn, exp in VARS:
        c = V(fn)
        row = {}
        cells = []
        for s in (1.42, 1.00):
            r, fl, both = run(c, s)
            rf, rr = r["flat"]["R"], r["H"]["R"]
            b = base[s][0]
            bf, br_ = b["flat"]["R"]["R"], b["H"]["R"]["R"]
            if rf is None:
                dRf = None
            else:
                dRf = math.log10(rf["R"] / bf)
            dRr = None if rr is None else math.log10(rr["R"] / br_)
            dsep = None
            cls = "undefined"
            if rf is not None and rr is not None:
                dsep = (math.log10(rr["R"]) - math.log10(rf["R"])) - (math.log10(br_) - math.log10(bf))
                cls = ("COMMON-MODE" if (dRf * dRr > 0 and abs(dsep) < 0.03) else "DIFFERENTIAL" if abs(dsep) >= 0.06 else "MIXED")
            row[s] = dict(Rf=None if rf is None else rf["R"], Rr=None if rr is None else rr["R"], dRf=dRf, dRr=dRr, dsep=dsep, cls=cls, flags=fl, both=both,
                          Rf_int=None if rf is None else (rf["lo"], rf["hi"]), Rr_int=None if rr is None else (rr["lo"], rr["hi"]))
            if len(both) == 1:
                fragile.append((vid, s, both))
            for nm, d in (("flat", dRf), ("rival", dRr)):
                if d is not None and abs(d) >= 0.14:
                    moves.append((vid, s, nm, round(d, 3)))
        a, b = row[1.42], row[1.00]
        f = lambda x: "  --  " if x is None else f"{x:6.2f}"
        g = lambda x: "  --  " if x is None else f"{x:+6.3f}"
        P(f" {vid:6s} | {desc:32s} | {f(a['Rf'])} {g(a['dRf'])} {f(a['Rr'])} {g(a['dRr'])} {g(a['dsep'])}  {a['cls']:12s} | "
          f"{a['flags']['flat']}/{a['flags']['H']}  {[L.NAMES[x] for x in a['both']]} | {f(b['Rf'])} {g(b['dRf'])} {f(b['Rr'])} {g(b['dRr'])}  {[L.NAMES[x] for x in b['both']]}")
        res[vid] = row
        if exp and row[1.42]["dRf"] is not None:
            got = "up" if row[1.42]["dRf"] > 0 else "down"
            exp_tally.append((vid, exp, got, got == exp))
    OUT["variants"] = {k: {str(s): v for s, v in row.items()} for k, row in res.items()}
    # jackknife summary
    jk = [res[f"V12.{j}"][1.42]["Rf"] for j in range(10) if res[f"V12.{j}"][1.42]["Rf"] is not None]
    jkr = [res[f"V12.{j}"][1.42]["Rr"] for j in range(10) if res[f"V12.{j}"][1.42]["Rr"] is not None]
    P(f"\nKURVS jackknife at s=1.42: R_flat range {min(jk):.2f}-{max(jk):.2f} (base {base[1.42][0]['flat']['R']['R']:.2f}); R_rival range {min(jkr):.2f}-{max(jkr):.2f} (base {base[1.42][0]['H']['R']['R']:.2f})")
    P(f"\nVariants making EXACTLY ONE law disfavoured by both brackets (frozen summary reading; s=1 and s=1.42): {fragile if fragile else 'none'}")
    P(f"Variants moving a law's R by >= 0.14 dex (as much as the in-repo 2-sigma half-width): {moves if moves else 'none'}")
    P("Direction expectations (hand E13), sign of dlogR_flat at s=1.42: " + "; ".join(f"{v}: exp {e}, got {g} {'ok' if k else 'WRONG'}" for v, e, g, k in exp_tally))
    P(f"  direction expectations met: {sum(k for *_, k in exp_tally)}/{len(exp_tally)}")
    verdict = "ROBUST" if not fragile else "FRAGILE"
    P(f"\nA-summary for the B block: the NON-DIAGNOSTIC verdict is {verdict} against single-input changes at s = 1 and 1.42 (frozen summary rule).")
    OUT["fragile"] = fragile
    OUT["moves"] = moves
    OUT["exp"] = exp_tally
    OUT["verdict"] = verdict
    with open(os.path.join(L.HERE, "CFG180_attacks_B_results.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    P(f"runtime {time.time() - T0:.1f} s")


if __name__ == "__main__":
    main()

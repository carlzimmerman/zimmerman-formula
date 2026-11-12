#!/usr/bin/env python3
"""FINAL-2 (EPOCH): score pre-registered halo-formation epochs against DD1's frozen table.

Reads
  fable52_push/DD1_deduce_from_data/dd1_table.csv      (DD1's frozen 3621-row table)
  closure_2026_11_11/FINAL2_epoch/predictions_frozen.csv  (the 6x6 pre-registered numbers)
Writes
  closure_2026_11_11/FINAL2_epoch/final2_measured.json
Prints the measured residual per class on both footings, and the score of each candidate.

Law, as pinned by DD1's KA4:  g_bar (g + a0) = g^2,  i.e. g_bar = g^2/(g + a0)
  -> g_obs_law(g_bar, a0) = 0.5 (g_bar + sqrt(g_bar^2 + 4 a0 g_bar))
  -> Y_law = log10(g_obs_law / g_bar);  X_law = a0 / g_obs_law
Statistic: X = g_obs/g_bar - 1; Y = log10(1+X) = log10(lgo) - log10(lgb);
           resid = Y_meas - Y_law(g_bar; a0).
Footings never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10.
"""
import csv, math, json, statistics as st
from collections import defaultdict

A0_CAN = 9.3603e-11
A0_ALT = 1.1312e-10
KPC = 3.0856775814913673e19
C = 2.99792458e8

import os
_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# 2026-11-12: the three paths below were absolute; they now resolve from this file, to the same files.
TABLE = (_REPO + "/"
         "fable52_push/DD1_deduce_from_data/dd1_table.csv")
PRED = (_REPO + "/"
        "closure_2026_11_11/FINAL2_epoch/predictions_frozen.csv")
OUT = (_REPO + "/"
       "closure_2026_11_11/FINAL2_epoch/final2_measured.json")


def gobs_law(gbar, a0):
    return 0.5 * (gbar + math.sqrt(gbar * gbar + 4.0 * a0 * gbar))


def ylaw(gbar, a0):
    return math.log10(gobs_law(gbar, a0) / gbar)


def load():
    lines = open(TABLE).read().splitlines()
    hdr = lines[1].split(',')          # lines[0] is a '#' comment
    rows = []
    for ln in lines[2:]:
        p = ln.split(',')
        if len(p) != len(hdr):
            continue
        d = dict(zip(hdr, p))
        if (d.get('bracket') or '').strip() != '':   # main table only
            continue
        try:
            rows.append(dict(cls=d['cls'], sys=d['sys'], r=float(d['r_kpc']),
                             lgb=float(d['lgb']), lgo=float(d['lgo']),
                             eY=float(d['eY']), z=float(d['z']),
                             last=int(d['last'])))
        except Exception:
            pass
    for x in rows:
        x['Y'] = x['lgo'] - x['lgb']
        x['rc'] = x['Y'] - ylaw(10 ** x['lgb'], A0_CAN)
        x['ra'] = x['Y'] - ylaw(10 ** x['lgb'], A0_ALT)
        x['dep'] = 10 ** x['lgo'] * x['r'] * KPC / (C * C)
    return rows


TARGET = [('tidal dwarfs', 'tidal_dwarfs'),
          ('NGC 1052 UDGs', 'DF2_DF4'),
          ('MW ultra-faints', 'MW_ultra_faints'),
          ('M31 dwarfs', 'bright_M31_dwarfs'),
          ('faint rotators', 'LSB_field_rotators'),
          ('X-COP', 'XCOP_clusters')]

CANDS = [('a_turnaround', '(a) turnaround of the baryon shell'),
         ('b_caustic',    '(b) first caustic / shell crossing'),
         ('c_shock',      '(c) the shock (VSH1)'),
         ('d_a0cross',    '(d) last epoch internal g > a0'),
         ('e_quench',     '(e) end of SF / last major merger'),
         ('f_fixed',      '(f) recombination / fixed early z')]


def spearman(a, b):
    if len(set(a)) < 2 or len(set(b)) < 2:
        return float('nan')

    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for pos, i in enumerate(s):
            r[i] = pos + 1
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb))
    return num / den if den > 0 else float('nan')


def main():
    rows = load()
    byc = defaultdict(list)
    for x in rows:
        byc[x['cls']].append(x)
    pred = {d['class']: d for d in csv.DictReader(open(PRED))}

    meas = {}
    print(f"main rows {len(rows)}")
    print("| class | pts | sys | med lg g_bar | med Y | resid CAN | resid ALT | se |")
    for cls, tag in TARGET:
        rs = byc[cls]
        ns = len(set(x['sys'] for x in rs))
        rc = st.median([x['rc'] for x in rs])
        ra = st.median([x['ra'] for x in rs])
        mad = st.median([abs(x['rc'] - rc) for x in rs])
        se = 1.2533 * 1.4826 * mad / math.sqrt(ns)
        meas[tag] = dict(cls=cls, n=len(rs), nsys=ns,
                         med_lgb=st.median([x['lgb'] for x in rs]),
                         med_Y=st.median([x['Y'] for x in rs]),
                         res_can=rc, res_alt=ra, se=se,
                         depth=st.median([x['dep'] for x in rs]))
        m = meas[tag]
        print(f"| {cls} | {m['n']} | {m['nsys']} | {m['med_lgb']:.3f} | {m['med_Y']:.3f} "
              f"| {rc:+.3f} | {ra:+.3f} | {se:.3f} |")

    tags = [t for _, t in TARGET]
    vc = [meas[t]['res_can'] for t in tags]
    va = [meas[t]['res_alt'] for t in tags]
    print(f"\nmeasured spread across the 6 target classes: {max(vc)-min(vc):.3f} dex (can), "
          f"{max(va)-min(va):.3f} dex (alt)")

    for footing, fk in (("canonical", "res_can"), ("alt", "res_alt")):
        print(f"\n=== {footing} footing ===")
        print(f"{'candidate':34s} {'rms':>6s} {'sign/6':>7s} {'<=0.15':>7s} "
              f"{'spread':>7s} {'rho':>6s} {'chi2':>7s}")
        ms = [meas[t][fk] for t in tags]
        c0 = st.median(ms)
        rms0 = math.sqrt(sum((c0 - m) ** 2 for m in ms) / len(ms))
        chi0 = sum(((c0 - m) / meas[t]['se']) ** 2 for t, m in zip(tags, ms))
        print(f"{'-- constant (class median), floor':34s} {rms0:6.3f} {'':>7s} {'':>7s} "
              f"{0.0:7.3f} {float('nan'):6.3f} {chi0:7.1f}")
        rows_sc = []
        for key, name in CANDS:
            ds = []
            sh = 0.0
            hit = 0
            for t in tags:
                p = float(pred[t][key]); m = meas[t][fk]
                ds.append(p - m)
                if abs(m) <= 0.05:
                    sh += 0.5 if abs(p - m) <= 0.10 else 0.0
                elif (p > 0) == (m > 0):
                    sh += 1.0
                if abs(p - m) <= 0.15:
                    hit += 1
            rms = math.sqrt(sum(x * x for x in ds) / len(ds))
            chi = sum((d / meas[t]['se']) ** 2 for t, d in zip(tags, ds))
            sp = max(float(pred[t][key]) for t in tags) - min(float(pred[t][key]) for t in tags)
            ps = [float(pred[t][key]) for t in tags]
            rows_sc.append((key, name, sh, hit, rms, sp, spearman(ps, ms), chi))
        order = sorted(rows_sc, key=lambda r: (r[4], -r[2], -r[3]))
        rank = {r[0]: i + 1 for i, r in enumerate(order)}
        for key, name, sh, hit, rms, sp, rho, chi in rows_sc:
            print(f"{name:34s} {rms:6.3f} {sh:7.1f} {hit:7d} {sp:7.3f} {rho:6.3f} {chi:7.1f}")
        print("rank: " + ", ".join(f"{r[1]}={rank[r[0]]}" for r in rows_sc))

    json.dump(meas, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()

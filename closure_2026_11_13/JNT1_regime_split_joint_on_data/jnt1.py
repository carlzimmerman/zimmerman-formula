#!/usr/bin/env python3
"""JNT1 (FROZEN_CRITERIA.md, 00292e1430): row S = SPARC rotation curves of SRJ2's cluster-regime galaxies under the
reference layout (FRZ1's cold dark energy NFW halo at z 0 + baryons), point by point, against DD1's class line (offset,
inner / outer shape) and against the law's scatter on the same galaxies; known answers KA1-KA4; M/L bracket.
SRJ3's srj3.py is executed read-only from its own path up to its 'RES = dict(' line (that executes SRJ2's srj2_rc.py
prefix, SRH1's srh1_rc.py prefix, FLD1 and PD1 prefixes, all unchanged; nothing is written in their folders).
  python3 jnt1.py            -> jnt1.json / jnt1.out
  python3 jnt1.py TWN|TWH|TWD -> jnt1_MUTATE_<twin>.json / .out (deliberately wrong halo)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
TWIN = sys.argv[1] if len(sys.argv) > 1 else None
assert TWIN in (None, "TWN", "TWH", "TWD")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
S3 = os.path.join(REPO, "closure_2026_11_12", "SRJ3_reference_layout_disc_fit"); SRC = os.path.join(S3, "srj3.py"); code = open(SRC).read()
N3 = {"__file__": SRC, "__name__": "srj3_lib"}; _a = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
    warnings.simplefilter("ignore"); exec(compile(code[:code.index('RES = dict(lane="SRJ3"')], SRC, "exec"), N3)
sys.argv = _a
NS, S = N3["NS"], N3["S"]
GALS, PRE, glaw, CR, A0, XTAB, rfold_kpc, PN, G, MS, KPC = (S[k] for k in ("GALS", "PRE", "glaw", "CR", "A0", "XTAB", "rfold_kpc", "PN", "G", "MS", "KPC"))
vgal, VST, SPF, FOOTS = NS["vgal"], NS["VST"], NS["SPF"], NS["FOOTS"]
UPS = PN["Q8"].UPS; iU = {u: int(np.where(np.isclose(UPS, u))[0][0]) for u in (0.35, 0.50, 0.65)}
SJ2 = json.load(open(os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint", "srj2_rc.json")))
SJ3 = json.load(open(os.path.join(S3, "srj3.json")))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"JNT1 row S{' TWIN ' + TWIN + ' (deliberately wrong)' if TWIN else ''} (criteria 00292e1430). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P(f"SPARC (QX8 loader) {len(GALS)}; VST {VST}; Upsilon grid {UPS[0]:.2f}-{UPS[-1]:.2f} ({len(UPS)})")

def Mb_of(q):
    VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
    return max(float(np.max(np.clip(VB2 * q["R"] / PN["G_KPC"], 0, None))), 1e3)
def gname(q): return q.get("name") or q["meta"].get("name", "?")

def model(ft, q, Tf, kind, twin=None):
    """log10 g_mod over all Upsilon columns (npts, nups)."""
    g = q["GB"]; Rm = q["Rm"]; a0 = A0[ft]; Mbs = Mb_of(q); X = XTAB[ft]["z0.0"]
    if kind == "ref":
        Xe = X * {None: 1.0, "TWH": 0.5, "TWD": 2.0, "TWN": 0.0}[twin]
        ge = g if twin == "TWN" else g + (G * CR(Rm, Mbs, Xe) / Rm ** 2)[:, None]
        return np.log10(np.maximum(ge, 1e-300))
    if kind == "refT": return np.log10(np.maximum(g + (G * CR(Rm, Mbs, X) / Rm ** 2)[:, None], 1e-300)) + Tf
    if kind == "law": return np.log10(np.maximum(glaw(g, a0), 1e-300))
    if kind == "lawT": return np.log10(np.maximum(glaw(g, a0), 1e-300)) + Tf
    raise ValueError(kind)

def resid(q, lg, col):
    """col: int (fixed Upsilon column) or 'fit' (QX8 per-galaxy best column). Returns (R_kpc, r, W) on OK points."""
    OK, W = q["OK"], q["W"]
    if col == "fit":
        r2 = np.where(OK, np.log10(q["GO"])[:, None] - lg, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        col = int(np.argmin((Wm * r2 * r2).sum(0) / np.maximum(Wm.sum(0), 1e-300)))
    ok = OK[:, col]; r = np.log10(q["GO"][ok]) - lg[ok, col]
    return q["Rm"][ok] / KPC, r, W[ok], col

def cls_line(v, e):
    v = np.asarray(v, float); n = len(v)
    if n == 0: return dict(n=0, med=float("nan"), se=float("nan"), line=False)
    med = float(np.median(v)); mad = float(np.median(np.abs(v - med)))
    se = max(1.2533 * 1.4826 * mad / math.sqrt(n), float(np.median(e)) / math.sqrt(n))
    return dict(n=n, med=med, se=se, mad=mad, line=bool(abs(med) <= 0.10 and abs(med) <= 3 * se))

def rowS(ft, members, kind, col, twin=None):
    per = []; wr2 = wr = ws = 0.0
    for i in members:
        q, Tf = GALS[i], PRE[ft][i]; Rk, r, W, c = resid(q, model(ft, q, Tf, kind, twin), col)
        d = float(np.sum(W * r) / np.sum(W)); e = 0.8686 / math.sqrt(np.sum(W)); Rl = float(Rk[-1]) if len(Rk) else float("nan")
        inn, out = Rk < 0.5 * Rl, Rk >= 0.5 * Rl
        D = float(np.sum(W[out] * r[out]) / np.sum(W[out]) - np.sum(W[inn] * r[inn]) / np.sum(W[inn])) if inn.any() and out.any() else None
        eD = 0.8686 * math.sqrt(1 / np.sum(W[out]) + 1 / np.sum(W[inn])) if D is not None else None
        per.append(dict(name=gname(q), npts=int(len(r)), U=float(UPS[c]), d=d, e=e, shape=D, e_shape=eD, R_last_kpc=Rl,
                        Vflat=q["meta"]["Vflat"], logMb=math.log10(Mb_of(q)), r_inner=float(np.median(r[inn])) if inn.any() else None, r_outer=float(np.median(r[out])) if out.any() else None))
        wr2 += float(np.sum(W * r * r)); wr += float(np.sum(W * r)); ws += float(np.sum(W))
    S1 = cls_line([p["d"] for p in per], [p["e"] for p in per])
    sh = [p for p in per if p["shape"] is not None]; S2 = cls_line([p["shape"] for p in sh], [p["e_shape"] for p in sh]); S2["n_left_out"] = len(per) - len(sh)
    return dict(per=per, S1=S1, S2=S2, rms=math.sqrt(wr2 / ws), mean=wr / ws, npts=int(sum(p["npts"] for p in per)))

def word(ref, law):
    if ref["S1"]["n"] < 5: return "NO POWER", []
    s3 = ref["rms"] <= law["rms"] + 0.02; bad = [k for k, ok in (("S1 offset", ref["S1"]["line"]), ("S2 shape", ref["S2"]["line"]), ("S3 scatter", s3)) if not ok]
    return ("REFERENCE FITS" if not bad else "REFERENCE FAILS"), bad

RES = dict(lane="JNT1", criteria="00292e1430", twin=TWIN, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
names = [gname(q) for q in GALS]
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    mem_names = SJ2["foot"][ft]["G3b"]["f1.00"]["graded"]["cluster_names"]
    members = [i for i, q in enumerate(GALS) if vgal(ft, Mb_of(q), 0.0) > VST[ft]]
    R["KA4"] = dict(n=len(members), names=[names[i] for i in members], stored=mem_names, pass_=bool([names[i] for i in members] == mem_names))
    fld_sub = [c["name"] for c in SJ2["foot"][ft]["G3a"]["cluster"]]
    P(f"\n[{ft}] row S members (PD1 M_b at Upsilon 0.5): {len(members)} {R['KA4']['names']}; KA4 vs srj2_rc.json -> {'PASS' if R['KA4']['pass_'] else 'FAIL'}; FLD1-M_b subset {fld_sub}")
    if not TWIN:
        # KA1: QX8 fixed-U 0.50 law reading on all 175
        ka = {}
        for kind in ("law", "lawT"):
            a = b = c = 0.0
            for i, q in enumerate(GALS):
                _, r, W, _ = resid(q, model(ft, q, PRE[ft][i], kind), iU[0.50]); a += np.sum(W * r); b += np.sum(W * r * r); c += np.sum(W)
            ka[kind] = dict(rms=float(math.sqrt(b / c)), mean=float(a / c))
        tgt = {"canonical": {"law": (0.1124, 0.0504), "lawT": (0.1181, 0.0594)}, "alt": {"law": (0.1029, 0.0239)}}[ft]
        ok = len(GALS) == 175 and all(abs(ka[k]["rms"] - v[0]) <= 5e-4 and abs(ka[k]["mean"] - v[1]) <= 5e-4 for k, v in tgt.items())
        R["KA1"] = dict(n=len(GALS), vals=ka, targets=tgt, pass_=bool(ok))
        P(f"[{ft}] KA1 loader {len(GALS)}; fixed U 0.50 all 175: law rms {ka['law']['rms']:.4f} mean {ka['law']['mean']:+.4f}, exact (T) {ka['lawT']['rms']:.4f} / {ka['lawT']['mean']:+.4f}; targets {tgt} -> {'PASS' if ok else 'FAIL'}")
        # KA2: SRJ2's reported reference reading, recomputed in this code
        a = b = c = 0.0; a0 = A0[ft]
        for i, q in enumerate(GALS):
            g = q["GB"]; Rm = q["Rm"]; Mbs = Mb_of(q)
            if i in members: lg = model(ft, q, PRE[ft][i], "refT")
            else:
                rt = 1.0 * rfold_kpc(ft, 0.0, math.log10(Mbs)) * KPC; gt = G * Mbs * MS / rt ** 2; ph = float(glaw(gt, a0)) - gt
                lg = np.log10(np.maximum(np.where((Rm < rt)[:, None], glaw(g, a0), g + ph * (rt / Rm[:, None]) ** 2), 1e-300)) + PRE[ft][i]
            _, r, W, _ = resid(q, lg, "fit"); a += np.sum(W * r); b += np.sum(W * r * r); c += np.sum(W)
        t2 = {"canonical": 0.0640, "alt": 0.0559}[ft]; v2 = math.sqrt(b / c)
        R["KA2"] = dict(rms=float(v2), mean=float(a / c), target=t2, stored=SJ2["foot"][ft]["G3b"]["f1.00"]["reported_reference"]["all"]["rms"], pass_=bool(abs(v2 - t2) <= 1e-4))
        P(f"[{ft}] KA2 SRJ2 reported reference reading (f 1, T, per-galaxy U): rms {v2:.5f} mean {a / c:+.5f} vs {t2} (stored {R['KA2']['stored']:.5f}) -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}")
        # KA3: SRJ3's construction on zC 400569 (canonical: listed there)
        gl = N3["gals"](ft); hit = [g_ for g_ in gl if g_["name"] == "zC 400569"]
        st = [g_ for g_ in SJ3["foot"][ft]["main"]["galaxies"] if g_["name"] == "zC 400569"]
        if hit and st:
            R["KA3"] = dict(d=hit[0]["d"], stored=st[0]["d"], pass_=bool(abs(hit[0]["d"] - st[0]["d"]) <= 1e-6 and (ft != "canonical" or abs(hit[0]["d"] + 0.0061041) <= 1e-6)))
            P(f"[{ft}] KA3 SRJ3 halo on zC 400569: d {hit[0]['d']:+.7f} vs srj3.json {st[0]['d']:+.7f} -> {'PASS' if R['KA3']['pass_'] else 'FAIL'}")
        else:
            R["KA3"] = dict(note="zC 400569 not cluster-regime on this footing", pass_=True, n_discs_reproduced=int(sum(abs(x["d"] - y["d"]) <= 1e-6 for x, y in zip(gl, SJ3["foot"][ft]["main"]["galaxies"]))), n=len(gl))
            P(f"[{ft}] KA3 zC 400569 not on this footing's list; discs reproduced {R['KA3']['n_discs_reproduced']} / {len(gl)}")
        # galaxy-regime last radius inside f R_fold
        gr = [i for i in range(len(GALS)) if i not in members]
        fmin_pd1 = max(float(GALS[i]["Rm"][-1] / KPC) / rfold_kpc(ft, 0.0, math.log10(Mb_of(GALS[i]))) for i in gr)
        R["below"] = dict(n=len(gr), f_min_PD1Mb=fmin_pd1, f_min_FLD1Mb_all=SJ2["foot"][ft]["C1_G3a"]["off_f_min"])
        P(f"[{ft}] SPARC below v_stiff: {len(gr)} galaxies; every last radius inside f R_fold for f >= {fmin_pd1:.4f} (PD1 M_b); FLD1 M_b (all 175) {R['below']['f_min_FLD1Mb_all']:.4f}")
    # row S
    cols = {"U0.50": iU[0.50]} if TWIN else {"U0.50": iU[0.50], "U0.35": iU[0.35], "U0.65": iU[0.65], "fit": "fit"}
    R["S"] = {}
    for cn, col in cols.items():
        ref = rowS(ft, members, "ref", col, TWIN); law = rowS(ft, members, "lawT", col)
        o = dict(ref=ref, lawT=law)
        if not TWIN: o["law_noT"] = rowS(ft, members, "law", col); o["refT"] = rowS(ft, members, "refT", col)
        w, bad = word(ref, law); o["word"] = w; o["failed_lines"] = bad
        lw, lbad = word(law, law); o["law_word_same_lines"] = lw; o["law_failed_lines"] = lbad
        R["S"][cn] = o
        P(f"[{ft}] row S {cn}: n {ref['S1']['n']} ({ref['npts']} points) | reference off {ref['S1']['med']:+.4f} se {ref['S1']['se']:.4f} -> {'holds' if ref['S1']['line'] else 'FAILS'}; "
          f"shape (outer - inner) {ref['S2']['med']:+.4f} se {ref['S2']['se']:.4f} (left out {ref['S2']['n_left_out']}) -> {'holds' if ref['S2']['line'] else 'FAILS'}; rms {ref['rms']:.4f} mean {ref['mean']:+.4f} => {w} {bad}")
        P(f"[{ft}]    law + T beside: off {law['S1']['med']:+.4f} se {law['S1']['se']:.4f}, shape {law['S2']['med']:+.4f} se {law['S2']['se']:.4f}, rms {law['rms']:.4f} mean {law['mean']:+.4f} (same lines: {lw} {lbad})"
          + ("" if TWIN else f" | law no T off {o['law_noT']['S1']['med']:+.4f} shape {o['law_noT']['S2']['med']:+.4f} rms {o['law_noT']['rms']:.4f} | reference + T off {o['refT']['S1']['med']:+.4f} shape {o['refT']['S2']['med']:+.4f} rms {o['refT']['rms']:.4f}"))
        if cn == "U0.50":
            for p, pl in zip(ref["per"], law["per"]):
                P(f"[{ft}]      {p['name']:<12} Vflat {p['Vflat']:5.1f} logMb {p['logMb']:.2f} pts {p['npts']:3d} R_last {p['R_last_kpc']:5.1f} kpc | ref d {p['d']:+.3f} shape {('n/a' if p['shape'] is None else format(p['shape'], '+.3f'))} (in {p['r_inner'] if p['r_inner'] is None else round(p['r_inner'], 3)} out {p['r_outer'] if p['r_outer'] is None else round(p['r_outer'], 3)}) | law+T d {pl['d']:+.3f} shape {('n/a' if pl['shape'] is None else format(pl['shape'], '+.3f'))}")
    if not TWIN:
        ws = {k: v["word"] for k, v in R["S"].items()}; R["S_word"] = ws["U0.50"]; R["fragile"] = bool(len(set(ws.values())) > 1)
        P(f"[{ft}] row S word (U 0.50): {R['S_word']}; bracket words {ws} -> {'FRAGILE' if R['fragile'] else 'bracket holds'}")
    else:
        R["S_word"] = R["S"]["U0.50"]["word"]; R["bites"] = R["S_word"] == "REFERENCE FAILS"
        P(f"[{ft}] twin {TWIN}: row S word {R['S_word']} -> {'bites' if R['bites'] else ('n/a (n < 5)' if R['S_word'] == 'NO POWER' else 'DOES NOT BITE')}")
tag = f"_MUTATE_{TWIN}" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"jnt1{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt1{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")

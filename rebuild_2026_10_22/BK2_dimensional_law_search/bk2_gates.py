#!/usr/bin/env python3
"""BK2 gates G4's S line and G12 DiskMass on F, form R. Shared by read and checks. kappa = 1/2 FITTED; not theory closed."""
import contextlib, io, pickle
from bk2_lib import *
import bk2_lib as B
_Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb")); UPS = _Q["UPS"]; GALS = _Q["gals"]; DR = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod"); _GG = {}
def _gg(q):
    if q["name"] not in _GG: t = np.atleast_2d(np.loadtxt(os.path.join(DR, q["name"] + "_rotmod.dat"), comments="#")); _GG[q["name"]] = (t[:, 0], t[:, 3])
    return _GG[q["name"]]
def s_line(f, a0, which=None):
    """EM1's statistic: per-galaxy U on UPS, pooled weighted rms, median U; which 0/1 picks even/odd sorted names; tilt as UR2's on vf."""
    names = sorted(q["name"] for q in GALS); idx = {n: i for i, n in enumerate(names)}; W2 = Ws = 0.0; U = []; V = []
    for q in GALS:
        if which is not None and idx[q["name"]] % 2 != which: continue
        R = q["Rm"]; gb = q["GB"]; r_, vg = _gg(q)
        if len(r_) != len(R): return None
        gg = np.clip(np.abs(vg) * vg, 0, None) * KMS2 / R; gg2 = np.minimum(gg[:, None], np.maximum(gb, 0)); gs = np.maximum(gb, 0) - gg2; n = gb.shape[1]; Rr = np.repeat(R[:, None], n, 1); M = np.maximum(gb, 1e-30) * Rr ** 2 / G; dl = np.ones_like(M)
        if len(R) > 2: dl[1:-1] = (np.log(M[2:]) - np.log(M[:-2])) / np.log(Rr[2:] / Rr[:-2]).clip(1e-9); dl[0] = dl[1]; dl[-1] = dl[-2]
        inner = np.zeros_like(gb)
        for k in range(len(R) - 2, -1, -1): inner[k] = inner[k + 1] + 0.5 * (gb[k] + gb[k + 1]) * (Rr[k + 1] - Rr[k])
        L = B._local(gs, gg2, Rr, dl, np.maximum(Rr * np.maximum(gb, 0) + inner + np.maximum(gb[-1:], 0) * Rr[-1:], 1e-30), a0); g = ev(f, L); OK = q["OK"]; okb = OK & np.isfinite(g) & (g > 0)
        if not np.array_equal(okb, OK): return None
        r = np.where(OK, np.log10(q["GO"])[:, None] - np.log10(np.where(okb, g, 1.0)), 0.0); Wm = np.where(OK, q["W"][:, None], 0.0); wr2 = (Wm * r * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); W2 += wr2[i]; Ws += ws[i]; U.append(UPS[i]); V.append(q["vf"] or 0)
    U = np.array(U); V = np.array(V); md = float(np.median(U)); rs = np.random.default_rng(11); seu = float(np.std(np.median(U[rs.integers(0, len(U), (1000, len(U)))], axis=1))); rms = math.sqrt(W2 / Ws); lo = (V > 0) & (V < 100); hi = V > 150; tilt = float(np.median(U[lo]) - np.median(U[hi])); ZU = 0.0 if .5 <= md <= .8 else min(abs(md - .5), abs(md - .8)) / max(seu, 1e-9); return dict(rms=rms, U=md, seU=seu, tilt=tilt, ZU=float(ZU), line=bool(rms <= .110 and .5 <= md <= .8), tilt_ok=bool(abs(tilt) <= .15))
_DM = {}
def diskmass(f, a0, fR=1.5):
    if not _DM:
        S576 = os.path.join(REPO, "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S576), "__name__": "h"}
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S576).read().split('P("=" * 100)')[0], "h", "exec"), n)
        _DM["n"] = n
    from scipy.optimize import brentq
    N_ = _DM["n"]; gal, terms, K_V, sexp, gbar, Gk = N_["gal"], N_["galaxy_terms"], N_["K_VERT"], N_["sexp"], N_["gbar"], N_["G"]; KU = 3.0857e13; rs = []; Ys = []
    def Fv(gb_k, R, Sig_k):
        """gb_k in code units; leaves in SI. Stars only reading for g_gas here: atomic and molecular shares are not split in gbar's return, so g_gas 0, [READING]."""
        gsi = max(gb_k, 1e-30) * 1e6 / (3.0857e19); Rs = R * 3.0857e19; L = B._local(np.array([gsi]), np.array([0.0]), np.array([Rs]), np.array([1.0]), np.array([2 * Rs * gsi]), a0); return float(ev(f, L)[0]) * 3.0857e19 / 1e6
    for g in gal.values():
        R = fR * g["hR"]; N_["gal_BD"] = g["BD"]; t = terms(g, R); go = t["vrot"] ** 2 / R; fun = lambda Y: Fv(gbar(t, R, Y), R, 0) - go
        try: Y = brentq(fun, .02, 5.0)
        except (ValueError, ZeroDivisionError): continue
        gb = gbar(t, R, Y); Sig = Y * t["I0"] * math.exp(-R / t["hR"]) + sexp(R, t["Ma"], 2 * t["hR"]) + sexp(R, t["Mm"], t["hR"]); KN = 2 * math.pi * Gk * Sig * (1 - math.exp(-1)); Bf = 1 + (Fv(gb, R, 0) - gb) * t["hz"] / R / KN; rs.append(math.sqrt(math.pi * Gk * K_V * t["hz"] * Sig * Bf) / t["smeas"]); Ys.append(Y)
    if len(rs) < 5: return None
    rs = np.array(rs); r_ = np.random.default_rng(576); bs = np.median(r_.choice(rs, size=(2000, len(rs))), axis=1); r = float(np.median(rs)); se = float(bs.std()); Z = (r - 1) / math.hypot(se, .23 * r); return dict(r=r, se=se, n=len(rs), Y=float(np.median(Ys)), Z=float(Z), line=bool(.9 <= r <= 1.1 and len(rs) >= 27), err=bool(abs(Z) <= 2))

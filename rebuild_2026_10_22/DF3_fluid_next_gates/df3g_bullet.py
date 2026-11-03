#!/usr/bin/env python3
"""DF3_fluid_next_gates, Bullet: equilibrium fluid per subcluster, column-by-column inelastic collision, Sigma added to the law's map (exact for reading N), UX6's grader unchanged. MG1's other pairs by mass rows. DF3G_MUTATE=1 flips the parcel shift. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import csv, io, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import df3g_run as R
import numpy as np
from scipy.ndimage import gaussian_filter
H, S = R.H, R.S; HERE = R.HERE; RB = R.RB; KPC = R.KPC; MSUN = R.MSUN
MUT = os.environ.get("DF3G_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; SGN = -1.0 if MUT else 1.0
p = os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"); s_ = open(p).read().split('say("=" * 90); say("UX6')[0]; a = 'OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")'; assert s_.count(a) == 1; s_ = s_.replace(a, "import io as _io; OUT = _io.StringIO()"); n = {"__file__": p, "__name__": "b"}; exec(compile(s_, p, "exec"), n)
XS, YS, XX, YY, SIGC, APS, GAS, GAL, observe = n["XS"], n["YS"], n["XX"], n["YY"], n["SIG_CRIT"], n["APS"], n["GAS"], n["GAL"], n["observe"]
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = tuple(A0F)
CENT = {"main": np.array([0.0, 0.0]), "sub": np.array([820.0, 220.0])}; DNOW = float(np.hypot(820, 220)); UX, UY = 820 / DNOW, 220 / DNOW
COMPS = {"main": [(GAS[0][0], GAS[0][1]), (GAL[0][0], GAL[0][1])], "sub": [(GAS[1][0], GAS[1][1]), (GAS[2][0], GAS[2][1]), (GAS[3][0], GAS[3][1]), (GAL[1][0], GAL[1][1])]}
def lawmap(f):
    q = os.path.join(HERE, "cache", f"lawmap_{f}.npz")
    if os.path.exists(q):
        z = np.load(q, allow_pickle=False); return z["S"], {k: float(z["m_" + k]) for k in APS}
    sp = {"L": dict(form="LAW", k=0.0, a0=A0F[f], scale=1.0)}; o = n["run"](sp)["L"]; np.savez(q, S=o[0], **{"m_" + k: o[1][k] for k in APS}); return o[0], o[1]
def plum(comps, rk): return sum(m * rk ** 3 / (rk ** 2 + a ** 2) ** 1.5 for m, a in comps)
class Fl: pass
def equil(comps, Rf, a0, M_tov=None, Mbt_=None):
    rk = np.geomspace(1e-3, 3e4, 500); Mb = np.maximum.accumulate(np.maximum(plum(comps, rk), 0.0)); Mbt = float(Mbt_ if Mbt_ else plum(comps, 3e5)); rta = H.RTA(Mbt * MSUN) / KPC; rk = rk[rk <= rta * 1.001]; rk = np.r_[rk, rta * 1.0005]; Mb = np.maximum.accumulate(np.maximum(plum(comps, rk), 0.0)); fair = Rf * Mbt; s = S.solve(rk * KPC, Mb * MSUN, rta * KPC, 300 * KPC, fair * MSUN, a0=a0); f = Fl(); f.r = rk; f.M = s["Mf"] / MSUN; f.rho = s["rho"]; f.fair = fair; f.Mbt = Mbt; f.noeq = bool(s["noeq"]); f.held = float(s["held"]) / MSUN; f.rh = float(s["rhalf"]) / KPC; f.gm = float(s["gmrc2"]); f.csc = float(s["csc"]); f.gr = bool(M_tov is not None and fair > M_tov)
    return f
def shells(f, nsh=240):
    e = np.geomspace(max(f.r[0], 1e-3), f.r[-1], nsh + 1); Me = np.interp(np.log(e), np.log(f.r), f.M); Me[0] = 0.0; dm = np.maximum(np.diff(Me), 0.0); rm = np.sqrt(e[1:] * e[:-1]); rh = dm * MSUN / (4 * math.pi / 3 * np.diff(e ** 3) * KPC ** 3); return e, dm, rm, rh
def column(e, rh, b):
    """Sigma(b), Msun/kpc^2, through shells of uniform rho (kg/m^3)."""
    B = b[:, None]; hi = np.sqrt(np.maximum(e[1:] ** 2 - B ** 2, 0.0)); lo = np.sqrt(np.maximum(e[:-1] ** 2 - B ** 2, 0.0)); return np.sum(2 * (hi - lo) * rh * KPC ** 3 / MSUN, axis=1)
GM, GP = np.polynomial.legendre.leggauss(40)
PHI = (np.arange(24) + .5) * 2 * math.pi / 24
def parcels(e, dm, rm):
    """deterministic rings: r, mu, phi. Rotate phi per shell to avoid a fixed spoke pattern."""
    gold = 2.399963; sh = (rm.size, GM.size, PHI.size); R_ = np.broadcast_to(rm[:, None, None], sh); mu = np.broadcast_to(GM[None, :, None], sh); ph = PHI[None, None, :] + (np.arange(rm.size) * gold)[:, None, None]; w = np.broadcast_to(dm[:, None, None] * (GP[None, :, None] / 2) / PHI.size, sh); st = np.sqrt(1 - mu ** 2)
    return (R_ * mu).ravel(), (R_ * st * np.cos(ph)).ravel(), (R_ * st * np.sin(ph)).ravel(), np.ascontiguousarray(w).ravel(), (R_ * st).ravel()
def csb(f, b):
    ro = np.exp(np.interp(np.log(np.maximum(b, f.r[0])), np.log(f.r), np.log(np.maximum(f.rho, 1e-300)))); return S.cs_of(ro) / 1e3
def collide(fm, fs, v, compact_main=0.0, compact_sub=0.0):
    """Returns per-species parcels shifted, stats. compact_* = mass at the centre as a point, which rides with its galaxies."""
    Em, dm, rm, rhm = shells(fm); Es, ds, rs, rhs = shells(fs); out = {}; stat = {}; bb = np.geomspace(1e-3, 3e4, 1500); Sm = column(Em, rhm, bb); Ss = column(Es, rhs, bb); fb = Ss / np.maximum(Sm + Ss, 1e-300); fr = lambda b: np.interp(np.log(np.maximum(b, 1e-3)), np.log(bb), fb); cm = np.maximum(csb(fm, bb), 1e-6); cs = np.maximum(csb(fs, bb), 1e-6); cmax = np.maximum(cm, cs); mg = lambda b: np.interp(np.log(np.maximum(b, 1e-3)), np.log(bb), v / cmax) >= 1.0
    for nm, (E, dq, rq), other, sign, comp, self_f, ot_f in (("main", (Em, dm, rm), fs, 1.0, compact_main, fm, fs), ("sub", (Es, ds, rs), fm, -1.0, compact_sub, fs, fm)):
        x, y, z, w, b = parcels(E, dq, rq); f_ = fr(b); merges = mg(b); shift = (f_ if nm == "main" else (1 - f_)) * DNOW * merges; tot = w.sum() + comp; withg = (w[shift <= 0.25 * DNOW].sum() + comp) / max(tot, 1e-300); frac = (w * shift).sum() / DNOW / max(tot, 1e-300); flag = w[~merges].sum() / max(tot, 1e-300); rh = max(self_f.rh, 1e-3); cc = float(S.cs_of(np.exp(np.interp(math.log(max(rh, self_f.r[0])), np.log(self_f.r), np.log(np.maximum(self_f.rho, 1e-300)))))) / 1e3; ro_self = float(np.exp(np.interp(math.log(max(rh, self_f.r[0])), np.log(self_f.r), np.log(np.maximum(self_f.rho, 1e-300))))); ro_ot = float(np.exp(np.interp(math.log(max(rh, ot_f.r[0])), np.log(ot_f.r), np.log(np.maximum(ot_f.rho, 1e-300))))); cen = float(self_f.csc * S.CL / 1e3)
        stat[nm] = dict(M=float(tot), M_held=float(w.sum()), M_point=float(comp), with_galaxies=float(withg), mean_speed_loss=float(frac), mach_centre=v / max(cen, 1e-9), mach_half=v / max(cc, 1e-9), subsonic_share=float(flag), ram_over_P_half=ro_ot * (v * 1e3) ** 2 / max(ro_self * (cc * 1e3) ** 2, 1e-300), rhalf_kpc=rh, gm_rc2=self_f.gm, cs_centre_over_c=self_f.csc, noeq=self_f.noeq, gr_noeq=self_f.gr)
        X_p = x + SGN * sign * shift + (0 if nm == "main" else DNOW)
        out[nm] = (X_p * UX - y * UY, X_p * UY + y * UX, w, comp)
    return out, stat
def deposit(sp):
    dx = 10.0; xe = np.r_[XS - dx / 2, XS[-1] + dx / 2]; ye = np.r_[YS - dx / 2, YS[-1] + dx / 2]; M = np.zeros((XS.size, YS.size)); ap = {k: 0.0 for k in APS}
    for nm, (X, Y, w, comp) in sp.items():
        H2, _, _ = np.histogram2d(X, Y, bins=[xe, ye], weights=w); M += H2
        if comp > 0:
            i = int(np.argmin(np.abs(XS - CENT[nm][0]))); j = int(np.argmin(np.abs(YS - CENT[nm][1]))); M[i, j] += comp
        for k, (c, Rp) in APS.items():
            d = np.hypot(X - c[0], Y - c[1]); ap[k] += float(w[d <= Rp].sum())
            if comp > 0 and math.hypot(*(CENT[nm] - c)) <= Rp: ap[k] += comp
    return gaussian_filter(M / dx ** 2 * 1.0, 2.0, mode="constant"), ap
def grade(sp, f):
    L0, mL = lawmap(f); Sg, ap = deposit(sp); Stot = L0 + Sg * 1.0; m = {k: mL[k] + ap[k] for k in APS}; o = observe(Stot, m); Lb = "PASSES" if False else None; return {k: o[k] for k in ("main", "sub", "M300", "ZO3", "ratio", "cls", "kappa_max")}
def label(st):
    a, b = st["main"]["with_galaxies"], st["sub"]["with_galaxies"]; return "PASSES LIKE GALAXIES" if a > .5 and b > .5 else ("STOPS WITH THE GAS" if a < .5 or b < .5 else "MIXED")
class Pl(Fl): pass
def plum_fl(M, a):
    f = Fl(); f.r = np.geomspace(1e-3, 3e4, 600); f.M = M * f.r ** 3 / (f.r ** 2 + a ** 2) ** 1.5; f.rho = 3 * M * MSUN / (4 * math.pi * (a * KPC) ** 3) * (1 + (f.r / a) ** 2) ** -2.5; f.rh = 1.3 * a; f.gm = 0.0; f.csc = 0.0; f.noeq = False; f.gr = False; f.held = M; f.fair = M; return f
def controls():
    S.Cfg.gamma = 1.0; S.Cfg.sigma = 1.0; S.Cfg.K = 1.0; ck = {}
    sp, st = collide(plum_fl(2.0e14, 565.0), plum_fl(2.32e13, 300.0), 4700.0); Sg = {}
    for nm in sp:
        X, Y, w, _ = sp[nm]; xp = X * UX + Y * UY; h, ed = np.histogram(xp, bins=np.arange(-1500, 2500, 20.0), weights=w); Sg[nm] = float(ed[h.argmax()] + 10.0)
    ck["K_gas_sign"] = dict(main_gas_peak_kpc_along_axis=Sg["main"], sub_gas_peak=Sg["sub"], BCGs=[0.0, DNOW], observed_offsets=[209.4, 194.1], main_offset=Sg["main"], sub_offset=DNOW - Sg["sub"], passed=bool(0 < Sg["main"] < DNOW and 0 < Sg["sub"] < DNOW and Sg["main"] < Sg["sub"] + 1e9), note="sign only; Plummer gas has no cool core; magnitude a limit of the column model")
    nosh = {}
    for nm, (M, a) in (("main", (2.39e14, 200.0)), ("sub", (1.57e14, 200.0))):
        f = plum_fl(M, a); E, d, r_, _ = shells(f); x, y, z, w, b = parcels(E, d, r_); Xp = x + (0 if nm == "main" else DNOW); nosh[nm] = (Xp * UX - y * UY, Xp * UY + y * UX, w, 0.0)
    g = grade(nosh, "canonical"); ck["K_on_galaxies"] = dict(dk_main=g["main"]["dkappa"], dk_sub=g["sub"]["dkappa"], d_bcg=[g["main"]["d_bcg"], g["sub"]["d_bcg"]], M300=g["M300"], cls=g["cls"], passed=bool(g["main"]["dkappa"] > 0 and g["sub"]["dkappa"] > 0))
    L0, mL = lawmap("canonical"); o = observe(L0, mL); ck["K_law_row"] = dict(M300=o["M300"], dk=[o["main"]["dkappa"], o["sub"]["dkappa"]], cls=o["cls"], passed=bool(abs(o["M300"][0] / 1.11e14 - 1) < .01 and abs(o["M300"][1] / .73e14 - 1) < .01))
    return ck
def tov(g, sg):
    return S.tov_max(S.m_of_K(sg ** 2 * 1e6 / g * S.RHO_A ** (1 - g))) if abs(g - 5 / 3) < 1e-6 else None
CELLS = ((1.0, 100.0), (5 / 3, 100.0), (1.0, 30.0), (5 / 3, 30.0), (2 / 3, 30.0))
def mg1_rows(Rf, a0, Mtv):
    T = {}
    for w in csv.DictReader(open(os.path.join(RB, "MG1_merger_sample", "mg1_table.csv"))): T.setdefault(w["system"], []).append(w)
    O = []
    for sy, q in T.items():
        if len(q) != 2 or sy == "Bullet": continue
        Fs = []
        for w in q:
            ML = float(w["M_lens"]); Mg = float(w["M_gas"]) if w["M_gas"] not in ("", "DEFAULT") else .12 * ML; Ms = float(w["M_star"]) if w["M_star"] not in ("", "DEFAULT") else .02 * ML; ag = float(w["a_gas"] or 300); ast = float(w["a_star"] or 200); Fs.append((equil([(Mg, ag), (Ms, ast)], Rf, a0, Mtv), ML, w["sub"]))
        for i, (ff, ML, sb) in enumerate(Fs):
            ot = Fs[1 - i][0]; E, d, r_, rh = shells(ff); E2, _, _, rh2 = shells(ot); x, y, z, w_, b = parcels(E, d, r_); bb = np.geomspace(1e-3, 3e4, 800); a_ = column(E, rh, bb); o_ = column(E2, rh2, bb); frac = np.interp(np.log(np.maximum(b, 1e-3)), np.log(bb), o_ / np.maximum(a_ + o_, 1e-300)); pm = max(ff.fair - ff.held, 0.0) if ff.noeq else 0.0; wg_H = float(w_[frac <= .25].sum() / max(w_.sum(), 1e-300)); wg_C = float((w_[frac <= .25].sum() + pm) / max(w_.sum() + pm, 1e-300)); M2 = float(w_[b <= 300].sum()); O.append(dict(system=sy, sub=sb, M_lens=ML, stays_H=wg_H, stays_C=wg_C, Mf300_over_Mlens_H=M2 / ML, Mf300_over_Mlens_C=(M2 + pm) / ML, noeq=ff.noeq, gr_noeq=ff.gr))
    return O
def main():
    out = dict(controls=controls()); out["control_ok"] = all(v["passed"] for v in out["controls"].values()); print(json.dumps(out["controls"], default=float), flush=True); out["law"] = {}
    for f in FEET:
        L0, mL = lawmap(f); o = observe(L0, mL); out["law"][f] = {k: o[k] for k in ("main", "sub", "M300", "ZO3", "ratio", "cls")}
    if MUT:
        json.dump(R.CO.fmt(out), open(os.path.join(HERE, f"df3g_bullet{TAG}.json"), "w"), indent=1, sort_keys=True, default=float); return
    out["cells"] = {}
    for g, sg in CELLS:
        Rf = R.rf_of(g, sg); Mt = tov(g, sg); tag = f"G{g:.3f}_s{sg:g}"; ce = dict(Rf=Rf, M_TOV=Mt, rows={}); out["cells"][tag] = ce
        for rd in ("N", "S"):
            for f in FEET:
                R.setc(g, sg, rd, "H"); Fm = equil(COMPS["main"], Rf, A0F[f], Mt); Fs_ = equil(COMPS["sub"], Rf, A0F[f], Mt)
                for v in (4700.0, 4000.0):
                    for mode in ("H", "C"):
                        pm = (max(Fm.fair - Fm.held, 0.0) if Fm.noeq else 0.0) if mode == "C" else 0.0; ps = (max(Fs_.fair - Fs_.held, 0.0) if Fs_.noeq else 0.0) if mode == "C" else 0.0
                        if Fm.gr or Fs_.gr: pass
                        sp, st = collide(Fm, Fs_, v, pm, ps); row = dict(stat=st, label=label(st), fair=[Fm.fair, Fs_.fair], held=[Fm.held, Fs_.held])
                        if rd == "N": row["grade"] = grade(sp, f)
                        else: row["grade"] = "NOT COMPUTED, A1"
                        ce["rows"][f"{rd}|{f}|{v:g}|{mode}"] = row; print(tag, rd, f, v, mode, row["label"], st["main"]["with_galaxies"], st["sub"]["with_galaxies"], row["grade"]["cls"] if rd == "N" else "", row["grade"]["M300"] if rd == "N" else "", flush=True)
        R.setc(g, sg, "N", "H"); ce["mg1"] = {f: mg1_rows(Rf, A0F[f], Mt) for f in FEET}
    json.dump(R.CO.fmt(out), open(os.path.join(HERE, f"df3g_bullet{TAG}.json"), "w"), indent=1, sort_keys=True, default=float)
if __name__ == "__main__": main()

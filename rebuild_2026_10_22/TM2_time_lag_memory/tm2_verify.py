#!/usr/bin/env python3
"""TM2 A1: post-result. Fresh code for W2; vector memory on orbits; K1 diagnosis. No import from tm2_map. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RB, "CU1_gas_term_replication")); sys.path.insert(0, os.path.join(RB, "UX3_cluster_gas_term"))
import numpy as np
from astropy.io import fits
from scipy.optimize import minimize_scalar
import cu1_core as c, ux3_common as u
np.seterr(all="ignore")
OUT = open(os.path.join(HERE, "tm2_verify.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
GN = 6.674e-11; G = 6.6743e-11; MSB = 1.989e30; MS = 1.98847e30; KPC = 3.0857e19; MYR = 3.15576e13; KMS = 1.02271e-3
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt"); KF = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); PI2 = math.pi**2; SC = 1.827e9
XS = (0.1, 0.2, 0.3, 0.5, 0.7); TAUS = (150., 300., 600., 1200., 5000.)
# ---------- orbits, vector mean
xc = c.XC(); PF = {}
for nm in xc.names:
    h_ = fits.open(os.path.join(c.XDIR, nm, nm + "_hydro_mass.fits")); f_ = fits.open(os.path.join(c.XDIR, nm, nm + "_fgas_profile.fits")); Rg = float(f_[1].header["R500"])
    a = np.asarray(h_[1].data["RADIUS"], float); b = np.asarray(h_[1].data["M_FORW"], float); p = np.asarray(f_[1].data["RADIUS"], float)*Rg; q = np.asarray(f_[1].data["MGAS"], float); i1 = (a > 0) & (b > 0); i2 = (p > 0) & (q > 0); PF[nm] = (np.log(a[i1]), np.log(b[i1]), np.log(p[i2]), np.log(q[i2]))
def ex(q, x, y):
    s0 = (y[3] - y[0])/(x[3] - x[0]); s1 = (y[-1] - y[-4])/(x[-1] - x[-4]); o = np.interp(q, x, y); return np.where(q < x[0], y[0] + s0*(q - x[0]), np.where(q > x[-1], y[-1] + s1*(q - x[-1]), o))
DT = 2.0; EDG = np.r_[0.0, np.geomspace(2.0, 10000.0, 60)]; rng = np.random.default_rng(20261103)
def orbit(nm, r0, beta):
    Mt = lambda r: np.exp(ex(np.log(r), PF[nm][0], PF[nm][1])); Mg = lambda r: np.exp(ex(np.log(r), PF[nm][2], PF[nm][3]))
    v2 = G*Mt(np.array(r0))*MS/(r0*KPC); vc = math.sqrt(v2)/1e3*KMS; sr = vc/math.sqrt(2); st = sr*math.sqrt(1 - beta); N = 400
    x = np.full(N, float(r0)); y = np.zeros(N); vx = rng.normal(0, sr, N); vy = rng.normal(0, st, N)
    acc = lambda r: G*Mt(r)*MS/(r*KPC)**2*(MYR**2/KPC)/r
    r = np.maximum(np.hypot(x, y), 2.0); A = acc(r); ot = np.zeros(len(EDG) - 1); j = 0; S = 0.0; n = 0; t = 0.0; g0 = float(G*Mg(np.array(r0))*MS/(r0*KPC)**2)
    for i in range(int(10000/DT)):
        vx -= .5*DT*A*x; vy -= .5*DT*A*y; x += DT*vx; y += DT*vy; r = np.maximum(np.hypot(x, y), 2.0); A = acc(r); vx -= .5*DT*A*x; vy -= .5*DT*A*y; t += DT
        S += float((G*Mg(r)*MS/(r*KPC)**2*(x/r)).mean()); n += 1
        if t >= EDG[j + 1] - 1e-9:
            ot[j] = S/n/g0; S = 0.0; n = 0; j += 1
            if j == len(ot): break
    return ot
def kw(tau):
    w = np.exp(-EDG[:-1]/tau) - np.exp(-EDG[1:]/tau); return w/w.sum()
ORB = {b_: np.array([orbit(xc.names[xc.cl[i]], float(xc.r[i]/(1e3*c.PC)), b_) for i in range(len(xc.r))]) for b_ in (0.0, 0.5)}
DYN = (xc.r/(1e3*c.PC))/np.array([math.sqrt(G*xc.mh[i]*MS/xc.r[i])/1e3*KMS for i in range(len(xc.r))])
def mv(tau, b_=0.0): return ORB[b_] @ kw(tau)
def xrow(foot, m):
    L = xc.law(foot); T = xc.term(foot)*m; dfn = lambda K: np.log10(xc.mh/(L*(1 + K*T))); wt = np.isin(xc.cl, (0, 2, 4, 6)); kr = minimize_scalar(lambda K: (dfn(K)[wt]**2).sum(), bounds=(0, 2000), method="bounded", options=dict(xatol=1e-5)).x
    def st(d, s): return float(d[s].mean()), float(np.sqrt((d[s]**2).mean()))
    al = np.ones_like(wt); fx = dfn(KF[foot]); rf = dfn(kr); ok = lambda d: abs(st(d, al)[0]) <= .05 and st(d, al)[1] <= .10 and abs(st(d, ~wt)[0]) <= .05 and st(d, ~wt)[1] <= .10
    return dict(kr=float(kr), fix=st(fx, al), fix_ok=bool(ok(fx)), ref=st(rf, al), ref_h=st(rf, ~wt), ref_ok=bool(ok(rf)))
say("=== vector memory on orbits, X-COP ===")
RES = dict(xcop={}, bullet={}, discs={}, keys={}, scan={})
say("median m_v by x; dyn Myr " + str([round(float(np.median(DYN[xc.x == x]))) for x in XS]))
for tau in TAUS:
    for b_ in (0.0, 0.5):
        m = mv(tau, b_); mx = [float(np.median(m[xc.x == x])) for x in XS]
        for f in FEET:
            o = xrow(f, m); RES["xcop"][f"{tau:g}|b{b_}|{f}"] = dict(m=mx, **o); say(f"tau {tau:6g} beta {b_} {f:9s} m_v {[round(v, 3) for v in mx]} | k fix {o['fix'][0]:+.3f},{o['fix'][1]:.3f} {'PASS' if o['fix_ok'] else 'FAIL'} | k refit {o['kr']:.2f} all {o['ref'][0]:+.3f},{o['ref'][1]:.3f} unseen {o['ref_h'][0]:+.3f},{o['ref_h'][1]:.3f} {'PASS' if o['ref_ok'] else 'FAIL'}")
# table m_v against ln(tau/t_dyn), isotropic
lnq = []; mm = []
for tau in np.geomspace(10, 8000, 25):
    lnq.append(np.log(tau/DYN)); mm.append(mv(tau, 0.0))
lnq = np.concatenate(lnq); mm = np.concatenate(mm); bins = np.linspace(-3, 5, 25); cen = .5*(bins[1:] + bins[:-1]); TAB = np.array([np.median(mm[(lnq >= bins[i]) & (lnq < bins[i + 1])]) if ((lnq >= bins[i]) & (lnq < bins[i + 1])).any() else np.nan for i in range(24)]); ok_ = np.isfinite(TAB); cen, TAB = cen[ok_], TAB[ok_]
say("m_v vs tau/t_dyn: " + " ".join(f"{math.exp(a_):.2g}:{b_:.2f}" for a_, b_ in zip(cen[::3], TAB[::3])))
# ---------- fresh W2 on the Bullet, linear in k
GAS = [(2.0e14, 565.0, 190.0, 90.0, 0), (1.5e13, 505.0, 525.0, 120.0, 1), (1.5e13, 90.0, 670.0, 170.0, 1), (-6.8e12, 70.0, 670.0, 170.0, 1)]
ST = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]; BC = np.array([[0.0, 0.0], [820.0, 220.0]]); GP = np.array([[190.0, 90.0], [670.0, 170.0]]); D = float(np.hypot(*BC[1])); UV = BC[1]/D; NV = np.array([-UV[1], UV[0]])
def pl(X, Y, Z, M, a, x0, y0):
    dx, dy = X - x0, Y - y0; f = -GN*M*MSB/((dx*dx + dy*dy + Z*Z + a*a)**1.5)/KPC**2; return f*dx, f*dy, f*Z
def lw(g, a): return .5*g + np.sqrt(.25*g*g + a*g)
def nodes(t):
    return np.r_[np.linspace(0, t, 13), np.geomspace(t, 10000.0, 21)[1:]]
def track(h, s):
    r = D*UV + (s/h["t"])*(h["b"]*NV - D*UV); n = np.hypot(*r); r = r*min(1, 3500/n) if n > 0 else r; com = h["q"]*D*UV; return [com - h["q"]*r, com + (1 - h["q"])*r]
ZM = np.r_[np.linspace(0, 1200, 61), np.geomspace(1200, 6000, 41)[1:]]
def build(h, step, smear):
    """returns dict foot -> (S_law, {tau: S_1}) kappa-free surface densities; smear True multiplies each flow's memory by m_v"""
    xs = np.arange(-500, 1400 + 1e-9, step); ys = np.arange(-400, 700 + 1e-9, step); XX, YY = np.meshgrid(xs, ys, indexing="ij"); ed = nodes(h["t"]); sm = .5*(ed[1:] + ed[:-1]); trk = [track(h, s) for s in sm]; now = track(h, 0.0)
    S0 = {f: np.zeros_like(XX) for f in FEET}; S1 = {(f, t): np.zeros_like(XX) for f in FEET for t in TAUS}; wt = {t: (np.exp(-ed[:-1]/t) - np.exp(-ed[1:]/t))/(1 - np.exp(-ed[-1]/t)) for t in TAUS}; nb = 4 if step >= 20 else 3
    for j0 in range(0, len(ys), nb):
        X, Y, Z = np.meshgrid(xs, ys[j0:j0 + nb], ZM, indexing="ij"); div0 = {f: 0.0 for f in FEET}; div1 = {k: 0.0 for k in S1}
        for ax, de in enumerate(((2., 0, 0), (0, 2., 0), (0, 0, 2.))):
            for sg in (1.0, -1.0):
                Xa, Ya, Za = X + sg*de[0], Y + sg*de[1], Z + sg*de[2]; gp = [pl(Xa, Ya, Za, m_, a_, x_, y_) for m_, a_, x_, y_, _ in GAS]; sp = [pl(Xa, Ya, Za, *q) for q in ST]; gb = [sum(q[i] for q in gp) + sum(q[i] for q in sp) for i in range(3)]
                rho = [q[0]/q[1]**3*(1 + ((Xa - q[2])**2 + (Ya - q[3])**2 + Za**2)/q[1]**2)**-2.5 for q in ST]; rs = rho[0] + rho[1]; wc = [rho[0]/rs, rho[1]/rs]; rc = [np.sqrt((Xa - BC[i, 0])**2 + (Ya - BC[i, 1])**2 + Za**2) for i in (0, 1)]
                FL = []
                for c_ in (0, 1):
                    acc = {t: 0.0 for t in TAUS}
                    for n_, s_ in enumerate(sm):
                        tr = trk[n_]; g_ = max(0.0, 1 - s_/h["t"])**h["p"]; sft = (np.array(now[c_]) - tr[c_]); vv = 0.0
                        for m_, a_, x_, y_, gr in GAS:
                            ofs = np.array([x_, y_]) - BC[gr]; pos = BC[gr] + (tr[gr] - np.array(now[gr])) + ofs*g_ + sft; vv = vv + pl(Xa, Ya, Za, m_, a_, pos[0], pos[1])[ax]
                        for t in TAUS: acc[t] = acc[t] + wt[t][n_]*vv
                    FL.append(acc)
                for f in FEET:
                    a0 = A0[f]; gy = gb[1] + a0/1000.0; g = np.sqrt(gb[0]**2 + gy**2 + gb[2]**2); L = lw(g, a0); comp = (gb[0], gy, gb[2])[ax]; div0[f] = div0[f] + sg*comp*(L/np.maximum(g, 1e-300) - 1)
                    for t in TAUS:
                        fac0, fac1 = 1.0, 1.0
                        if smear:
                            vc = 1500.0*KMS  # km/s scale for t_dyn from the term's own M300, PROVISIONAL, one number
                            fac0 = np.interp(np.log(t/(np.maximum(rc[0], 20.0)/vc)), cen, TAB); fac1 = np.interp(np.log(t/(np.maximum(rc[1], 20.0)/vc)), cen, TAB)
                        div1[(f, t)] = div1[(f, t)] + sg*(L/a0)*(wc[0]*fac0*FL[0][t] + wc[1]*fac1*FL[1][t])
        for f in FEET: S0[f][:, j0:j0 + nb] = 2*np.trapz(-div0[f]/4.0/(4*math.pi*GN)*KPC**2/MSB, ZM, axis=2)
        for k_ in S1: S1[k_][:, j0:j0 + nb] = 2*np.trapz(-div1[k_]/4.0/(4*math.pi*GN)*KPC**2/MSB, ZM, axis=2)
    base = sum(q[0]*q[1]**2/(math.pi*((XX - q[2])**2 + (YY - q[3])**2 + q[1]**2)**2) for q in [g_[:4] for g_ in GAS] + ST)
    for f in FEET: S0[f] += base
    return xs, ys, XX, YY, S0, S1
SD = math.sqrt((1/8)**2 + .15**2)
def read(xs, ys, XX, YY, S, step):
    o = {}; cl = True; m300 = []; 
    for n_, (bc, gc) in zip(("main", "sub"), zip(BC, GP)):
        mid = .5*(bc + gc); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350; i, j = np.unravel_index(int(np.argmax(np.where(w, S, -np.inf))), S.shape); edge = not (0 < i < S.shape[0] - 1 and 0 < j < S.shape[1] - 1) or not w[i - 1:i + 2, j - 1:j + 2].all(); lm = (not edge) and S[i, j] >= S[i - 1:i + 2, j - 1:j + 2].max()
        pk = np.array([XX[i, j], YY[i, j]]); dg = float(np.hypot(*(pk - gc))); db = float(np.hypot(*(pk - bc))); sp = float(np.hypot(*(bc - gc))); dk = float((S[np.hypot(XX - bc[0], YY - bc[1]) <= 100].mean() - S[np.hypot(XX - gc[0], YY - gc[1]) <= 100].mean())/SC); z = (dg/sp - 1)/SD; o[n_] = dict(peak=pk.tolist(), dg=dg, db=db, Z=z, dk=dk, g=bool(lm and db < dg))
        m300.append(float(S[np.hypot(XX - bc[0], YY - bc[1]) < 300].sum()*step*step))
    o["M300"] = m300; o["ZM"] = [(m300[0]/3.5e14 - 1)/.15, (m300[1]/2.3e14 - 1)/.15]; o["ratio"] = m300[1]/m300[0]; bad = any((not o[q]["g"]) or abs(o[q]["Z"]) > 3 or o[q]["dk"] <= 0 for q in ("main", "sub")) or any(abs(z) > 3 for z in o["ZM"]); o["cls"] = "FAIL" if bad else ("PASS" if all(abs(o[q]["Z"]) <= 2 for q in ("main", "sub")) and all(abs(z) <= 2 for z in o["ZM"]) else "TENSION"); return o
def fmt(o): return f"m {o['main']['peak']} Z{o['main']['Z']:+.2f} s {o['sub']['peak']} Z{o['sub']['Z']:+.2f} dk {o['main']['dk']:+.3f} {o['sub']['dk']:+.3f} M {o['M300'][0]/1e14:.2f}({o['ZM'][0]:+.1f}) {o['M300'][1]/1e14:.2f}({o['ZM'][1]:+.1f}) r {o['ratio']:.2f} {o['cls']}"
HP = dict(t=180., q=.12, p=1, b=0.); HH = dict(t150=dict(t=150., q=.12, p=1, b=0.), t260=dict(t=260., q=.12, p=1, b=0.), p2=dict(t=180., q=.12, p=2, b=0.), b256=dict(t=180., q=.12, p=1, b=256.), q40=dict(t=180., q=.40, p=1, b=0.))
say("\n=== fresh W2, 10 kpc, history P; k scan ===")
xs, ys, XX, YY, S0, S1 = build(HP, 10.0, False); GRID = (9.87, 8.64, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.29)
for f in FEET:
    for t in TAUS:
        o = {}
        for kv in (PI2, .65*KF[f], KF[f]) + tuple(np.arange(7.0, 20.01, .5)):
            o[round(float(kv), 3)] = read(xs, ys, XX, YY, S0[f] + kv*S1[(f, t)], 10.0)
        pa = [k_ for k_, v in sorted(o.items()) if v["cls"] == "PASS"]; te = [k_ for k_, v in sorted(o.items()) if v["cls"] in ("PASS", "TENSION")]; RES["scan"][f"{t:g}|{f}"] = dict(PASS=pa, PASS_or_TENSION=te, pi2=o[round(PI2, 3)], fit=o[round(KF[f], 3)])
        say(f"{f:9s} tau {t:6g}: PASS k {pa[:1]}-{pa[-1:]}; PASS or TENSION k {te[:1]}-{te[-1:]}; pi2: {fmt(o[round(PI2, 3)])}; fit: {fmt(o[round(KF[f], 3)])}")
say("\n=== fresh W2 at pi^2 and k fit, other histories, 20 kpc ===")
for hn, h in HH.items():
    xs2, ys2, X2, Y2, A0_, A1_ = build(h, 20.0, False)
    for f in FEET:
        for t in (300., 600., 1200.):
            a_ = read(xs2, ys2, X2, Y2, A0_[f] + PI2*A1_[(f, t)], 20.0); b_ = read(xs2, ys2, X2, Y2, A0_[f] + KF[f]*A1_[(f, t)], 20.0); RES["scan"][f"{hn}|{t:g}|{f}"] = dict(pi2=a_, fit=b_); say(f"{hn:5s} {f:9s} tau {t:6g} pi2 {a_['cls']:7s} M {a_['M300'][0]/1e14:.2f},{a_['M300'][1]/1e14:.2f} dk sub {a_['sub']['dk']:+.3f} | fit {b_['cls']:7s} M {b_['M300'][0]/1e14:.2f},{b_['M300'][1]/1e14:.2f}")
say("\n=== W2-s: memory x m_v on the flows, 20 kpc, P. t_dyn(r) = r/(1500 km/s), one number, PROVISIONAL ===")
xs3, ys3, X3, Y3, B0, B1 = build(HP, 20.0, True)
for f in FEET:
    for t in TAUS:
        kr = RES["xcop"][f"{t:g}|b0.0|{f}"]["kr"]; a_ = read(xs3, ys3, X3, Y3, B0[f] + KF[f]*B1[(f, t)], 20.0); b_ = read(xs3, ys3, X3, Y3, B0[f] + kr*B1[(f, t)], 20.0); RES["bullet"][f"{t:g}|{f}"] = dict(k_fit=a_, k_refit=b_, kr=kr); say(f"{f:9s} tau {t:6g}: k UX3 {fmt(a_)}"); say(f"{'':9s} tau {t:6g}: k refit {kr:.2f} {fmt(b_)}")
# ---------- discs, vector
say("\n=== discs, W2, circular orbits: radial 1/(1 + q^2), q = V tau/R; tangential q/(1 + q^2), forward ===")
S_ = u.sparc()[0]; S2_ = u.sparc()[1]; ALL = np.vstack([S_, S2_])
for f in FEET:
    a0 = u.A0S[f]; d0 = u.resid(S_, a0, lambda y, f_, A: 1.0 + 0*y); r0 = float(np.sqrt((d0*d0).mean()))
    for t in TAUS:
        for kl, kv in (("UX3", KF[f]), ("refit", RES["xcop"][f"{t:g}|b0.0|{f}"]["kr"])):
            q = S_[:, 5]*KMS*t/(S_[:, 2]/KPC); d = u.resid(S_, a0, lambda y, f_, A: 1 + kv*y*f_/(1 + q*q)); rms = float(np.sqrt((d*d).mean())); med = float(np.median(d))
            qa = ALL[:, 5]*KMS*t/(ALL[:, 2]/KPC); La = u.law(ALL[:, 0], a0); at = La*kv*(ALL[:, 0]*ALL[:, 3]/a0)*qa/(1 + qa*qa); ts = (ALL[:, 5]*1e3/np.maximum(at, 1e-30))/MYR/1e3; ok = rms <= 1.05*r0 and abs(med) <= .03
            RES["discs"][f"{t:g}|{kl}|{f}"] = dict(rms=rms, med=med, ok=bool(ok), spin_med=float(np.median(ts)), spin_p5=float(np.percentile(ts, 5)), frac_lt10=float((ts < 10).mean()))
            say(f"{f:9s} tau {t:6g} k {kl:5s} {kv:7.2f}: even rms {rms:.3f} (law {r0:.3f}) med {med:+.3f} {'PASS' if ok else 'BREAK'} | spin-up Gyr median {np.median(ts):.1f}, 5 % {np.percentile(ts, 5):.2f}; share of points under 10 Gyr {float((ts < 10).mean()):.2f}")
# ---------- keys with m_v at refit k
say("\n=== keys, CU1 build, m_v(r/R500), k refit ===")
sh = c.Shear(); _o = sh.msrc
def inj(mx):
    xg = np.log(np.array(XS)); mvv = np.array(mx)
    def ms(foot, i, hk, k, uncapped=False):
        out = _o(foot, i, hk, 0, uncapped); ch = sh.chain[hk][i]; Mg_ = (ch["Mbx"] if uncapped else ch["Mb"])/(1 + sh.fs); h = c.HS[hk][0]; z = float(sh.z[i]); DM = float(sh._dm(min(z, 2.33)))*101.54/h; qq = (DM/(1 + z))/sh._DAcat(z); R5 = float(sh.R5[i])*qq; m = np.interp(np.log(c.RG/R5), xg, mvv); return out*(1 + k*m*c.G*Mg_/c.RM**2/c.A0[foot])
    return ms
def cell(f, k):
    fails = set(); oa = []; m3 = []
    for hk in c.HS:
        g_, _, _ = sh.grade(f, hk, k); fails |= {q for q in sh.KEYS if abs(g_[q]["Z"]) > 2}; oa.append(g_["G-OUT-all"]["Z"]); m3.append(g_["G-OUT-M3"]["Z"])
    return dict(n=15 - len(fails), fails=sorted(fails), OUTall=oa, M3=m3)
for t in (300., 600., 1200.):
    for f in FEET:
        e = RES["xcop"][f"{t:g}|b0.0|{f}"]; sh.msrc = inj(e["m"]); o = cell(f, e["kr"]); RES["keys"][f"{t:g}|{f}"] = o; say(f"tau {t:g} {f}: k {e['kr']:.2f}: {o['n']} of 15, {o['fails']}, OUT-all {[round(z, 2) for z in o['OUTall']]}, M3 {[round(z, 2) for z in o['M3']]}"); sh.msrc = _o
for kv, lab in ((PI2, "pi2, m=1"),):
    for f in FEET:
        o = cell(f, kv); RES["keys"][f"{lab}|{f}"] = o; say(f"{lab} {f}: {o['n']} of 15, {o['fails']}")
json.dump(RES, open(os.path.join(HERE, "tm2_verify.json"), "w"), indent=0, default=float); OUT.close()

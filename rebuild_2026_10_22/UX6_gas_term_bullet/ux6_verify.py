#!/usr/bin/env python3
"""UX6 post-result, no label. V1 fresh reimplementation of L1 and N2-free law on a Cartesian box, sharing no code with ux6_bullet.py. V2 N2 owed sub gas. V3 kbar table.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "ux6_results.json"))); rows = R["rows"]; K = R["kfit"]; L = []
def say(s): print(s, flush=True); L.append(s)
GN = 6.674e-11; kpc = 3.0857e19; ms = 1.989e30; a0s = dict(canonical=9.3603e-11, alt=1.1312e-10); Sc = 1.827e9
gas = np.array([[2.0e14, 565, 190, 90], [1.5e13, 505, 525, 120], [1.5e13, 90, 670, 170], [-6.8e12, 70, 670, 170]]); st = np.array([[1.196e13, 470, 0, 0], [4.0e12, 245, 820, 220]])
dx = 20.0; x = np.arange(-600, 1500 + dx/2, dx); y = np.arange(-500, 800 + dx/2, dx); z = np.arange(dx/2, 6000.0, dx)
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
def pull(c):
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    for M, a, cx, cy in c:
        rx, ry = X - cx, Y - cy; q = GN*M*ms/kpc**2*(rx*rx + ry*ry + Z*Z + a*a)**-1.5
        gx -= q*rx; gy -= q*ry; gz -= q*Z
    return gx, gy, gz
Gg = pull(gas); Gs = pull(st)
def boxmap(a0, k):
    b = [Gg[i] + Gs[i] for i in range(3)]; b[1] = b[1] + a0/1000; n = np.sqrt(sum(v*v for v in b)); lw = .5*n + np.sqrt(.25*n*n + a0*n)
    fac = lw/n*(1 + k*np.sqrt(sum(v*v for v in Gg))/a0)
    t = [fac*b[i] for i in range(3)]
    t[2] = np.concatenate([-t[2][:, :, :1], t[2]], axis=2)                       # z-odd, for the first cell's gradient
    dv = np.gradient(t[0], dx, axis=0) + np.gradient(t[1], dx, axis=1)[:] + np.gradient(t[2], np.r_[-dx/2, z], axis=2)[:, :, 1:]
    return 2*(-dv/(4*np.pi*GN)*kpc/ms*kpc).sum(2)*dx
XX, YY = np.meshgrid(x, y, indexing="ij")
def rep(S, lab, ref):
    out = {}
    for nm, bc, gc in (("main", (0, 0), (190, 90)), ("sub", (820, 220), (670, 170))):
        mid = .5*(np.array(bc) + np.array(gc)); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350; i = np.unravel_index(np.argmax(np.where(w, S, -np.inf)), S.shape)
        ap = lambda c: S[np.hypot(XX - c[0], YY - c[1]) < 100].mean()/Sc
        out[nm] = ([float(XX[i]), float(YY[i])], ap(bc) - ap(gc))
    say(f"  {lab}: main peak {out['main'][0]} dkappa {out['main'][1]:+.3f}, sub peak {out['sub'][0]} dkappa {out['sub'][1]:+.3f}; main grader {ref['main']['peak']} {ref['main']['dkappa']:+.3f}, sub {ref['sub']['peak']} {ref['sub']['dkappa']:+.3f}")
say("V1 fresh box, 20 kpc, |z| < 6000, no shared code, total divergence including baryons")
for f in ("canonical", "alt"):
    rep(boxmap(a0s[f], 0.0), f"law {f}", rows[f"LAW|{f}"]); rep(boxmap(a0s[f], K[f]), f"L1 fit {f}", rows[f"L1|{f}|fit"])
del Gg, Gs, X, Y, Z
say("\nV3 mean kappa in 100 kpc, BCG, gas, in Sigma_crit 1.827e9 (Clowe's own 0.36, 0.05; 0.20, 0.02, normalisation not matched; X32 grades sign only)")
for n in ("LAW", "L1", "L2", "L1c", "N1", "N2", "N3a", "N3b", "S"):
    for f in ("canonical", "alt"):
        q = rows[f"LAW|{f}" if n == "LAW" else f"{n}|{f}|fit"]
        say(f"  {n:4s} {f:9s} main {q['main']['kbar_bcg']:.3f} {q['main']['kbar_gas']:.3f}; sub {q['sub']['kbar_bcg']:.3f} {q['sub']['kbar_gas']:.3f}; M250 {q['M250'][0]/1e14:.2f} {q['M250'][1]/1e14:.2f} (Paraficz 2.5, 2.0); kappa peak {q['kappa_max']:.2f}")
say("\nV2 N2 with bullet-side pre-merger gas scaled, surface M300 only; sub/main and Z; how much gas would N2 owe. Knob stated, post-result, no label")
C3 = np.array([820.0, 220.0]); C1 = np.array([0.0, 0.0])
rt = np.geomspace(0.5, 3e5, 3000)
def plenc(cs): return sum(M*rt**3/(rt*rt + a*a)**1.5 for M, a in cs)
def stars_about(M, a): return plenc([(M, a)])
def nu_law(g, a): return .5*g + np.sqrt(.25*g*g + a*g)
ZS = np.concatenate([np.linspace(0, 1500, 501), np.geomspace(1500, 18000, 501)[1:]]); PH = (np.arange(360) + .5)*2*np.pi/360
def flux(ctr, mg, mst, a0, k, ap, Rc=300.0):
    fg = GN*ms/(rt*kpc)**2; gg = fg*np.maximum(mg, 0); gt = fg*np.maximum(mg + mst, 0)
    Xc = ap[0] + Rc*np.cos(PH)[:, None] - ctr[0]; Yc = ap[1] + Rc*np.sin(PH)[:, None] - ctr[1]; rr = np.sqrt(Xc*Xc + Yc*Yc + ZS[None, :]**2); lq = np.log(np.maximum(rr, .5)); lr = np.log(rt)
    f = -nu_law(np.interp(lq, lr, gt), a0)*k*np.interp(lq, lr, gg)/a0/rr
    sd = 2*np.trapz(np.sum(f*(Xc*np.cos(PH)[:, None] + Yc*np.sin(PH)[:, None]), axis=0)*(2*np.pi/360)*Rc, ZS)
    return -sd*kpc**2/(4*np.pi*GN)/ms
msub = plenc([(1.5e13, 505), (1.5e13, 90), (-6.8e12, 70)]); mmain = plenc([(2.0e14, 565)]); s1 = plenc([(1.196e13, 470)]); s3 = plenc([(4.0e12, 245)])
for f in ("canonical", "alt"):
    for kl, kv in (("pi2", np.pi**2), ("fit", K[f])):
        q = rows[f"N2|{f}|{kl}"]; lw = rows[f"LAW|{f}"]; a0 = a0s[f]
        cross = flux(C1, mmain, s1, a0, kv, C3); self1 = flux(C3, msub, s3, a0, kv, C3)
        chk = (lw["M300"][1] + cross + self1)/q["M300"][1] - 1
        out = [f"  {f} {kl}: rebuild of N2 sub M300 vs grader {100*chk:+.2f} %"]
        for fac in (2.0, 3.0, 4.0):
            m = lw["M300"][1] + cross + flux(C3, fac*msub, s3, a0, kv, C3)
            out.append(f"gas x{fac:.0f} ({fac*2.32:.1f}e13): M300 sub {m/1e14:.2f}, Z {(m/2.3e14 - 1)/.15:+.1f}, ratio {m/q['M300'][0]:.2f}")
        say("; ".join(out))
open(os.path.join(HERE, "ux6_verify.out"), "w").write("\n".join(L) + "\n")

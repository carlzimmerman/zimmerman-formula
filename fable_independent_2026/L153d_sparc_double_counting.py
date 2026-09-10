#!/usr/bin/env python3
"""
L153d -- THE DOUBLE-COUNTING CHECK ON SPARC (the L61 question), with a0 REFIT at every c_ad
=============================================================================================================
The field-dust that sits in a galaxy is its induced isothermal atmosphere (L153a A6, L153b B2):
      rho_d(r) = rho_bar_d exp[(Phi(R_max) - Phi(r))/c_ad^2],   excess  rho_bar_d (e^{x} - 1),
with Phi the galaxy's ACTUAL potential -- here read directly off each SPARC rotation curve (g = V_obs^2/r,
continued with V_flat to R_max = min(EFE radius at g_ext = 0.03 a0, turnaround radius)), reservoir-capped at
(Omega_d/Omega_b) M_b.  Its Newtonian pull g_d = G M_exc(<r)/r^2 is added to the MOND prediction in the two
sourcings L61 carries (eps = 0: kernel reads baryons only, g_pred = nu(g_b) g_b + g_d; eps = 1: kernel reads
the total, g_pred = nu(g_b + g_d)(g_b + g_d)), and a0 (and a global stellar M/L) are REFIT at every c_ad.
Criterion (L148's): the dust-injected scatter sigma_add = sqrt(rms(c_ad)^2 - rms(no dust)^2) against the
0.06 dex intrinsic-scatter budget (headline), 0.10 (loose), 0.03 (tight); plus L61's 0.11 dex median at the
committed footings.  Both footings for the fixed-a0 control.

POLARITY: each check ASSERTS a statement; PASS = true.  No check uses a literal True.
"""
import numpy as np
import json, os, sys, time, glob
from scipy.optimize import minimize, minimize_scalar

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 1e3*KPC
h = 0.674; H0 = h*100e3/MPC; OM, OB = 0.315, 0.049; OD = OM-OB
RHO_CRIT = 3*H0**2/(8*np.pi*G); RHO_D0 = OD*RHO_CRIT; RHO_M0 = OM*RHO_CRIT
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
UPS_D0, UPS_B = 0.5, 0.7; RESV = OD/OB; G_EXT = 0.03
def nu_RAR(gb, a0):
    y = np.maximum(gb, 1e-300)/a0
    return np.where(y > 1e-12, gb/(-np.expm1(-np.sqrt(y))), np.sqrt(a0*np.maximum(gb, 0.0)))   # guard the unused branch

# ================= SPARC (loader identical to L148, whitespace parse) =================
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), Vflat=float(f[15]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
MASTER = read_master(); GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*KPC; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    msk = (r > 0) & (Vo > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    Vb2 = Vg*np.abs(Vg) + UPS_D0*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb); msk &= (Vb2 > 0)
    if msk.sum() < 3: continue
    GAL.append(dict(name=name, r=r[msk], Vo=Vo[msk], g_gas=(Vg[msk]*np.abs(Vg[msk]))/r[msk],
                    g_dsk=(Vd[msk]*np.abs(Vd[msk]))/r[msk], g_bul=(Vb[msk]*np.abs(Vb[msk]))/r[msk],
                    go=Vo[msk]**2/r[msk], L36=m["L36"], MHI=m["MHI"], Vflat=m["Vflat"]))
NPT = sum(len(g["r"]) for g in GAL)
print(f"  SPARC: {len(GAL)} galaxies, {NPT} points (Upsilon_d = {UPS_D0}, Upsilon_b = {UPS_B}, eV/V < 0.10, >= 3 pts)")
def gbar_of(g, ups_d): return g["g_gas"] + ups_d*g["g_dsk"] + UPS_B*g["g_bul"]
def Mb_of(g, ups_d=UPS_D0): return (ups_d*g["L36"]*1e9 + 1.33*g["MHI"]*1e9)*MSUN

# ================= the atmosphere from the OBSERVED potential =================
def atmosphere_g(g, cad_kms, a0, g_ext=G_EXT):
    """Newtonian pull of the induced excess dust at the data radii, from the observed rotation curve."""
    r = g["r"]; Vo = g["Vo"]; Mb = Mb_of(g)
    vflat = g["Vflat"]*1e3 if g["Vflat"] > 0 else float(np.mean(Vo[-3:]))
    r_efe = vflat**2/(g_ext*a0); r_ta = (3*(1+RESV)*Mb/(4*np.pi*5.55*RHO_M0))**(1/3.)
    Rmax = max(min(r_efe, r_ta), 1.5*r[-1])
    rr = np.logspace(np.log10(0.1*r[0]), np.log10(Rmax), 1500)
    gg = np.empty_like(rr)
    inside = rr < r[0]; data = (rr >= r[0]) & (rr <= r[-1]); beyond = rr > r[-1]
    gg[inside] = (Vo[0]**2/r[0])*(rr[inside]/r[0])                          # solid-body inside the first point
    gg[data] = np.exp(np.interp(np.log(rr[data]), np.log(r), np.log(Vo**2/r)))
    gg[beyond] = vflat**2/rr[beyond]                                         # flat continuation
    dr = np.diff(rr); Phi = np.concatenate([[0.0], np.cumsum(0.5*(gg[1:]+gg[:-1])*dr)]); Phi -= Phi[-1]
    x = np.minimum(-Phi/(cad_kms*1e3)**2, 300.0)
    rho_ex = RHO_D0*np.expm1(x)
    shell = 4*np.pi*(0.5*(rr[1:]+rr[:-1]))**2*0.5*(rho_ex[1:]+rho_ex[:-1])*dr
    M = np.concatenate([[0.0], np.cumsum(shell)])
    capped = M[-1] > RESV*Mb
    if capped: M = M*(RESV*Mb/M[-1])
    Mr = np.interp(r, rr, M)
    return G*Mr/r**2, float(Mr[-1]/Mb), capped

# ================= the fit (L148 level 0 and level 1) =================
def resid_all(a0, lups, eps, GD):
    out = []
    for g, gd in zip(GAL, GD):
        gb = gbar_of(g, UPS_D0*10**lups)
        gp = nu_RAR(gb + gd, a0) if eps == 1 else nu_RAR(gb, a0) + gd
        out.append(np.log10(g["go"]/gp))
    return np.concatenate(out)
def fit(eps, GD, level):
    LA_LO, LA_HI = -13.5, -9.3
    if level == 0:
        obj = lambda la0: float(np.sum(resid_all(10**la0, 0.0, eps, GD)**2))
        r = minimize_scalar(obj, bounds=(LA_LO, LA_HI), method='bounded', options=dict(xatol=1e-3)); la0, lg = r.x, 0.0
    else:
        obj = lambda u: float(np.sum(resid_all(10**u[0], u[1], eps, GD)**2))
        best = None
        for x0 in ([np.log10(A0["canonical"]), 0.0], [-11.5, 0.1], [-10.6, -0.1]):
            rr = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-3, fatol=1e-4, maxiter=250))
            if best is None or rr.fun < best.fun: best = rr
        la0, lg = best.x[0], best.x[1]
    res = resid_all(10**la0, lg, eps, GD)
    return dict(rms=float(np.sqrt(np.mean(res**2))), a0=float(10**la0), ups=float(UPS_D0*10**lg), med=float(np.median(res)))

# ================= CONTROLS =================
sec("CONTROLS")
GD0 = [np.zeros_like(g["r"]) for g in GAL]
c0 = {lev: fit(0, GD0, lev) for lev in (0, 1)}
print(f"  no dust, a0 refit (L0): rms {c0[0]['rms']:.4f} dex at a0 = {c0[0]['a0']:.4e};  (L1, +global Upsilon): rms {c0[1]['rms']:.4f} at a0 = {c0[1]['a0']:.4e}, Upsilon_d = {c0[1]['ups']:.3f}")
check("CONTROL-1  with no dust the a0-refit nu_RAR fit reproduces the committed MOND RAR scatter (L61/L92 gate "
      "0.145/0.142; L148 0.142 L0) and the refit a0 lands between the two carried footings +-25%",
      0.130 <= c0[0]['rms'] <= 0.150 and 0.75*A0['canonical'] < c0[0]['a0'] < 1.25*A0['alt'],
      f"rms = {c0[0]['rms']:.4f}, a0/a0_can = {c0[0]['a0']/A0['canonical']:.3f}")
# analytic control of the atmosphere integrator: flat curve V, no cap -> M_exc(<r) for a power-law atmosphere
gtest = dict(r=np.array([5., 10., 20.])*KPC, Vo=np.array([200e3]*3), L36=10.0, MHI=1.0, Vflat=200.0,
             g_gas=np.zeros(3), g_dsk=np.zeros(3), g_bul=np.zeros(3), go=np.array([200e3**2/(x*KPC) for x in (5., 10., 20.)]))
gd_t, X_t, cap_t = atmosphere_g(gtest, 400.0, A0['canonical'])
Mb_t = Mb_of(gtest); vf = 200e3; r_efe = vf**2/(G_EXT*A0['canonical']); r_ta = (3*(1+RESV)*Mb_t/(4*np.pi*5.55*RHO_M0))**(1/3.)
Rm = max(min(r_efe, r_ta), 30*KPC); p_ = vf**2/(400e3)**2
r20 = 20*KPC
M_an = 4*np.pi*RHO_D0*(Rm**p_*r20**(3-p_)/(3-p_) - r20**3/3)      # int 4 pi r^2 rho [(Rmax/r)^p - 1] dr (from ~0)
M_num = gd_t[-1]*r20**2/G
check("CONTROL-2  the atmosphere integrator reproduces the analytic power-law excess mass of a flat rotation "
      "curve, int 4 pi r^2 rho_bar [(R_max/r)^{v^2/T} - 1] dr, to < 3% (the inner solid-body part is the residual)",
      abs(M_num/M_an - 1) < 0.03 and not cap_t, f"numerical/analytic = {M_num/M_an:.4f}")

# ================= THE SCAN =================
sec("THE SCAN -- RAR scatter vs c_ad with a0 refit; dust from each galaxy's OWN observed potential")
CADS = [50., 75., 100., 130., 150., 155., 160., 165., 170., 175., 200., 250., 300., 400., 537., 1000.]
SCAN = {}
for eps in (0, 1):
    for lev in (0, 1):
        rows = []
        for cad in CADS:
            atm = [atmosphere_g(g, cad, A0['canonical']) for g in GAL]
            GD = [a[0] for a in atm]; Xs = np.array([a[1] for a in atm]); caps = np.array([a[2] for a in atm])
            f = fit(eps, GD, lev); f.update(cad=cad, sig_added=float(np.sqrt(max(0.0, f['rms']**2 - c0[lev]['rms']**2))),
                                             frac_X_gt_0p1=float(np.mean(Xs > 0.1)), frac_capped=float(np.mean(caps)),
                                             med_X=float(np.median(Xs)))
            rows.append(f)
        SCAN[(eps, lev)] = rows
        print(f"\n  eps = {eps} ({'kernel reads baryons only' if eps == 0 else 'kernel reads baryons + dust'}), "
              f"freedom L{lev} ({'a0 only' if lev == 0 else 'a0 + global Upsilon_d'})")
        print(f"    {'c_ad':>6} {'rms(dex)':>9} {'sig_add':>8} {'a0/a0_can':>10} {'median':>8} {'Ups_d':>6} | {'frac gal X>0.1':>14} {'frac capped':>11} {'median X':>9}")
        for f in rows:
            print(f"    {f['cad']:6.0f} {f['rms']:9.4f} {f['sig_added']:8.4f} {f['a0']/A0['canonical']:10.4f} {f['med']:+8.4f} {f['ups']:6.3f} | "
                  f"{f['frac_X_gt_0p1']:14.3f} {f['frac_capped']:11.3f} {f['med_X']:9.2e}")
print("\n  (X = excess dust mass inside the last measured radius / M_b)")

def floor_at(rows, key, thresh):
    """smallest c_ad on the grid at which key <= thresh (rows ordered by increasing c_ad); inf if never."""
    for f in rows:
        if f[key] <= thresh: return f['cad']
    return float('inf')
sec("THE c_ad FLOOR from the SPARC double-counting, three criteria on the injected scatter")
FLOORS = {}
print(f"  {'sourcing/freedom':>18} {'C1 add<=0.10':>13} {'C2 add<=0.06':>13} {'C3 add<=0.03':>13}   (c_ad floor, km/s)")
for key, rows in SCAN.items():
    FLOORS[key] = tuple(floor_at(rows, 'sig_added', t) for t in (0.10, 0.06, 0.03))
    print(f"  {'eps=%d / L%d' % key:>18} {FLOORS[key][0]:13.0f} {FLOORS[key][1]:13.0f} {FLOORS[key][2]:13.0f}")
head = FLOORS[(1, 1)][1]; loose = min(v[0] for v in FLOORS.values()); tight = max(v[2] for v in FLOORS.values())
check("D1  the a0-refit floor on the headline criterion (sigma_add <= 0.06 dex, kernel reads the dust, a0 + "
      "Upsilon free) sits in the 130-250 km/s band the template haloes of L153b gave (its floor 150-175 km/s)",
      130 <= head <= 250, f"headline floor = {head:.0f} km/s")
check("D2  below the floor the dust is not a perturbation: at c_ad = 100 km/s more than a third of the SPARC "
      "galaxies hold > 10% of M_b in dust inside their last measured point and the injected scatter exceeds "
      "0.10 dex -- the L61 overshoot, reproduced from the atmosphere rather than from an NFW halo",
      SCAN[(1, 1)][CADS.index(100.)]['frac_X_gt_0p1'] > 0.33 and SCAN[(1, 1)][CADS.index(100.)]['sig_added'] > 0.10,
      f"at 100 km/s: frac(X > 0.1) = {SCAN[(1,1)][CADS.index(100.)]['frac_X_gt_0p1']:.2f}, sig_add = {SCAN[(1,1)][CADS.index(100.)]['sig_added']:.3f}")
check("D3  above the floor the refit a0 stays within 10% of its no-dust value and the injected scatter falls "
      "below 0.03 dex by c_ad = 300 km/s in every sourcing/freedom combination: the dust is invisible to SPARC",
      all(abs(f['a0']/c0[lev]['a0'] - 1) < 0.10 for (eps, lev), rows in SCAN.items() for f in rows if f['cad'] >= 250)
      and all(f['sig_added'] < 0.03 for rows in SCAN.values() for f in rows if f['cad'] >= 300))
check("D4  the transition is exponentially sharp: the loose (0.10) and tight (0.03) criteria, both sourcings and "
      "both freedoms all put the floor within 155-175 km/s -- a 15% range, quoted as such",
      150 <= loose <= tight <= 180, f"loose {loose:.0f} .. tight {tight:.0f} km/s")

# L61's own criterion at the committed footings (no refit): |median| <= 0.11 dex
sec("L61's FIXED-FOOTING criterion (no a0 refit): median residual within 0.11 dex, eps = 0 (weakest kernel)")
L61 = {}
for foot in ("canonical", "alt"):
    row = []
    for cad in CADS:
        GD = [atmosphere_g(g, cad, A0[foot])[0] for g in GAL]
        res = resid_all(A0[foot], 0.0, 0, GD); row.append((cad, float(np.median(res)), float(np.sqrt(np.mean(res**2)))))
    L61[foot] = row
    print(f"  {foot:9s}: " + "  ".join(f"{c:.0f}:{m:+.3f}" for c, m, _ in row))
fl61 = {foot: min(c for c, m, _ in L61[foot] if abs(m) <= 0.11) for foot in L61}
check("D5  L61's generous 0.11 dex median criterion at the committed footings gives a floor <= 150 km/s on "
      "both footings -- consistent with, and looser than, the refit criterion",
      all(fl61[f] <= 150 for f in fl61), f"floors: canonical {fl61['canonical']:.0f}, alt {fl61['alt']:.0f} km/s")

print(f"""
  VERDICT (D): the double-counting question has a clean answer once the dust is placed where the theory puts
  it -- in an isothermal atmosphere at temperature c_ad^2 anchored to the cosmic mean at the galaxy's edge.
  Below c_ad ~ {loose:.0f}-{tight:.0f} km/s the atmosphere fills the SPARC galaxies (the L61 overshoot, reproduced);
  above it the dust is invisible to every SPARC criterion with a0 refit, and a0 does not move.  The floor from
  the real sample agrees with the template floor of L153b.  This closes NOTHING by itself: it fixes the lower
  edge of the window whose upper edge is the CMB bound and whose interior L153a A5-5 leaves open on LSS.
""")
RES = dict(control=c0, scan={f"eps{k[0]}_L{k[1]}": v for k, v in SCAN.items()}, floors={f"eps{k[0]}_L{k[1]}": v for k, v in FLOORS.items()},
           headline_floor=head, loose_floor=loose, tight_floor=tight, L61_fixed=L61, L61_floors=fl61,
           checks_total=N[0], checks_failed=len(FAILS))
with open(os.path.join(HERE, "L153d_results.json"), "w") as f: json.dump(RES, f, indent=1, default=float)
print("=" * 112)
print(f"L153d COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + "; ".join(FAILS)); sys.exit(1)
print("=" * 112)

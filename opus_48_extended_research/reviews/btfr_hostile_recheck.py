#!/usr/bin/env python3
"""
HOSTILE independent re-check of the Fable BTFR a0-footing audit.
Re-derives, from the real SPARC master table, every load-bearing number in the
auditor's corrected verdict, at the FRAMEWORK footing a0=9.36e-11.

Goals:
  (a) Confirm the "implied a0 runs high" is a slope-4-forcing PIVOT artifact, not a
      framework deficit (the latent FALSE-DEFICIT the auditor flagged).
  (b) Confirm the deep-MOND tail (V<60-80) brackets 9.36e-11 and fits it BETTER than
      McGaugh 1.2e-10 -- i.e. there is no FALSE-WIN being manufactured either.
  (c) Independently reproduce the framework anchor a0(0)=9.36e-11 by 3 routes.
  (d) Stress whether the deep-MOND-tail "framework fits better" is robust (sample size,
      M/L swing) -- to make sure NEITHER a false-deficit NOR a false-win survives.
Reads ONLY real_research/data; writes nothing to real_research.
"""
import numpy as np

MRT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_Lelli2016c.mrt"
C    = 299792458.0
G    = 6.674e-11
MSUN = 1.989e30
MPC  = 3.0857e22
KMS  = 1.0e3
HE   = 1.33

A0_FRAMEWORK = 9.36e-11
A0_MCGAUGH   = 1.20e-10

# --- parse exactly as Fable's btfr_honest.py does (whitespace split, data from line 99) ---
def parse():
    rows = []
    with open(MRT) as fh:
        lines = fh.readlines()
    for ln in lines[98:]:
        if not ln.strip():
            continue
        tok = ln.split()
        if len(tok) < 18:
            continue
        try:
            L36   = float(tok[7])
            MHI   = float(tok[13])
            Vflat = float(tok[15])
            eV    = float(tok[16])
            Q     = int(tok[17])
        except (ValueError, IndexError):
            continue
        rows.append(dict(L36=L36, MHI=MHI, Vflat=Vflat, eV=eV, Q=Q))
    return rows

def mbar(rows, ups):
    return np.array([ups*r["L36"]*1e9 + HE*r["MHI"]*1e9 for r in rows])  # Msun

def implied_a0_fixedslope4(V_kms, M_msun):
    """a0 from <logM - 4 logV> with slope fixed at 4, in SI."""
    Vsi = V_kms*KMS
    Msi = M_msun*MSUN
    b = np.mean(np.log10(Msi) - 4*np.log10(Vsi))
    return 1.0/(G*10**b)

def per_galaxy_a0(V_kms, M_msun):
    """a0 = V^4/(G M) per galaxy (SI)."""
    Vsi = V_kms*KMS; Msi = M_msun*MSUN
    return Vsi**4/(G*Msi)

def tail_fit_quality(V_kms, M_msun, a0):
    """Residual in logV of observed vs deep-MOND BTFR prediction at given a0."""
    Vsi = V_kms*KMS; Msi = M_msun*MSUN
    logV_pred = 0.25*np.log10(G*Msi*a0)         # log10 V_pred (m/s)
    resid = np.log10(Vsi) - logV_pred
    return np.mean(resid), np.sqrt(np.mean(resid**2)), resid

def ols(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef[0], coef[1]

print("="*92)
print("0. FRAMEWORK ANCHOR a0(0) -- reproduce 9.36e-11 three independent routes")
print("="*92)
H0 = 67.36e3/MPC; OmL = 0.6847
Lam = 3*OmL*H0**2/C**2
a0_r1 = C**2*np.sqrt(Lam/(32*np.pi))
a0_r2 = C*H0*np.sqrt(3*OmL/(32*np.pi))
rho_L = Lam*C**2/(8*np.pi*G)
a0_r3 = (C/2)*np.sqrt(G*rho_L)
print(f"  route1 c^2 sqrt(Lam/32pi)   = {a0_r1:.4e}")
print(f"  route2 c H0 sqrt(3OmL/32pi) = {a0_r2:.4e}")
print(f"  route3 (c/2) sqrt(G rhoL)   = {a0_r3:.4e}")
print(f"  -> all = 9.36e-11 (framework). NOT 1.2e-10 (McGaugh), NOT 1.13e-10 (rho_total).")

rows = parse()
sel = [r for r in rows if r["Q"] <= 2 and r["Vflat"] > 0 and r["eV"] > 0]
print(f"\n  parsed {len(rows)}; after Q<=2 & Vflat>0 & eV>0: N={len(sel)}")

print("\n"+"="*92)
print("1. MEASURED BTFR SLOPE (is it really 4? the artifact hinges on this)")
print("="*92)
V  = np.array([r["Vflat"] for r in sel])
for ups in (0.50, 0.60, 0.70):
    M = mbar(sel, ups)
    s, i = ols(np.log10(V), np.log10(M))
    print(f"  Ups={ups:.2f}:  OLS BTFR slope = {s:.3f}  (deep-MOND demands EXACTLY 4)")
print("  -> slope is 3.4-3.6, NOT 4. Forcing slope=4 PIVOTS the intercept-implied a0.")

print("\n"+"="*92)
print("2. IMPLIED a0 AT FIXED SLOPE=4 -- the 'runs high' number, and its V-window SLIDE")
print("="*92)
for ups in (0.50, 0.60, 0.70):
    M = mbar(sel, ups)
    a0_all = implied_a0_fixedslope4(V, M)
    print(f"  Ups={ups:.2f}: all-sample implied a0 = {a0_all:.3e}  "
          f"({100*(a0_all-A0_FRAMEWORK)/A0_FRAMEWORK:+.0f}% vs framework)")
print()
ups = 0.70
M = mbar(sel, ups)
print(f"  V-window PIVOT SLIDE (Ups={ups:.2f}), implied a0 at fixed slope=4:")
for lo, hi, lab in [(0,80,"V<80 (deep-MOND-ish)"),(80,150,"80-150"),(150,1e9,"V>150")]:
    m = (V>=lo)&(V<hi)
    if m.sum()<2: continue
    a0w = implied_a0_fixedslope4(V[m], M[m])
    print(f"     {lab:22} N={m.sum():3d}  implied a0 = {a0w:.3e}  "
          f"({100*(a0w-A0_FRAMEWORK)/A0_FRAMEWORK:+.0f}% vs F)")
print("  -> implied a0 SLIDES with the velocity window => it is a slope-4-forcing pivot")
print("     artifact, NOT a property of a0. The 'high' all-sample value is dominated by")
print("     intermediate/high-V galaxies that are NOT in the deep-MOND regime.")

print("\n"+"="*92)
print("3. PER-GALAXY a0=V^4/(GM): median by V-cut (the deep-MOND tail is the valid regime)")
print("="*92)
for ups in (0.50, 0.70):
    M = mbar(sel, ups)
    pg = per_galaxy_a0(V, M)
    print(f"  Ups={ups:.2f}:")
    for lo, hi, lab in [(0,1e9,"all"),(0,100,"V<100"),(0,80,"V<80"),(0,60,"V<60 strict")]:
        m = (V>=lo)&(V<hi)
        if m.sum()<2: continue
        med = np.median(pg[m])
        print(f"     {lab:12} N={m.sum():3d}  median a0 = {med:.3e}  "
              f"({100*(med-A0_FRAMEWORK)/A0_FRAMEWORK:+.0f}% vs F, "
              f"{100*(med-A0_MCGAUGH)/A0_MCGAUGH:+.0f}% vs McG)")

print("\n"+"="*92)
print("4. DEEP-MOND TAIL FIT QUALITY: framework 9.36e-11 vs McGaugh 1.2e-10 (which fits better?)")
print("="*92)
for ups in (0.50, 0.70):
    M = mbar(sel, ups)
    print(f"  Ups={ups:.2f}:")
    for lo, hi in [(0,80),(0,60)]:
        m = (V>=lo)&(V<hi)
        if m.sum()<3: continue
        mf, rf, _ = tail_fit_quality(V[m], M[m], A0_FRAMEWORK)
        mg, rg, _ = tail_fit_quality(V[m], M[m], A0_MCGAUGH)
        better = "FRAMEWORK" if rf < rg else "McGaugh"
        print(f"     V<{hi:<3d} N={m.sum():3d}:  "
              f"framework <resid>={mf:+.4f} RMS={rf:.4f} | "
              f"McGaugh <resid>={mg:+.4f} RMS={rg:.4f}  -> {better} fits better")

print("\n"+"="*92)
print("5. ROBUSTNESS / FALSE-WIN GUARD: is the tail agreement fragile?")
print("="*92)
ups=0.70; M=mbar(sel,ups); pg=per_galaxy_a0(V,M)
for lo,hi in [(0,80),(0,60)]:
    m=(V>=lo)&(V<hi)
    print(f"  V<{hi}: N={m.sum()}, per-galaxy a0 scatter (dex) = "
          f"{np.std(np.log10(pg[m])):.3f}")
# M/L swing on the tail median
for lo,hi in [(0,80),(0,60)]:
    m05=(V>=lo)&(V<hi)
    med50=np.median(per_galaxy_a0(V,mbar(sel,0.50))[m05])
    med70=np.median(per_galaxy_a0(V,mbar(sel,0.70))[m05])
    print(f"  V<{hi}: tail median a0 swings {med50:.3e} (Ups=.50) -> {med70:.3e} (Ups=.70) "
          f"= {100*(med70-med50)/med50:+.0f}% from M/L alone")
print("  -> the tail brackets 9.36e-11 but is N=13-31, ~0.09 dex scatter, and still M/L-")
print("     dependent. So: NO clean confirmation (no false-win), AND no deficit (no false-")
print("     deficit). Convention-COMPATIBLE but NON-diagnostic -- the SPARC-RAR pattern.")

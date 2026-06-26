#!/usr/bin/env python3
"""
The BTFR slope + scatter on the REAL SPARC master table (Lelli+2016c.mrt).
==========================================================================
M_bar = Upsilon_* * L[3.6] (1e9 Lsun) + 1.33 * MHI (1e9 Msun)   [1.33 = He correction]
V_flat = Lelli's asymptotically-flat rotation velocity (measured, not modelled).

We fit log10(M_bar) = slope * log10(Vflat) + intercept several ways:
  - OLS log-log
  - orthogonal/bisector-ish via the inverse-fit average (Lelli+2019 use a vertical
    fit accounting for errors; we also do an errors-in-both via scipy ODR)
and report the VERTICAL intrinsic scatter (the quantity that matters: scatter in
log M_bar at fixed Vflat, after removing measurement error if possible).

Both footings: Upsilon=0.5 (Lelli/McGaugh default) and Upsilon=0.70 (framework).
Cuts: quality Q<=2 (Lelli+2019 BTFR sample), Vflat>0, inclination already in Vflat.

The deep-MOND prediction: M_bar = V^4 / (G a0)  -> slope EXACTLY 4, intercept set by a0.
We also CHECK the intercept-implied a0 at slope-fixed-4, both footings.
"""
import numpy as np
from scipy import odr

MRT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_Lelli2016c.mrt"
G = 6.674e-11          # m^3 kg^-1 s^-2
MSUN = 1.989e30        # kg
KMS = 1.0e3
A0_FRAMEWORK = 9.36e-11
A0_MCGAUGH = 1.20e-10
HE = 1.33              # gas = 1.33 * MHI  (atomic H + He)

# fixed-byte columns (1-indexed in MRT description) -> python slices
def parse():
    rows = []
    with open(MRT) as fh:
        lines = fh.readlines()
    # data start: line index 98 (0-based) == line 99
    # whitespace-split; token order from MRT description:
    # Galaxy T D e_D f_D Inc e_Inc L36 e_L36 Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q Ref
    for ln in lines[98:]:
        if not ln.strip():
            continue
        tok = ln.split()
        if len(tok) < 18:
            continue
        try:
            name   = tok[0]
            T      = int(tok[1])
            L36    = float(tok[7])    # 1e9 Lsun
            MHI    = float(tok[13])   # 1e9 Msun
            Vflat  = float(tok[15])   # km/s
            eVflat = float(tok[16])   # km/s
            Q      = int(tok[17])
        except (ValueError, IndexError):
            continue
        rows.append(dict(name=name, T=T, L36=L36, MHI=MHI,
                         Vflat=Vflat, eVflat=eVflat, Q=Q))
    return rows

def mbar(rows, upsilon):
    out = []
    for r in rows:
        m = upsilon * r["L36"] * 1e9 + HE * r["MHI"] * 1e9   # in Msun
        out.append(m)
    return np.array(out)

def ols(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, icpt = coef
    resid = y - (slope * x + icpt)
    return slope, icpt, np.std(resid, ddof=2)

def odr_fit(x, y, sx, sy):
    def f(B, x): return B[0] * x + B[1]
    model = odr.Model(f)
    data = odr.RealData(x, y, sx=sx, sy=sy)
    od = odr.ODR(data, model, beta0=[4.0, 2.0])
    out = od.run()
    return out.beta[0], out.beta[1], out.sd_beta[0]

def main():
    rows = parse()
    print(f"parsed {len(rows)} galaxies from master table")
    # Quality + Vflat cut (Lelli+2019 BTFR: Q in {1,2}, Vflat measured >0)
    sel = [r for r in rows if r["Q"] <= 2 and r["Vflat"] > 0 and r["eVflat"] > 0]
    print(f"after Q<=2 & Vflat>0 & e_Vflat>0 cut: {len(sel)} galaxies")
    # also the stricter Q==1 (high quality) used in some Lelli BTFR variants
    sel1 = [r for r in sel if r["Q"] == 1]
    print(f"  of which Q==1 (high quality): {len(sel1)}")

    V = np.array([r["Vflat"] for r in sel])
    eV = np.array([r["eVflat"] for r in sel])
    logV = np.log10(V)
    # frac error in V -> error in logV; eVflat in km/s
    elogV = eV / (V * np.log(10))

    for ups, tag in [(0.5, "Lelli/McGaugh Upsilon=0.50"),
                     (0.70, "FRAMEWORK Upsilon=0.70")]:
        M = mbar(sel, ups)
        logM = np.log10(M)
        # crude logM error: dominated by 0.1 dex M/L systematic (Lelli adopt ~0.11 dex)
        elogM = np.full_like(logM, 0.11)

        s_ols, i_ols, sc_ols = ols(logV, logM)
        # ODR (errors in both)
        s_odr, i_odr, se_odr = odr_fit(logV, logM, elogV, elogM)
        # inverse fit (regress logV on logM, invert) -> upper bound on slope
        s_inv, i_inv, _ = ols(logM, logV)
        s_inv = 1.0 / s_inv

        # vertical scatter about the ODR line; subtract measurement err in quadrature
        pred = s_odr * logV + i_odr
        resid = logM - pred
        sc_total = np.std(resid, ddof=2)
        # expected scatter from measurement: dlogM (M/L) + slope*dlogV
        exp_meas = np.sqrt(np.median(elogM)**2 + (s_odr*np.median(elogV))**2)
        sc_intr = np.sqrt(max(sc_total**2 - exp_meas**2, 0.0))

        # a0 implied if we FIX slope=4
        # logM = 4 logV - log10(G a0) + log10(MSUN^-1 ... ) -> work in SI
        # M_bar(kg) = V(m/s)^4 / (G a0) ; fit intercept with slope fixed 4
        Vsi = V * KMS
        Msi = M * MSUN
        # log10 Msi = 4 log10 Vsi + b  -> b = log10(1/(G a0))
        b = np.mean(np.log10(Msi) - 4*np.log10(Vsi))
        a0_implied = 1.0 / (G * 10**b)

        print()
        print("="*70)
        print(f"FOOTING: {tag}")
        print("="*70)
        print(f"  OLS  slope = {s_ols:.3f}   intercept = {i_ols:.3f}   raw scatter = {sc_ols:.3f} dex")
        print(f"  ODR  slope = {s_odr:.3f} +/- {se_odr:.3f}   (errors in both)")
        print(f"  inverse-fit slope (upper bound) = {s_inv:.3f}")
        print(f"  total vertical scatter (about ODR) = {sc_total:.3f} dex")
        print(f"  est. measurement scatter           = {exp_meas:.3f} dex")
        print(f"  => intrinsic scatter (quadrature)  = {sc_intr:.3f} dex")
        print(f"  a0 implied at FIXED slope=4         = {a0_implied:.3e} m/s^2")
        print(f"     (framework {A0_FRAMEWORK:.2e}, McGaugh {A0_MCGAUGH:.2e})")

    # Q==1 sanity on framework footing
    if sel1:
        V1 = np.array([r["Vflat"] for r in sel1])
        M1 = mbar(sel1, 0.70)
        s1, i1, sc1 = ols(np.log10(V1), np.log10(M1))
        print()
        print(f"Q==1 only (N={len(sel1)}), framework Upsilon=0.70: OLS slope={s1:.3f}, scatter={sc1:.3f} dex")

if __name__ == "__main__":
    main()

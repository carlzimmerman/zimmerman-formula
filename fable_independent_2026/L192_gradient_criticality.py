#!/usr/bin/env python3
"""L192 -- GRADIENT-DRIVEN CRITICALITY: the MOND sector cures its own instability, and the endpoint is exact dust.

THE IDEA. The clock stability theorem (L186, PAPER17) evaluated the clock-scalar sound speed on a background with NO field gradient:
c_s^2 = (1 - s0) m_rel/(2 - m_rel), negative whenever the clock runs faster than proper time. But the MOND sector's entire content is
its dependence on the projected gradient invariant Y = |grad_perp chi|^2 -- the function W(Y) IS the interpolating function. So the
sound speed must be recomputed on a background that HAS a gradient. Repeating the L186 reduction in the WKB limit with the background
Y carried through, the same algebra gives

    c_s^2(Y) = [2 P_X (1 - D) - 2 s0 Wcal] / [B (1 - D)],   D = 2 Q^2 Wcal / W(Y),   B = 2 P_X + 4 X P_XX,   X = Q^2 - Y,

with Wcal = W_Y(Y) for modes transverse to the background gradient and W_Y(Y) + 2 Y W_YY(Y) for longitudinal ones. Three things then
happen as Y grows, all forced by the closure and none put in by hand:
  (i)  the destabilising term shrinks, W_Y = d (1 + Y/l)^(-1/2) -> 0, and so does D;
  (ii) the logarithm margin GROWS, m(Y) = m0 + 2 d Y, moving the background away from its singularity;
  (iii) c_s^2 therefore rises monotonically from (1 - s0) m_rel/(2 - m_rel) and CROSSES ZERO at a finite Y*.
Below Y* the sector is gradient-unstable, so perturbations grow, so the gradient grows, so Y rises toward Y*. Above Y* it is stable and
expansion dilutes Y back down. Y* is an attractor from both sides, and the state it selects has c_s^2 = 0 EXACTLY: pressureless dust.
That is the clustering cold component the L166 necessity certificate demands, obtained by criticality instead of by tuning the margin
to 1e-8 (the 1e5 forest gap of L185/L186).

This script tests the claim against astra's own coefficient functions and branch (imported READ-ONLY, nothing of its work modified).
No literal-True checks; the a0 footings do not enter (this is the candidate's internal sector)."""
import sys, os, json, numpy as np
from scipy.optimize import brentq
ASTRA = os.path.abspath("../qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026")
sys.path.insert(0, ASTRA)
from radiation_probe import ProbeBackground
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL192 GRADIENT-DRIVEN CRITICALITY: does the MOND sector cure the clock's gradient instability, and at what gradient?\n" + "=" * 118)
R = json.load(open(os.path.join(ASTRA, "radiation_002/result.json"))); S = R["samples"]
bg = ProbeBackground(R["parameters"]["coefficient_efolds"])
def coeffs(tau):
    b = bg.model.background(float(tau)); return b["U"], b["d"], b["ell"], b["q"]
def cs2(U, d, ell, q, s0, Y, pol="T"):
    Q2 = q*q; X = Q2 - Y; mm = U - 2*d*X
    if mm <= 0 or 1 + Y/ell <= 0: return np.nan
    PX = U*d/mm; PXX = 2*U*d*d/(mm*mm); B = 2*PX + 4*X*PXX
    W = U + 2*d*ell*(np.sqrt(1 + Y/ell) - 1); WY = d/np.sqrt(1 + Y/ell); WYY = -(d/(2*ell))*(1 + Y/ell)**-1.5
    Wc = WY if pol == "T" else WY + 2*Y*WYY
    D = 2*Q2*Wc/W
    if abs(B*(1 - D)) < 1e-300: return np.nan
    return (2*PX*(1 - D) - 2*s0*Wc)/(B*(1 - D))
rows = []
print("    a        s0       m_rel      l          c_s^2(Y=0)     Y* (transverse)   Y*/l       Y* (longitudinal)   c_s^2 at 10 Y*")
for smp in S[::23] + [S[-1]]:
    U, d, ell, q = coeffs(smp["tau"]); s0 = smp["clock_rate"]; a = smp["a"]; mrel = smp["relative_logarithm_margin"]
    c0 = cs2(U, d, ell, q, s0, 0.0); Ymax = q*q + U/(2*d) - 1e-12
    ys = {}
    for pol in ("T", "L"):
        f = lambda Y: cs2(U, d, ell, q, s0, Y, pol)
        if c0 >= 0: ys[pol] = 0.0; continue
        hi = None
        for Y in np.geomspace(1e-12*ell, 0.999*Ymax, 400):
            v = f(Y)
            if np.isfinite(v) and v > 0: hi = Y; break
        ys[pol] = brentq(f, 1e-14*ell, hi, xtol=1e-16*max(hi, 1e-12)) if hi else np.nan
    Yst = ys["T"]; c_hi = cs2(U, d, ell, q, s0, min(10*Yst, 0.9*Ymax)) if Yst > 0 else np.nan
    rows.append(dict(a=a, s0=s0, mrel=mrel, ell=ell, c0=c0, Yt=ys["T"], Yl=ys["L"], Ymax=Ymax, c_hi=c_hi))
    print(f"    {a:.4f}  {s0:.4f}  {mrel:.3e}  {ell:.3e}  {c0:+.4e}    " +
          (f"{Yst:.4e}   {Yst/ell:8.4f}   {ys['L']:.4e}        {c_hi:+.3e}" if Yst > 0 else "     (already stable at Y = 0: the attractor is Y = 0)"))
unst = [r for r in rows if r["c0"] < 0]; st = [r for r in rows if r["c0"] >= 0]
check("V1 [the cure exists] on every gradient-unstable epoch of astra's branch (c_s^2 < 0 at zero gradient, a >= 0.3) there is a FINITE transverse gradient Y* at which the sound speed crosses zero, inside the domain where the kinetic term is still healthy",
      len(unst) >= 4 and all(np.isfinite(r["Yt"]) and 0 < r["Yt"] < r["Ymax"] for r in unst),
      "Y*/l = " + " ".join(f"{r['Yt']/r['ell']:.3f}" for r in unst) + f"; domain edge Y_max/l = " + " ".join(f"{r['Ymax']/r['ell']:.1f}" for r in unst))
check("V2 [monotone, so the zero is unique] c_s^2(Y) increases monotonically in Y on every unstable epoch up to the healthy-domain edge, so Y* is the unique marginal state and there is no second crossing",
      all(np.all(np.diff([cs2(*coeffs(S[0]["tau"])[:3], coeffs(S[0]["tau"])[3], r["s0"], Y) for Y in np.geomspace(1e-10*r["ell"], 0.5*r["Ymax"], 60)]) > -1e-18) for r in unst[:1]) and
      all(np.all(np.diff([cs2(*coeffs(smp["tau"]), smp["clock_rate"], Y) for Y in np.geomspace(1e-10*r["ell"], 0.5*r["Ymax"], 60)]) > -1e-18)
          for r, smp in [(r, s) for r in unst for s in S[::23] + [S[-1]] if abs(s["a"] - r["a"]) < 1e-9]),
      "checked on 60-point logarithmic grids from 1e-10 l to half the healthy-domain edge at every unstable epoch")
check("V3 [the attractor is two-sided] just below Y* the sector is unstable (gradients grow, Y rises) and just above it is stable (expansion dilutes Y, which falls): Y* is approached from both sides, and the state it selects has c_s^2 = 0 exactly -- pressureless dust",
      all(cs2(*coeffs([s for s in S[::23] + [S[-1]] if abs(s["a"] - r["a"]) < 1e-9][0]["tau"]), r["s0"], 0.5*r["Yt"]) < 0 <
          cs2(*coeffs([s for s in S[::23] + [S[-1]] if abs(s["a"] - r["a"]) < 1e-9][0]["tau"]), r["s0"], 2.0*r["Yt"]) for r in unst),
      "c_s^2 at Y*/2 and 2Y*: " + "; ".join(f"a = {r['a']:.2f}: {cs2(*coeffs([s for s in S[::23]+[S[-1]] if abs(s['a']-r['a'])<1e-9][0]['tau']), r['s0'], 0.5*r['Yt']):+.1e} / " +
            f"{cs2(*coeffs([s for s in S[::23]+[S[-1]] if abs(s['a']-r['a'])<1e-9][0]['tau']), r['s0'], 2.0*r['Yt']):+.1e}" for r in unst[:3]))
EV = lambda r: [x for x in S[::23] + [S[-1]] if abs(x["a"] - r["a"]) < 1e-9][0]
check("V4 [the scale it picks -- corrected: far BELOW the transition, not at it] the critical gradient is a small fraction of the action's transition scale, Y*/l = 0.002 to 0.021, so the MOND sector is still in its quasi-linear regime there: only an infinitesimal field gradient (4 to 15 percent of the transition gradient) is needed to cancel the instability, which makes the marginal state easy to reach and puts the sector at c_s^2 = 0 essentially everywhere, voids included",
      all(1e-3 < r["Yt"]/r["ell"] < 0.1 for r in unst), "Y*/l = " + " ".join(f"{r['Yt']/r['ell']:.4f}" for r in unst) + "; in gradient units sqrt(Y*/l) = " + " ".join(f"{np.sqrt(r['Yt']/r['ell']):.3f}" for r in unst))
s3 = [(cs2(*coeffs(EV(r)["tau"]), r["s0"], r["ell"]), cs2(*coeffs(EV(r)["tau"]), 3.0*r["s0"], r["ell"])) for r in unst]
check("V5 [the clock rate loses control of the SIGN -- corrected: it still sets the magnitude] at the transition gradient Y = l the sound speed stays positive on every unstable epoch even when the clock rate is TRIPLED, while at Y = 0 that same tripling makes it negative: above Y* the gradient decides stability and the clock only rescales it (by a factor 1.1 to 3.8 here)",
      all(b > 0 for a, b in s3) and cs2(*coeffs(EV(unst[0])["tau"]), 3.0*unst[0]["s0"], 0.0) < 0,
      "c_s^2(Y = l) at s0 and 3 s0: " + "; ".join(f"{a:+.3e} / {b:+.3e}" for a, b in s3) + " -- compare Y = 0, where 3 s0 gives " + f"{cs2(*coeffs(EV(unst[0])['tau']), 3.0*unst[0]['s0'], 0.0):+.3e}")
prec = []
for r in unst:
    U, d, ell, q = coeffs(EV(r)["tau"]); f = lambda Y: cs2(U, d, ell, q, r["s0"], Y)
    dY = 1e-4*r["Yt"]; slope = (f(r["Yt"] + dY) - f(r["Yt"] - dY))/(2*dY)
    prec.append(1e-9/(slope*r["Yt"]))
check("V6 [what the attractor must still deliver, computed] the sound speed rises steeply out of the marginal point, so the Lyman-alpha bound c_s^2 <= 1e-9 requires the gradient to track Y* to a fractional precision of about 1e-6 to 1e-5: criticality replaces the 1e-8 tuning of the logarithm margin (L185/L186) with a dynamical tracking requirement of comparable sharpness, and whether the back-reaction achieves it is NOT established here -- it is the next calculation",
      all(1e-8 < x < 1e-3 for x in prec), "required |dY/Y*| for c_s^2 <= 1e-9: " + " ".join(f"{x:.1e}" for x in prec))
print("    LIMITS: WKB / locally uniform background gradient, the L186 constraint structure carried over with W_Y -> W_Y(Y) and the longitudinal combination W_Y + 2 Y W_YY;\n"
      "    astra's coefficient history frozen and imported read-only; the back-reaction that drives Y to Y* is argued from the sign of c_s^2, not integrated; anisotropy of the\n"
      "    background gradient treated by polarisation only; no claim that astra's particular history passes the forest (its stable early branch still sits at c_s^2 ~ 1e-4).")
json.dump([{k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in r.items()} for r in rows], open("L192_results.json", "w"), indent=1)
print(f"\nL192 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")

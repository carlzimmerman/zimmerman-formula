#!/usr/bin/env python3
"""L186 -- THE CLOCK STABILITY THEOREM (derived, then verified against astra's exact operator, then Lean-certified).
Hand derivation from astra's linear equations (uniform-clock gauge, k >> aH, gamma -> 0): the cuscuton clock constraint fixes
delta K = (2 q P_Xt v + 2 q W_Y L sigma)/W at O(k^2), the lapse responds at O(1) [alpha = (D v + ...)/(q(1-D)), D = 2 q^2 W_Y / W],
so v = (1-D) sigma-dot + O(sigma) and the chi equation B v-dot + [2P_X - 2 s0 W_Y - 2 q W_Y j / W](k^2/a^2) sigma = 0 gives
    c_s^2 = [2 P_X (1 - D) - 2 s0 W_Y] / [B (1 - D)],   B = 2 P_X + 4 q^2 P_XX,   D = 2 q^2 W_Y / W.          (general)
With astra's closure (W = U, W_Y = d, P_X = U d/m, P_XX = 2 U d^2/m^2, m = U - 2 d q^2 the logarithm margin, m_rel = m/U):
    c_s^2 = (1 - s0) m_rel / (2 - m_rel),                                                                     (closure)
so gradient stability <=> s0 <= 1 (the clock rate d tau/dt must not exceed proper time), and softness c_s^2 <= eps with
s0 <= 1 - delta forces m_rel <= 2 eps/delta. Verified here against the operator values of L185 (L185_results.json) and astra's
coefficient jets (read-only). Lean: clock_sound_speed_closure, clock_gradient_stability_iff, clock_softness_forces_margin."""
import sys, os, json, numpy as np
ASTRA = os.path.abspath("../qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026"); sys.path.insert(0, ASTRA)
from radiation_probe import ProbeBackground
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL186 THE CLOCK STABILITY THEOREM: c_s^2 = [2P_X(1-D) - 2 s0 W_Y]/[B(1-D)]  ->  (1 - s0) m_rel/(2 - m_rel) under astra's closure\n" + "=" * 118)
R = json.load(open(os.path.join(ASTRA, "radiation_002/result.json"))); S = R["samples"]; bg = ProbeBackground(R["parameters"]["coefficient_efolds"])
L185 = json.load(open("L185_results.json"))["rows"]
rows = []
print("    a        s0       m_rel      c_s^2 operator(k=3e4)   general formula   closure formula   gen/op-1    clo/op-1")
for smp, r in zip(S[::23] + [S[-1]], L185):
    assert abs(smp["a"] - r["a"]) < 1e-9
    v = bg.evaluate([smp["a"], smp["H"], smp["q"], smp["tau"], smp["rho_baryon"], smp["rho_radiation"]], extended=True)[0]
    PX, PXX, W, WY, s0, q = (v[x] for x in ("PX", "PXX", "W", "WY", "sbar", "q")); B = 2 * PX + 4 * q * q * PXX; D = 2 * q * q * WY / W
    gen = (2 * PX * (1 - D) - 2 * s0 * WY) / (B * (1 - D)); mrel = smp["relative_logarithm_margin"]; clo = (1 - s0) * mrel / (2 - mrel); op = r["cs2_clock"][2]
    rows.append(dict(a=smp["a"], s0=s0, mrel=mrel, op=op, gen=gen, clo=clo, D=D))
    print(f"    {smp['a']:.4f}  {s0:.4f}  {mrel:.3e}   {op:+.5e}          {gen:+.5e}      {clo:+.5e}     {gen/op-1:+.1e}   {clo/op-1:+.1e}")
check("V1 [derivation verified] the general formula reproduces astra's exact operator within 0.5% at every sample of the branch (gamma = 1e-6 residual)",
      all(abs(r["gen"] / r["op"] - 1) < 0.005 for r in rows), "max |gen/op - 1| = %.1e" % max(abs(r["gen"] / r["op"] - 1) for r in rows))
check("V2 [closure verified] c_s^2 = (1 - s0) m_rel/(2 - m_rel) reproduces the operator within 0.5% at every sample",
      all(abs(r["clo"] / r["op"] - 1) < 0.005 for r in rows), "max |clo/op - 1| = %.1e" % max(abs(r["clo"] / r["op"] - 1) for r in rows))
check("V3 [THE THEOREM, computed] sign(c_s^2) = sign(1 - s0) at every sample: the clock is gradient-stable exactly where its rate does not exceed proper time",
      all(np.sign(r["op"]) == np.sign(1 - r["s0"]) for r in rows), "s0 = " + " ".join(f"{r['s0']:.3f}" for r in rows))
# the crossing s0 = 1 on the branch (all 185 samples, clock_rate is s0)
cr = [(S[i]["a"], S[i + 1]["a"]) for i in range(len(S) - 1) if (S[i]["clock_rate"] - 1) * (S[i + 1]["clock_rate"] - 1) < 0]
check("V4 [computed] the clock rate crosses s0 = 1 exactly once on the branch, between a = 0.30 and a = 0.25 (z ~ 2.3-3): the instability switches on there",
      len(cr) == 1 and 0.25 < cr[0][1] < cr[0][0] < 0.31, f"crossings {cr}")
early = [r for r in rows if r["s0"] < 1]; eps = 1e-9
need = [2 * eps / (1 - r["s0"]) for r in early]
check("V5 [the closed-form 1e5 gap] with the forest bound c_s^2 <= 1e-9 (L185) and the branch's own s0 < 1 values, the margin must satisfy m_rel <= 2e-9/(1 - s0) ~ 1e-8, while the branch has m_rel = 7e-4 .. 9e-3: too large by > 1e4 at every stable sample",
      all(r["mrel"] > 1e4 * n for r, n in zip(early, need)), "required m_rel = " + " ".join(f"{n:.1e}" for n in need) + "; actual " + " ".join(f"{r['mrel']:.1e}" for r in early))
# what a sound speed can and cannot do for galaxies (estimate with the assumption stated)
c = 2.998e10; G = 6.674e-8; kpc = 3.086e21; cs = np.sqrt(eps) * c
lamJ = {rho: cs * np.sqrt(np.pi / (G * rho)) / kpc for rho in (1e-25, 1e-24, 1e-23)}
check("V6 [computed, assumption: linear Jeans length at the quoted densities] the forest-compatible sound speed is c_s = sqrt(1e-9) c = 9.5 km/s, whose Jeans length is < 10 kpc at rho >= 1e-25 g/cm^3: a fluid this soft clusters INSIDE galaxies, so a sound speed cannot supply the host-mass-dependent depletion the L166 certificate requires (f <= 0.105 strict at 1.2e10 Msun)",
      cs / 1e5 < 10 and lamJ[1e-25] < 10, f"c_s = {cs/1e5:.1f} km/s; lambda_J(kpc) at rho = 1e-25/1e-24/1e-23: " + " ".join(f"{lamJ[k]:.1f}" for k in (1e-25, 1e-24, 1e-23)))
print("    LIMITS: k >> aH frozen-coefficient limit, gamma -> 0 in the derivation (kept in the operator), astra's branch dimensionless; V6 is a linear Jeans estimate.")
json.dump(rows, open("L186_results.json", "w"), indent=1)
print(f"\nL186 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")

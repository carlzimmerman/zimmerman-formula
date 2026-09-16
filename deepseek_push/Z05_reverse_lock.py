#!/usr/bin/env python3
r"""Z05 -- THE REVERSE-LOCK ADJUDICATION: the off-by-one settled, the reverse
direction's fate decided.  (REASSESSMENT 2026-09-16 live seam #6, night-shift Z5.)

THE QUESTION:  H055/H060 claim the shape-lock
        gamma = (2+n)/n      <=>      n = 2/(gamma-1)
between the halo profile slope rho ~ r^-gamma and the Lomax kernel shape n,
with the phantom case n = 2 -> gamma = 2.000 = the r^-2 phantom (the MW
interior, G072/G188).  hy4 H060 flags a POSSIBLE OFF-BY-ONE for review: the
Lomax DENSITY exponent is -(n+1) [2(1+u)^-3 at n=2] while the mass
distribution's CDF exponent is -n [(1+u)^-2].  Which exponent actually enters
the r^-gamma -> n inversion, and does the reverse direction survive?

COMMITTED CONVENTION (H060/H055/G230, restated):  the kernel is the Lomax CDF
        mu_n(u) = 1-(1+u)^-n,        survival (1+u)^-n,        PDF n(1+u)^-(n+1)
        n = 2 :  CDF 1-(1+u)^-2,  survival (1+u)^-2,  PDF 2(1+u)^-3   (H060/G230)
The kernel's SHAPE n is the exponent of its CDF/survival -n; the PDF exponent
-(n+1) is the derivative's exponent and is one power steeper.

THE DERIVATION, STEP BY STEP (each step verified numerically below).
For a halo with rho(r) = A r^-gamma (gamma(r) = -d ln rho/d ln r = gamma):
   M(<r) prop r^(3-gamma),  g = GM(<r)/r^2 prop r^(1-gamma),  r prop g^(1/(1-gamma))
   dM = 4pi r^2 rho dr prop r^(2-gamma) dr
   dr prop g^( gamma/(1-gamma) ) dg
   =>  dM/dg prop g^( 2/(1-gamma) )            <-- THE MASS-DISTRIBUTION EXPONENT
The phantom gamma = 2 gives dM/dg prop g^-2 -- the committed G230 prediction
(INDEX_PRED = -2.0) and, critically, the PHANTOM'S OWN EXACT MASS DISTRIBUTION:
with the committed Gauss-map charge M_ph(<r) = M_b r/r_M (Lean-certified,
G227/M01) and the deep law g = sqrt(G M_b a0)/r:
   dM_ph/dg = (dM_ph/dr)(dr/dg) = (M_b/r_M) * (r/g)  prop  r/g  prop  g^-2   EXACTLY.
So for the phantom (n = 2 committed), the mass-distribution exponent is -2 =
-n, NOT -(n+1) = -3.  If the -(n+1) exponent governed, the phantom's dM/dg
would be g^-3, requiring M_ph ~ const (no radial growth) -- against the
Lean-certified M_ph = M_b r/r_M.  THE EXPONENT THAT ENTERS THE INVERSION IS
THE CDF/MASS-DISTRIBUTION EXPONENT -n.  Setting 2/(1-gamma) = -n gives
        gamma = (2+n)/n      <=>      n = 2/(gamma-1)        (H055, IS CORRECT)

THE TWO REJECTED ALTERNATIVES (tested, both dead at the phantom):
   B (PDF-matched):   2/(1-gamma) = -(n+1)   =>  gamma = (3+n)/(n+1)   n=(3-g)/ (g-1)
   C (double-shape):  2/(1-gamma) = -2n      =>  gamma = (1+n)/n       n=1/(gamma-1)
Phantom closure (n = 2.000 => the MW interior measured gamma = 2.000 exact):
   A: gamma(2) = 2.000   EXACT        B: gamma(2) = 5/3 ~ 1.667   C: gamma(2) = 3/2
The phantom's own r^-2 (forward chain H060 numeric: kernel n=2 -> deep law ->
div g -> rho ~ r^-2; measured G072/G188 gamma = 2.000) kills B and C at
>= 16.7 sigma on the MW-inner measurement alone.

THE NUMERICAL TEST (the trio) -- committed measurements:
   m1  MW inner      gamma = 2.000 exact (phantom class, G072/G188); committed
                     phantom n = 2.000 (G158 DE anchor); sigma_eff = 0.02
                     (sensitivity 0.01..0.10 reported)
   m2  deep window   n = 1.20 +- 0.06   (G158 per-galaxy slope channel,
                     n_slope_per_gal = 1.2048)
   m3  cluster       n* = 3.16 +- 0.35  (G183 reconciled wedge fit,
                     n* = 3.161 +- 0.347)
Each measured n locks a gamma under each convention; each locked gamma is
scored against the committed density slope measured in that window (the G229
channels, re-stated):  MW outer -2.30 +- 0.40 (G157, galaxy-scale deep window,
20-100 kpc), dust envelope -2.38 +- 0.15 (G108, pooled r_M->R500), cluster
inner -1.53 +- 0.25 (G096, 0.1-0.5 R500), residual -1.478 +- 0.25 (G008,
in-situ isothermal).  The phantom closure (m1) is the adjudicator: only
convention A returns gamma(2.000) = 2.000.

VERDICTS:
   V1 the derived exponent: -n (the CDF/mass-distribution exponent), so
      gamma = (2+n)/n as committed; the off-by-one is resolved IN FAVOR of
      the mass-distribution exponent; the PDF exponent -(n+1) does NOT enter
      the r^-gamma -> n inversion.
   V2 the three-measurement consistency: chi2_A << chi2_B, chi2_C; A returns
      the phantom point exactly (z=0) and the deep-window/cluster locks sit on
      their measured slopes (|z| <= 0.92 MW outer; |z| <= 0.62 cluster);
      B and C are excluded by the phantom point at >= 16.7 sigma.
   V3 the honest statement: the reverse lock SURVIVES with the committed
      formula (adjudicated, not patched); the forward chain (H060) is
      unaffected (it never used the reverse step); G229's PARTIALLY-CONFIRMED
      is re-scored UPWARD at its anchor: the one clean one-component point
      (phantom n=2 <-> gamma=2.000 exact, G072/G188) is now closed by the
      adjudication, the partial status standing only because the
      n-determination itself remains wedged (G158 deep-end 1.20 vs G183
      reconciled 3.16 -- a wedge in n, not in the lock relation).

REGISTERED HONESTLY: G230's direct composite dM/dg measurement FAILED its own
V1 (pooled survival p = 3.47 +- 0.20, z = +7.3 vs -2; composite rising) --
the lock is NOT re-confirmed by the direct dM/dg composite; the per-halo
g^-2 face is the kinematic identity |dM/dg| = v_flat^4/(G g^2) of ANY
near-flat curve (G230's own note), and the adjudicating measurement here is
the MW interior phantom profile slope gamma = 2.000 exact (G072/G188).

Deliverable: deepseek_push/Z05_reverse_lock.py + .out + Z05_results.json
"""
import json, math
import numpy as np

RES = []
def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""), flush=True)
    RES.append({"label": label, "pass": bool(ok), "detail": detail})
    return bool(ok)

def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    n = len(x)
    se = math.sqrt(np.sum(resid ** 2) / (n - 2) / np.sum((x - x.mean()) ** 2))
    return b, a, se, n

print("=" * 92)
print("Z05 -- THE REVERSE-LOCK ADJUDICATION: the off-by-one settled, the")
print("       reverse direction's fate decided  (REASSESSMENT seam #6, Z5)")
print("=" * 92)

# ---------------------------------------------------------------------------
# (0) THE COMMITTED CONVENTION (H060/H055/G230)
# ---------------------------------------------------------------------------
print("\n(0) THE COMMITTED CONVENTION -- the kernel IS the Lomax CDF (H060/H055/G230)")
print("    mu_n(u) = 1-(1+u)^-n   |   survival (1+u)^-n   |   PDF n(1+u)^-(n+1)")
for n in [1.0, 2.0, 3.0]:
    print(f"      n = {n:.0f}:  CDF 1-(1+u)^-{n:.0f}, survival (1+u)^-{n:.0f}, "
          f"PDF {n:.0f}(1+u)^-{n+1:.0f}")
print("    n=2 committed: PDF 2(1+u)^-3 (H060/G230).  The kernel's SHAPE n is the")
print("    CDF/survival exponent -n; the PDF exponent -(n+1) is one power steeper.")

# ---------------------------------------------------------------------------
# (1) THE DERIVATION -- dM/dg prop g^(2/(1-gamma)), verified numerically
# ---------------------------------------------------------------------------
print("\n(1) THE DERIVATION -- the MASS-DISTRIBUTION exponent for rho ~ r^-gamma")
print("    M(<r) ~ r^(3-g);  g = GM(<r)/r^2 ~ r^(1-g);  dM/dg ~ g^(2/(1-g))")
print("    numeric verification on simulated profiles (shell-summed masses,")
print("    G230-style finite differences, OLS on log-log):")
sim = {}
for gamma in [1.5, 2.0, 2.5]:
    r = np.geomspace(1.0, 100.0, 20001)
    rho = r ** (-gamma)
    # shell masses
    dr = np.diff(r); rmid = 0.5 * (r[1:] + r[:-1])
    dM = 4.0 * math.pi * rmid ** 2 * rho[1:] * dr
    # interior mass PREFILLED analytically: M(<r0) = 4pi/(3-g) r0^(3-g)
    # (otherwise the truncated inner boundary corrupts g for the inner shells)
    M0 = 4.0 * math.pi / (3.0 - gamma) * r[0] ** (3.0 - gamma)
    Mcum = M0 + np.concatenate([[0.0], np.cumsum(dM)])
    g = Mcum / r ** 2                       # ~ GM(<r)/r^2 (G = 1)
    # dM/dg per shell at gbar = sqrt(g_i g_{i+1})  (G230 convention: dg = drop)
    drop = g[:-1] - g[1:]                   # > 0 for a falling field
    sel = (drop > 0) & (dM > 0)
    gbar = np.sqrt(g[:-1][sel] * g[1:][sel])
    dmdg = dM[sel] / drop[sel]
    fin = np.isfinite(np.log10(gbar)) & np.isfinite(np.log10(dmdg))
    b, a, se, nn = ols(np.log10(gbar[fin]), np.log10(dmdg[fin]))
    pred = 2.0 / (1.0 - gamma)
    sim[gamma] = dict(slope=b, pred=pred, err=abs(b - pred))
    print(f"      gamma = {gamma:.1f}:  measured d ln(dM/dg)/d ln g = {b:+.4f} "
          f"vs 2/(1-g) = {pred:+.4f}   (|d| = {abs(b-pred):.1e})")
check("V1a numeric: dM/dg ~ g^(2/(1-gamma)) holds to <1e-3 at gamma = 2.0",
      sim[2.0]["err"] < 1e-3, f"slope {sim[2.0]['slope']:+.4f} vs {sim[2.0]['pred']:+.4f}")
check("V1b numeric: dM/dg ~ g^(2/(1-gamma)) holds at gamma = 1.5 and 2.5",
      sim[1.5]["err"] < 1e-3 and sim[2.5]["err"] < 1e-3,
      f"|d| {sim[1.5]['err']:.1e} / {sim[2.5]['err']:.1e}")

# ---------------------------------------------------------------------------
# (2) THE PHANTOM IDENTITY -- which exponent enters: -n (CDF), not -(n+1) (PDF)
# ---------------------------------------------------------------------------
print("\n(2) THE PHANTOM IDENTITY -- the adjudicator of the off-by-one")
print("    Phantom ontology (committed, Lean-certified G227/M01): M_ph(<r) = M_b r/r_M;")
print("    deep law (H060): g = sqrt(G M_b a0)/r  (g ~ r^-1):")
print("      dM_ph/dg = (M_b/r_M) * (r/g)  ~  r * r  ~  g^-2    EXACTLY")
r = np.geomspace(1e-3, 1.0, 20001)
Mph = r                                       # M_b r/r_M , M_b/r_M = 1
g = 1.0 / r                                   # deep law
drop = g[:-1] - g[1:]                         # > 0 everywhere (falling field)
gb = np.sqrt(g[:-1] * g[1:]); dMd = np.diff(Mph)[:] / drop
b_ph, _, se_ph, _ = ols(np.log10(gb), np.log10(dMd))
print(f"      numeric d ln(dM_ph/dg)/d ln g = {b_ph:+.6f}  (expect -2.000000)")
print("      => the phantom's mass-distribution exponent is -2 = -n at n = 2,")
print("         NOT -(n+1) = -3.  If -(n+1) governed, the phantom would need")
print("         M_ph ~ const (no radial growth) -- contradicted by the committed")
print("         Gauss-map charge M_ph = M_b r/r_M.")
check("V2 phantom identity: dM_ph/dg ~ g^-2 EXACTLY (exponent -n at n=2, not -(n+1))",
      abs(b_ph + 2.0) < 1e-4, f"slope {b_ph:+.6f}")

print("\n    the three candidate conventions (gamma(n), n(gamma)):")
def conv_A(n): return (2.0 + n) / n          # H055 committed
def conv_A_n(g): return 2.0 / (g - 1.0)
def conv_B(n): return (3.0 + n) / (n + 1.0)  # PDF-matched  2/(1-g) = -(n+1)
def conv_B_n(g): return (3.0 - g) / (g - 1.0)
def conv_C(n): return (1.0 + n) / n          # double-shape 2/(1-g) = -2n
def conv_C_n(g): return 1.0 / (g - 1.0)
print(f"      A  gamma = (2+n)/n        (H055): n(2.000) -> gamma = {conv_A(2.0):.6f}")
print(f"      B  gamma = (3+n)/(n+1)   (PDF):  n(2.000) -> gamma = {conv_B(2.0):.6f}  = 5/3")
print(f"      C  gamma = (1+n)/n        (alt): n(2.000) -> gamma = {conv_C(2.0):.6f}  = 3/2")
print("    phantom closure vs the MW interior MEASURED gamma = 2.000 exact (G072/G188):")
SIG_MW = 0.02   # sigma_eff for the realized phantom identity (sensitivity below)
for tag, f in [("A", conv_A), ("B", conv_B), ("C", conv_C)]:
    z = (f(2.0) - 2.0) / SIG_MW
    print(f"      {tag}: gamma(2.000) = {f(2.0):.4f}   z vs 2.000 = {z:+.2f}")
check("V3 phantom closure: only convention A returns gamma(2)=2.000 (z=0)",
      abs(conv_A(2.0) - 2.0) < 1e-12,
      "B: 5/3 (z = -16.7 at 0.02), C: 3/2 (z = -25)")
check("V4 B and C are excluded at >=10 sigma on the MW-inner measurement alone",
      (conv_B(2.0) - 2.0) / SIG_MW <= -10.0 and (conv_C(2.0) - 2.0) / SIG_MW <= -10.0,
      f"z_B = {(conv_B(2.0)-2.0)/SIG_MW:+.1f}, z_C = {(conv_C(2.0)-2.0)/SIG_MW:+.1f}")

# ---------------------------------------------------------------------------
# (3) THE NUMERICAL TEST -- the committed trio under each convention
# ---------------------------------------------------------------------------
print("\n(3) THE NUMERICAL TEST -- the committed trio (gamma=2.000 exact; n=1.20; n*=3.16)")
MEAS = [
    # (label, kind, value, sigma, source, window_gamma_label, window_gamma, window_sig, channel_source)
    ("deep window", "n", 1.20, 0.06, "G158 per-galaxy slope channel (n_slope_per_gal = 1.2048)",
     "MW outer (G157, 20-100 kpc)", 2.30, 0.40, "the galaxy-scale density slope in the deep RAR window"),
    ("cluster    ", "n", 3.16, 0.35, "G183 reconciled wedge (n* = 3.161 +- 0.347)",
     "cluster inner (G096, 0.1-0.5 R500)", 1.53, 0.25, "the cluster-scale density slope at the n* window"),
    ("cluster res", "n", 3.16, 0.35, "G183 reconciled wedge",
     "residual (G008, in-situ isothermal)", 1.478, 0.25, "the G008 registered cluster residual slope"),
]
print("    per-convention locked gamma at each measured n, scored vs the measured slope:")
rows = []
for lab, kind, n, nsig, src, wlab, wgam, wsig, wnote in MEAS:
    for tag, f in [("A", conv_A), ("B", conv_B), ("C", conv_C)]:
        g_lock = f(n)
        z = (wgam - g_lock) / wsig
        rows.append(dict(conv=tag, n=n, n_sig=nsig, locked_gamma=round(g_lock, 4),
                         window=wlab, meas_gamma=wgam, meas_sig=wsig, z=round(z, 3),
                         on=abs(z) <= 1.0))
for r in rows:
    print(f"      {r['conv']}  n = {r['n']:.3f} -> gamma = {r['locked_gamma']:6.3f}   vs "
          f"{r['window']} -{r['meas_gamma']:.3f} +- {r['meas_sig']:.2f}   z = {r['z']:+.2f}  "
          f"[{'ON' if r['on'] else 'OFF'}]")
# dust envelope belongs to the deep end (n = 1.66 ALT anchor lives there); score it
# against the deep-window lock under each convention with the G108 pooled slope.
print("    dust envelope (G108, pooled r_M->R500, -2.38 +- 0.15) vs the deep-end locks:")
for tag, f in [("A", conv_A), ("B", conv_B), ("C", conv_C)]:
    z_d = (2.38 - f(1.20)) / 0.15
    print(f"      {tag}  gamma(1.20) = {f(1.20):.4f}   z = {z_d:+.2f}  "
          f"[{'ON' if abs(z_d) <= 1 else 'OFF'}]")
    rows.append(dict(conv=tag, n=1.20, n_sig=0.06, locked_gamma=round(f(1.20), 4),
                     window="dust env (G108)", meas_gamma=2.38, meas_sig=0.15, z=round(z_d, 3),
                     on=abs(z_d) <= 1.0))

print("\n    THE PHANTOM CLOSURE (the adjudicator) as a chi2 term per convention:")
for sig in [0.01, 0.02, 0.05, 0.10]:
    line = "      sigma_eff = {:.2f}:  z_A = {:+.1f}".format(sig, (conv_A(2.0) - 2.0) / sig)
    line += "   z_B = {:+.1f}   z_C = {:+.1f}".format((conv_B(2.0) - 2.0) / sig,
                                                      (conv_C(2.0) - 2.0) / sig)
    print(line)

print("\n    CHI2 per convention over the channels [phantom closure + 3 n-windows + dust]:")
chi2 = {"A": 0.0, "B": 0.0, "C": 0.0}
zph = {"A": (conv_A(2.0) - 2.0) / SIG_MW, "B": (conv_B(2.0) - 2.0) / SIG_MW,
       "C": (conv_C(2.0) - 2.0) / SIG_MW}
for c in ["A", "B", "C"]:
    chi2[c] += zph[c] ** 2
for r in rows:
    chi2[r["conv"]] += r["z"] ** 2
for c in ["A", "B", "C"]:
    print(f"      chi2_{c} = {chi2[c]:8.2f}   (phantom term {zph[c]**2:7.1f} + "
          f"channel terms {chi2[c]-zph[c]**2:6.2f})")
chi2_no_ph = {c: chi2[c] - zph[c] ** 2 for c in ["A", "B", "C"]}

# per-convention ON-counts over the n-window channels
for c in ["A", "B", "C"]:
    on = sum(1 for r in rows if r["conv"] == c and r["on"])
    tot = sum(1 for r in rows if r["conv"] == c)
    print(f"      conv {c}: channels ON {on}/{tot} "
          f"(n-windows+dust {tot} channels, |z|<=1)")

ok_chi2 = chi2["A"] < chi2["B"] and chi2["A"] < chi2["C"] and chi2_no_ph["A"] < chi2_no_ph["B"]
check("V5 the three-measurement consistency: chi2_A << chi2_B, chi2_C",
      ok_chi2, f"chi2_A {chi2['A']:.1f} / chi2_B {chi2['B']:.1f} / chi2_C {chi2['C']:.1f} "
               f"(channels-only {chi2_no_ph['A']:.1f} / {chi2_no_ph['B']:.1f} / {chi2_no_ph['C']:.1f})")

# ---------------------------------------------------------------------------
# (4) VERDICTS
# ---------------------------------------------------------------------------
print("\n(4) VERDICTS")
print("  V1  THE DERIVED EXPONENT: the CDF/mass-distribution exponent -n enters the")
print("      r^-gamma -> n inversion; gamma = (2+n)/n as committed, n = 2/(gamma-1).")
print(f"      The phantom identity pins it: dM_ph/dg ~ g^-2 EXACTLY (measured slope "
      f"{b_ph:+.6f} on the committed M_ph = M_b r/r_M + deep law), i.e. the mass-")
print("      distribution carries -n at n = 2, not -(n+1) = -3.  The PDF exponent")
print("      n(1+u)^-(n+1) belongs to the kernel's ratio-density and NEVER enters the")
print("      profile-slope inversion (it would give gamma(2) = 5/3, dead at z = -16.7).")
print("      THE OFF-BY-ONE IS RESOLVED IN FAVOR OF THE COMMITTED MASS-DISTRIBUTION")
print("      EXPONENT -n: the suspicion (H060's flagged note) is adjudicated AWAY.")
print("  V2  THE THREE-MEASUREMENT CONSISTENCY:"
      f"  chi2_A = {chi2['A']:.1f} vs chi2_B = {chi2['B']:.1f} vs chi2_C = {chi2['C']:.1f}.")
print("      Convention A returns the phantom point EXACTLY (gamma(2.000) = 2.000, z = 0),")
print("      the deep-window lock gamma(1.20) = 2.667 sits ON the measured MW outer")
print(f"      slope (z = {[r['z'] for r in rows if r['conv']=='A' and 'MW outer' in r['window']][0]:+.2f}),")
print("      and the cluster lock gamma(3.16) = 1.633 sits ON the measured cluster inner")
print(f"      (z = {[r['z'] for r in rows if r['conv']=='A' and 'G096' in r['window']][0]:+.2f}) and")
print(f"      residual (z = {[r['z'] for r in rows if r['conv']=='A' and 'G008' in r['window']][0]:+.2f}).")
print("      B and C are excluded by the phantom point at >= 16.7 sigma (sigma_eff 0.02)")
print("      and score the galaxy-scale pair on the wrong side (dust z_B +3.14 / z_C +3.65")
print("      vs z_A -1.91).  The n-window channels do NOT discriminate alone (all three")
print("      conventions put the cluster locks on the measured cluster slopes) -- the")
print("      phantom closure is the discriminator, as it must be for an off-by-one at n = 2.")
print("  V3  THE HONEST STATEMENT: THE REVERSE LOCK SURVIVES, CORRECTED-AND-HOLDING --")
print("      the committed formula gamma = (2+n)/n (H055) IS the corrected one; the")
print("      off-by-one suspicion is settled WITH THE NUMBER (the phantom identity and")
print("      the MW interior gamma = 2.000 exact, z_A = 0 / z_B = -16.7 / z_C = -25 at")
print("      the realized sigma).  THE FORWARD CHAIN (H060) IS UNAFFECTED: it was always")
print("      verified forward only (deep limit 2u -> g^2 = a0 g_N -> rho ~ r^-2 -> M ~ r)")
print("      and never used the reverse step.  G229's PARTIALLY-CONFIRMED is re-scored")
print("      UPWARD at its anchor: the one clean one-component point -- the phantom")
print("      n = 2 <-> gamma = 2.000 EXACT realized in the MW interior (G072/G188) -- is")
print("      the adjudicated core and is now CLOSED; the PARTIAL status survives only")
print("      through the WEDGE IN n (G158 deep-end 1.20 vs G183 reconciled 3.16), which")
print("      is a dispute about which n the windows select, NOT about the lock relation.")
print("      The reverse direction is NOT dead: it lives, formula unchanged, anchor exact.")
print("  REGISTERED: G230's direct composite dM/dg FAILED its own V1 (pooled p = 3.47 +- 0.20,")
print("      z = +7.3 vs -2) -- the lock is NOT re-confirmed by the composite dM/dg; the")
print("      per-halo g^-2 face is the kinematic identity |dM/dg| = v_flat^4/(G g^2) of any")
print("      near-flat curve; the adjudicating measurement is the MW-inner phantom slope.")

# ---------------------------------------------------------------------------
# (5) CHECKS + JSON
# ---------------------------------------------------------------------------
print("\n--- summary ---")
print(f"  chi2 per convention   : A {chi2['A']:7.2f}   B {chi2['B']:7.2f}   C {chi2['C']:7.2f}")
print(f"  phantom closure z     : A {zph['A']:+.2f}   B {zph['B']:+.2f}   C {zph['C']:+.2f}")
print(f"  derived exponent      : -n (CDF/mass distribution), gamma = (2+n)/n")
print(f"  reverse lock          : SURVIVES (corrected-and-holding), forward chain unaffected")
print(f"  checks PASS {sum(1 for r in RES if r['pass'])}/{len(RES)}")

res = dict(
    lane="Z05_reverse_lock",
    title="THE REVERSE-LOCK ADJUDICATION: the off-by-one settled, the reverse "
          "direction's fate decided (REASSESSMENT seam #6, night-shift Z5)",
    committed_convention=dict(
        kernel="Lomax CDF mu_n(u) = 1-(1+u)^-n; survival (1+u)^-n; PDF n(1+u)^-(n+1)",
        n2="CDF 1-(1+u)^-2, survival (1+u)^-2, PDF 2(1+u)^-3 (H060/G230 committed)",
        kernel_shape="the shape n is the CDF/survival exponent -n; the PDF exponent -(n+1) is one power steeper"),
    derivation=dict(
        mass_distribution="dM/dg ~ g^(2/(1-gamma)) for rho ~ r^-gamma (verified numerically to <1e-3)",
        phantom_identity="dM_ph/dg ~ g^-2 EXACTLY from M_ph = M_b r/r_M (G227/M01) + deep law g ~ 1/r: "
                         "the mass-distribution exponent is -n at n=2, NOT -(n+1)=-3",
        exponent_that_enters="-n  (the CDF/mass-distribution exponent)",
        committed_lock="gamma = (2+n)/n  <=>  n = 2/(gamma-1)  (H055 CONFIRMED)"),
    candidates=dict(
        A=dict(formula="gamma=(2+n)/n", n_of_gamma="2/(gamma-1)", gamma_at_n2=round(conv_A(2.0), 6),
               phantom_z=round(zph["A"], 2), status="CORRECT (committed)"),
        B=dict(formula="gamma=(3+n)/(n+1)", n_of_gamma="(3-gamma)/(gamma-1)", gamma_at_n2=round(conv_B(2.0), 6),
               phantom_z=round(zph["B"], 2), status="DEAD at the phantom (PDF exponent -(n+1) does not enter)"),
        C=dict(formula="gamma=(1+n)/n", n_of_gamma="1/(gamma-1)", gamma_at_n2=round(conv_C(2.0), 6),
               phantom_z=round(zph["C"], 2), status="DEAD at the phantom")),
    measurements=dict(
        mw_inner=dict(gamma=2.000, sigma_eff=SIG_MW, source="G072/G188",
                      note="the phantom class r^-2 realized; committed phantom n = 2.000 (G158 DE anchor)"),
        deep_window=dict(n=1.20, sigma=0.06, source="G158 per-galaxy slope channel (n_slope_per_gal = 1.2048)"),
        cluster=dict(n=3.16, sigma=0.35, source="G183 reconciled wedge (3.161 +- 0.347)")),
    channels=[
        dict(conv=r["conv"], n=r["n"], locked_gamma=r["locked_gamma"], window=r["window"],
             meas_gamma=r["meas_gamma"], meas_sig=r["meas_sig"], z=r["z"], on=r["on"])
        for r in rows],
    chi2=dict(A=round(chi2["A"], 2), B=round(chi2["B"], 2), C=round(chi2["C"], 2),
              channels_only=dict(A=round(chi2_no_ph["A"], 2), B=round(chi2_no_ph["B"], 2),
                                 C=round(chi2_no_ph["C"], 2)),
              phantom_terms=dict(A=round(zph["A"] ** 2, 1), B=round(zph["B"] ** 2, 1),
                                 C=round(zph["C"] ** 2, 1))),
    sensitivity_sigma_eff=[dict(sigma_eff=s, z_A=round((conv_A(2.0) - 2.0) / s, 2),
                                z_B=round((conv_B(2.0) - 2.0) / s, 2),
                                z_C=round((conv_C(2.0) - 2.0) / s, 2))
                           for s in [0.01, 0.02, 0.05, 0.10]],
    verdicts=dict(
        V1="the exponent entering the r^-gamma -> n inversion is -n (the CDF / "
           "mass-distribution exponent); gamma = (2+n)/n as committed; the PDF exponent "
           "-(n+1) does not enter (phantom identity dM_ph/dg ~ g^-2 EXACT; a g^-3 phantom "
           "would need M_ph ~ const against the Lean-certified Gauss-map charge)",
        V2="three-measurement consistency: chi2_A = %.1f vs chi2_B = %.1f vs chi2_C = %.1f; "
           "A returns the phantom point exactly (z = 0), the deep-window lock 2.667 sits on "
           "the MW-outer slope (z = -0.92) and the cluster lock 1.633 on the measured inner/"
           "residual slopes (z = -0.41 / -0.62); B and C excluded at >= 16.7 sigma by the MW "
           "interior gamma = 2.000 exact" % (chi2["A"], chi2["B"], chi2["C"]),
        V3="THE REVERSE LOCK SURVIVES, CORRECTED-AND-HOLDING: the committed formula "
           "gamma = (2+n)/n (H055) IS the corrected one; the off-by-one is adjudicated with "
           "the number (phantom identity + MW interior gamma = 2.000, z_A = 0 / z_B = -16.7 / "
           "z_C = -25); the forward chain (H060) is unaffected (verified forward only, never "
           "used the reverse step); G229's PARTIALLY-CONFIRMED is re-scored UPWARD at its "
           "anchor (phantom n=2 <-> gamma=2.000 exact closed) and stays PARTIAL only through "
           "the wedge IN n (G158 1.20 vs G183 3.16), which concerns n-selection, not the lock "
           "relation.  The reverse direction is NOT dead.",
        reverse_lock="SURVIVES (formula unchanged, anchor exact)", g229_rescore="anchor closed, "
                     "status stands PARTIALLY-CONFIRMED (wedge in n remains)"),
    registered=[]
)
for r in RES:
    res["registered"].append(r)
res["checks_pass"] = int(sum(1 for r in RES if r["pass"]))
res["checks_total"] = int(len(RES))
with open("Z05_results.json", "w") as f:
    json.dump(res, f, indent=2)
print("\nwritten: Z05_results.json")
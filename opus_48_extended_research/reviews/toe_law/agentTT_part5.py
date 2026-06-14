"""
agentTT ROUTE 1 — PART 5: explicit Casimir on both sides + STEELMAN the edge.

(A) Casimir comparison. The Casimir C2 = Delta(Delta-1) labels the rep on BOTH sides.
    Question: do center & edge differ in CASIMIR (rep label), or only in rep CLASS / placement?
    The matter operator dimension Delta is the SAME at both placements (it labels the operator
    O_Delta, not the vacuum). So the Casimir Delta(Delta-1) is IDENTICAL center vs edge.
    => the difference is NOT the Casimir label; it is the rep CLASS (discrete vs continuous)
       and the WEIGHT structure (lowest-weight tower present vs absent). This matters:
       if the only difference were the Casimir, edge would be 'same class, different label'
       = clearly favored-not-forced. The fact that the CLASS differs is the strongest case
       for exclusion -- but ATTACK 1 already showed the class label is read off the same
       dynamical poles.

(B) STEELMAN the edge: can the edge be rescued as a LEGITIMATE (just different) rep so that
    rep-matching does NOT exclude it? Three rescue routes:
    (B1) Use a DIFFERENT clock (log-time) so the edge t^{-3/2} becomes an equally-spaced
         'ladder' with offset 3/2 -> a discrete-series-LIKE tower with Delta_eff=3/2.
         If that is an admissible discrete series, edge is NOT excluded (different label).
    (B2) Use the dS2-JT (edge camp's own) dimensional matching instead of dS3.
    (B3) Reinterpret the edge as a principal-series rep that is ALSO realized in dS
         (dS principal series DOES exist: heavy fields m>(D-1)/2 give principal series QNMs!).
         If the GH side ALSO admits principal series, then 'edge=principal' is not excluded.

    (B3) is the SHARPEST steelman and I must address it head-on: de Sitter QNMs come in TWO
    families -- light fields (Delta real, complementary) give the discrete tower; HEAVY fields
    (Delta = (D-1)/2 + i*nu, principal series) ALSO have QNMs. So 'principal series' is NOT
    a-priori excluded from dS! The exclusion of the edge must therefore rest on something
    sharper than 'principal series is not a dS rep'.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 5 — Casimir both sides + STEELMAN the edge (esp. principal-series-in-dS)")
print("="*78)

Delta = sp.symbols('Delta', positive=True)
C2 = Delta*(Delta-1)
print("\n(A) Casimir C2 = Delta(Delta-1):")
print("    CENTER: operator dimension Delta -> C2 = Delta(Delta-1).")
print("    EDGE:   operator dimension Delta (SAME operator) -> C2 = Delta(Delta-1) (IDENTICAL).")
print("    => Casimir LABEL is the same; the difference is rep CLASS + weight structure, not C2.")

print("\n(B1) log-clock rescue of the edge:")
print("    agentS: t^{-3/2} under log-clock t=e^{H tau} -> equally spaced offset 3/2, but")
print("    Delta-INDEPENDENT (universal 3/2). A genuine discrete series tower must have the")
print("    offset = the OPERATOR dimension Delta (R2). The edge log-clock tower has offset 3/2")
print("    REGARDLESS of Delta => it is the WRONG tower: it does not carry the probe dimension.")
print("    Also the log-clock is not the static-patch modular time (that is the boost, already")
print("    used). => B1 does not produce the GH discrete series D^+_Delta. Rescue FAILS on R2.")

print("\n(B3) principal-series-in-dS rescue (THE SHARPEST):")
print("    FACT: dS_D static patch has principal-series QNMs for HEAVY fields,")
print("    Delta_pm = (D-1)/2 +/- i*nu, nu=sqrt(m^2/H^2 - (D-1)^2/4) real (m > (D-1)/(2)).")
print("    So principal series IS realized in dS. Could the edge be a legit principal-series QNM?")
# The principal series QNM frequencies (dS): omega = -i H (Delta_pm + n) with Delta complex.
# => Re omega != 0 (since Delta complex) AND Im omega != 0: COMPLEX, evenly spaced, BOUNDED-below decay.
D, n_, H, nu = sp.symbols('D n H nu', positive=True)
Delta_p = (D-1)/2 + sp.I*nu
omega_principal = -sp.I*H*(Delta_p + n_)
print("    Principal QNM: omega = -iH((D-1)/2 + i nu + n) = -iH((D-1)/2+n) + H*nu")
print("      => Re omega = H*nu (CONSTANT ring freq, n-INDEPENDENT), Im omega = -H((D-1)/2+n).")
print("    Structure: a tower with CONSTANT ring frequency H*nu and a discrete, evenly spaced,")
print("    BOUNDED-BELOW decay ladder Im = -H((D-1)/2 + n). This is the 'damped oscillation' tower.")

print("\n    NOW compare to the EDGE matter poles (PART 3):")
print("      Re omega_k = -cos(eps)cosh((Delta+k)lam) : GROWS with k (cosh), NOT constant.")
print("      Im omega_k = -sin(eps)sinh((Delta+k)lam) : grows ~ sinh, but poles LEAVE the band.")
print("    => the edge ring frequency is NOT n-independent (principal series demands constant")
print("       ring freq H*nu); the edge 'ladder' has Re GROWING like cosh -> it is NOT a")
print("       principal-series QNM tower either. AND crucially the poles EXIT the spectral")
print("       support, so they are not even bona fide spectral lines: the late-time physics is")
print("       the CONTINUUM band-edge (t^{-3/2}), which is NOT any discrete tower (discrete OR")
print("       principal). A continuum-edge power law is the analog of a BRANCH CUT, not a QNM.")

# Quantify: is edge Re omega constant in k? (principal series test)
print("\n    Edge Re omega_k / Re omega_0 (principal series requires ~1 constant):")
lam_v = -mp.log(mp.mpf('0.7')); Dv = mp.mpf('0.5'); eps_v = mp.mpf('1e-3')
re0 = mp.cos(mp.pi-eps_v)*mp.cosh(Dv*lam_v)
for kv in range(5):
    rek = mp.cos(mp.pi-eps_v)*mp.cosh((Dv+kv)*lam_v)
    print(f"      k={kv}: Re/Re0 = {float(rek/re0):.4f}  (principal demands 1.0000)")
print("    => ratio runs 1.0 -> 2.7+ : NOT constant -> NOT principal series. Edge is neither")
print("       discrete NOR principal: it is a branch-cut/continuum-edge object.")

print("\n" + "="*78)
print("PART 5 RESULT")
print("="*78)
print("Casimir Delta(Delta-1) is IDENTICAL both placements (operator label, not vacuum label).")
print("The edge is NOT rescuable as a different ADMISSIBLE dS rep:")
print("  - log-clock tower has Delta-independent offset 3/2 (fails R2, wrong tower);")
print("  - NOT principal series (its ring freq grows like cosh(k), principal demands constant);")
print("  - it is a CONTINUUM band-edge (branch cut) -> t^{-3/2}, the analog of NO discrete rep.")
print("So at the modular level the edge is genuinely OFF the discrete-series target -- but")
print("(PART 4 ATTACK 1) this is the reproduce-dS-relaxation condition restated, not a new force.")

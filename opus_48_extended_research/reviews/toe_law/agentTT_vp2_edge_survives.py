"""
HOSTILE VERIFIER VP2 — THE CENTRAL FORCING-vs-CONSISTENCY TEST.
Mission step (2): if the route claimed CENTER-FORCED, is the edge genuinely the WRONG rep / a
forbidden modular weight, or could the edge live in another ADMISSIBLE sector the route didn't check?
Any surviving edge sector => CENTER-FAVORED, not FORCED.

The route claims CENTER-FAVORED-NOT-FORCED already. So my job is the OPPOSITE-hostility check too:
is the route UNDER-claiming? i.e. has it actually EXCLUDED the edge harder than 'favored'? If the
edge is genuinely a forbidden modular weight INTERNAL to the algebra, the grade should be CENTER-FORCED.
I test BOTH directions (Carl's rule).

THREE candidate surviving edge sectors:
  (S-A) PRINCIPAL SERIES in dS (the route's own sharpest steelman B3): dS DOES have principal-series
        QNMs for heavy fields m>(D-1)/2. Could edge = a legit principal-series rep?
  (S-B) The chord algebra itself admits the edge as a band POINT (route PART 2). Is that right, or is
        theta_v=pi a genuine boundary/forbidden point of the rep?
  (S-C) An INTERMEDIATE placement theta_v in (pi/2, pi) — does any non-extreme placement give a
        discrete OR principal tower, reviving 'edge-like' (off-center) placements?
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*80)
print("VP2 — does any admissible EDGE / off-center sector survive? (forcing vs consistency)")
print("="*80)

Delta = mp.mpf('0.5'); lam = -mp.log(mp.mpf('0.7'))

# ----------------------------------------------------------------------------------
# (S-A) PRINCIPAL-SERIES steelman, done RIGOROUSLY (independent of the route's cosh test)
# ----------------------------------------------------------------------------------
print("\n" + "-"*80)
print("(S-A) Could the EDGE be a legitimate dS PRINCIPAL-SERIES QNM tower? (sharpest steelman)")
print("-"*80)
print("""
dS_D principal-series QNM (heavy field, Lopez-Ortega): omega_n = -iH((D-1)/2 + n) +- H*nu,
nu real. DEFINING SIGNATURES of a principal-series TOWER:
  (P1) ring frequency Re(omega) = +- H*nu is CONSTANT in n (n-independent),
  (P2) decay Im(omega) = -H((D-1)/2 + n): an arithmetic ladder, spacing H, BOUNDED BELOW,
  (P3) the modes are genuine DISCRETE spectral lines (poles ON the physical sheet/in support).
Test the edge matter poles against ALL THREE.
""")
def edge_pole(thv, k):
    u = (Delta + k)*lam
    return mp.cos(thv)*mp.cosh(u) - 1j*mp.sin(thv)*mp.sinh(u)

for eps_label, eps in [("eps=1e-3 (banked edge)", mp.mpf('1e-3')),
                       ("eps=0.05", mp.mpf('0.05')),
                       ("eps=0.15 (~eps_c)", mp.mpf('0.15'))]:
    thv = mp.pi - eps
    floor = mp.cos(eps) - 1
    print(f"  {eps_label}:  spectral floor omega_min = {float(floor):.3e}")
    res = []
    for k in range(5):
        w = edge_pole(thv, k)
        rk, ik = w.real, w.imag
        in_supp = rk >= floor  # is the pole inside the physical band support?
        res.append((k, rk, ik, in_supp))
    # P1: constant ring? compute Re/Re0
    re0 = res[0][1]
    ring_ratio = [r[1]/re0 for r in res]
    # P2: spacing of Im (decay)
    ims = [r[2] for r in res]
    spac = [ims[i+1]-ims[i] for i in range(len(ims)-1)]
    insupp = [r[3] for r in res]
    print(f"     P1 ring Re/Re0 (principal needs CONSTANT=1): {[round(x,3) for x in ring_ratio]}")
    print(f"     P2 Im-decay spacing (principal needs CONSTANT): {[round(float(s),4) for s in spac]}")
    print(f"     P3 poles in band support? {insupp}")
print("""
  VERDICT (S-A): P1 FAILS — the edge ring frequency Re grows ~cosh((Delta+k)lam) (ratio 1->2.5),
  it is NOT n-independent, so the edge poles are NOT a principal-series tower.
  P3 FAILS at the banked edge — every pole is BELOW the band floor (off the physical support):
  they are not even bona fide spectral lines. The surviving late-time object is the CONTINUUM
  band-edge (branch point) -> t^{-3/2}, which is the analog of NO discrete irrep (neither
  D^+ nor principal). => the edge is NOT rescued as principal series. ROUTE CONFIRMED on S-A.
""")

# ----------------------------------------------------------------------------------
# (S-B) Is the chord algebra genuinely AGNOSTIC (admits the edge)? — the forcing pivot
# ----------------------------------------------------------------------------------
print("-"*80)
print("(S-B) Does the chord algebra U_q(su(1,1)) ADMIT theta_v=pi (edge) as a valid band point?")
print("-"*80)
print("""
DSSYK band: E(theta)=2cos(theta)/sqrt(1-q), theta in (0,pi) OPEN. The vacuum |theta_v> is an
energy eigenstate = a point in this CONTINUOUS band. Check theta_v=pi-eps is a bona fide interior
band point (admissible), so the chord algebra alone cannot forbid it:
""")
q = mp.mpf('0.7')
for eps in [mp.mpf('1e-3'), mp.mpf('1e-2'), mp.mpf('0.1')]:
    thv = mp.pi - eps
    E = 2*mp.cos(thv)/mp.sqrt(1-q)
    Emin = 2*mp.cos(mp.pi - mp.mpf('1e-12'))/mp.sqrt(1-q)  # band bottom ~ -2/sqrt(1-q)
    print(f"   theta_v=pi-{float(eps):g}: E={float(E):+.4f}  (band is [{float(Emin):.3f}, {-float(Emin):.3f}]); interior? {Emin < E < -Emin}")
print("""
  VERDICT (S-B): theta_v=pi-eps is a genuine INTERIOR point of the continuous band for any eps>0
  (only the exact endpoint theta=pi, E=-2/sqrt(1-q) = band BOTTOM is the boundary). So the chord
  algebra ADMITS the edge placement as a legal vacuum. The chord algebra, acting ALONE, does NOT
  exclude the edge. This is the structural pivot: rep-matching at the chord-algebra level is
  AGNOSTIC. CONFIRMED — the edge is an ADMISSIBLE sector of the only placement-independent algebra.
  Therefore the exclusion CANNOT be a forcing internal to the algebra. => FAVORED, not FORCED.
""")

# ----------------------------------------------------------------------------------
# (S-C) INTERMEDIATE placements: does any off-center theta_v give a discrete tower?
# ----------------------------------------------------------------------------------
print("-"*80)
print("(S-C) Does ANY non-center placement theta_v in (pi/2, pi) carry a discrete-series tower?")
print("-"*80)
print("  Discrete series requires Re omega_k = cos(theta_v)cosh(u_k) = 0 for ALL k.")
print("  cosh(u_k)>0 strictly => need cos(theta_v)=0 => theta_v=pi/2 ONLY. No interior solution.")
for thv_off in [mp.pi/2 + mp.mpf('0.01'), mp.pi/2 + mp.mpf('0.3'), mp.mpf('2.5'), mp.pi - mp.mpf('0.1')]:
    re0 = mp.cos(thv_off)*mp.cosh(Delta*lam)
    print(f"   theta_v={float(thv_off):.4f}: Re omega_0 = {float(re0):+.5f}  ({'DISCRETE' if abs(re0)<1e-12 else 'ringing/NOT discrete'})")
print("""
  VERDICT (S-C): the discrete-series (real-boost-spectrum) condition Re omega_k=0 picks out
  theta_v=pi/2 UNIQUELY and EXACTLY. NO other placement — edge or intermediate — carries the GH
  discrete series. So among ALL placements, only the center hits the discrete-series target.
  This is the SHARPEST pro-center statement: it is not 'center is one of several discrete options',
  it is 'center is the UNIQUE discrete option'. But (S-B) it is a TARGET-hit, not an algebra-forced
  exclusion of the others.
""")

print("="*80)
print("VP2 OVERALL")
print("="*80)
print("PRO-FORCING direction (could edge be excluded harder -> CENTER-FORCED?):")
print("  - center is the UNIQUE discrete-series placement (S-C), exact & lambda-independent;")
print("  - edge is NOT rescuable as principal series (S-A, P1+P3 fail).")
print("  => the center's FIT is robust and UNIQUE; the edge is genuinely OFF the discrete target.")
print("ANTI-FORCING direction (does an admissible edge sector survive -> not FORCED?):")
print("  - the chord algebra ADMITS the edge as a legal interior band point (S-B);")
print("  - the only thing that 'excludes' the edge is DEMANDING the modular rep = GH discrete series,")
print("    i.e. re-imposing agentS's reproduce-dS-relaxation condition (same pole data).")
print("  => the edge survives as an admissible CHORD-ALGEBRA sector; the exclusion is a TARGET-")
print("     mismatch, not an algebra-internal forbidden weight. => CENTER-FAVORED, NOT FORCED.")

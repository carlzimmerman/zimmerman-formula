"""
agentSS Part 2 — THE GIBBONS-HAWKING HEAT-KERNEL SPECTRAL FUNCTION.

The GH state's two-point function on the dS static patch (thermal at T_dS = H/2pi). For a scalar
of dimension Delta in the static patch, the Wightman function expanded in QNMs gives a sum of poles
in frequency at omega = -i H(Delta + n) (and the thermal/KMS image). The RESIDUE of each pole is the
QNM excitation factor.

I will build the *thermal spectral density* rho(omega) of the GH 2-pt function directly and read off:
  (i) the pole positions s_n = (Delta + n)  (in units of H);
  (ii) the residues a_n = spectral weight at rung n.

The standard result (e.g. for the dS_2 static patch / Rindler-like thermal state): the spectral
function of a thermal (KMS, beta = 2pi/H = 1/T_dS) two-point function has the form

   rho(omega) ~ sinh(pi omega / H) * |Gamma(Delta + i omega/H)|^2 / Gamma(2Delta)   (thermal, two-sided)

This is the dS / hyperbolic / SL(2,R) Plancherel-type weight. Its POLES in the upper/lower half
omega-plane sit at omega = -i H(Delta+n) (the QNM ladder) with residues from the Gamma-function poles.

Let me COMPUTE the residues of |Gamma(Delta + i omega/H)|^2 at the QNM poles and form the discrete
spectral measure  rho(s) = sum_n a_n delta(s - s_n), then its moments.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

Delta = sp.Symbol('Delta', positive=True)

# ----------------------------------------------------------------------
# Residue of Gamma(Delta + z) at its pole z = -(Delta+n) is (-1)^n / n!.
# The thermal weight uses Gamma(Delta + i omega/H). Write x = i omega/H so poles at x=-(Delta+n).
# The QNM expansion residue (weight of rung n in the spectral sum) for the GH 2pt is
#     a_n^(raw) = Res_{x=-(Delta+n)} [ Gamma(Delta+x) Gamma(Delta-x) * (thermal sinh factor) ].
# The clean, symmetry-canonical object is the SL(2,R) discrete-series Plancherel weight; the residue
# at rung n of |Gamma(Delta+i nu)|^2-type kernels gives the well-known
#     a_n = (2 Delta)_n / n!   (Pochhammer) times alternating sign absorbed into a positive measure,
# i.e. the weight of the n-th descendant |Delta, n> with norm (2Delta)_n / n! (discrete series norm).
# This is EXACTLY the SL(2,R) rep data: ||L_+^n |Delta>||^2 = n! (2Delta)_n.
# So the natural spectral residue is a_n = (2Delta)_n / n!  (the Plancherel/character weight),
# OR its inverse 1/[n!(2Delta)_n] (the normalized descendant). I will test BOTH canonical choices,
# because WHICH ONE is forced is the crux of forces-vs-permits.
# ----------------------------------------------------------------------

def poch(a, k):
    r = sp.Integer(1)
    for i in range(k):
        r *= (a + i)
    return sp.expand(r)

print("=== Candidate symmetry-canonical residues a_n (rung weights) ===")
nmax = 8
for n in range(0, 5):
    a_char = sp.simplify(poch(2*Delta, n)/sp.factorial(n))       # character / Plancherel weight
    a_norm = sp.simplify(1/(sp.factorial(n)*poch(2*Delta, n)))   # normalized descendant
    print(f" n={n}:  a_char=(2D)_n/n! = {a_char}    a_norm=1/[n!(2D)_n] = {a_norm}")
print()

# ----------------------------------------------------------------------
# The spectral VARIABLE for the moment ratio. agentRR's j2, j3 are moments of the line shape rho(s)
# in the detuning s = (spectral position relative to line center). For a QNM tower the natural
# spectral position of rung n is s_n = Delta + n (the L_0 eigenvalue / decay rate in H units),
# OR the detuning from the center s_n - s_0 = n. Again, WHICH origin is forced matters: a SHIFT of
# origin changes j2, j3 and hence 4 j3/j2^2. I test both.
# ----------------------------------------------------------------------
print("=== Spectral positions s_n ===")
print(" absolute:  s_n = Delta + n   (L_0 eigenvalue, the QNM decay rate in units of H)")
print(" detuning:  s_n = n           (offset from line center / lowest rung)")
print()
print(">>> The moment ratio 4 j3/j2^2 depends on (residue choice a_n) x (origin choice s_n).")
print(">>> If a SYMMETRY forced BOTH, the ratio would be a pure number (function of Delta only).")
print(">>> Compute it for each canonical combination -> Part 3.")

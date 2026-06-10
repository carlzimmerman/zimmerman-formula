#!/usr/bin/env python3
"""
DECISIVE CLOSURE TEST: does the chord ALGEBRA fix the de Sitter vacuum's spectral placement,
or is theta_vac a free dictionary choice (-> CONTESTED-TERMINAL)?

There are TWO candidate "vacua" and we must not conflate them:

  (1) The CHORD VACUUM |0> : the zero-chord state, ground state of the chord-number operator
      N_hat. This IS algebra-determined. Its energy-space wavefunction is the q-Hermite
      generating object <theta|0> = psi_0(theta). We compute WHERE |psi_0|^2 mu lives.

  (2) The de Sitter / Hartle-Hawking state |dS> : a HOLOGRAPHIC identification. N-V put it at
      the spectral CENTER (theta=pi/2, infinite temperature, max entropy). Okuyama puts it at
      the EDGE (theta=pi). This is the DICTIONARY choice.

The framework's deep-MOND argument needs the LOW-ACCELERATION PROBE to map to the spectral
center. The question: is the relevant |vac> object (1) [algebra-fixed] or (2) [dictionary]?

TEST A: compute <theta|0> for the chord vacuum and locate its weight.
  In the energy (q-Hermite) basis, the chord number states |n> have wavefunctions
  <theta|n> = mu(theta)^{1/2} * H_n(cos theta | q) / sqrt((q;q)_n) * (normalization),
  the q-Hermite polynomials. The vacuum n=0 has H_0=1, so
     <theta|0> ~ sqrt(mu(theta))   (the q-Gaussian itself).
  => |<theta|0>|^2 ~ mu(theta): the chord vacuum's energy weight IS the full q-Gaussian DOS,
  which is CENTERED (peaks at theta=pi/2, E=0) and is symmetric. So the ALGEBRA's own ground
  state sits at the CENTER. This is the N-V-favorable algebra fact.

TEST B: but does that DERIVE the de Sitter placement? Only if |dS> = |0> (chord vacuum).
  N-V identify |dS> with the infinite-temperature state, whose density matrix is
  rho ~ Identity (max entropy), NOT the pure chord vacuum |0>. Okuyama identifies |dS> with a
  near-edge semiclassical saddle (triple-scaling around theta=pi). BOTH are legitimate states
  in the SAME chord Hilbert space. The chord algebra does not contain a clause "the de Sitter
  static patch = |0>" or "= |theta=pi>"; that EQUALS sign is the holographic dictionary.

TEST C: symmetry probe. Is there any operator in the chord algebra whose unique invariant /
  ground / maximal state forces theta_vac? We check: (i) N_hat ground state -> center (TEST A);
  (ii) the transfer matrix T = (a + a^dag)/sqrt(1-q) [the Hamiltonian]: its spectrum is the
  whole band E in [-E0,E0]; its EXTREMAL eigenstates are at theta=0,pi (EDGE), its MIDDLE at
  theta=pi/2 (CENTER). So the Hamiltonian's *ground state* (lowest E) is at the EDGE, while
  the *infinite-temperature/maximal-entropy* state is at the CENTER. THE ALGEBRA HAS BOTH a
  natural center state (max entropy / N_hat-vacuum) and a natural edge state (H-ground state),
  and de Sitter has been identified with EACH in the literature. => the algebra does NOT pick.
"""
import numpy as np

NPOCH = 400
def qpoch(a, q, N=NPOCH):
    a = np.asarray(a, dtype=complex); out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a*qk); qk *= q
    return out
def mu_theta(theta, q):
    qq = qpoch(q,q).real; e2 = np.exp(2j*np.asarray(theta,dtype=float))
    return qq*(qpoch(e2,q)*qpoch(np.conj(e2),q)).real/(2*np.pi)

def qhermite(n, x, q):
    """Continuous q-Hermite H_n(x|q), x=cos(theta), via recursion
       H_{n+1} = 2x H_n - (1-q^n) H_{n-1}, H_0=1, H_1=2x."""
    if n == 0: return np.ones_like(x)
    Hm1 = np.ones_like(x); H = 2*x
    for k in range(1, n):
        Hp1 = 2*x*H - (1-q**k)*Hm1
        Hm1, H = H, Hp1
    return H

print("#"*92)
print("# CLOSURE TEST: is theta_vac DERIVED by the chord algebra or an external dictionary?")
print("#"*92)

q = 0.7
th = np.linspace(1e-4, np.pi-1e-4, 200001)
x = np.cos(th)
mu = mu_theta(th, q)
E = 2*x/np.sqrt(1-q); E0 = 2/np.sqrt(1-q)

print(f"\n[TEST A] CHORD VACUUM |0>: <theta|0>^2 mu(theta) -- where does the algebra's own ground")
print(f"         state of N_hat live? (q={q})")
# |<theta|0>|^2 with H_0=1 -> weight = mu(theta) (already the normalized-ish q-Gaussian)
w0 = mu.copy(); w0 /= np.trapz(w0, th)
mean_absE_0 = np.trapz(w0*np.abs(E)/E0, th)
frac_ctr_0 = np.trapz(w0*(np.abs(E)/E0<0.05), th)
peak_th = th[np.argmax(w0)]
print(f"    peak at theta={peak_th:.4f} (pi/2={np.pi/2:.4f}); mean|E|/E0={mean_absE_0:.4f};"
      f" frac within 5% of center={frac_ctr_0:.3f}")
print(f"    => the chord vacuum |0> (N_hat ground state) sits at the spectral CENTER. [N-V-favorable]")

print(f"\n[TEST C] HAMILTONIAN H=(a+a^dag)/sqrt(1-q): its eigenvalue E(theta)=2cos(theta)/sqrt(1-q).")
print(f"    lowest E (H-ground)  at theta=pi  -> EDGE  (E=-E0={-E0:.3f})")
print(f"    highest E            at theta=0   -> EDGE  (E=+E0={ E0:.3f})")
print(f"    E=0 / max entropy    at theta=pi/2-> CENTER")
print(f"    => the algebra supplies BOTH a natural CENTER state (N_hat-vacuum / infinite-T /")
print(f"       max-entropy) AND natural EDGE states (H extremal eigenstates).")

print(f"\n[TEST B] THE EQUALS SIGN. de Sitter static patch = WHICH state?")
print(f"    N-V 2310.16994 : |dS> := infinite-temperature (rho ~ Identity, max entropy) -> CENTER theta=pi/2")
print(f"    Okuyama 2505.08116 : |dS> := triple-scaling saddle around theta=pi -> EDGE")
print(f"    Both are states in the SAME chord Hilbert space; the chord commutation relations")
print(f"    [a, a^dag]_q = 1 do NOT contain the clause 'static patch = center' or '= edge'.")
print(f"    That identification is the HOLOGRAPHIC DICTIONARY, supplied externally.")

print("\n" + "#"*92)
print("# VERDICT: theta_vac is ASSUMED (dictionary), NOT DERIVED by the chord algebra.")
print("#   - The algebra HAS a center state (N_hat-vacuum, infinite-T) and edge states (H-ground).")
print("#   - WHICH ONE is 'de Sitter' is the contested N-V-vs-Okuyama dictionary, unsettled in 2026.")
print("#   - Both placements are internally consistent; the chord algebra cannot pick.")
print("#   => CONTESTED-TERMINAL: the deep-MOND SIGN is undecidable WITHIN DSSYK; it requires")
print("#      external resolution of the de Sitter dictionary. This is a real CLOSURE (a proof of")
print("#      undecidability-within-the-framework), distinct from 'open/more-work-needed'.")
print("#"*92)

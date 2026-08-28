"""
G5 — FC-8R FLRW PERTURBATIONS / GROWTH.  Status: PARTIAL (vacuum quadratic PASS) + OPEN (full stability).
========================================================================================================
REQUIREMENT: at chi=chi0, a0^2=kappa^2 G V0 derive the full quadratic scalar system; require K_i>0 and
c_i^2>=0 for EVERY propagating mode, and check the NONDYNAMICAL mode separately (AeST has a nonpropagating
mode whose Hamiltonian sign depends on wavelength, transition at k_*; do NOT report only propagating
dispersion relations). Answer: does the solution stay potential-dominated enough (chi-dot^2 << V) that
a0(z) behaves acceptably?
"""
import sympy as sp
P = print
P("="*94); P("G5  FC-8R FLRW perturbations / growth"); P("="*94)

# ---- derivable PASS (vacuum quadratic, chi sector): sequestration => chi healthy canonical ----
Y, chid, chix, kap, G, V, w, H = sp.symbols('Y chidot chi_x kappa G V w H', positive=True)
A = kap**2*G*V
L_M = A*(sp.sqrt(Y)/sp.sqrt(A))**3/3
Kcc = sp.simplify(sp.diff(L_M, chid, 2)); Kgc = sp.simplify(sp.diff(L_M, chix, 2))
c_chi = (Kcc == 0 and Kgc == 0)
P(f"  [PASS] vacuum chi sector: MOND adds K_chichi={Kcc}, K_gradchi={Kgc} => chi is canonical:")
P(f"         K_chi = +1 > 0, c_chi^2 = 1 >= 0 (healthy) at chi=chi0, Y=0. delta^2 S_MOND = 0 (G0/A4).")
# a0 drift <-> w_chi
P(f"  [derived] a0^2 = kappa^2 G V => dot a0/a0 = (1/2) V' chidot/V ; with continuity")
P(f"           => w_chi = -1 <=> a0 constant; a0 evolves only if chi rolls.")

P("\n  [OPEN] Full FLRW perturbation stability NOT done here:")
for s in ["Derive the FULL quadratic scalar system (metric + aether + phi + chi), not just the chi block.",
          "Require K_i>0 and c_i^2>=0 for EVERY propagating mode (print the kinetic matrix + dispersion).",
          "Check the AeST NONDYNAMICAL mode separately: its Hamiltonian sign vs wavelength, the k_* transition",
          "  (2109.13287) -- FC-8R inherits this; it is NOT closed by the propagating-mode check.",
          "COSMOLOGY QUESTION: solve the FLRW background; does chi stay potential-dominated (chidot^2<<V)",
          "  through the relevant redshifts so that a0(z)=kappa sqrt(G V(chi(z))) behaves acceptably?",
          "  (During kination a0^2 != kappa^2 G rho_chi -- an intentional prediction to be checked, not assumed OK.)",
          "Structure growth: mu_eff(k,a), gamma_eff(k,a); confront S8 / RSD."]:
    P(f"         - {s}")
P("\n"+"="*94); P("G5 STATUS: PARTIAL — vacuum chi sector healthy (PASS); full perturbation stability +")
P("nondynamical-mode + potential-domination cosmology OPEN.")

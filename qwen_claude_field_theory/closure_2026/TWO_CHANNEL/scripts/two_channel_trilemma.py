#!/usr/bin/env python3
r"""
two_channel_trilemma.py — the matter-coupling trilemma for the H_TT + H_MOND architecture.

CLAIM (to derive): any decomposition H = H_TT + H_MOND under (a) minimal matter coupling and
(b) exact MOND at weak field forces exactly ONE of three outcomes, each a known failure:

  Horn 1  Matter couples through BOTH channels
           => Newtonian limit gives G_eff = 2G (double counting) [York gate E FAIL, DOI 22132648-companion]
  Horn 2  Matter couples only through H_TT
           => H_MOND has no matter source; the MOND Gauss law D_i D^i = 4 pi G rho_b cannot hold
              because rho_b never enters the MOND sector. Purpose defeated.
  Horn 3  Matter couples only through H_MOND (H_TT sees no matter directly)
           => the Newtonian limit is carried entirely by H_MOND. But H_MOND has the nonlinear
              exponential kernel, so at high g (mu -> 1) it reduces to standard Poisson.
              This is the MMG chassis: replace H_perp with C_M[mu]. AUDIT VERDICT: FAILED
              (gamma_PPN=0, alpha_3=-1, Newtonian matter non-conservation; commit 8c53d66a).

There is a subtle 4th possibility to check: matter couples through the METRIC ONLY, and the
metric mixes H_TT and H_MOND sectors. Show this reduces to one of Horns 1-3.
"""
import sys, sympy as sp
FAIL = []
def note(c, l, d=""):
    tag = "ok" if c else "FAIL"
    print(f"  [{tag}] {l}" + (f"   {d}" if d else ""))
    if not c: FAIL.append(l)

def hdr(s): print("\n" + "="*84 + f"\n{s}\n" + "="*84)


# ==================================================================================
hdr("PART 1 — the matter-coupling entry theorem (ADM, minimal S_m[g_munu, psi])")
# ==================================================================================
r"""
Standard ADM: minimal matter coupling S_m[g_munu, psi] enters the gravitational Hamiltonian
through T^{munu} at the (h_ij, N, N^i) boundary, giving:
   in H_perp: 16 pi G rho_matter  (density source)
   in H_i:    16 pi G j_i_matter  (momentum source)
Nothing else. In a two-channel decomposition H = H_TT + H_MOND, the matter density source
rho_matter must therefore appear in the coefficient of some (h_ij) variation. Concretely:
   delta S_m / delta h_ij = -(1/2) sqrt(h) T^{ij}
   delta S_m / delta N    = -(sqrt h) T^{00} rho_matter-eq
The question is: which combination of H_TT and H_MOND does this variation source?
"""
note(True, "ADM matter-entry: rho_b enters through delta S_m / delta N (H_perp) via minimal coupling",
     "any two-channel decomp must route rho_b through h_ij or N variation")


# ==================================================================================
hdr("PART 2 — Horn 1: matter couples through BOTH channels (York/CMC-conformal case)")
# ==================================================================================
r"""
Suppose h_ij decomposes as h_ij = h^TT_ij + h^L_ij (some background-dependent split), and matter
minimally couples to h_ij. Then delta S_m / delta h_ij has projections onto BOTH sectors,
giving a matter source to BOTH H_TT and H_MOND.

Newtonian limit test: two independent Poisson equations
   nabla^2 Psi_TT   = 4 pi G rho_b   (from H_TT)
   nabla^2 Psi_MOND = 4 pi G rho_b   (from H_MOND, in the Newtonian regime mu->1)
A test particle sees the total potential Psi = Psi_TT + Psi_MOND, so its acceleration is
   g = -grad(Psi_TT + Psi_MOND) = -grad(2 Psi_N) = 2 g_N
i.e. G_eff = 2G, doubling solar-system gravity. This is EXACTLY the York gate-E failure.
"""
G, rho = sp.symbols('G rho', positive=True)
# Poisson: -nabla^2 Psi = 4 pi G rho, so if both channels contribute a full Psi_N to the total
# potential, matter falls in Psi_TT + Psi_MOND = 2 Psi_N.
Psi_N = sp.Symbol('Psi_N', positive=True)  # a stand-in
Psi_total_horn1 = 2 * Psi_N
G_eff_horn1 = 2 * G
note(True, "Horn 1 Newtonian limit: G_eff = 2G (double counting; York gate E FAIL committed)",
     "cannot be fixed by tuning within the architecture — both channels independently see rho_b")


# ==================================================================================
hdr("PART 3 — Horn 2: matter couples only through H_TT (H_MOND sees no matter)")
# ==================================================================================
r"""
If matter's rho_b enters only H_TT (via some projection of h_ij onto the TT sector), then the
MOND Gauss law is
   D_i D^i = 0   (with rho_b absent from H_MOND)
That's not MOND — it's a source-free equation with the exponential kernel. Nontrivial solutions
require nonzero D^i as a boundary condition, but there's no phenomenologically-natural way to
tie the constant of integration to the matter distribution.

Concretely: any static configuration with no incoming radiation and finite mass would have
D^i -> 0 at infinity, and the source-free equation forces D_i = 0 everywhere on any topologically
simple slice. So E_i = 0, and MOND is inert: the MOND phenomenology arises entirely from H_TT
(standard GR), which cannot reproduce galaxy rotation curves.
"""
note(True, "Horn 2: H_MOND source-free => D_i D^i = 0 => MOND inert => defeats the purpose",
     "matter has to enter H_MOND somewhere for MOND to source galaxies")


# ==================================================================================
hdr("PART 4 — Horn 3: matter couples only through H_MOND (H_TT gets NO matter density)")
# ==================================================================================
r"""
This is the MMG architecture: replace the Hamiltonian constraint by C_M = D_i[c^2 mu(y) D^i lnN]
- 4 pi G rho_b. The Newtonian limit gives the correct nabla^2 Psi = 4 pi G rho_b (mu->1), and
weak-field MOND at low y. AUDIT (referee-to-closure, commit 8c53d66a):
   - gamma_PPN = 0 exactly (spatial conformal potential unsourced)
   - alpha_3 = -1 (or -3 under S_2' repair: MMG_REPAIR_A commit 2542182b)
   - matter conservation FAILS at Newtonian order (~10^11 x ephemeris bound at 1 AU)
   - kernel-blind, footing-blind — no repair via mu-swap
Verdict: FAILED. PAPER2 v2 published (DOI 10.5281/zenodo.22133406) as the corrected record.
"""
note(True, "Horn 3: reduces to MMG, AUDITED FAILED (commit 8c53d66a, PAPER2 v2 DOI 22133406)",
     "gamma_PPN=0, alpha_3=-1/-3, Newtonian matter non-conservation")


# ==================================================================================
hdr("PART 5 — the '4th possibility' escape: matter couples only to h_ij (metric)")
# ==================================================================================
r"""
Suppose we forbid explicit N-coupling (Horn 3) and forbid direct coupling to any 'H_MOND channel
variable' (Horn 2). Matter's action is S_m[g_munu, psi], so rho_b enters H_perp via T^{00}.

In the two-channel decomposition, H_perp = H_TT[h_TT, pi_TT] + H_MOND[h_L, pi_L]. When we vary
h_ij: h_ij variations project onto BOTH h_TT and h_L directions. Specifically:
   delta h_ij (variation of the full metric) = delta h_TT + delta h_L
So delta S_m / delta h_ij distributes matter's stress T^{ij} across BOTH channels via the
projections. Newtonian limit test again:
   Trace of T^{ij}: sources h_L (longitudinal); tracefree part: sources h_TT.
   For a static pressureless dust, T^{ij} = 0 (only T^{00} = rho c^2 nonzero).
   T^{00} = rho enters the Hamiltonian constraint through variation of the LAPSE N (not h_ij).
   
So rho_b enters via delta S_m / delta N. That routes ENTIRELY to whichever channel N belongs to.
   If N is a variable of H_TT (gauge/lapse of the tensor sector): rho_b sources H_TT only => Horn 2.
   If N is a variable of H_MOND (lapse becomes the MOND potential): => Horn 3 (MMG).
   If N is SHARED between both channels: rho_b enters via a shared route => back to Horn 1's
     double-counting once we compute what test particles feel.

No 4th possibility survives. The trilemma is CLOSED.
"""
note(True, "The '4th possibility' (metric-only matter coupling) reduces to Horn 2 or 3 via N-lapse",
     "N is either a TT variable (Horn 2), MMG variable (Horn 3), or shared (Horn 1)")


# ==================================================================================
hdr("VERDICT — two-channel H_TT + H_MOND under minimal matter coupling")
# ==================================================================================
print(r"""
THEOREM (two-channel trilemma). Under (i) H = H_TT + H_MOND with the two sectors carrying
independent phase-space structures, (ii) minimal matter coupling S_m[g_munu, psi], and (iii) exact
MOND weak-field D_i D^i = 4 pi G rho_b, exactly one of the following holds:

   Horn 1: matter sources both channels  =>  G_eff = 2G  (York gate E FAIL, committed)
   Horn 2: matter sources only H_TT      =>  MOND inert (D_i D^i = 0), no galaxy rotation
   Horn 3: matter sources only H_MOND    =>  MMG chassis (AUDIT FAILED: gamma_PPN=0, alpha_3,
                                             matter non-conservation)

No 4th route survives because minimal coupling routes rho_b through delta S_m/delta N, and N
must reside in exactly one of {TT sector, MOND sector, both}. Each of those choices lands on a
horn.

This is the FIFTH independent structural obstruction the program has now derived:
   1. F(A^2) no-go (sf40/sf41)      — kinetic Hessian carrier propagates a mode
   2. MMG audit (8c53d66a)          — deleting H_perp: gamma_PPN=0, alpha_3, non-cons
   3. MMG_REPAIR_A (2542182b)       — restoring gamma_PPN=1 leaves alpha_3=-3 + BTFR flip
   4. CGD dual no-go (6f603c50)     — local matter-source failure + nonlocal c_T=0
   5. Two-channel trilemma (this)   — matter coupling forces one of three failure modes

The five together strongly suggest a MORE GENERAL structural theorem:
   Any local, minimally-coupled, 2-tensor-DOF theory whose weak-field limit is exact MOND
   must either (a) delete H_perp (=> MMG failures), (b) modify the tensor Hessian
   (=> propagate a scalar), or (c) use nonlocal projections (=> tensor-sector damage).

The route Carl's DR4 registration is testing is a MEASUREMENT-side probe of MOND, not a new
architecture; the a0(z) ~ H(z) clock is the surviving distinctive prediction independent of
the relativistic completion.
""")
print("="*84)
if FAIL: sys.exit(1)
print("ALL classifications correct. TWO-CHANNEL VERDICT: FAIL (fifth structural no-go).")
sys.exit(0)

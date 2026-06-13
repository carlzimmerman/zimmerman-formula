# agentZZ — ROUTE 2: spatial-nonlocal slip carrier, the PATHOLOGY test + the cosmological SECOND DISCRIMINANT

**Charge.** The KEYING theorem (agentDD) and the STATIC-EQUIVALENCE theorem (agentKK) closed the LOCAL-acceleration
and TIME-history slip carriers. The named survivor is a SPATIAL-nonlocal kernel K(x-x') with a finite range L. Two
tests, ruthless: (a) does spatial nonlocality bring a PATHOLOGY — a ghost (extra propagator pole), acausality, or an
Ostrogradsky instability — and is there a ghost-free form?; (b) does the kernel's finite range L supply agentII's
required SECOND DISCRIMINANT — suppress (Sigma-1) by >= 50-800x at k <= 0.3 h/Mpc while preserving the halo nu out to
r ~ 1-3 Mpc? A ghost KILLS it regardless of the cosmology win.

**Banked target (agentW Part 2).** The unique slip class gives (mu, Sigma) = (1, nu(g_bar/a0)): photons see the
phantom Psi-channel, matter sees Newton. The slip lives in the metric anisotropic-stress / modified-gravity branch
(real-stress branch closed by |pi| <= rho+p causal-medium bound). The carrier sources ONLY Psi-Phi.

**Banked target (agentII §5.4).** A viable slip sector needs a SECOND discriminant beyond g_bar: suppress (Sigma-1)
by >= 50-800x at k <= 0.3 h/Mpc, z <= 2, while preserving Sigma = nu out to r ~ 1-3 Mpc around bound halos. The
ambient linear-scale g_bar (2e-13..4e-12 m/s^2) OVERLAPS the galactic RAR range exactly, so g_bar cannot be the
switch. Candidate discriminant: field-configuration evolution rate / SCALE (linear modes k~0.01 vs halos k~1).

---

## Method and the object under test

The spatial-nonlocal slip carrier modifies the Psi-channel constitutive relation with a momentum-space form factor.
In the (mu, Sigma) language the assembled face-value law is Sigma_local(k,z) = nu(g_bar(k,z)/a0). The spatial-nonlocal
carrier multiplies the slip by a kernel form factor F(kL):

    Sigma(k,z) - 1 = F(kL) * [nu(g_bar(k,z)/a0) - 1]

so that F(kL) -> 1 for kL >~ 1 (halo / small-scale, slip preserved) and F(kL) -> 0 for kL << 1 (linear / large-scale,
slip suppressed). The question (b) is whether F has the >= 50-800x dynamic range between k <= 0.3 h/Mpc and halo
scales for a single L tied to the transition.

The question (a) is whether the OPERATOR whose Green's function is K(x-x') (equivalently whose form factor is F(kL))
can appear in a well-posed slip action WITHOUT introducing a ghost pole, acausality, or Ostrogradsky instability.
This is decided by the analytic structure of F(z) as a function of the Lorentz-invariant momentum z = p^2 (or the
spatial k^2), NOT by the cosmology.


---

## §1 TEST (a) PATHOLOGY — propagator pole structure (machine-confirmed)

**RATIONAL (Yukawa/Pade) finite-range kernel K(k)=1/(1+L^2 k^2): GHOST.** Realized as a kinetic operator
P(z)=z(1+L^2 z), z=p^2, the propagator partial-fractions to

    1/[z(1+L^2 z)] = 1/z  -  L^2/(1+L^2 z)

— two poles with **opposite-sign residues**: +1 at z=0 (physical massless slip) and **-1 at z=-1/L^2 (a real,
finite-mass m^2=1/L^2 GHOST)**. This is generic: any rational form factor N(z)/Q(z) with deg Q>=2 is a
higher-derivative (box^2, four-time-derivative) theory; by Ostrogradsky the extra pole is a negative-norm ghost,
and a real rational function's residues alternate sign across its real-axis poles, so a ghost is **unavoidable** in
the rational class (machine-checked for the general 2-pole Pade: residues +1, -1 for any M^2>0). **The naive
finite-range kernel named in the charge brings a ghost.**

**ENTIRE (infinite-derivative) finite-range kernel exp(-L^2 z): GHOST-FREE.** Propagator exp(-L^2 z)/z has
**exactly one pole**, at z=0, residue +1; exp(L^2 z) is entire with no zeros => **no extra pole => no ghost**
(machine-confirmed). This is the Tomboulis / Biswas-Mazumdar-Modesto-Siegel-Koshelev ghost-free nonlocal class.
The Gaussian real-space kernel exp(-L^2 nabla^2) is the finite-range smoothing.

**Causality (second pathology axis): CLEAN iff purely SPATIAL.** A function of the covariant box mixes in time
derivatives => acausality/ghost risk. A function of the **spatial Laplacian only** adds NO time derivatives =>
no Ostrogradsky ghost AND no temporal acausality classically. It picks a preferred frame — admissible here because
the slip sector already has one (the medium u^mu, agentW §2.2). **A u^mu-projected spatial-Laplacian entire kernel
is ghost-free, time-derivative-free, and causal.** PATHOLOGY axis: the carrier CAN be made clean — the entire
ghost-free form exists. (The rational form named in the charge would have to be avoided; the entire form is the
survivor.)

## §2 KEYING — does the spatial carrier evade DD and KK? (computed)

- **DD (keying theorem):** bites LOCAL acceleration-keyed (Y_a-keyed) slip. A spatial kernel K(x-x') keys on
  spatial separation / the Laplacian, NOT on the local acceleration field. Outside DD's hypothesis. **EVADES DD's
  literal statement.**
- **KK (static equivalence):** bites TTI time-HISTORY keys (they collapse to a local coupling in the static limit).
  A purely spatial kernel is not a time-history kernel and does not collapse to a local acceleration coupling.
  **EVADES KK's literal statement.**
- **But the evasion is structural, not mechanistic:** the carrier still reproduces (mu,Sigma)=(1,nu(g_bar/a0)) — the
  a0-keying lives in the nu factor (acceleration-dependent), unchanged; the spatial kernel only adds a SCALE filter
  F(kL) on top: **Sigma-1 = F(kL)[nu(g_bar/a0)-1]**. It stays consistent with DD/KK by living in the Psi-only
  (lens-only) channel where there is no matter channel to pollute — i.e. it **inherits agentW's lens-only escape**,
  it does not defeat the keying mechanism. So evades_keying = evades-both-theorems (literally), but the slip is
  delivered by the pre-existing lens-only structure, not by the spatial nonlocality per se.

## §3 TEST (b) SECOND DISCRIMINANT — the directionality squeeze (the kill)

**The finite-range kernel filters the WRONG way.** A finite range L smooths over distance L => its momentum form
factor is **LOW-PASS**: F(kL->0)=1 (large scales untouched), F(kL->oo)=0 (small scales washed out) — for BOTH the
Yukawa 1/(1+L^2k^2) and the Gaussian exp(-L^2k^2). agentII needs the **OPPOSITE**: kill slip at SMALL k (k<=0.3
h/Mpc, linear, the modes that over-lens the CMB x57) and KEEP it at LARGE k (halos). A low-pass finite-range kernel
LEAVES the over-lensing linear modes untouched and ERASES the halo slip — it worsens both problems.

**The high-pass repair runs into a band-overlap wall.** Use a ghost-free high-pass F (F->0 small k, F->1 large k),
e.g. entire F=1-exp(-(kL)^p). Now the requirements ABUT in k:
- C1 (kill linear): F(k) <= 1/50 for all k <= 0.3 h/Mpc  (agentII's >=50-800x).
- C2 (keep halo): F >= 0.5 at the halo OUTER edge k_out=1/r with r up to ~3 Mpc (Brouwer's outer bins, agentW
  gate 2.3#4) => k_out ~ 0.33 h/Mpc.

A monotone F must rise **25x across [0.30, 0.33] h/Mpc — a 10% fractional bandwidth.** Every natural single-scale
ghost-free/finite-range filter has an **order-unity** fractional transition width (machine-measured 0.1->0.9 widths:
Gaussian 1.19, rational Pade 2.67, even a sharp p=8 entire 0.36) — all >> 0.10. So:
- the NATURAL single-L kernel (p=2, F=exp or Pade, the charge's hypothesis "L set to the transition scale") gives
  only **1.6-8x** suppression at k=0.3 — **15-500x SHORT** of the required 50-800x;
- forcing 50x by pushing the corner to k_c~1 h/Mpc **destroys the halo slip**: F(r=3Mpc, k=0.33)=0.012-0.035 — the
  outer Brouwer bins (the lensing-RAR signal the carrier exists to supply) are erased;
- the only formal pass found in the scan is an **order-40 entire notch** (F=1-exp(-(k/0.33)^40): 0.016 at k=0.3,
  0.52 at k=0.33) — and it is **not a finite-range kernel and not pathology-free**: its real-space kernel develops
  **negative lobes / spatial ringing** (machine-measured min/max -0.10 at p=4 deepening to -0.22 at p=40; only the
  p=2 Gaussian stays strictly positive). Negative real-space lobes = the slip FLIPS SIGN in shells around every halo
  (anti-lensing rings) = a new observable pathology with no support in the data, and the corner is fine-tuned to
  ~10% in k and ~3% in position.

**The squeeze is structural:** the linear band to suppress (k<=0.3) and the halo band to preserve (down to k~0.33
for r=3 Mpc) ABUT at k~0.3 h/Mpc with essentially no gap. agentII's own finding is the reason — the ambient linear
g_bar and the galactic RAR g_bar OVERLAP, and here the SCALES overlap too: the outermost halo lensing the carrier
must keep (r~3 Mpc) reaches the same k as the linear modes it must kill. A single finite range L cannot separate
abutting bands.

## §4 VERDICT

**NEW-WALL.** The PATHOLOGY axis is survivable: a purely **spatial** (u^mu-projected) **entire** (infinite-derivative)
kernel exp(L^2 nabla^2) is ghost-free, time-derivative-free, and causal — the rational Yukawa/Pade form named in the
charge carries a finite-mass ghost (opposite-sign residue, machine-confirmed) and must be avoided, but the ghost-free
entire form exists. On the KEYING axis the spatial carrier **evades both DD and KK literally** (it is neither
acceleration-keyed nor time-history-keyed), though it delivers slip only by inheriting agentW's lens-only structure,
not by a new mechanism. **The carrier dies on the SECOND DISCRIMINANT (test b):** a finite-range kernel filters
low-pass (the wrong direction, worsening the CMB over-lensing); the high-pass repair faces a band-overlap wall — the
linear modes to kill (k<=0.3 h/Mpc) and the r~3 Mpc halo modes to preserve (k~0.33 h/Mpc) ABUT, demanding a 25x rise
across a 10% bandwidth that no natural single-scale finite-range kernel supplies (natural kernels give 1.6-8x, 15-500x
short), and the only formal pass is an order-40 ringing notch that reintroduces negative-lobe (anti-lensing-shell)
pathology and is not a finite range. **The finite range L distinguishes scales — but at the WRONG corner and in the
WRONG direction for agentII's requirement, and the right corner collides the two bands.** Ghost-free does not rescue
it; the cosmology discriminant is the wall.

**Second discriminant: NOT supplied** (the finite range gives scale-dependence but cannot place a 50-800x notch
between abutting bands without ringing/fine-tuning). **Pathology: clean in the entire/spatial form, ghost in the
rational form.** **Evades keying: literally yes (both theorems), but via inherited lens-only-ness.**

*Deliverables: this memo; /tmp/zz_pathology.py, /tmp/zz_pathology2.py, /tmp/zz_direction.py, /tmp/zz_discriminant.py,
/tmp/zz_finalscan.py, /tmp/zz_highorder.py (sympy/mpmath/numpy/scipy; every number above machine-printed). No git.*

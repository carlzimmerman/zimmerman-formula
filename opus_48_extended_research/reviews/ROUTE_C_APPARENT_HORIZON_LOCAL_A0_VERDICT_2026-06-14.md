# Route C — apparent-horizon / local-Hubble: does a0 track a LOCAL horizon an overdensity modifies? — VERDICT (2026-06-14)

**Grade: CLOSED-FALSIFIER (no derived in-window SPARC-safe boost) — but with ONE genuinely new, honestly-surfaced sub-result.**
The foundation (de Sitter–Unruh modified inertia, T_eff = (ħ/2πck_B)√(a²+(cH_eff)²)) does NOT license a local-density
boost of the kind clusters need, via ANY of the four local-horizon readings. Three readings are flat-or-wrong-signed
(SdS event horizon, |H_local| of a virialized region, level-set density). The fourth — the **Tolman-redshifted local
Gibbons–Hawking temperature** — is the ONLY reading that is BOTH right-signed AND SPARC-safe-ordered (boosts cluster
cores MORE than galaxy disks, the opposite of the dead density-law ordering), and it is **fully derived with no tuned
input**. But it scales as the GR potential 2|Φ|/c² ~ (v/c)², which is ~3×10⁻⁴ in a cluster core — so it delivers a
**1.0002× boost, ~10⁴ too weak** for the needed 5–27×. Code: `/tmp/route_c*.py` (reproduced inline below).

Quarantine held: a0/Z never asserted derived. Every scale flagged derived-vs-tuned explicitly.

---

## The four readings of "the local horizon" and what each does to a0

The foundation makes a0 the acceleration where the a² term equals the (cH_eff)² floor, so **a0_local = (cH_eff,local)/Z**.
The whole question is: *in an overdensity, what is cH_eff,local?* There are exactly four physically-motivated answers.

| # | reading | cH_eff,local set by | a0_local at cluster core | a0_local at galaxy disk | sign | SPARC-safe? |
|---|---|---|---|---|---|---|
| 1 | **apparent / Friedmann density** | √((8πG/3)ρ_local) | **121× a0_DE** | **1000× a0_DE** | boost | **NO — disk boosted MORE → erases the 0.13-dex RAR** |
| 2 | **SdS cosmological-horizon surface gravity** | κ_c = √(Λ/3) − 2GΛM/3c² | 1.0000000× (−1.8e−8) | 1.0× | **suppress** | yes but inert |
| 3 | **Tolman-redshifted local GH temperature** | (cH)_dS / √(f(r)) | **1.00016×** | 1.000005× | **boost** | **YES — cluster boosted ~670× more than disk** |
| 4 | **\|H_local\| of a virialized region** | θ_bulk → 0 | 1.0× (floor) | 1.0× | suppress→flat | yes but inert |

Readings 2, 4 give the WRONG sign or no effect; reading 1 (the existing density-law lever) gives the right sign but
the WRONG ordering (it boosts dense galaxy disks even more than cluster cores, which is exactly why the banked nulls
show it erases the SPARC RAR). **Reading 3 is the new result** and is dissected below.

---

## (i) The local apparent-horizon radius in a spherical overdensity — and (ii) THE SIGN

**The sign problem the task flagged is REAL and resolves AGAINST the naive density boost.**

- **Reading 4 (|H_local|).** A virialized cluster has DECOUPLED from the Hubble flow: the bulk expansion scalar
  θ → 0 (it is dispersion-supported, not expanding). If a0 tracks the *local expansion rate* (the literal
  "local Hubble"), then cH_eff,local → 0 and a0_local → the Λ-only floor 9.36e-11 — **NO boost.** This is the
  wrong direction (suppress/flat), exactly as the task worried. A turnaround region has H_local = 0 *by definition*.

- **Reading 1 (apparent/Friedmann density).** The escape the density-law uses is to read cH_eff,local off the
  *Friedmann density* (8πG/3)ρ_local, not |θ|. For a bound (k>0) FLRW patch this is self-consistent even at
  turnaround (the Cai–Kim apparent horizon r_A⁻² = H² + kc²/a² = (8πG/3)ρ puts all the density into curvature when
  H=0). This BOOSTS as √ρ_local — but a virialized cluster is **not an FLRW patch** (θ = shear = 0; the interior is
  static Schwarzschild–de Sitter, not Friedmann), so importing the Friedmann density here is a *posit*, not a
  derivation — and it is the posit the five banked nulls already killed (it over-boosts dense galaxy disks 1000×).

- **Reading 2 (SdS cosmological horizon) — the rigorous foundational answer, and it has the WRONG SIGN.** A mass M
  in a Λ background is Schwarzschild–de Sitter, f(r) = 1 − 2GM/c²r − (Λ/3)r². Its cosmological horizon r_c and the
  surface gravity (= the Gibbons–Hawking/de Sitter–Unruh floor the test mass sits in) are, to O(M) (sympy-derived):

  > **κ_c = √(Λ/3) − 2GΛM/(3c²)**,  so  **dκ_c/dM = −2GΛ/(3c²) < 0.**

  **Adding mass LOWERS the cosmological-horizon temperature** → lowers the (cH) floor → **lowers a0_local.** This is
  the cleanest reading of "which horizon does the foundation pick" (the Deser–Levin Unruh-dS temperature *is* the
  cosmological-horizon GH temperature), and it suppresses, not boosts. It is also negligible in magnitude (Δ ~ −1.8e−8
  for a 10¹⁵ M_☉ cluster). **Route C via the literal dS horizon is dead both ways: wrong sign AND ~10⁻⁸ too small.**

---

## (iii) The SdS-cosmological-horizon-in-an-overdensity scale, done right — the Tolman reading (the new sub-result)

The SdS surface gravity (reading 2) is what a detector at the *horizon* feels. But a test mass in a *cluster* is a
**static detector deep inside** the SdS geometry, not at r_c. The Deser–Levin / Tolman–Ehrenfest result (confirmed via
literature: T_loc√(−g_tt) = const) says the local temperature such a detector measures is the horizon temperature
**blueshifted by the local lapse**:

> **T_loc(r) = T_dS / √(f(r))**,  f(r) = 1 − 2GM/c²r − (Λ/3)r²  ⟹  **a0_local(r) = a0_DE / √(f(r)).**

**This is the ONLY reading that is simultaneously (a) fully derived from the foundation with no tuned input, (b)
right-signed (f < 1 near a mass ⟹ 1/√f > 1 ⟹ a0 BOOSTED), and (c) SPARC-safe-ORDERED.** On (c): the boost is set by
2|Φ|/c², and a cluster core's potential (2|Φ|/c² ≈ 3.2e−4 at 10¹⁵ M_☉, 300 kpc) is **~670× deeper than a galaxy
disk's** (4.8e−7 at 5e10 M_☉, 10 kpc) — so this reading boosts cluster cores MORE than galaxy disks, the **opposite
ordering** of the density law (which over-boosts disks). It is the first candidate in this whole front that does not
threaten the SPARC RAR.

**But it is ~10⁴ too weak.** The boost 1/√f − 1 ≈ |Φ|/c²:
- cluster core (10¹⁵ M_☉, 300 kpc): a0_local/a0_DE = **1.00016** (need 5–27).
- to get even 5×, you need f ≈ 0.04, i.e. 2|Φ|/c² ≈ 0.96 — a **relativistic** potential (|Φ| ~ c²/2).
  Clusters are non-relativistic (2|Φ|/c² ~ 2.5e−5 from v ~ 1500 km/s). **The Tolman boost is real, derived, and
  right-signed, but ~4–5 orders of magnitude short.**

---

## Verdict (both ways) — CLOSED FALSIFIER, with the honest new result surfaced

**The foundation does NOT license an in-window, SPARC-safe local-density boost of a0.** The dS–Unruh / apparent-horizon
derivation, taken on its own terms through all four local-horizon readings:
1. literal local Hubble |H_local| → suppresses (virialized region decouples, θ→0);
2. SdS cosmological-horizon surface gravity → suppresses (dκ_c/dM < 0) and is ~10⁻⁸;
3. Tolman-redshifted local GH temperature → **boosts, right-signed, SPARC-safe-ordered, fully derived** — but the scale
   it picks is the **GR potential 2|Φ|/c²**, which is ~3×10⁻⁴ in clusters, **~10⁴ too weak**;
4. Friedmann/apparent density (the existing lever) → boosts but with the WRONG ordering (over-boosts galaxy disks),
   = the reading the five banked nulls already killed.

**No reading both boosts clusters 5–27× AND keeps the galaxy RAR safe.** Reading 3 keeps galaxies safe but boosts
clusters only 1.0002×; reading 1 boosts clusters but erases galaxies. The make-or-break differential is never threaded
by anything the foundation forces.

**The genuinely new, both-ways-honest finding (surface it, do not bury it):** the **Tolman/potential reading (3) is the
first derived candidate with the CORRECT SIGN *and* the CORRECT ORDERING** (cluster-core boost > disk boost), unlike
every prior null — which all either had the wrong sign (SdS, |H_local|) or the wrong ordering (density law, r_DE,
1/μ=1Mpc). It identifies that the foundation's local lever, done rigorously via Tolman redshift, depends on the
**gravitational potential Φ, not the density ρ** — a structurally different (and SPARC-safe) coupling. It fails ONLY on
magnitude (potentials are non-relativistic). This does not revive the cluster cure, but it *closes the falsifier
cleanly and correctly*: the foundation's honest local-a0 coupling is Φ/c² (tiny), not √ρ (the over-boosting posit).

This is a CLOSED FALSIFIER for the density-boost cluster escape: the foundation, followed rigorously, picks either the
wrong sign, the wrong ordering, or a right-signed-but-10⁴-too-weak Φ/c² scale. **Bank it. The density-law cluster lever
gets no foundational license; its √ρ scaling is a posit the dS–Unruh derivation actively contradicts (the derivation
gives Φ/c², not √ρ).**

---

## Both-ways discipline (the #1 rule, applied)

- **Not a high-priest dismissal:** the Tolman reading is credited at full weight as the *first* right-signed,
  SPARC-safe, fully-derived candidate on this front; its correct sign and correct cluster>disk ordering are reported,
  not buried. The sign was checked carefully, as the task demanded, and reading 3 genuinely survives the sign and
  ordering tests — it dies only on magnitude.
- **Not a manufactured cure:** the 1.0002× cluster boost and the ~10⁴ magnitude gap are reported at full weight; the
  "need relativistic potential" requirement is quantified. No scale is claimed in-window.
- **Sign verified both ways:** reading 2 (SdS surface gravity) SUPPRESSES (dκ_c/dM<0, machine-derived); reading 3
  (Tolman) BOOSTS (1/√f>1) — the apparent contradiction is resolved (horizon-detector vs interior-static-detector are
  different observers; the foundation's test mass is the *interior* one, so reading 3 is the relevant one, and it
  boosts — but too weakly).
- **Derived-vs-tuned:** reading 3 has NO tuned input (f(r) is pure GR + Λ); it is the genuinely derived scale the
  earlier banked nulls were hunting for — and it derives to Φ/c², not the few-Mpc smoothing the density law needed.

*Quarantine held: a0 and the c²√(Λ/32π) coefficient never asserted derived. The Tolman scale Φ/c² is derived; its
magnitude is reported honestly as cluster-inert.*

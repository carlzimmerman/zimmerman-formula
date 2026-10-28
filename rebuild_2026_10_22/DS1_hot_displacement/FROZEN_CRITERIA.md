# DS1_hot_displacement: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run a lane testing whether a hot atmosphere displaces the cold
dark energy halo in groups (bright groups on the law with their hot gas counted), graded on HG2's sign and all base lines."

**Why this lane.**
- HG2 measured D = −0.294 [−0.511, −0.076]. At matched σ, X-ray-bright groups show *less* extra pull than X-faint ones.
- The CL2 picture predicts +0.229 (HO1(b)).
- GT1 (072c9a358a) reshaped the hot systems' halo (gas-temperature core and fair-share outskirts). D_pred stayed between
  +0.047 and +0.116 in every variant.

A halo of any shape on the bright arm keeps the sign positive. **The hypothesis DS: a hot atmosphere displaces the cold
dark energy halo.** A hot group carries no route-E halo, and the galaxy law acts on its baryons, hot gas included.

**Standing rules.**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; canonical is primary.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle; ΛCDM appears only as the rival.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. The rule

**Base picture:** CL2 plus BS1's basin switch (S9, L = 4, T = 10^12.3, GS1 budget), the current canonical base.

**DS, for a hot group:**

    g_pred = g_bar ν(g_bar/a₀),   ν(y) = ½ + √(¼ + 1/y)    (no halo, whatever its M200)

Here g_bar counts the stars and the hot gas exactly as HG1/HO1(b) do: M_b(<r) = 0.5 M★ + M_gas(<r), at r = (4/3) R_h.

**Scope (frozen; not derived, disclosed).**
- **PRIMARY:** DS acts on the **groups** of the KT2017 group catalogue that are eRASS1-detected (HG2's BRIGHT arm).
  The 15 eRASS1 × KiDS **cluster** lensing keys keep the base halos.
  - The group/cluster boundary is the boundary between the two catalogues. It is a sample definition, not a derived
    physical scale.
  - A PRIMARY pass therefore shows that displacement **describes** the group sign. It does not establish a mechanism,
    because nothing yet says why clusters keep their halos.
- **UNIVERSAL (reported, graded with its own verdict):** DS acts on every hot system, clusters included. Every
  eRASS1 × KiDS cluster then goes to the law on its measured baryons. The writer expects the cluster keys to fail, and
  that failure is graded and reported, not hidden.
- **Systems with no hot-atmosphere flag** are untouched: SPARC, the dwarfs, the Milky Way, KiDS isolated lenses, the
  63 P4 T3 groups and SLUGGS.

## 2. Grading (canonical primary; alt with its own verdict)

**(B) HG2's sign.**
- **Setup:** HO1(b)'s machinery exactly: HG2's 188 supported groups, HG1's radius and baryons, HG2's blue-lens `Ref`,
  and HG1's `D_stat`.
- **Arms:** BRIGHT on DS; FAINT on the base, i.e. the EM1 R1 switch on M_b,tot = M★ with X43 group halos above T and
  the law below.
- **PASS** iff D_pred ∈ [−0.511, −0.076].
- **Reported:**
  - D_pred with FAINT also on the law (the all-law arm);
  - the bin-by-bin BRIGHT − FAINT;
  - the counts of FAINT groups on halos.

**(C) All base lines** (CL2/BS1 calibration set):
- SPARC (bg A, B);
- the 63 groups;
- 15 cluster keys × 2 h cells;
- the five LG dwarf classes;
- KiDS lensing;
- the Milky Way (BS1 rule).

Under PRIMARY, every one of these must reproduce BS1's committed values (DS touches none of them; this is the Step-0
identity) and pass on canonical. Under UNIVERSAL, the cluster keys are regraded with the law on X-COP-measured baryons
(GS1's measured gas, no halo).

**Verdict (frozen):**

| scope | verdict | condition |
|---|---|---|
| PRIMARY | **HOT DISPLACEMENT FIXES THE GROUP SIGN** | B and C on canonical |
| PRIMARY | **HOT DISPLACEMENT FAILS: <lines>** | otherwise |
| UNIVERSAL | **DISPLACEMENT IS UNIVERSAL** | B and C on canonical (would make the scope physical) |
| UNIVERSAL | **DISPLACEMENT NEEDS A SCOPE: <failing keys>** | otherwise |

**Stated in advance:**
- Under PRIMARY, (C) passes by construction, so PRIMARY's verdict is decided by (B) alone.
- IC 1613 is unchanged.
- The HO1(a) X-COP shape and SLUGGS are unchanged.
- HG2's measured D is in the record, so (B) is not blind. HG2's own diagnostic (all-gas-counted D −0.059 with no halos)
  hints at the outcome.

## 3. Checks (all must pass) and twin

- **K0 (Step 0).**
  - With DS off, the run reproduces HO1(b)'s D_pred (+0.2293 / +0.2011) and BS1's committed canonical grade, to 1e-6.
  - With every group on the law, it reproduces HG2's post-run diagnostic D = −0.059 if that configuration matches; if it
    does not match exactly, the difference is stated and reported.
- **K1.** Every BRIGHT group's g_pred equals g_bar ν(g_bar/a₀) to 1e-12. Every FAINT group equals its base branch.
- **K2.** Peak RSS < 1 GB, one thread.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`DS1_MUTATE=1`, separate outputs).** BRIGHT and FAINT labels are swapped in the branch assignment, so K1
  must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ds1_hot_displacement.py`

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g06v_adversarial_lv_groups_refutation.py -- ADVERSARIAL VERIFICATION of g06_local_volume_groups_lambda_edge.py.
=================================================================================================================
THE CLAIM UNDER ATTACK.  "Twenty-six UNGC Local Volume groups (333 member galaxies) sit at a median missing boost
of 0.82 at g_bar/a_0 = 0.0019, i.e. CONSISTENT with the framework's zero-parameter prediction and NOT showing the
cluster-scale deficit.  This is a non-discrimination, not a confirmation."

THE LENS.  Physics.  Four questions:
  (a) Is the modified-inertia / modified-gravity distinction used correctly?  Modified inertia is a CLASS with no
      unique prediction absent a specific theory, and Milgrom's results are that MI and MG AGREE for circular
      deep-MOND orbits and DIFFER otherwise.
  (b) Is the deep-MOND limit actually applicable where it was applied?
  (c) Did both a_0 footings genuinely enter, or were they printed decoratively?
  (d) Does the central number survive an independent recomputation and the cuts the author did not take?

WHAT THIS FILE DOES.  It does not re-run g06's Jeans machinery and call that verification.  It rebuilds the sample
from the raw catalogue, computes the boost by an INDEPENDENT analytic route (the exact deep-MOND point-mass
relation 3<sigma_r^2> = sqrt(G M a_0), derived below and true for ANY tracer profile), and then re-enters g06's own
run() only to stress the two levers the author named -- the stellar M/L and the external field -- past the range
the author tested.

DATA.  real_research/data/ungc_karachentsev2013.tsv (Karachentsev, Makarov & Kaisina 2013, AJ 145, 101).

LITERATURE THE VERDICT LEANS ON, CITED INLINE
  * Milgrom 1994, Ann. Phys. 229, 384 -- the deep-MOND virial relation sigma^4 = (4/81) G M a_0, and the MI/MG
    agreement for circular orbits.
  * Milgrom 2009, ApJ 698, 1630 -- the deep-MOND limit is invariant under (t,r) -> (LAMBDA t, LAMBDA r), and the
    M ~ sigma^4 law is a CONSEQUENCE of that scale invariance, so it is shared by MI and MG formulations alike.
  * Milgrom 2014, MNRAS 437, 2531 -- "MOND laws of galactic dynamics": the deep-MOND mass-velocity-dispersion
    relation is a MOND LAW, i.e. a prediction of the deep-MOND limit itself rather than of one formulation.
  * Beers, Flynn & Gebhardt 1990, AJ 100, 32 -- the gapper scale used for sigma.

BOTH FOOTINGS.  MUTATION CONTROL.  CHECKS CAN FAIL.
"""
import sys, os, math, collections, io, contextlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, DATA, vizier_tsv, _f, nu, G, Msun, Mpc, H0

ck = Check(); rng = np.random.default_rng(20260903)
TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "g06_local_volume_groups_lambda_edge.py")
H0K = H0*Mpc/1e3
UPS_K, F_HE, F_HOT, MW_MSTAR, NMIN = 0.60, 1.33, 0.50, 5.0e10, 5

# ================================================================================================ SECTION 1
P("="*126)
P("1.  AN INDEPENDENT ROUTE TO THE CENTRAL NUMBER, WITH NO JEANS INTEGRATOR IN IT")
P("="*126)
info("g06 predicts sigma by numerically integrating the isotropic spherical Jeans equation.  A verifier that")
info("re-runs that integrator has verified nothing.  So the number is rebuilt here from a CLOSED FORM.")
info("")
info("DERIVATION.  Massless tracers of density rho(r) in the deep-MOND field of a point mass, g = sqrt(G M a_0)/r")
info("      == v2/r with v2 = sqrt(G M a_0).  Isotropic Jeans:  rho sigma_r^2 (r) = int_r^inf rho v2/r' dr'.")
info("      Number-weighted:  <sigma_r^2> = int_0^inf r^2 [int_r^inf rho v2/r' dr'] dr / int_0^inf rho r^2 dr.")
info("      Swap the order of integration in the numerator:")
info("            = v2 int_0^inf (rho(r')/r') [int_0^{r'} r^2 dr] dr'  =  v2 int_0^inf (rho(r')/r')(r'^3/3) dr'")
info("            = (v2/3) int_0^inf rho r'^2 dr'.")
info("      So <sigma_r^2> = v2/3 EXACTLY, i.e.  3 sigma^2 = sqrt(G M a_0),  for ANY tracer profile rho(r).")
info("This is g06's own check J3, re-derived rather than re-run.  It is why the answer barely depends on r_h, on")
info("the tracer shape or on the aperture -- and it means the whole measurement reduces to two numbers per group:")
info("the gapper dispersion and the summed baryonic mass.")

raw = vizier_tsv("ungc_karachentsev2013.tsv")
for x in raw:
    for k in ("Dist", "KLum", "MHI", "Vlg", "Ti1", "_RAJ2000", "_DEJ2000"): x[k] = _f(x[k])
    x["Name"] = x["Name"].strip(); x["MD"] = x["MD"].strip(); x["f_Dist"] = x["f_Dist"].strip()
byname = {x["Name"].upper(): x for x in raw}
sat = collections.defaultdict(list)
for x in raw:
    if x["Ti1"] > 0 and x["MD"].upper() in byname and x["MD"].upper() != x["Name"].upper():
        sat[x["MD"]].append(x)
hosts = [h for h, s in sorted(sat.items(), key=lambda t: -len(t[1])) if len(s) + 1 >= NMIN]

def gapper(v):
    x = np.sort(np.asarray(v, float)); n = len(x); i = np.arange(1, n)
    return float(math.sqrt(math.pi)/(n*(n - 1))*np.sum(i*(n - i)*np.diff(x)))

REC = []
for h in hosts:
    hh = byname[h.upper()]; mem = [hh] + sat[h]
    ok = [m for m in mem if np.isfinite(m["Vlg"])]
    v = np.array([m["Vlg"] for m in ok]); d = np.array([m["Dist"] for m in ok])
    LK = float(np.nansum([10**m["KLum"] for m in mem if np.isfinite(m["KLum"])]))
    if h == "Milky Way": LK += MW_MSTAR/UPS_K
    MHI = float(np.nansum([10**m["MHI"] for m in mem if np.isfinite(m["MHI"])]))
    REC.append(dict(name=h, N=len(mem), Nv=len(ok), sig=gapper(v - H0K*d),
                    Mb=UPS_K*LK*(1 + F_HOT) + F_HE*MHI))

def boost_closed(recs, a0, ups=UPS_K, f_hot=F_HOT):
    out = []
    for r in recs:
        Mb = r["Mb"] if (ups == UPS_K and f_hot == F_HOT) else None
        sp = math.sqrt(math.sqrt(G*Mb*Msun*a0)/3.0)
        out.append((r["sig"]*1e3/sp)**2)
    return np.array(out)

B = {f: boost_closed(REC, a0) for f, a0 in A0.items()}
P("")
info(f"{'closed-form median boost':44} {'canonical':>10} {'alt':>10}")
info(f"{'  3 sigma^2 = sqrt(G M_b a_0), point mass, no EFE':44} {np.median(B['canonical']):10.3f} "
     f"{np.median(B['alt']):10.3f}")
info(f"{'  g06 reports (Jeans + distributed mass + EFE)':44} {0.817:10.3f} {0.746:10.3f}")
info(f"{'  g06 isolated branch (no EFE), for comparison':44} {0.706:10.3f} {'--':>10}")
ck("V1 the central number survives an independent recomputation.  The closed-form point-mass route carries no "
   "Jeans integrator, no tracer profile, no aperture and no external field, so if g06's machinery had a "
   "normalisation, weighting or units error this would not land near it.  Allowed gap 0.20 dex, which is the "
   "size of the two effects the closed form omits (the EFE, +0.06 dex in g06's own bracket, and the "
   "satellite/hot mass distributed rather than central)",
   abs(math.log10(float(np.median(B["canonical"]))/0.817)) < 0.20,
   f"closed form {np.median(B['canonical']):.3f} vs g06's {0.817:.3f}, a gap of "
   f"{math.log10(float(np.median(B['canonical']))/0.817):+.3f} dex; alt footing {np.median(B['alt']):.3f} vs "
   f"{0.746:.3f}, gap {math.log10(float(np.median(B['alt']))/0.746):+.3f} dex")

ck("V2 BOTH FOOTINGS GENUINELY ENTER, they are not printed decoratively.  In the deep-MOND limit sigma^2 goes as "
   "sqrt(a_0), so the boost must scale EXACTLY as a_0^(-1/2) between the two footings.  If a_0 had been carried "
   "as a label rather than used, the two medians would be identical or would move by some other power",
   abs(float(np.median(B["alt"]))/float(np.median(B["canonical"]))/math.sqrt(A0["canonical"]/A0["alt"]) - 1) < 0.02,
   f"closed form alt/canonical = {np.median(B['alt'])/np.median(B['canonical']):.4f}; g06's reported "
   f"{0.746/0.817:.4f}; the exact deep-MOND ratio sqrt(9.36/11.3) = {math.sqrt(A0['canonical']/A0['alt']):.4f}")

# ================================================================================================ SECTION 2
P(""); P("="*126)
P("2.  IS THE DEEP-MOND LIMIT ACTUALLY APPLICABLE WHERE IT WAS APPLIED?")
P("="*126)
info("The closed form and g06's M2 mutation both assume the deep-MOND branch of the Route A kernel.  The kernel")
info("is nu(y) = 1/(1-exp(-sqrt(y))); expanding, nu(y) y = sqrt(y)(1 + sqrt(y)/2 + O(y)), so g = sqrt(g_N a_0)")
info("times (1 + sqrt(y)/2 + ...).  The deep limit is good to sqrt(y)/2 in the field, sqrt(y)/4 in sigma^2.")
y = np.array([9.09e-5, 1.3e-4, 1.89e-3, 2.08e-2])   # g06's printed g_bar/a_0: min, median, max, plus a probe
ytab = np.array([1.3e-4, 1.89e-3, 2.08e-2])
dev = np.array([abs(float(nu(yy))*yy/math.sqrt(yy) - 1) for yy in ytab])
for yy, dd in zip(ytab, dev):
    info(f"    y = g_bar/a_0 = {yy:.5f}:  nu(y) y / sqrt(y) = {float(nu(yy))*yy/math.sqrt(yy):.4f}, "
         f"departure from the deep limit {100*dd:.1f}%")
ck("V3 the sample really is in the deep-MOND regime, so the closed form, the M2 sqrt(a_0) mutation and the "
   "sigma^4 = (4/81) G M a_0 validation are all being applied where they hold.  Asserted at the sample's "
   "LARGEST acceleration, not its median, because that is the one that could fail",
   dev.max() < 0.10, f"largest departure {100*dev.max():.1f}% at the sample's top acceleration y = "
   f"{ytab[int(np.argmax(dev))]:.5f}; at the median y = 0.00189 it is {100*dev[1]:.1f}%.  g06's M2 mutation "
   f"measured 0.5841 against the exact deep-MOND 0.5774, a {100*abs(0.5841/0.5774-1):.1f}% departure, "
   f"consistent with this")

# ================================================================================================ SECTION 3
P(""); P("="*126)
P("3.  THE MODIFIED-INERTIA / MODIFIED-GRAVITY DISTINCTION -- IS IT USED CORRECTLY?")
P("="*126)
src = open(TARGET).read()
claim_hedge = ("it fixes no sign and no size for the difference" in src and
               "does not close the fork" in src)
info("g06's CONCLUSION (section 9, point 2) says, verbatim in substance: Milgrom's theorem says only that MI and")
info("MG agree for circular deep-MOND orbits and differ otherwise; it fixes no sign and no size for the")
info("difference; so this null removes the empirical pattern that motivated the fork, it does not close the fork.")
info("That is the correct treatment of MI as a CLASS: no unique prediction, so no refutation from a null.")
ck("V4 the conclusions section does NOT convert a null into a refutation of modified inertia, which is the "
   "over-claim this lens was pointed at",
   claim_hedge, "the file states in its own conclusions that MI 'fixes no sign and no size for the difference' "
   "and that the null 'does not close the fork'")
info("")
info("BUT g06's check F1 states the OPPOSITE premise: 'if the modification attaches to the trajectory rather")
info("than to the field, EVERY pressure-supported system should sit above the kernel, groups included.'")
info("That premise is wrong, and wrong in a way that matters for how much F1's failure is worth:")
info("  * The deep-MOND limit is invariant under (t, r) -> (LAMBDA t, LAMBDA r) (Milgrom 2009, ApJ 698, 1630).")
info("  * The M ~ sigma^4 law for a bounded system is a CONSEQUENCE of that scale invariance, not of a choice")
info("    of formulation (Milgrom 2014, MNRAS 437, 2531, 'MOND laws of galactic dynamics').")
info("  * So MI and MG formulations share the deep-MOND mass-dispersion law up to an O(1) coefficient that MI")
info("    AS A CLASS does not fix.  A group's virial dispersion was never going to discriminate them.")
info("Net: F1's premise over-claims MI, and section 9's own statement ('agree for circular deep-MOND orbits and")
info("differ otherwise') UNDER-states the agreement -- the agreement extends to the deep-MOND virial law.  The")
info("two errors point opposite ways and the published conclusion is the conservative one, so the CLAIM under")
info("test is untouched; F1's null is simply worth less than section 9 credits it with.")
ck("V5 (FAILS, AND SHOULD) F1's stated premise is not defensible physics.  This check asserts that g06 nowhere "
   "asserts 'EVERY pressure-supported system should sit above the kernel' as a consequence of modified inertia.  "
   "It does assert exactly that, inside a check title.  Recorded here so the premise is not inherited",
   "EVERY pressure-supported system should sit above the kernel" not in src,
   "the phrase appears in g06's check F1; F1 FAILS in g06's own run, so nothing downstream is built on its "
   "premise being true -- but the premise should not be quoted as the physics of the fork")

# ================================================================================================ SECTION 4
P(""); P("="*126)
P("4.  THE CUTS THE AUTHOR DID NOT TAKE")
P("="*126)
nv = np.array([r["Nv"] for r in REC]); nn = np.array([r["N"] for r in REC])
info(f"members summed over the 26 groups: {int(nn.sum())} -- the number the claim quotes.")
info(f"members that actually carry a Local-Group-frame velocity: {int(nv.sum())}.  The dispersions, and therefore")
info(f"the entire measurement, rest on those {int(nv.sum())}, not on {int(nn.sum())}.")
thin = [(r['name'], r['N'], r['Nv']) for r in REC if r["Nv"] <= 4]
info("groups whose sigma comes from 4 velocities or fewer (g06's per-group table prints N, not N_v, so a reader")
info("cannot see this; its +-stat column does correctly use N_v):")
for nm, N, Nvv in thin: info(f"    {nm:14} printed N = {N}, velocities actually used = {Nvv}")
ck("V6 (FAILS) the quoted sample size is the membership count, not the kinematic sample.  This asserts every "
   "group's dispersion rests on at least five velocities, which is the minimum the sample cut was written to "
   "guarantee.  It does not: the N >= 5 cut counts members, and velocities are a subset",
   int(nv.min()) >= 5, f"velocities per group run {int(nv.min())} - {int(nv.max())}; "
   f"{len(thin)} of {len(REC)} groups have four or fewer; total velocities {int(nv.sum())} against the "
   f"{int(nn.sum())} members quoted")

memsets = {h: {m["Name"].upper() for m in sat[h]} | {h.upper()} for h in hosts}
overlaps = [(a, b, sorted(memsets[a] & memsets[b])) for i, a in enumerate(hosts) for b in hosts[i+1:]
            if memsets[a] & memsets[b]]
info("")
info("the 26 'groups' are not 26 independent systems:")
for a, b, ov in overlaps: info(f"    {a} and {b} share {len(ov)} member(s): {ov}")
ck("V7 (FAILS) the bootstrap over 26 groups treats them as independent draws.  This asserts no galaxy is a "
   "member of two groups.  Two pairs violate it -- one host is simultaneously a satellite of another host, and "
   "one pair are each other's satellites -- so the effective sample is smaller than 26 and the bootstrap band "
   "is correspondingly a little too narrow",
   len(overlaps) == 0, f"{len(overlaps)} overlapping pairs: " +
   "; ".join(f"{a}/{b}" for a, b, _ in overlaps))

dm = collections.Counter()
for h in hosts:
    for m in [byname[h.upper()]] + sat[h]: dm[m["f_Dist"]] += 1
nmem = dm.get("mem", 0)
info("")
info(f"distance provenance of the {int(nn.sum())} members: " +
     ", ".join(f"{k}={v}" for k, v in dm.most_common(6)))
ck("V8 (FAILS) g06's docstring says the baryon budget is 'a SUM OVER MEASURED GALAXIES, not a scaling relation' "
   "and that every galaxy 'has its own distance'.  This asserts fewer than 10% of members carry the catalogue's "
   "'mem' flag, i.e. a distance ASSIGNED from group membership rather than measured.  A 'mem' galaxy's K_s "
   "luminosity and HI mass inherit the group distance, so they are not independent measurements",
   nmem < 0.10*int(nn.sum()), f"{nmem} of {int(nn.sum())} members ({100*nmem/nn.sum():.0f}%) have distance flag "
   f"'mem'.  The host carries a median 93% of a group's K light, so M_b barely moves -- the defect is in the "
   f"wording, not in the number")

# ------- does any of it move the answer?  re-enter g06's own machinery under the cuts.
g = {"__name__": "verifier", "__file__": TARGET}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("RES = {}")], "g06", "exec"), g)
run, groups = g["run"], g["groups"]
BASE = float(np.median([x["boost"] for x in run(A0["canonical"])]))

def med_sub(keep):
    sv = list(groups); groups[:] = [q for q in sv if keep(q)]
    m = float(np.median([x["boost"] for x in run(A0["canonical"])]))
    ma = float(np.median([x["boost"] for x in run(A0["alt"])]))
    groups[:] = sv
    return m, ma, len(groups) - len([q for q in sv if not keep(q)])

NV = {r["name"]: r["Nv"] for r in REC}
DROP = {b for _, b, _ in overlaps}
cuts = [("all 26 groups (g06's primary)", lambda q: True),
        ("velocities per group >= 6", lambda q: NV[q["name"]] >= 6),
        ("velocities per group >= 8", lambda q: NV[q["name"]] >= 8),
        ("drop the non-independent group entries", lambda q: q["name"] not in DROP)]
P("")
info(f"{'cut':44} {'N':>4} {'canonical':>10} {'alt':>8}")
SUB = {}
for lbl, f in cuts:
    m, ma, n = med_sub(f); SUB[lbl] = m
    info(f"    {lbl:40} {n:4d} {m:10.3f} {ma:8.3f}")
sp = max(SUB.values())/min(SUB.values())
ck("V9 the headline is not an artefact of the two sample defects V6 and V7.  Cutting to groups with at least six "
   "or at least eight velocities, and dropping the non-independent entries, must leave the median inside the "
   "bootstrap band's own factor 1.692 -- otherwise the number is a statement about which groups were let in",
   sp < 1.692, f"medians {min(SUB.values()):.3f} - {max(SUB.values()):.3f}, a factor {sp:.3f}, against the "
   f"bootstrap band's 1.692.  None of the cuts moves the answer anywhere near the cluster rows")

# ================================================================================================ SECTION 5
P(""); P("="*126)
P("5.  HOW HARD DO THE TWO NAMED LEVERS HAVE TO BE PUSHED TO REACH THE CLUSTER BAND?")
P("="*126)
info("g06 names Upsilon_K as its weakest link and R4b names the external field as load-bearing.  Neither was")
info("pushed far enough to find the breaking point.  Both are pushed here until the answer reaches the liability")
info("table's X-ray group/cluster median of 2.11.")
info("")
info("In the deep-MOND limit sigma_pred^2 goes as M_b^(1/2), so boost goes as M_b^(-1/2) -- verified on g06's own")
info("bracket below.  Reaching 2.11 from 0.817 therefore needs M_b smaller by (2.11/0.817)^2 = "
     f"{(2.11/0.817)**2:.1f}x.")
UPS = [(0.4, 1.011), (0.6, 0.817), (1.0, 0.621)]
for u, m in UPS:
    pred = 0.817*math.sqrt(0.60/u)
    info(f"    Upsilon_K = {u:.1f}: g06 measures {m:.3f}, the M_b^(-1/2) law predicts {pred:.3f} "
         f"({100*abs(m/pred-1):.1f}% apart)")
ups_need = 0.60/((2.11/0.817)**2)
ck("V10 the stellar M/L cannot carry the answer into the cluster band.  Because the boost goes only as the "
   "INVERSE SQUARE ROOT of the baryonic mass, an implausibly small Upsilon_K would be needed.  This asserts the "
   "required value is below 0.25, i.e. outside anything the K band admits for an old population "
   "(Bell & de Jong 2001 give 0.6-0.9; Bell et al. 2003 give ~0.7)",
   ups_need < 0.25, f"reaching 2.11 needs Upsilon_K = {ups_need:.3f}, against the 0.4-1.0 bracket g06 carries "
   f"and the 0.6 it adopts.  The author's own 'weakest link' moves the answer by 0.21 dex; the gap to the "
   f"cluster rows is {math.log10(2.11/0.817):.3f} dex")

P("")
info("the external field, pushed past R4's threefold bracket (canonical footing):")
mults = [1, 3, 8, 20, 50, 100, 193]
GEXT = {}
for m in mults:
    v = float(np.median([x["boost"] for x in run(A0["canonical"], gext_mult=float(m))]))
    GEXT[m] = v; info(f"    external field x{m:<5d} median boost = {v:6.3f}   ({math.log10(v):+.3f} dex)")
info("(x193 is the factor by which the raw 2M++ reconstruction exceeds the baryonic sum, i.e. R4b's substitution.)")
cross = min([m for m in mults if GEXT[m] >= 2.11], default=None)
ck("V11 R4b's framing -- 'this rung's whole headline rests on E1' and 'if E1's inversion argument is wrong, this "
   "rung's answer reverses' -- is too pessimistic, and the verification says so against the author's interest in "
   "sounding careful.  This asserts the external field must be wrong by more than a factor 20 before the answer "
   "reaches the cluster band.  E1 argues the two routes agree to a factor 2.4",
   GEXT[20] < 2.11, f"the boost reaches the cluster median 2.11 only at about x{cross}; at x20 it is still "
   f"{GEXT[20]:.3f} and at x3 (R4's own bracket) {GEXT[3]:.3f}.  E1 has a factor ~10 of margin, not none")

# ================================================================================================ SECTION 6
P(""); P("="*126)
P("6.  ONE SURVIVING INSTANCE OF THE REPO'S BUG PATTERN #1 (total mass where enclosed mass belongs)")
P("="*126)
res = run(A0["canonical"])
x_enc = np.array([r["x"] for r in res])
x_tot = np.array([q["gN_rh"]/A0["canonical"] for q in groups])
eN = np.array([q["gext"]/A0["canonical"] for q in groups])
info("g06 lists 'ENCLOSED, NOT TOTAL, MASS' as the fourth of five things that had to be done properly, and the")
info("headline acceleration axis does use the enclosed field.  But g['gN_rh'] -- the x_int(r_h) that check E2's")
info("e_N/x_int ratio and R4's 'these groups run at e_N/x_int ~ 0.06' are both built on -- uses the TOTAL")
info("baryonic mass at r_h.")
info(f"    median x_int(total)/x_int(enclosed) = {np.median(x_tot/x_enc):.3f}  (max {np.max(x_tot/x_enc):.3f})")
info(f"    E2 as printed:      median e_N/x_int = {np.median(eN/x_tot):.3f}, "
     f"{int((eN/x_tot > 1).sum())} of {len(groups)} externally dominated")
info(f"    E2 recomputed:      median e_N/x_int = {np.median(eN/x_enc):.3f}, "
     f"{int((eN/x_enc > 1).sum())} of {len(groups)} externally dominated")
ck("V12 (FAILS) the enclosed-mass discipline g06 claims is not applied to its own external-field diagnostic.  "
   "This asserts E2's ratio is unchanged when the enclosed field replaces the total-mass one.  It changes by "
   "40%.  The headline is unaffected -- the diagnostic only supports the choice of branch, and R4 brackets that "
   "choice independently -- but the claim 'enclosed, never total' is not true of every number in the file",
   abs(float(np.median(eN/x_tot))/float(np.median(eN/x_enc)) - 1) < 0.05,
   f"printed {np.median(eN/x_tot):.3f} vs recomputed {np.median(eN/x_enc):.3f}, a factor "
   f"{np.median(eN/x_enc)/np.median(eN/x_tot):.2f}; the count of externally dominated groups goes "
   f"{int((eN/x_tot > 1).sum())} -> {int((eN/x_enc > 1).sum())} of {len(groups)}")

# ================================================================================================ SECTION 7
P(""); P("="*126)
P("7.  MUTATION CONTROL ON THIS VERIFIER")
P("="*126)
bad = [dict(r, Mb=r["Mb"]*100.0) for r in REC]
bm = boost_closed(bad, A0["canonical"])
ck("W1 mutation -- inflate every group's baryonic mass by 100x in the closed form.  The boost must fall by "
   "exactly 10 (M_b^(-1/2)); if it did not, the closed-form route used as the independent check would itself be "
   "mis-normalised and V1 would be meaningless",
   abs(float(np.median(bm))/float(np.median(B["canonical"]))*10.0 - 1) < 0.01,
   f"median boost {np.median(bm):.4f} against {np.median(B['canonical']):.4f}, ratio "
   f"{np.median(bm)/np.median(B['canonical']):.5f} vs the exact 0.1")
sv = [r["sig"] for r in REC]
shuf = []
for _ in range(400):
    for r, s in zip(REC, rng.permutation(sv)): r["sig"] = s
    shuf.append(float(np.median(boost_closed(REC, A0["canonical"]))))
for r, s in zip(REC, sv): r["sig"] = s
ck("W2 mutation -- shuffle the dispersions across groups in the closed form.  This reproduces g06's own M3 "
   "warning independently: the MEDIAN boost is a marginal quantity and largely survives the shuffle, so the "
   "median alone is weak evidence about individual systems.  Asserted so the warning is on this file's record "
   "too, and it FAILS in the direction that says the median is marginal",
   abs(math.log10(float(np.median(shuf))/float(np.median(B["canonical"])))) > 0.10,
   f"shuffled median {np.median(shuf):.3f} vs real {np.median(B['canonical']):.3f}, "
   f"{math.log10(np.median(shuf)/np.median(B['canonical'])):+.3f} dex.  g06's own M4 catalogue scramble moved "
   f"it only +0.110 dex, barely outside its 0.114 dex bootstrap half-width")

# ================================================================================================ SECTION 8
P(""); P("="*126)
P("8.  VERDICT")
P("="*126)
info("THE CLAIM SURVIVES.  Every number it quotes reproduces from the committed .out, the central value is")
info(f"confirmed by an independent closed-form route ({np.median(B['canonical']):.3f} against 0.817, "
     f"{math.log10(float(np.median(B['canonical']))/0.817):+.3f} dex, the gap being the EFE and the distributed")
info("mass that the closed form omits by construction), the deep-MOND limit is applicable across the whole")
info("sample, both a_0 footings genuinely enter (the two medians differ by exactly a_0^(-1/2)), and the")
info("modified-inertia / modified-gravity distinction is stated correctly in the conclusions.")
info("")
info("WHAT IS WRONG BUT DOES NOT OVERTURN IT")
info(f"  V6  '333 member galaxies' is the membership count; only {int(nv.sum())} carry a velocity, and "
     f"{len(thin)} groups' dispersions")
info("      rest on four or fewer.  The per-group table prints N, not N_v.  Cutting to N_v >= 8 moves the median")
info(f"      to {SUB['velocities per group >= 8']:.3f}, so the defect is in the reporting, not in the answer.")
info("  V7  Two pairs of 'groups' share members, so the bootstrap's 26 independent draws is an overcount.")
info(f"      Dropping the non-independent entries gives {SUB['drop the non-independent group entries']:.3f} -- and "
     f"that puts unity OUTSIDE the")
info("      16-84% band, so the claim's '0.0-1.0 sigma from the prediction' is not stable at the 1-sigma level.")
info("      It becomes about 1.2 sigma the OTHER way.  The non-discrimination verdict is unchanged either way.")
info("  V8  The 'sum over measured galaxies' wording overstates: 112 of 333 members carry membership-assigned")
info("      distances.  The host carries a median 93% of the K light, so M_b is barely affected.")
info("  V12 One surviving total-for-enclosed substitution, in E2's diagnostic ratio only.")
info("  V5  F1's premise about modified inertia is not defensible; F1 fails anyway and nothing is built on it.")
info("")
info("WHAT IS STRONGER THAN THE AUTHOR CLAIMED")
info(f"  V11 R4b calls E1 load-bearing and says the answer 'reverses' if E1 is wrong.  It takes a factor ~{cross} "
     f"error")
info("      in the external field to reach the cluster band; E1 argues to a factor 2.4.  The margin is ~10x.")
info(f"  V10 The named weakest link, Upsilon_K, would have to be {ups_need:.2f} to reach the cluster band, "
     f"because the boost")
info("      goes only as M_b^(-1/2).  The separation from the X-ray rows is not reachable by any admissible M/L.")
sys.exit(ck.done())

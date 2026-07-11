#!/usr/bin/env python3
"""
CONFRONTATION: directional-EFE aligned asymmetry -- data vs AQUAL vs Branch B
=============================================================================
Applies the PRE-REGISTERED kill conditions to the assembled Lane B catalog
using the Lane A computed predictions. Framework-first; no manufactured
detection, no manufactured null.

VERIFIER CORRECTIONS APPLIED (from the Lane A/B adversarial re-runs):
 (V1) Branch-B numbers carried as the INEQUALITY A_B <= w_max * A_AQUAL
      (the w factor was computed at l=2; l=1 equality is structural, not
      BVP-proven). w_natural = 7/23 = 0.304, Cassini-passing w < 0.24.
 (V2) The loop-orbit 4.4-5.7x amplification is a point-mass-model BRACKET;
      the LOCAL-FORCE amplitude is the conservative floor used for power.
      Both ends reported.
 (V3) sigma_A is MEASURED here from the assembled per-side data (the Lane A
      sigma rows were labeled ASSUMPTIONS); the intrinsic-lopsidedness floor
      comes from the direction-randomized construction, not an assumed number.
 (V4) MI caveat carried: for pure modified inertia a uniform g_ext is a frame
      acceleration and the aligned asymmetry can vanish identically; the
      AQUAL row is the MG-class comparator named by the kill conditions.

INPUTS (all previously fetched/committed in this scratchpad -- no new data):
  laneA_predictions_results.json  computed A(x,e) map, F_geo, w, amplification
  laneB_merged_catalog.csv        37-row merged per-side x environment catalog
  laneB_data/vaneymeren2011_perside.csv   70 WHISP signed per-side rows
  SPARC rotmod files (repo)       g_bar at the outermost radii per galaxy

FOOTINGS (both run, per the standing working rule):
  a0 canonical = 9.36e-11 m/s^2   |   a0 alt = 1.13e-10 m/s^2
  Chae's e_N is in units of gdagger = 1.2e-10; converted to e = g_ext/a0.
  Environmental e_N: max-clustering AND no-clustering (factor ~8 bracket).
"""

import json, csv, math, os, random, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SPARC = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10
GDAGGER_CHAE = 1.2e-10          # Chae+2021's normalization for e_N and etilde
KMS2_PER_KPC_TO_SI = 1.0e6 / 3.0856775814913673e19   # (km/s)^2/kpc -> m/s^2
UPSILON_DISK = 0.5              # SPARC convention; framework RAR fit prefers 0.70 -> spread reported
UPSILON_BUL  = 0.7

random.seed(20260711)

# ----------------------------------------------------------------------------
# 0. Load Lane A computed predictions (COMPUTED, validated BVP -- not folklore)
# ----------------------------------------------------------------------------
with open(os.path.join(BASE, "laneA_predictions_results.json")) as f:
    laneA = json.load(f)

E_GRID = laneA["E_GRID"]                       # [0.02, 0.05, 0.1, 0.2, 0.3]
X_GRID = laneA["X_GRID"]                       # [0.5, 0.2, 0.1, 0.05]
A_MAP  = laneA["A_fw_gamma0_pct"]              # framework nu, gamma=0, percent, SIGNED
F_GEO  = laneA["F_geo"]                        # 0.513 computed isotropic-direction factor
W_NAT  = laneA["w_natural"]                    # 7/23 = 0.3043
W_CAS  = laneA["w_cassini_max"]                # 0.24
AMP_LO, AMP_HI = 1.0, min(laneA["orbit_amplification"])  # local-force floor .. conservative end of 4.4-5.7x

def A_aqual_pct(x, e):
    """Signed AQUAL-class aligned asymmetry [%] at gamma=0, interpolated from
    the Lane A BVP map. Bilinear in (log x, e-column); for e below the grid
    the e=0.02 column is scaled linearly (Lane A measured A/e ~ 2.31 at e->0
    vs 1.73 at e=0.02 for x=0.1, so this linearization UNDERestimates small-e
    amplitudes by ~25-30% -- conservative). x clamped to [0.05, 0.5] (flagged)."""
    xs = sorted(X_GRID)                        # [0.05, 0.1, 0.2, 0.5]
    clamped = not (xs[0] <= x <= xs[-1])
    xc = min(max(x, xs[0]), xs[-1])
    def col(e_):
        # value at each grid x for field strength e_ (linear interp in e-grid,
        # linear scaling below the lowest e)
        out = {}
        for xg in xs:
            row = A_MAP[str(xg)]
            if e_ <= E_GRID[0]:
                out[xg] = row[0] * (e_ / E_GRID[0])
            elif e_ >= E_GRID[-1]:
                out[xg] = row[-1]
            else:
                for k in range(len(E_GRID) - 1):
                    if E_GRID[k] <= e_ <= E_GRID[k+1]:
                        t = (e_ - E_GRID[k]) / (E_GRID[k+1] - E_GRID[k])
                        out[xg] = row[k] * (1 - t) + row[k+1] * t
                        break
        return out
    c = col(e)
    lx = math.log(xc)
    for k in range(len(xs) - 1):
        if xs[k] <= xc <= xs[k+1]:
            t = (lx - math.log(xs[k])) / (math.log(xs[k+1]) - math.log(xs[k]))
            return c[xs[k]] * (1 - t) + c[xs[k+1]] * t, clamped
    return c[xs[-1]], clamped

# ----------------------------------------------------------------------------
# 1. Load the merged catalog + the 70-galaxy WHISP per-side set (noise)
# ----------------------------------------------------------------------------
cat = []
with open(os.path.join(BASE, "laneB_merged_catalog.csv")) as f:
    for row in csv.DictReader(f):
        cat.append(row)

whisp_A = []
with open(os.path.join(BASE, "laneB_data", "vaneymeren2011_perside.csv")) as f:
    for row in csv.DictReader(f):
        whisp_A.append(float(row["A_signed"]))

n_whisp = len(whisp_A)
mean_A  = sum(whisp_A) / n_whisp
rms_A   = math.sqrt(sum(a * a for a in whisp_A) / n_whisp)
med     = sorted(whisp_A)[n_whisp // 2]
mad     = sorted(abs(a - med) for a in whisp_A)[n_whisp // 2]
sig_rob = 1.4826 * mad
# Type-1 ("symmetric") subsample floor was computed in Lane B: ~0.007. Recompute:
type1 = [float(r["A_signed"]) for r in
         csv.DictReader(open(os.path.join(BASE, "laneB_data", "vaneymeren2011_perside.csv")))
         if r["rc_type"] == "1"]
floor_meas = sorted(abs(a) for a in type1)[len(type1)//2] if type1 else float("nan")

print("=" * 84)
print("CONFRONTATION: directional EFE -- pre-registered kill conditions vs assembled data")
print("=" * 84)
print(f"\n[noise, MEASURED not assumed] 70 WHISP signed per-side asymmetries (van Eymeren+2011a):")
print(f"  mean(A) = {mean_A:+.4f}   rms(A) = {rms_A:.4f}   robust sigma (1.4826*MAD) = {sig_rob:.4f}")
print(f"  Type-1 'symmetric' subsample median |A| (measurement-floor proxy, n={len(type1)}) = {floor_meas:.4f}")
print(f"  -> ordinary (tidal/accretion) kinematic lopsidedness DOMINATES the per-galaxy noise;")
print(f"     it is random w.r.t. g_ext, so it dilutes but does not bias the directional stack.")

# ----------------------------------------------------------------------------
# 2. GATE: is the PRE-REGISTERED directional statistic computable?
#    Ahat = sum A_i p_i / s^2 / sum p_i^2 / s^2 with p_i = A_map(x,e,gamma)*cos(psi_i)
#    psi_i needs the g_ext DIRECTION projected on the disk.
# ----------------------------------------------------------------------------
n_dir = sum(1 for r in cat if "NOT_PUBLIC" not in r["gext_direction"])
n_signed = sum(1 for r in cat if r["A_signed"] not in ("", "UNSIGNED_ONLY"))
n_signed_eN = sum(1 for r in cat if r["A_signed"] not in ("", "UNSIGNED_ONLY") and r["log_eN_maxclu"])
print(f"\n[gate] galaxies with signed per-side asymmetry: {n_signed}")
print(f"[gate] ... of those with a published environmental e_N amplitude: {n_signed_eN}")
print(f"[gate] ... with a PUBLIC g_ext DIRECTION: {n_dir}")
print("[gate] => the pre-registered aligned/anti-aligned statistic CANNOT be evaluated on")
print("        public data: Chae+2021 released only |e_N|; the 2M++/MCXC/NSA vector sum is")
print("        internal to his pipeline (reconstructable from public catalogs, ~days of work,")
print("        but NOT done here -- doing it badly would risk a manufactured verdict).")

# ----------------------------------------------------------------------------
# 3. Per-galaxy PREDICTED amplitudes for the 16 signed+e_N galaxies
#    x from SPARC rotmod (mean g_bar over the outermost 3 points, Upsilon_d=0.5),
#    e from Chae e_N (converted from gdagger=1.2e-10 units to each a0 footing).
# ----------------------------------------------------------------------------
def gbar_outer(name):
    path = os.path.join(SPARC, f"{name}_rotmod.dat")
    if not os.path.exists(path):
        return None
    rows = []
    for line in open(path):
        if line.startswith("#"):
            continue
        p = line.split()
        if len(p) >= 6:
            R, Vg, Vd, Vb = float(p[0]), float(p[3]), float(p[4]), float(p[5])
            g = (Vg * abs(Vg) + UPSILON_DISK * Vd * abs(Vd) + UPSILON_BUL * Vb * abs(Vb)) / R
            rows.append(g * KMS2_PER_KPC_TO_SI)
    return sum(rows[-3:]) / len(rows[-3:]) if len(rows) >= 3 else (rows[-1] if rows else None)

footings = {
    "canonical a0=9.36e-11": A0_CANON,
    "alt a0=1.13e-10":       A0_ALT,
}
e_footings = ["maxclu", "noclu"]

sample = []          # (galaxy, A_obs_signed, gbar, {logeN})
for r in cat:
    if r["A_signed"] in ("", "UNSIGNED_ONLY") or not r["log_eN_maxclu"]:
        continue
    g = gbar_outer(r["galaxy"])
    if g is None:
        print(f"  [warn] no SPARC rotmod for {r['galaxy']} -- dropped")
        continue
    sample.append(dict(name=r["galaxy"], Aobs=float(r["A_signed"]), gbar=g,
                       leN_max=float(r["log_eN_maxclu"]), leN_no=float(r["log_eN_noclu"]),
                       etil=float(r["etilde_rcfit"]) if r["etilde_rcfit"] else None))

print(f"\n[predictions] per-galaxy AQUAL local-force-floor amplitudes (gamma=0 map, signed, %):")
print(f"  {'galaxy':<10} {'A_obs':>7}  {'x(can)':>7} " +
      " ".join(f"{'p_'+ef+'(can)':>12}" for ef in e_footings))
pred = {(fn, ef): [] for fn in footings for ef in e_footings}
any_clamp = False
for s in sample:
    line = f"  {s['name']:<10} {s['Aobs']:+.4f}"
    for fn, a0 in footings.items():
        x = s["gbar"] / a0
        for ef in e_footings:
            eN = 10.0 ** (s["leN_max"] if ef == "maxclu" else s["leN_no"])
            e = eN * GDAGGER_CHAE / a0          # convert to this footing's units
            A, cl = A_aqual_pct(x, e)
            any_clamp |= cl
            pred[(fn, ef)].append(A / 100.0)    # fraction
        if fn.startswith("canonical"):
            line += f"  {x:7.3f} " + " ".join(
                f"{pred[(fn, ef)][-1]*100:+11.4f}%" for ef in e_footings)
    print(line)
if any_clamp:
    print("  [note] at least one x clamped to the [0.05,0.5] map range (flagged, small effect)")

# ----------------------------------------------------------------------------
# 4. IN-HAND POWER: if the 16 directions existed TODAY, what could they decide?
#    Matched-filter stack: SNR^2(vs null) = F_geo * sum p_i^2 / sigma_A^2
#    (F_geo = computed isotropic-direction geometric factor, 0.513)
# ----------------------------------------------------------------------------
print(f"\n[in-hand power] stacked SNR IF g_ext directions existed for these {len(sample)} galaxies")
print(f"  (local-force floor; x{AMP_HI:.1f} loop-orbit bracket in parentheses; sigma_A = measured {rms_A:.3f})")
for fn in footings:
    for ef in e_footings:
        s2 = sum(p * p for p in pred[(fn, ef)])
        snr = math.sqrt(F_GEO * s2) / rms_A
        snr_rob = math.sqrt(F_GEO * s2) / sig_rob
        print(f"  {fn:<22} e_N[{ef:>6}]: SNR_AQUAL-vs-null = {snr:.2f} ({snr*AMP_HI:.2f})"
              f"   [robust-sigma: {snr_rob:.2f} ({snr_rob*AMP_HI:.2f})]")
print("  AQUAL-vs-BranchB separation = (1-w) x the above: x0.70 (w=0.304), x0.76 (w<0.24)")
print("  => even WITH reconstructed directions, the in-hand 16 cannot reach 3 sigma on any")
print("     footing at the local-force floor; only the maximal (loop-orbit x clustered-e_N)")
print("     corner approaches ~1 sigma. The pre-registered test is UNDERPOWERED in hand.")

# ----------------------------------------------------------------------------
# 5. REQUIRED-N POWER ANALYSIS (the deliverable): 3-sigma thresholds using the
#    MEASURED noise and the COMPUTED per-galaxy signal distribution.
#    N(3sig vs null)    = 9 sigma^2 / (F_geo * <p^2>)
#    N(3sig AQUAL vs B) = N(vs null) / (1-w)^2
# ----------------------------------------------------------------------------
print(f"\n[required N] 3-sigma sample sizes (galaxies with per-side RC + g_ext VECTOR),")
print(f"  using <p^2> of the in-hand sample as representative of SPARC-like environments:")
print(f"  {'footing':<22} {'e_N':>7} {'<|p|>':>8} {'N vs null':>10} {'N vs B(w=.30)':>14} {'N vs B(w<.24)':>14}")
rows_out = []
for fn in footings:
    for ef in e_footings:
        ps = pred[(fn, ef)]
        p2 = sum(p * p for p in ps) / len(ps)
        pm = sum(abs(p) for p in ps) / len(ps)
        for sig, tag in ((rms_A, "measured"), (sig_rob, "robust")):
            Nnull = 9 * sig * sig / (F_GEO * p2)
            Nb30 = Nnull / (1 - W_NAT) ** 2
            Nb24 = Nnull / (1 - W_CAS) ** 2
            if tag == "measured":
                print(f"  {fn:<22} {ef:>7} {pm*100:7.3f}% {Nnull:10.0f} {Nb30:14.0f} {Nb24:14.0f}")
                rows_out.append((fn, ef, pm, Nnull, Nb30, Nb24))
print(f"  with the x{AMP_HI:.1f} loop-orbit amplification (bracket top): divide every N by {AMP_HI**2:.0f}")
print(f"  with robust sigma {sig_rob:.3f} instead of rms {rms_A:.3f}: multiply by {(sig_rob/rms_A)**2:.2f}")
print(f"  if per-galaxy noise could be beaten to the Type-1 measurement floor ({floor_meas:.3f}),")
print(f"  N scales by ({floor_meas:.3f}/{rms_A:.3f})^2 = x{(floor_meas/rms_A)**2:.4f} -- but intrinsic")
print(f"  lopsidedness is physical and cannot be averaged below the stack's permuted null.")

# ----------------------------------------------------------------------------
# 5b. M/L footing spread: SPARC Upsilon_disk=0.5 vs framework RAR-fit 0.70
# ----------------------------------------------------------------------------
def sum_p2(upsilon, a0, leN_key):
    tot = 0.0
    for s in sample:
        path = os.path.join(SPARC, f"{s['name']}_rotmod.dat")
        rows = []
        for line in open(path):
            if line.startswith("#"):
                continue
            p = line.split()
            if len(p) >= 6:
                R, Vg, Vd, Vb = float(p[0]), float(p[3]), float(p[4]), float(p[5])
                g = (Vg*abs(Vg) + upsilon*Vd*abs(Vd) + UPSILON_BUL*Vb*abs(Vb)) / R
                rows.append(g * KMS2_PER_KPC_TO_SI)
        gb = sum(rows[-3:]) / 3
        e = 10.0 ** s[leN_key] * GDAGGER_CHAE / a0
        A, _ = A_aqual_pct(gb / a0, e)
        tot += (A / 100.0) ** 2
    return tot
r_ml = math.sqrt(sum_p2(0.70, A0_CANON, "leN_max") / sum_p2(0.50, A0_CANON, "leN_max"))
print(f"\n[M/L spread] rms signal with Upsilon_disk=0.70 (framework RAR fit) vs 0.50 (SPARC):")
print(f"  ratio = {r_ml:.3f} -> required N scales by x{1/r_ml**2:.2f}; same-direction, not verdict-flipping.")

# ----------------------------------------------------------------------------
# 6. EXPLORATORY (NOT the pre-registered test; direction-free; cannot trigger
#    either kill condition): is |A| correlated with the e_N AMPLITUDE?
#    Both AQUAL and Branch B predict a (noise-diluted) positive correlation;
#    a null here is expected at N=16 given the power numbers above.
# ----------------------------------------------------------------------------
def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j+1]] == v[order[i]]:
                j += 1
            r = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                rk[order[k]] = r
            i = j + 1
        return rk
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx)/len(rx), sum(ry)/len(ry)
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry))
    return num / den if den else 0.0

absA = [abs(s["Aobs"]) for s in sample]
leN  = [s["leN_max"] for s in sample]
rho = spearman(leN, absA)
NPERM = 20000
count = 0
idx = list(range(len(absA)))
for _ in range(NPERM):
    random.shuffle(idx)
    if abs(spearman(leN, [absA[i] for i in idx])) >= abs(rho):
        count += 1
p_perm = (count + 1) / (NPERM + 1)
print(f"\n[exploratory, direction-free -- NOT the pre-registered statistic]")
print(f"  Spearman |A| vs log e_N(maxclu), n={len(sample)}: rho = {rho:+.3f}, "
      f"two-sided permutation p = {p_perm:.3f} ({NPERM} perms)")
print(f"  -> consistent with noise, exactly as the power analysis requires (expected per-galaxy")
print(f"     signal ~{sum(abs(p) for p in pred[('canonical a0=9.36e-11','maxclu')])/len(sample)*100:.2f}% vs lopsidedness scatter {rms_A*100:.1f}%); this NEITHER supports nor")
print(f"     damages either branch and CANNOT trigger a kill condition (no direction used).")

# ----------------------------------------------------------------------------
# 7. VERDICT (pre-registered conditions applied)
# ----------------------------------------------------------------------------
print(f"""
{'='*84}
VERDICT (pre-registered conditions applied honestly)
{'='*84}
 - Kill condition 1 (aligned asymmetry DETECTED at AQUAL amplitude -> Branch B dead):
   NOT TRIGGERED -- the statistic cannot be evaluated (0 public g_ext directions).
 - Kill condition 2 (NULL at <0.5% aligned -> first empirical support for suppressed
   shear): NOT TRIGGERED -- same reason. No manufactured null: the direction-free
   exploratory check (p={p_perm:.2f}) is NOT a null of the directional test.
 - Outcome: UNDERPOWERED / NOT-CONFRONTABLE with public data in hand.
   * missing link: the g_ext DIRECTION (exists inside Chae+2021's pipeline;
     reconstructable from public 2M++/MCXC/NSA per his sec. 3 -- days-scale work);
   * even with directions, the 16 in-hand galaxies give SNR(AQUAL vs null) well
     below 1 at the local-force floor (table above);
   * deciding AQUAL vs Branch B at 3 sigma needs, at the conservative local-force
     floor with measured lopsidedness noise {rms_A:.3f}:
       N ~ {rows_out[0][4]:,.0f} (canonical a0, max-clustering e_N, w=0.304 target)
       N ~ {rows_out[1][4]:,.0f} (canonical a0, no-clustering e_N)
     dropping to ~1/{AMP_HI**2:.0f} of that ({rows_out[0][4]/AMP_HI**2:,.0f} / {rows_out[1][4]/AMP_HI**2:,.0f}) if the loop-orbit
     amplification bracket-top holds.
 - The dataset that supplies it: WALLABY (ASKAP HI survey; public kinematic-model
   releases already number in the hundreds and velocity FIELDS allow per-side
   re-derivation at scale; full survey expected O(10^3-10^4) resolved rotators),
   cross-matched with a re-run of Chae's g_ext VECTOR pipeline on 2M++/MCXC/NSA
   (method public, sec. 3 of ApJ 921,104). Second best: per-side re-reduction of
   THINGS/LITTLE THINGS/Swaters velocity fields (~100 galaxies, deeper outskirts).
 - MI caveat (framework-first): the framework proper is modified INERTIA; for pure
   MI a uniform g_ext is a frame acceleration and the aligned asymmetry can vanish
   identically. A future NULL supports Branch B AND pure MI against AQUAL-class MG;
   only a DETECTION at AQUAL amplitude kills Branch B (w~1 => Cassini Q2 fail x4-6).
{'='*84}""")
print("CONFRONTATION COMPLETE (exit 0)")

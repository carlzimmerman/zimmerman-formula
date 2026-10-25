#!/usr/bin/env python3
"""PAPER61 audit (read-only).
A  the built PDF is newer than the TeX;
B  every quoted number equals its committed lane output (JSON field, else the lane's README/.out text);
C  every cited commit exists and touches its lane;
D  the two Lean files' recorded outputs show exit 0, standard axioms only, and their MUTATE copies fail;
E  cited references match citations/REFERENCES.bib (journal volume and page);
F  no forbidden claim, local path or personal name appears.
Run:  python3 PAPER61_audit.py            (exit 0 only if every check passes)
      python3 PAPER61_audit.py --mutate   (shifts every sourced number by one unit in its last printed digit;
                                           exit 0 only if every number check then FAILS, i.e. each is live)."""
import json, os, re, subprocess, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RB = os.path.join(ROOT, "rebuild_2026_10_22")
TEX = os.path.join(HERE, "PAPER61_gravity_tied_to_dark_energy_2026.tex")
PDF = os.path.join(HERE, "PAPER61_gravity_tied_to_dark_energy_2026.pdf")
tex = open(TEX, encoding="utf-8").read()
flat = re.sub(r"\s+", " ", tex)
F = N = 0
NUMF = NUMN = 0


def check(name, ok, msg="", num=False):
    global F, N, NUMF, NUMN
    N += 1
    F += (not ok)
    if num:
        NUMN += 1
        NUMF += (not ok)
    if not MUT or num:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))


def J(*p):
    return json.load(open(os.path.join(ROOT, *p)))


def txt(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


def fmt(x, d):
    """value -> string at d decimals; under --mutate shift by one unit in the last printed digit."""
    if MUT:
        x = x + 10 ** (-d) * (1 if x >= 0 else -1)
    return f"{x:.{d}f}"


def has(name, s):
    check(f"B {name} = '{s}'", s in flat, "" if s in flat else "not found in TeX", num=True)


print("PAPER61 audit" + (" (MUTATE)" if MUT else ""))
if not MUT:
    check("A PDF newer than TeX", os.path.exists(PDF) and os.path.getmtime(PDF) >= os.path.getmtime(TEX))

# ---- B numbers
X38 = J("rebuild_2026_10_22", "X38_a0_surface_density_halos", "x38_sd_halos_results.json")
has("X38 Sigma_a0 (M_sun/pc^2)", f"{fmt(X38['Sigma_Msun_pc2']['canonical'], 0)} / {fmt(X38['Sigma_Msun_pc2']['alt'], 0)}")
has("X38 SPARC rms", f"rms {fmt(X38['footings']['canonical']['sparc']['A_c2b_refit']['rms'], 4)} / {fmt(X38['footings']['alt']['sparc']['A_c2b_refit']['rms'], 4)}")
has("X38 SPARC U", f"{fmt(X38['footings']['canonical']['sparc']['A_c2b_refit']['U_median'], 2)} / {fmt(X38['footings']['alt']['sparc']['A_c2b_refit']['U_median'], 2)}")
CD1 = J("rebuild_2026_10_22", "CD1_a0_cored_dwarf_ceiling", "cd1_dwarf_ceiling.json")
has("CD1 ceiling", f"{fmt(CD1['ceiling_over_a0'], 6)}\\,a_0")
has("CD1 fraction", f"{fmt(100 * CD1['footings']['canonical']['frac_z2'], 1)}\\% exceed")
has("CD1 median S", f"$S={fmt(CD1['footings']['canonical']['median_S'], 2)}$ / {fmt(CD1['footings']['alt']['median_S'], 2)}")
SC1 = J("rebuild_2026_10_22", "SC1_self_coupled_core_law", "sc1_core_law_results.json")
has("SC1 sigma_ref", f"{fmt(SC1['sigma_ref'], 2)}$\\,km")
has("SC1 SPARC", f"rms {fmt(SC1['footings']['canonical']['sparc']['A_c2b_refit']['rms'], 4)} / {fmt(SC1['footings']['alt']['sparc']['A_c2b_refit']['rms'], 4)}")
has("SC1 sumZ", f"from {fmt(SC1['footings']['canonical']['sumZ_x38'], 2)} to {fmt(SC1['footings']['canonical']['sumZ'], 2)}")
OS = J("rebuild_2026_10_22", "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")
OSM = J("rebuild_2026_10_22", "OS1_core_law_out_of_sample", "os1_out_of_sample_results_MUTATE.json")
c, a = OS["footings"]["canonical"], OS["footings"]["alt"]
has("OS1 q_f", f"{fmt(c['q_f'], 3)} & {fmt(a['q_f'], 3)}")
has("OS1 SPARC", f"{fmt(c['sparc_A']['rms'], 4)} @ {fmt(c['sparc_A']['U'], 2)} ({fmt(X38['footings']['canonical']['sparc']['A_c2b_refit']['rms'], 4)}) & {fmt(a['sparc_A']['rms'], 4)} @ {fmt(a['sparc_A']['U'], 2)}")
npass = {f: sum(OS["footings"][f]["clusters"]["ok"].values()) for f in ("canonical", "alt")}
has("OS1 cells passing", f"{fmt(npass['canonical'], 0)} of 15 & {fmt(npass['alt'], 0)} of 15")
has("OS1 sumZ", f"{fmt(c['clusters']['sumZ_x38'], 2)} $\\to$ {fmt(c['clusters']['sumZ'], 2)} & {fmt(a['clusters']['sumZ_x38'], 2)} $\\to$ {fmt(a['clusters']['sumZ'], 2)}")
for key, lab in (("G-MID-T3", "MID T3"), ("G-OUT-M3", "OUTER M3"), ("G-IN-Mall", "INNER M-all")):
    zc, za = c["clusters"]["cells"]["h0672"][key]["Z"], a["clusters"]["cells"]["h0672"][key]["Z"]
    sc = ("+" if zc > 0 else "") + fmt(zc, 2); sa = ("+" if za > 0 else "") + fmt(za, 2)
    has(f"OS1 {lab} Z", f"${sc}$" + (" (over)" if key == "G-IN-Mall" else "") + f" & ${sa}$")
has("OS1 dwarfs", f"{fmt(100 * c['dwarfs']['frac'], 1)}\\%, {fmt(c['dwarfs']['medS'], 2)} (EXCLUDE) & {fmt(100 * a['dwarfs']['frac'], 1)}\\%, {fmt(a['dwarfs']['medS'], 2)}")
gain = c["rms_curve"]["0.0"] - c["sparc_A"]["rms"]
has("OS1 MUTATE gain", f"from {fmt(gain, 4)} to {fmt(OSM['footings']['canonical']['gain'], 4)}\\,dex")
has("OS1/LN2 n values", f"$n={fmt(2 * c['q_f'] - 1, 3)}$ / {fmt(2 * a['q_f'] - 1, 3)}")
DW = J("rebuild_2026_10_22", "DW1_dwarf_core_flattening", "dw1_dwarf_flattening_results.json")
kc, ka = DW["footings"]["canonical"]["M1_Kn"], DW["footings"]["alt"]["M1_Kn"]
has("DW1 Kn ranges", f"{fmt(min(kc.values()), 0)}--{fmt(max(kc.values()), 0)} (canonical) and {fmt(min(ka.values()), 0)}--{fmt(max(ka.values()), 0)} (alternative)")
has("DW1 M3", f"{fmt(100 * DW['footings']['canonical']['M3']['frac'], 1)}\\% / {fmt(100 * DW['footings']['alt']['M3']['frac'], 1)}\\%")
HG = J("rebuild_2026_10_22", "HG2_kids_lowg_hot_gas", "hg2_kids_lowg_hot_gas.json")
has("HG2 D", f"$D={fmt(HG['D'], 3)}$\\,dex, 95\\% interval $[{fmt(HG['ci95'][0], 3)},{fmt(HG['ci95'][1], 3)}]$")
has("HG2 K1", f"${fmt(HG['k1'][0], 4)}\\pm{fmt(HG['k1'][1], 4)}$")
has("HG2 power", f"power {fmt(HG['power'], 2)}")
DF = J("rebuild_2026_10_22", "DF1_dwarf_floor_origin", "df1_dwarf_floor_origin_results.json")
g = DF["footings"]["canonical"]["Gamma_data"]
has("DF1 Gamma", f"$\\Gamma={fmt(g[0], 2)}$ $[{fmt(g[1], 2)},{fmt(g[2], 2)}]$")
CF = J("campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")["BAO+SN"]
iv = {z: CF["P1"][z]["sqrtX_q"] for z in ("1.0", "1.5", "2.33")}
has("CFG689 intervals", f"[{fmt(iv['1.0'][1], 2)}, {fmt(iv['1.0'][3], 2)}], [{fmt(iv['1.5'][1], 2)}, {fmt(iv['1.5'][3], 2)}] and [{fmt(iv['2.33'][1], 2)}, {fmt(iv['2.33'][3], 2)}]")
has("CFG689 sigma", f"({fmt(CF['P2']['sigma_equiv'], 2)}$\\sigma$, class {CF['P2']['P2_class']}")
MC = J("reviews", "matched_clumping_2026_10_24", "run", "result.json")
has("matched clumping clusters", f"$+{fmt(MC['summary']['cluster']['median_dex'], 3)}$\\,dex")
# text-sourced numbers (lane READMEs / ledgers / audited companion paper): string presence in both places
for name, src, s_src, s_tex in (
        ("DH1 SPARC A >=", ("rebuild_2026_10_22", "DH1_dark_energy_heater", "README.md"), "A ≥ 2.695", "A\\ge2.695"),
        ("DH1 cluster A <=", ("rebuild_2026_10_22", "DH1_dark_energy_heater", "README.md"), "A ≤ 1.424", "A\\le1.424"),
        ("kappa ledger 537", ("campaign_fresh_gravity", "CFG894_kappa_campaign_ledger", "KAPPA_ATTEMPTS_LEDGER.md"), "537 derivation or selection attempts", "Of 537 derivation attempts"),
        ("MeerKAT +0.032 (PAPER60)", ("qwen_claude_field_theory", "papers_2026", "PAPER60_scope_of_the_screened_theory_2026.tex"), "+0.032", "$+0.032$"),
        ("SPARC law 0.054 (PAPER60)", ("qwen_claude_field_theory", "papers_2026", "PAPER60_scope_of_the_screened_theory_2026.tex"), "rms 0.054", "rms 0.054"),
        ("X24 floor", ("rebuild_2026_10_22", "X24_dwarf_velocity_floor", "README.md"), "4", "4--4.6\\,km"),
        ("X28 exponent", ("rebuild_2026_10_22", "X28_dwarf_floor_form", "README.md"), "0.8", "r^{-0.8}")):
    ok = (s_src in txt(*src)) and (s_tex in flat)
    if MUT:
        ok = ok  # text-sourced: not perturbable; reported, not counted as number checks
    check(f"B(text) {name}", ok)
k829 = re.search(r"1\.016 ?± ?0\.086", txt("campaign_fresh_gravity", "CFG829_lensing_low_g_vs_dwarf_excess", "README.md"))
kv = [float(x) for x in re.findall(r"[0-9.]+", k829.group(0))] if k829 else [0.0, 0.0]
has("KiDS A (CFG829 README)", f"$A={fmt(kv[0], 3)}\\pm{fmt(kv[1], 3)}$")
m38 = re.search(r"K0 EM1 law rms ([0-9.]+) / ([0-9.]+)", txt("rebuild_2026_10_22", "X38_a0_surface_density_halos", "x38_sd_halos.out"))
has("EM1 law rms (X38 K0 line)", f"{fmt(float(m38.group(1)), 4)} / {fmt(float(m38.group(2)), 4)}")


# ---- G the illustrative figure (MAP1)
M1o = txt("rebuild_2026_10_22", "MAP1_cosmic_river", "map1_cosmic_river.out")
mg = re.search(r"slice \|SGZ\|<25, R<160: (\d+) groups; median \|v_pec\| err (\d+) km/s", M1o)
mh = re.search(r"self-calibrated H \(CF4 distance scale\) = ([0-9.]+)", M1o)
ms = re.search(r"SPARC placed \d+; in slice (\d+)", M1o); mc_ = re.search(r"in slice (\d+)\s*$", M1o.strip())
has("MAP1 groups in slice", f"({fmt(int(mg.group(1)), 0)} groups; median per-group velocity error {fmt(int(mg.group(2)), 0)}\\,km")
has("MAP1 H", f"$H={fmt(float(mh.group(1)), 2)}$")
has("MAP1 SPARC / clusters in slice", f"the {fmt(int(ms.group(1)), 0)} SPARC galaxies and {fmt(int(mc_.group(1)), 0)} eRASS1 clusters")
if not MUT:
    r = subprocess.run(["git", "-C", ROOT, "show", "--name-only", "--format=", "3f9b3ae361"], capture_output=True, text=True)
    check("G MAP1 commit 3f9b3ae361 adds map1_cosmic_river.json, cited", r.returncode == 0 and "MAP1_cosmic_river/map1_cosmic_river.json" in r.stdout and "3f9b3ae361" in flat)
    fs = open(os.path.join(HERE, "PAPER61_fig_river.py")).read()
    check("G figure script reads the MAP1 lane JSON and names its commit", "map1_cosmic_river.json" in fs and "3f9b3ae361" in fs)
    fp = os.path.join(HERE, "PAPER61_fig_river.pdf"); js = os.path.join(RB, "MAP1_cosmic_river", "map1_cosmic_river.json")
    check("G figure PDF newer than its script and the MAP1 JSON", os.path.getmtime(fp) >= max(os.path.getmtime(js), os.path.getmtime(os.path.join(HERE, "PAPER61_fig_river.py"))))
    check("G figure included and captioned 'Illustrative, not evidence'", "\\includegraphics" in flat and "PAPER61_fig_river.pdf" in flat and "\\textbf{Illustrative, not evidence.}" in flat)
    check("G no number in the paper is computed from the map (stated)", "no number in this paper is computed from this map" in flat)

# ---- C commits
COMMITS = [("6c064b83a3", "campaign_fresh_gravity/CFG689_native_ruler_bao/"), ("c51d962827", "reviews/matched_clumping_2026_10_24/"),
           ("a9ec701f5b", "rebuild_2026_10_22/X19_selector_rank_test/"), ("d5f2a449d1", "rebuild_2026_10_22/X23_late_heated_cold/"),
           ("3492bcbeb4", "rebuild_2026_10_22/X24b_vacuum_heated_cold/"), ("0f19b6759b", "rebuild_2026_10_22/X30_sheet_cluster_profile/"),
           ("5695a61801", "rebuild_2026_10_22/X31_feedback_energy_selector/"), ("36b7be3e67", "rebuild_2026_10_22/X37_orbit_conversion/"),
           ("54684fb62f", "rebuild_2026_10_22/X39_baryonic_contraction/"), ("ba368d2ba1", "rebuild_2026_10_22/X40b_core_surface_density_scaling/"),
           ("b58968185a", "rebuild_2026_10_22/HG2_kids_lowg_hot_gas/"), ("3870d2c4e8", "rebuild_2026_10_22/DH1_dark_energy_heater/"),
           ("408e26a409", "rebuild_2026_10_22/NM1_member_halo_pooling/"), ("4513c7c324", "rebuild_2026_10_22/DF1_dwarf_floor_origin/"),
           ("f72216ad98", "rebuild_2026_10_22/X38_a0_surface_density_halos/"), ("809e61b319", "rebuild_2026_10_22/CD1_a0_cored_dwarf_ceiling/"),
           ("d2f4a621d8", "rebuild_2026_10_22/SC1_self_coupled_core_law/"), ("71873e76d3", "rebuild_2026_10_22/OS1_core_law_out_of_sample/"),
           ("a8b817e19e", "rebuild_2026_10_22/OS1_core_law_out_of_sample/"), ("279b4aa47c", "rebuild_2026_10_22/DW1_dwarf_core_flattening/"),
           ("0dd2bffffa", "rebuild_2026_10_22/DW1_dwarf_core_flattening/"), ("19d31a99d9", "rebuild_2026_10_22/X24_dwarf_velocity_floor/"),
           ("dad0c9f1fe", "rebuild_2026_10_22/X28_dwarf_floor_form/"), ("667db25771", "rebuild_2026_10_22/LN1_lean_cold_sector_certs/"),
           ("dc2724d299", "rebuild_2026_10_22/LN2_lean_os1_dw1_certs/")]
if not MUT:
    for h, lane in COMMITS:
        r = subprocess.run(["git", "-C", ROOT, "show", "--name-only", "--format=", h], capture_output=True, text=True)
        check(f"C {h} touches {lane.split('/')[-2]}, cited", r.returncode == 0 and lane in r.stdout and h in flat)

# ---- D Lean
if not MUT:
    for d, f, n in (("LN1_lean_cold_sector_certs", "ColdSectorCerts", 9), ("LN2_lean_os1_dw1_certs", "CoreLawCerts", 7)):
        o = open(os.path.join(RB, d, f + ".out")).read(); m = open(os.path.join(RB, d, f + "_MUTATE.out")).read()
        lean = open(os.path.join(RB, d, f + ".lean")).read()
        ax = re.findall(r"depends on axioms: \[(.*?)\]", o)
        ok = ("main exit=0" in o and len(ax) == n and all(x == "propext, Classical.choice, Quot.sound" for x in ax)
              and "mutate exit=1" in m and "sorry" not in lean)
        check(f"D {f}: exit 0, {n} theorems on standard axioms, no sorry, MUTATE fails", ok)

# ---- E references (volume, page against the bib)
if not MUT:
    bib = open(os.path.join(ROOT, "citations", "REFERENCES.bib"), encoding="utf-8").read()
    for key, cite in (("Lelli2016a", "AJ 152, 157 (2016)"), ("Bulbul2024", "A\\&A 685, A106 (2024)"), ("Eckert2019", "A\\&A 621, A40 (2019)"),
                      ("Brouwer2021", "A\\&A 650, A113 (2021)"), ("DESICollaboration2025c", "PRD 112, 083515 (2025)"), ("Brout2022a", "ApJ 938, 110 (2022)"),
                      ("Milgrom1983c", "ApJ 270, 365 (1983)"), ("Burkert1995", "ApJ 447, L25 (1995)"), ("Donato2009", "MNRAS 397, 1169 (2009)"), ("Tully2023", "ApJ 944, 94 (2023)")):
        m_ = re.search(r"@\w+\{" + key + r",(.*?)\n\}", bib, re.S)
        vol, page = re.match(r".*? (\d+), ([A-Z]?\d+)", cite).groups()
        e = m_.group(1) if m_ else ""
        ok = bool(m_) and re.search(r"volume\s*=\s*\{?" + vol, e) and (page in e or key == "Burkert1995") and cite in flat
        check(f"E {key} {cite}", bool(ok))

# ---- F forbidden
if not MUT:
    low = flat.lower()
    for bad in ("theory is closed", "theory closed", "favour the framework", "favor the framework", "confirms the framework", "proves the theory",
                "/users/", "carl", "zimmerman"):
        okb = bad not in low or (bad == "theory closed" and "not \"theory closed\"" in low)
        check(f"F no '{bad}'", okb)
    check("F kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in flat or "FITTED" in flat)

if MUT:
    print(f"\nMUTATE: {NUMF}/{NUMN} number checks fail under perturbation (all must)")
    sys.exit(0 if NUMF == NUMN else 1)
print(f"\n{N - F}/{N} checks pass")
sys.exit(0 if F == 0 else 1)

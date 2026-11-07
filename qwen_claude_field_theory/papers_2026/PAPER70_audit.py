#!/usr/bin/env python3
"""PAPER70 audit (draft v0.2): each quoted number appears in the TeX and, as the literal given, in the committed file named
beside it; naming rules; no local paths; no pending placeholder. Run: python3 PAPER70_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal; exit 0 only if every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER70_field_equations_closure_2026.tex"), encoding="utf-8").read()
C = "closure_2026_11_06/"
Q17 = C + "QX17_covariant_field_equations/RESULT.md"; Q17A = C + "QX17A_ac2q_field_equations/RESULT.md"
Q17B = C + "QX17B_adm_lean_solutions/RESULT.md"; Q17C = C + "QX17C_fd_spherical_solver/RESULT.md"
GB1 = C + "GB1_all_gates_battery/RESULT.md"; KD1 = C + "KD1_unpinned_kq_dust/RESULT.md"
LD1 = C + "LD1_late_decaying_cold/RESULT.md"; HC1 = C + "HC1_hot_fermion_all_gates/RESULT.md"
SE1 = C + "SE1_shock_entropy_sector/RESULT.md"; SE2 = C + "SE2_step_as_systematics/RESULT.md"
EV1 = C + "EV1_environment_reread/RESULT.md"; NOGO = C + "ALL_GATES_NOGO_2026_11_06.md"
CF = C + "CLOSURE_FINAL.md"; VH = "rebuild_2026_10_22/VH1_v3s_health_gates/README.md"
P68 = "qwen_claude_field_theory/papers_2026/PAPER68_screened_khronon_action_2026.zenodo.json"
SEED = C + "SEED_2026_11_06.md"
L = [
 ("$a_0=9.3603\\times10^{-11}$", VH, "9.3603e-11"), ("$1.1312\\times10^{-10}$", VH, "1.1312e-10"),
 ("PAPER67 (DOI 10.5281/zenodo.23968171", P68, "10.5281/zenodo.23968171"),
 ("PAPER68 (DOI 10.5281/zenodo.23990944", P68, "10.5281/zenodo.23990944"),
 ("PAPER69 (DOI 10.5281/zenodo.24025170", SEED, "10.5281/zenodo.24025170"),
 ("$K|P|=a_0u/(1+u)$", Q17, "attained at K|P| = a0 u/(1+u)"),
 ("P equation max rel $3.8\\times10^{-41}$", Q17, "PASS, max rel 3.8e-41"),
 ("khronon equation $1.8\\times10^{-41}$", Q17, "PASS, max rel 1.8e-41"),
 ("full stress tensor $1.2\\times10^{-40}$", Q17, "PASS, max rel 1.2e-40"),
 ("fails at 0.17--0.78", Q17, "K2 then fails at 0.17-0.78"),
 ("fails at 0.23/0.39/$7.3\\times10^{-3}$", Q17A, "K2 fails at 0.23 / 0.39 / 7.3e-3"),
 ("has 12 theorems, standard axioms only", Q17B, "has 12 theorems, standard axioms only"),
 ("converges in 1--6 steps", Q17C, "converges in 1-6 Newton steps"),
 ("(worst $3.9\\times10^{-7}$)", Q17C, "| 3.9e-7 |"),
 ("to $7.1\\times10^{-6}$ of", Q17C, "| 7.1e-6 |"),
 ("on the law to $4.8\\times10^{-6}$", Q17C, "| 4.8e-6 |"),
 ("$4.1\\times10^{-6}$ (Sun)", Q17C, "Full minus weak is 4.1e-6 relative for the Sun"),
 ("$5.4\\times10^{-7}$ (galaxy)", Q17C, "5.4e-7 for the galaxy"),
 ("only 0.71/0.67 of the law", Q17C, "gives 0.71 / 0.67 at 1e3 Lstar"),
 ("at least 3.97\\,$\\sigma_U$", GB1, "by at least 3.97 sigma_U"),
 ("cosmic capture 4.111", KD1, "| 4.111 | 4.112 |"),
 ("$\\chi^2$ 46.3/53.0 against 18.48", LD1, "**46.3, FAIL**"), ("$\\chi^2$ 46.3/53.0 against 18.48", LD1, "**53.0, FAIL**"),
 ("against 18.48", LD1, "line 18.48"),
 ("11.1377\\,eV", HC1, "m = 11.1377 eV"), ("$\\chi^2$ 166.0--194.2", HC1, "chi^2 166.0-194.2"),
 ("FAILS 7 of 9 gates", HC1, "it blocks on 7 of 9 gates"),
 ("(f $\\le$ 0.04)", SE1, "(f <= 0.04)"),
 ("X-COP $+0.440$", SE2, "| **+0.440** |"), ("groups $+0.232$", SE2, "| **+0.232** |"),
 ("Coma UDGs $+1.120$", SE2, "| **+1.120** |"),
 ("about 1.6$\\times$ the phantom", EV1, "about 1.6x the phantom"), ("Coma UDGs 4--46$\\times$", EV1, "4-46x for Coma UDGs"),
 ("largest time-mean on any rung 0.147 of the line", CF, "Largest time-mean on any rung 0.147 of the line"),
 ("$\\le0.33$ / $0.19$", NOGO, "<= 0.33 / 0.19"), ("$\\sim4.2$ / $3.8$", NOGO, "~4.2 / 3.8"),
 ("1.2--3.5 / 0.9--2.9", NOGO, "1.2-3.5 / 0.9-2.9"), ("$\\sim0.9$ / $0.8$", NOGO, "~0.9 / 0.8"),
 ("$\\sim1.7$ / $1.3$", NOGO, "~1.7 / 1.3"), ("Coma UDGs & $\\sim80$", NOGO, "| Coma UDGs | ~80 |"),
 ("($w\\le0.01$), lensing $\\chi^2\\le18.5$", NOGO, "(w <= 0.01), and lensing chi^2 <= 18.5"),
 ("$\\mu_K\\ge8.9\\times10^6$", NOGO, "mu_K >= 8.9e6"), ("galaxies allow at most 79", NOGO, "galaxies need <= 0.1-79"),
]
SE2R = SE2; CH = C + "FRW_RECONCILIATION_CHAIN/CHAIN.md"; CQ2 = "cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/README.md"
OM = "campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md"; AT2 = "rebuild_2026_10_22/AT2_a0z_on_disk_samples/README.md"
V3W = "rebuild_2026_10_22/V3W_v3s_weak_spots/README.md"
L += [
 ("multiplies the induced lapse term by $(1-z)^2$, not the legacy $(1-2z)^2$", CH, "The legacy (1 - 2z)^2 is wrong for A1 as defined"),
 ("$c^2=z/(1-z+z^2)$", CH, "UV c^2 = z/(1-z+z^2)"),
 ("$+0.440$ [$+0.372$, $+0.484$]", SE2R, "| **+0.440** | [+0.412, +0.463] | [+0.372, +0.484] |"),
 ("$+0.408$ [$+0.341$, $+0.451$]", SE2R, "| **+0.408** | [+0.380, +0.431] | [+0.341, +0.451] |"),
 ("$+0.232$ [$+0.078$, $+0.362$]", SE2R, "| **+0.232** | [+0.156, +0.318] | [+0.078, +0.362] |"),
 ("$+0.194$ [$+0.041$, $+0.324$]", SE2R, "| **+0.194** | [+0.119, +0.279] | [+0.041, +0.324] |"),
 ("$+1.120$ [$+0.541$, $+1.718$]", SE2R, "| **+1.120** | [+0.823, +1.421] | [+0.541, +1.718] |"),
 ("$+1.075$ [$+0.472$, $+1.673$]", SE2R, "| **+1.075** | [+0.774, +1.372] | [+0.472, +1.673] |"),
 ("X-ray ellipticals & $+0.067$ & $+0.050$", SE2R, "| +0.067 | [-0.064, +0.179] |"),
 ("X-ray ellipticals & $+0.067$ & $+0.050$", SE2R, "| +0.050 | [-0.078, +0.159] |"),
 ("KiDS early/late & $+0.085$ & $+0.084$", SE2R, "| +0.085 | [-0.000, +0.162] |"),
 ("KiDS early/late & $+0.085$ & $+0.084$", SE2R, "| +0.084 | [+0.001, +0.163] |"),
 ("bright M31 dSphs (21) & $+0.228$ & $+0.219$", SE2R, "| +0.228 | [+0.006, +0.455] |"),
 ("bright M31 dSphs (21) & $+0.228$ & $+0.219$", SE2R, "| +0.219 | [-0.006, +0.447] |"),
 ("($z$ 3.04 / 2.55)", SE2R, "| 3.04 | 0.0025 |"), ("($z$ 3.04 / 2.55)", SE2R, "| 2.55 | 0.0087 |"),
 ("$\\gamma_\\infty$ 1.0019 / 1.0100", CQ2, "pipeline γ_inf V3S (spread) | 1.0019 (0.0200) | 1.0100 (0.0068)"),
 ("plain QUMOND (1.1494 / 1.2081)", CQ2, "plain QUMOND (1.1494 / 1.2081)"),
 ("SHA-256 1d65509dbf", CQ2, "SHA-256 1d65509dbf"),
 ("($\\sigma_{\\rm tot}=0.028$)", OM, "σ_tot = 0.028"),
 ("falsified at $\\hat\\gamma$ 1.084--1.23 if the stability requirements pass", OM, "falsified at γ̂ 1.084-1.23 if the stability requirements pass"),
 ("all 52 cells are BLOCKED", AT2, "52 (sample, z*) cells, 52 BLOCKED"),
 ("(0.30--0.60\\,dex) is 4--11$\\times$", AT2, "common mode (0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex)"),
 ("(0.084\\,dex at $z^*$ 2.33)", AT2, "0.055 / 0.072 / 0.074 / 0.084 dex at z* 1.0 / 1.2 / 1.5 / 2.33"),
 ("to $\\le6.5\\times10^{-5}$ at 310\\,kpc", V3W, "M_lens/M_dyn = 1 to ≤ 6.5e-5 (at 310 kpc)"),
 ("$A=1.129\\pm0.206$ (canonical)", V3W, "A = 1.129 ± 0.206"), ("$1.035\\pm0.187$ (alt)", V3W, "A = 1.035 ± 0.187"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        fp = os.path.join(ROOT, p)
        cache[p] = ws(open(fp, encoding="utf-8").read()) if os.path.exists(fp) else ""
    return cache[p]
def mutate(lit):
    m = re.search(r"\d", lit)
    return lit if not m else lit[:m.start()] + str((int(m.group()) + 1) % 10) + lit[m.end():]
ok = 0; bad = []
for frag, path, lit in L:
    in_tex = ws(frag) in ws(TEX)
    l2 = mutate(lit) if MUT else lit
    in_src = ws(l2) in src(path)
    if MUT:
        if not re.search(r"\d", lit) or not in_src: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src: ok += 1
    else: bad.append(("tex" if not in_tex else "src", frag, path))
body = TEX.split("\\begin{document}")[1]
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower()),
 ("no pending placeholder", "\\pend{" not in body),
 ("no LCDM input claimed", "No $\\Lambda$CDM inputs were used" in TEX),
 ("not deposited stated", "Not deposited" in TEX),
 ("seed abstract verbatim", "The next lane must find one covariant quantity that sets that amplitude (not just a switch) in today's hot systems and is non-zero in the early universe, or show the two failures need separate causes." in ws(TEX)),
 ("erratum stated", "erratum on PAPER68's printed form only; no number changes" in TEX),
]
if not MUT:
    for name, good in rules:
        if good: ok += 1
        else: bad.append(("rule", name, ""))
for b in bad: print("FAIL", *b)
total = len(L) + (0 if MUT else len(rules))
print(f"{ok} of {total} checks pass" + (" (mutate: each mutated literal must fail)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(0 if not bad else 1)

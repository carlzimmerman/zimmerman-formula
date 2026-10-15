"""CFG800 -- score Cookson+26 and Chae & Yoon 26 against the sealed CFG740 prediction.  Criteria: FROZEN_CRITERIA.md (aa71ca510).
Inputs transcribed from the papers' arXiv sources (table chi_sq_table of 2602.24035; text of 2607.14450).  Seconds.
Run: python3 cfg800.py   (CFG800_MUTATE=1: framework shift 0.20).  kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG800_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


# Cookson+26 table chi_sq_table (d_h < 130 pc, 5 dof): cut, N, chi2_Newton, chi2_MOND, published Newton tension (sigma)
COOK = [("v<=2.5", 1421, 2.48, 15.10, 0.28), ("v<=2", 1417, 2.33, 14.90, 0.25), ("v<=1.5", 1408, 1.92, 15.49, 0.18),
        ("v<=1.5 & ipd=0", 1216, 1.46, 16.09, 0.10)]
SHIFT = 0.20 if MUT else 3.2e-4          # CFG740 envelope, 30 kAU (max of the 1-30 kAU range)
CHAE = (1.15, 1.20)                       # Chae & Yoon 26 velocity boost at r_p/r_M > 1
FALS = 1.01                               # CFG740 falsifier, s <= 50 kAU
tens = lambda p: stats.norm.isf(p / 2)
P("CFG800  2026 wide-binary papers vs sealed CFG740" + ("  [MUTATE shift 0.20]" if MUT else ""))
P(f"  framework velocity shift used: {SHIFT:.1e} (CFG740 envelope at 30 kAU)")
R = dict(lane="CFG800", mutate=MUT, cookson=[], k1=True)
ok = True
for cut, n, cn, cm, tpub in COOK:
    pN = stats.chi2.sf(cn, 5)
    k1 = abs(tens(pN) - tpub) <= 0.05
    R["k1"] &= bool(k1)
    dF = (cm - cn) * (SHIFT / 0.20) ** 2
    pF = stats.chi2.sf(cn + dF, 5)
    ok &= pF >= 0.05
    R["cookson"].append(dict(cut=cut, N=n, chi2_N=cn, chi2_M=cm, p_N=pN, dchi2_F=dF, chi2_F=cn + dF, p_F=pF))
    P(f"  Cookson {cut:15s} N {n}: Newton chi2 {cn:.2f} (p {pN:.3f}, {tens(pN):.2f} sig vs pub {tpub}) ; framework +{dF:.1e} -> p {pF:.3f} ; MOND p {stats.chi2.sf(cm, 5):.4f}")
P(f"  K1 (tensions reproduced within 0.05 sigma): {'PASS' if R['k1'] else 'FAIL'}")
s1 = "CONSISTENT" if ok else "INCONSISTENT"
P(f"  S1 Cookson: {s1}  (disclosed: d<150 pc without the ipd cut gives MOND 12x preferred; with ipd=0, Newton 88x)")
s2 = "INCOMPATIBLE: kills CFG740 if confirmed" if CHAE[0] > FALS else "COMPATIBLE"
P(f"  S2 Chae & Yoon: claimed velocity boost {CHAE[0]}-{CHAE[1]} vs falsifier {FALS} -> {s2}")
P("  DR4 rule (frozen): R-1 >= 0.01 at >=3 sigma -> FRAMEWORK KILLED; |R-1| < 0.01 at 2 sigma -> CONSISTENT (standard MOND excluded); else UNDECIDED")
R.update(S1=s1, S2=s2)
if MUT:
    P(f"  MUTATE: p_F (ipd cut) {R['cookson'][-1]['p_F']:.4f} -> {'bites' if R['cookson'][-1]['p_F'] < 0.05 else 'DID NOT BITE'}")
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg800_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg800{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)

#!/usr/bin/env python3
"""CFG712 PREDICT (criteria d73d64603): per SLACS lens, gamma_pred = 1 - dln kappa/dln R at theta_E from Auger+2009 de Vaucouleurs
light + the law, normalised only by Etherington+2022's R_Ein,eff. Reads ONLY name and R_Ein,eff from the Etherington table (never
the gamma column). Writes cfg712_predictions.json (sealed by hash before scoring). kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, re, json, math, hashlib, contextlib
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from astropy.cosmology import Planck18 as cosmo
import astropy.units as u
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG712_MUTATE", "0") == "1"
VARIANT = os.environ.get("CFG712_RE", "I")                 # I (primary) or V
TAG = ("_MUTATE" if MUT else "") + ("" if VARIANT == "I" else "_ReV")
G, MSUN, C = C4.G_SI, C4.MSUN, 2.99792458e8
ETH = os.path.join(os.path.dirname(REPO), "_external_data", "etherington2022", "src", "6_Results.tex")
AUG = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")

# ---- Etherington: name + R_Ein,eff ONLY (third cell); the gamma cell is never parsed here
s = open(ETH).read(); i = s.find("label{table: SLACS mass"); blk = s[s.rfind("begin{table", 0, i):i]
eth = {}
for line in blk.splitlines():
    m = re.search(r"(J\d{4}[+-]\d{4})", line)
    if not m or "&" not in line: continue
    cells = line.split("&")
    k = [j for j, c in enumerate(cells) if m.group(1) in c][0]
    thE = float(re.findall(r"\d+\.\d+", cells[k + 1])[0])
    eth[m.group(1)] = thE
# ---- Auger+2009: z, R_e
lines = [l.rstrip("\n") for l in open(AUG, encoding="latin-1")]
hi = [j for j, l in enumerate(lines) if l.startswith("recno")][0]
hdr = lines[hi].split("\t"); col = {c: j for j, c in enumerate(hdr)}
def F(v):
    try: return float(v.strip())
    except Exception: return float("nan")
aug = {}
for r in [l.split("\t") for l in lines[hi + 3:] if l.strip() and not l.startswith("#")]:
    nm = r[col["SDSS"]].strip(); key = "J" + nm[:4] + nm[nm.find("+") if "+" in nm else nm.find("-"):][:5] if nm else None
    m = re.match(r"J?(\d{4})\d*\.?\d*([+-]\d{4})", nm.replace(" ", ""))
    if m: aug["J" + m.group(1) + m.group(2)] = dict(zl=F(r[col["zlens"]]), zs=F(r[col["zsrc"]]), ReI=F(r[col["Re(I)"]]), ReV=F(r[col["Re(V)"]]))

# ---- universal de Vaucouleurs deprojection in units of R_e (unit total mass)
b4 = 7.669
X = np.logspace(-3.5, np.log10(400), 900)
Sig = lambda x: np.exp(-b4 * (x ** 0.25 - 1))
dSig = lambda x: Sig(x) * (-b4 * 0.25 * x ** -0.75)
rho = np.array([-1 / math.pi * quad(lambda t: dSig(math.sqrt(x * x + t * t)) / math.sqrt(x * x + t * t), 0, 60, limit=300)[0] for x in X])
rho = np.maximum(rho, 0)
m3 = np.concatenate([[0], np.cumsum(0.5 * (4 * math.pi * X[1:] ** 2 * rho[1:] + 4 * math.pi * X[:-1] ** 2 * rho[:-1]) * np.diff(X))])
m3 /= m3[-1]                                              # M*(<x)/M*

def hcol(y):
    return np.interp(np.log10(np.maximum(y, 1e-14)), C4._KNS["LYG"], C4._KNS["_HM"])

def proj(rr, M, R):
    d = np.gradient(M, rr); w = np.where(rr > R, 1 - np.sqrt(np.clip(1 - (R / rr) ** 2, 0, 1)), 1.0)
    return float(np.trapz(d * w, rr))

def predict_one(zl, zs, Re_as, thE, a0):
    Dl = cosmo.angular_diameter_distance(zl).to(u.m).value; Ds = cosmo.angular_diameter_distance(zs).to(u.m).value
    Dls = cosmo.angular_diameter_distance_z1z2(zl, zs).to(u.m).value
    Scr = C ** 2 / (4 * math.pi * G) * Ds / (Dl * Dls); arc = Dl / 206264.806
    Re = Re_as * arc; R_E = thE * arc; ME = Scr * math.pi * R_E ** 2
    r = X * Re
    def Mtot(Ms):
        gN = G * Ms * m3 / r ** 2
        return (gN + (a0 * hcol(gN / a0) if a0 > 0 else 0.0)) * r ** 2 / G
    f = lambda lm: proj(r, Mtot(10 ** lm * MSUN), R_E) / ME - 1
    lMs = brentq(f, 8.0, 13.5, xtol=1e-5)
    M = Mtot(10 ** lMs * MSUN)
    e = 0.02
    kap = lambda R: (proj(r, M, R * (1 + e)) - proj(r, M, R * (1 - e))) / (2 * e * R) / (2 * math.pi * R)
    k1, k2 = kap(R_E * 0.95), kap(R_E * 1.05)
    gam = 1 - (math.log(k2) - math.log(k1)) / (math.log(1.05) - math.log(0.95))
    gN_E = G * 10 ** lMs * MSUN * float(np.interp(R_E / Re, X, m3)) / R_E ** 2
    return dict(gamma_pred=gam, logMstar=lMs, thetaE_over_Re=thE / Re_as, gN_over_a0_at_thetaE=gN_E / a0 if a0 > 0 else None)

out = {"lane": "CFG712", "criteria": "d73d64603", "variant_Re": VARIANT, "mutate": MUT, "lenses": {}}
L = []
names = sorted(set(eth) & set(aug))
L.append(f"Etherington SLACS lenses {len(eth)}, Auger matches {len(names)}")
for foot, a0v in C4.A0.items():
    a0 = 1e-30 if MUT else a0v
    for nm in names:
        A = aug[nm]; Re_as = A["ReI"] if VARIANT == "I" else A["ReV"]
        if not all(math.isfinite(v) for v in (A["zl"], A["zs"], Re_as)): continue
        try:
            p = predict_one(A["zl"], A["zs"], Re_as, eth[nm], a0v if not MUT else 1e-30)
        except ValueError:
            continue
        out["lenses"].setdefault(nm, {})[foot] = p
    g = [v[foot]["gamma_pred"] for v in out["lenses"].values() if foot in v]
    L.append(f"{foot}: n {len(g)}, median gamma_pred {np.median(g):.3f}, 16-84% {np.percentile(g,16):.3f}-{np.percentile(g,84):.3f}")
js = json.dumps(out, indent=1, sort_keys=True, default=float) + "\n"
open(os.path.join(HERE, f"cfg712_predictions{TAG}.json"), "w").write(js)
L.append(f"sha256(cfg712_predictions{TAG}.json) = {hashlib.sha256(js.encode()).hexdigest()}")
open(os.path.join(HERE, f"cfg712_predict{TAG}.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))

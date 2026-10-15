"""CFG802 -- is CFG799's 3.2 sigma hint at 541.700 GHz real?  Criteria: FROZEN_CRITERIA.md (502a680ae).
Imports CFG799's pipeline read-only.  Run: python3 -I cfg802.py <data_dir>   (CFG802_MUTATE=1: injected line).
kappa = 1/2 FITTED; not theory closed.
"""
import importlib.util, json, os, sys
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(sys.argv[1])
MUT = os.environ.get("CFG802_MUTATE") == "1"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

src = os.path.join(HERE, "..", "CFG799_hifi_totalpower_search", "cfg799.py")
argv0 = sys.argv[:]; sys.argv = [src, DATA]
spec = importlib.util.spec_from_file_location("cfg799", src); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
sys.argv = argv0
R799 = json.load(open(os.path.join(HERE, "..", "CFG799_hifi_totalpower_search", "cfg799_results.json")))

NU_H, NU_S = 541.700, 541.702
man, obs = M.load()
spectra = []
for oid, o in obs.items():
    a = M.anchor(o)
    if a["ok"]:
        spectra += M.build_spectra(oid, o, a["tS"])
sp, _ = M.prep(spectra)
P("CFG802  CFG799 hint test at 541.700 GHz" + ("  [MUTATE]" if MUT else ""))
base = M.stack(M.amps(sp, NU_H))
if MUT:
    A = 3 * base["a"]
    for s in sp:
        for sb in range(4):
            s["Tall"][sb] = s["Tall"][sb] + A * M.gauss(s["IF"][sb] - M.if_of(s, NU_H))
    P(f"  MUTATE: injected {A * 1e3:.1f} mK line at {NU_H} GHz")
a_all = M.amps(sp, NU_H)
st = M.stack(a_all)
k1 = MUT or abs(st["a"] - R799["main"]["nu_2"]["a"]) < 1e-4
P(f"  K1 stack at nu_h: a = {st['a'] * 1e3:+.2f} +- {st['sig'] * 1e3:.2f} mK, z {st['z']:+.2f} (CFG799 {R799['main']['nu_2']['a'] * 1e3:+.2f}): {'PASS' if k1 else 'FAIL'}")
P(f"  scan peak nu_s {NU_S}: z {M.stack(M.amps(sp, NU_S))['z']:+.2f}")

RICH = ("orion", "sgr b2", "irc+10216", "irc10216", "g34", "w49", "w51", "ngc6334", "ngc 6334", "dr21", "hot core", "hc")
def target(s):
    return obs[s["obs"]]["man"].get("target", "").lower()
med_obs = np.median([int(x[2]["obs"]) for x in a_all])
splits = {
    "pol H|V": (lambda s: s["pol"] == "h"),
    "early|late": (lambda s: int(s["obs"]) <= med_obs),
    "USB|LSB": (lambda s: s["usb"]),
    "line-rich|other": (lambda s: any(k in target(s) for k in RICH)),
}
R = dict(lane="CFG802", mutate=MUT, K1=bool(k1), base=st, splits={})
persist = True
P("\n  T1 splits (z_A / z_B, agreement):")
for name, f in splits.items():
    A_ = M.stack([x for x in a_all if f(x[2])]); B_ = M.stack([x for x in a_all if not f(x[2])])
    agree = abs(A_["a"] - B_["a"]) / np.hypot(A_["sig"], B_["sig"]) if A_["n"] and B_["n"] else np.nan
    ok = (A_["z"] >= 1.5) and (B_["z"] >= 1.5) and (agree < 2)
    persist &= bool(ok)
    R["splits"][name] = dict(A=A_, B=B_, agree=agree, ok=bool(ok))
    P(f"    {name:16s}: n {A_['n']}/{B_['n']}  a {A_['a'] * 1e3:+.1f}/{B_['a'] * 1e3:+.1f} mK  z {A_['z']:+.2f}/{B_['z']:+.2f}  |d|/s {agree:.2f}  -> {'ok' if ok else 'FAILS'}")
P(f"    T1: {'PERSISTS' if persist else 'DOES NOT PERSIST'}")

P("\n  T2 width (z vs assumed FWHM):")
zw = {}
sig0 = M.SIG_G
for fw in (1.14, 2.0, 4.0, 8.0, 16.0):
    M.SIG_G = fw / 2.3548
    zw[fw] = M.stack(M.amps(sp, NU_H))["z"]
    P(f"    FWHM {fw:5.2f} MHz: z {zw[fw]:+.2f}")
M.SIG_G = sig0
best = max(zw, key=lambda k: zw[k])
narrow = best <= 2.0
P(f"    T2: best FWHM {best} MHz -> {'NARROW' if narrow else 'BROAD'}")
R["width_z"] = zw

P("\n  T3 leave-one-observation-out:")
oids = sorted({x[2]["obs"] for x in a_all})
loo = {o: M.stack([x for x in a_all if x[2]["obs"] != o])["z"] for o in oids}
mn = min(loo, key=loo.get)
notdriven = loo[mn] >= 2
P(f"    {len(oids)} obs; min z {loo[mn]:+.2f} when dropping {mn} ({obs[mn]['man'].get('target', '?')}) -> {'NOT DRIVEN' if notdriven else 'DRIVEN'}")
R["loo_min"] = dict(obs=mn, z=loo[mn])

sc = R799.get("scan", {})
zs = np.array(sc.get("z", [])) if isinstance(sc, dict) else np.array([])
if zs.size:
    frac = float(np.mean(np.abs(zs) >= abs(st["z"]) - 1e-9))
    neff = len(zs) / 3
    p_loc = 2 * norm.sf(abs(st["z"])); p_glob = 1 - (1 - p_loc) ** neff
    P(f"\n  T4 look-elsewhere: {frac * 100:.1f}% of {len(zs)} scan steps have |z| >= {abs(st['z']):.2f}; local p {p_loc:.4f}, trials-corrected p {p_glob:.3f} (N_eff {neff:.0f})")
    R["lee"] = dict(frac=frac, p_loc=p_loc, p_glob=p_glob)
else:
    P("\n  T4 look-elsewhere: scan z array not found in CFG799 results")

cls = "HINT SURVIVES" if (persist and narrow and notdriven) else "HINT FADES"
why = [n for n, ok in (("T1 splits", persist), ("T2 width", narrow), ("T3 leave-one-out", notdriven)) if not ok]
P(f"\n  CLASS: {cls}" + (f"  (killed by: {', '.join(why)})" if why else "") + (f"   MUTATE: {'bites' if cls == 'HINT SURVIVES' else 'DID NOT BITE'}" if MUT else ""))
R.update(cls=cls, why=why)
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg802_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg802{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)

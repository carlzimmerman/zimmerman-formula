"""CFG88 post-comparison 2 (after reading CFG42's script): the sensitivity tables re-scored with recipe B (CFG42-style: gas A2, halo mass + gas fixed at Upsilon = 2 in the Upsilon scan,
1.2533 rms/sqrt n) beside my frozen recipe A (bootstrap, everything propagated), and the four LVD error-recipe cross combinations.  Reported only."""
import math, os, numpy as np
import cfg88_post as Pst          # monkeypatches predict (recipe-B predictor) -- so recipe A is computed with the ORIGINAL predict saved below
import cfg88 as C
from cfg88 import Cfg, med, boot_stat
predict_B = C.predict
# reload the original predict for recipe A
import importlib, types
src = open("cfg88.py").read(); mod = types.ModuleType("cfg88_orig"); mod.__dict__["__name__"] = "cfg88_orig"; mod.__dict__["__file__"] = os.path.abspath("cfg88.py")
exec(compile(src.replace('if __name__ == "__main__":\n    main()', ''), "cfg88_orig", "exec"), mod.__dict__)
ufd, cls, lvd, col, CAL = Pst.ufd, Pst.cls, Pst.lvd, Pst.col, Pst.CAL
def rowA(P, cfg): 
    return mod.row(P, cfg, CAL, True)
def rowB(P, cfg):
    cens = np.array([s["ul"] for s in P]); base = cfg.copy(gas="A2")
    C.predict = predict_B
    x = C.offsets(P, base, CAL); m = med(x, cens)
    err = boot_stat(x, cens, nb=1000, seed=42) if cens.any() else 1.2533 * float(np.std(x)) / math.sqrt(len(x))
    ms = [med(C.offsets(P, base.copy(ups=u), CAL), cens) for u in (1.0, 4.0)]; fU = 0.5 * abs(ms[1] - ms[0])
    fl = [med(C.offsets(P, base.copy(small_mcoll=v), CAL), cens) for v in Pst.FLOORS]; fC = 0.5 * (max(fl) - min(fl))
    return m, math.sqrt(err ** 2 + fU ** 2 + fC ** 2)
def show(tag, cfg):
    parts = []
    for k, P in (("UFD", ufd), ("cls", cls), ("LVD", lvd), ("Col", col)):
        a = rowA(P, cfg.copy(phi=1.0)); mB, eB = rowB(P, cfg.copy(phi=1.0))
        parts.append(f"{k} {mB:+.3f} zB {mB/eB:+.2f} zA {a['z']:+.2f}")
    print(f"{tag:32s} " + " | ".join(parts))
print("rule offsets (recipe-B predictor) with z under recipe B (CFG42-style) and A (frozen); canonical footing")
for k in mod.CONC: show("conc " + k, Cfg(conc=k))
for k in mod.KERNELS: show("kernel " + k, Cfg(kernel=k))
for v in (1e8, 3e8, 1e9, 3e9, 1e10): show(f"clamp {v:.0e}", Cfg(clamp=v))
show("unclamped", Cfg(unclamped=True))
# LVD error recipe cross table
print("\nM31 LVD rule, error-recipe cross table (canonical): offset -0.107")
C.predict = predict_B; cens = np.zeros(len(lvd), bool)
base = Cfg(gas="A2")
x = C.offsets(lvd, base, CAL); m = float(np.median(x)); an = 1.2533 * x.std(ddof=1) / math.sqrt(len(x)) if False else 1.2533 * float(np.std(x)) / math.sqrt(len(x)); bs = boot_stat(x, cens, nb=4000, seed=88)
fUB = 0.5 * abs(np.median(C.offsets(lvd, base.copy(ups=4.0), CAL)) - np.median(C.offsets(lvd, base.copy(ups=1.0), CAL)))
fC = 0.5 * (max(np.median(C.offsets(lvd, base.copy(small_mcoll=v), CAL)) for v in Pst.FLOORS) - min(np.median(C.offsets(lvd, base.copy(small_mcoll=v), CAL)) for v in Pst.FLOORS))
C.predict = mod.predict
xa = mod.offsets(lvd, Cfg(), CAL); ms = [float(np.median(mod.offsets(lvd, Cfg(ups=u), CAL))) for u in (1.0, 4.0)]; fUA = 0.5 * abs(ms[1] - ms[0])
print(f"  analytic 1.2533 rms/sqrt n = {an:.4f}; bootstrap SE(median) = {bs:.4f}; Upsilon floor (halo+gas fixed) = {fUB:.4f}; Upsilon floor (halo+gas propagate) = {fUA:.4f}; collapse floor = {fC:.4f}")
for en, e in (("analytic", an), ("bootstrap", bs)):
    for un, u in (("U fixed-aux", fUB), ("U propagated", fUA)):
        t = math.sqrt(e ** 2 + u ** 2 + fC ** 2); print(f"  {en:9s} + {un:12s}: total {t:.4f} -> z = {m/t:+.2f}")

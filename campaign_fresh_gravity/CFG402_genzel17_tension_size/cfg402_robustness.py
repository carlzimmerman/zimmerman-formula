"""CFG402 POST-FREEZE (labelled): is the tension one galaxy? Sum without zC 406690, and zC 406690 at inclination 25 +- 12 deg (Table 1 prior)."""
import os, sys, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ.pop("MUTATE", None)
src = open(os.path.join(HERE, "..", "CFG401_genzel17_gas_shape", "cfg401_gas_shape.py")).read()
exec(src.split('LF = np.linspace(-3, 3, 601)')[0].replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = "{os.path.join(HERE, "..", "CFG401_genzel17_gas_shape")}"'))
LF = np.linspace(-4, 3, 701); SC = np.logspace(-3, 2, 251)
def chi(d, a0):
    gb = gshape(d["R"], d["Rh"], d["bt"], d["fgas"]); return min(float(np.sum(((np.log10(d["gobs"]) - np.log10((1.0 if a0 == 0 else C4.nu_mono(gb*10**lf*1e11/a0))*gb*10**lf*1e11))/d["elog"])**2)) for lf in LF)
for foot in A0:
    s = sum(chi(d, A0[foot]*de(d["z"])) - min(chi(d, A0[foot]*x) for x in SC) for g, d in data.items() if g != "zC 406690")
    print(f"{foot}: summed DE penalty WITHOUT zC 406690 = {s:.2f}")
g = "zC 406690"; d0 = data[g]; z, kpa, inc0, Rh, s0, bt, vc, ms, mb = T1[g]
for inc in (13, 25, 37):
    f = math.sin(math.radians(inc0)) / math.sin(math.radians(inc))       # rescale deprojected v
    V = np.sqrt(np.maximum(d0["gobs"] * d0["R"] * KPC / 1e6 - 3.36 * s0**2 * (d0["R"] / Rh), 1e-6)) * f
    d = dict(d0); d["gobs"] = (V**2 + 3.36 * s0**2 * (d0["R"] / Rh)) * 1e6 / (d0["R"] * KPC)
    pen = chi(d, A0["canonical"]*de(z)) - min(chi(d, A0["canonical"]*x) for x in SC)
    print(f"zC 406690 at inclination {inc} deg: DE penalty {pen:.2f}")

#!/usr/bin/env python3
"""CFG540 Part B (descriptive, FROZEN_CRITERIA.md section 5): MHONGOOSE ultra-deep HI profiles (Veronese+2026, J/A+A/712/A74).
No rotation curves are in this catalogue, so no RAR or outer-slope test is possible from it.
M_HI(<R) from the global stacked face-on profile; for N_HI thresholds 1e20 and 1e19 cm^-2: the radius where the profile first
drops below, the HI mass fraction beyond, and the gas-only spherical g_bar there (1.33 M_HI(<R)) in units of a0 (both footings).
kappa = 1/2 FITTED; footings never pooled.
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("CFG540_DATA", os.path.join(HERE, "..", "..", "..", "_external_data", "vizier2026"))
G, MSUN, KPC, MH = 6.674e-11, 1.989e30, 3.0857e19, 1.6735e-27
FOOT = {"can": 9.36e-11, "alt": 1.13e-10}
OUT = []


def log(s=""):
    print(s); OUT.append(s)


def read():
    t1, pr, sect = {}, {}, None
    for l in open(os.path.join(DATA, "J_A_A_712_A74.tsv")):
        if l.startswith("#Table"):
            sect = "t1" if "table1" in l else "pr"
            continue
        if l.startswith("#"): continue
        r = l.rstrip("\n").split("\t")
        if not r[0].strip().isdigit(): continue
        if sect == "t1":
            t1[r[1].strip()] = dict(name=r[2].strip(), D=float(r[5]), lMHI=float(r[6]), inc=int(r[7]), lMs=float(r[8]))
        else:
            pr.setdefault(r[1].strip(), []).append((float(r[3]), float(r[6])))
    return t1, pr


def main():
    t1, pr = read()
    log(f"CFG540 Part B: MHONGOOSE, {len(t1)} galaxies, {sum(len(v) for v in pr.values())} profile rows. No rotation curves in the catalogue.")
    res = dict(galaxies={})
    for h, p in pr.items():
        R = np.array([0.0] + [q[0] for q in p]); N = np.array([p[0][1]] + [q[1] for q in p]) * 1e19 * 1e4   # m^-2
        N = np.maximum(N, 0.0)
        dM = 2 * np.pi * R * KPC * N * MH
        M = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(R * KPC))]) / MSUN
        Mtot = M[-1]
        g = dict(name=t1[h]["name"], lMHI_cat=t1[h]["lMHI"], lMHI_profile=math.log10(Mtot), Rmax_kpc=float(R[-1]),
                 lMs=t1[h]["lMs"], thresholds={})
        line = f"{h} {t1[h]['name']:11s} logMHI cat {t1[h]['lMHI']:.2f} prof {math.log10(Mtot):.2f}  Rmax {R[-1]:5.1f} kpc"
        for th in (1e20, 1e19):
            below = np.where((N < th * 1e4) & (R > 0))[0]
            if len(below) == 0:
                g["thresholds"][f"{th:.0e}"] = None; line += f" | N<{th:.0e}: never"; continue
            i = below[0]                                         # frozen literal: first drop below
            above = np.where((N >= th * 1e4) & (R > 0))[0]       # disclosed variant: outermost crossing (ring/central-hole safe)
            io = int(min(above[-1] + 1, len(R) - 1)) if len(above) else i
            fbo = float(1 - M[io] / Mtot)
            Rt = float(R[i]); fb = float(1 - M[i] / Mtot)
            gb = G * 1.33 * M[i] * MSUN / (Rt * KPC) ** 2
            gl = G * 1.33 * Mtot * MSUN / (R[-1] * KPC) ** 2
            g["thresholds"][f"{th:.0e}"] = dict(R_kpc=Rt, R_over_Rmax=Rt / R[-1], frac_HI_beyond=fb,
                                                lg_gas_over_a0={k: math.log10(gb / v) for k, v in FOOT.items()},
                                                lg_gas_at_Rmax_over_a0={k: math.log10(gl / v) for k, v in FOOT.items()},
                                                outermost_R_kpc=float(R[io]), outermost_frac_HI_beyond=fbo)
            line += f" | N<{th:.0e}: R {Rt:5.1f} kpc, HI beyond {100 * fb:4.1f}%, log g_gas/a0 {math.log10(gb / FOOT['can']):+.2f}/{math.log10(gb / FOOT['alt']):+.2f} (outermost: {R[io]:.1f} kpc, {100 * fbo:.1f}%)"
        log(line)
        res["galaxies"][h] = g
    for th in ("1e+20", "1e+19"):
        f = [g["thresholds"][th]["frac_HI_beyond"] for g in res["galaxies"].values() if g["thresholds"].get(th)]
        fo = [g["thresholds"][th]["outermost_frac_HI_beyond"] for g in res["galaxies"].values() if g["thresholds"].get(th)]
        res[f"frac_beyond_{th}"] = dict(N=len(f), median=float(np.median(f)), max=float(np.max(f)), mean=float(np.mean(f)),
                                        outermost_median=float(np.median(fo)), outermost_mean=float(np.mean(fo)), outermost_max=float(np.max(fo)))
        log(f"HI mass beyond N_HI={th} cm^-2 (first drop, frozen literal): median {100 * np.median(f):.1f}%, mean {100 * np.mean(f):.1f}%, max {100 * np.max(f):.1f}% (N {len(f)})")
        log(f"   outermost crossing (disclosed variant): median {100 * np.median(fo):.1f}%, mean {100 * np.mean(fo):.1f}%, max {100 * np.max(fo):.1f}%")
    d = [g["lMHI_profile"] - g["lMHI_cat"] for g in res["galaxies"].values()]
    res["profile_minus_catalogue_dex"] = dict(median=float(np.median(d)), min=float(np.min(d)), max=float(np.max(d)))
    log(f"Profile-integrated minus table1 log M_HI: median {np.median(d):+.2f} dex (range {np.min(d):+.2f}..{np.max(d):+.2f})")
    json.dump(res, open(os.path.join(HERE, "cfg540_mhongoose_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg540_mhongoose.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()

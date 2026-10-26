"""IB1 diagnostics (NOT GRADED): where does the core law's ~2x INNER over-prediction come from?

D1  per-bin lensing amplitude A = n/d (all 326, MGAS500 'all' cell): measured, cross shear, OS1 Burkert prediction.
D2  OS1 halo + baryon mass vs the gas's own hydrostatic mass (106 KT clusters; isothermal kT, the record's beta-model
    gas shape: beta 2/3, r_c 0.15 R500, F1/X2 convention), at r = 0.15, 0.3, 0.46, 1, 2 Mpc.
D3  lensing of the hydrostatic mass alone (route E: total mass = M_HSE, Newtonian, truncated at 3 Mpc like the gas):
    INNER / MID / OUTER A for the 106 KT clusters, next to the measured A and OS1's prediction.

Read-only on IC1's loader (ic1b_lib -> SC1 -> X38 -> X30/X2/X7). kappa = 1/2 FITTED. Not theory closed.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ib1_diagnostics.py
"""
import os, sys, io, json, math, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "IC1_inner_cluster_band"))
import numpy as np
import ic1b_lib as L

NX = L.NX; G, MPC, MSUN = NX["G"], NX["MPC"], NX["MSUN"]; RG, RM = NX["RG"], NX["RM"]
MY, HXI, BANDS, BN = NX["MY"], NX["HXI"], NX["BANDS"], L.BN
MP, KEV = 1.67262192e-27, 1.602176634e-16
OUT = []; RES = {}
def P(s): OUT.append(s); print(s, flush=True)

def m_hse(i, foot, hk, rcut=3.0):
    """Isothermal hydrostatic mass of the record's beta-model gas: M = 3 beta (kT/mu m_p) r^3 / (G (r^2 + r_c^2))."""
    pp = L.prep(i, foot, hk); s2 = L.KT[i] * KEV / (0.6 * MP); rc = 0.15 * pp["R500"]; r = np.minimum(RG, rcut)
    return 3 * (2 / 3) * s2 * (r * MPC) ** 3 / (G * ((r * MPC) ** 2 + (rc * MPC) ** 2))

def halo_os1(i, foot, hk):
    pp = L.prep(i, foot, hk); q = L.QF[foot]; Sg = L.SIG[foot] * (L.SIG_C[i] / L.SREF) ** q
    r0, sat = L.solve_r0_shape(pp["Mfair"], pp["rta"], Sg, L.B_burk)
    return pp["Mb"] + math.pi * Sg * r0 ** 2 * L.B_burk(np.minimum(RM, pp["rta"]) / r0), r0 / MPC, sat

P("IB1 diagnostics (not graded); kappa = 1/2 FITTED; not theory closed")
hk = "h0672"; hx = HXI[hk]; d = L.DAT[hk]; WB = d["W"] * d["B"][None, :]
nbin = (WB * (d["D"] - MY["leakP"][:, hx, 0])).sum(0); xbin = (WB * d["Dx"]).sum(0)
IK = np.where(L.OKK)[0]
for foot in L.FEET:
    P(f"\n=== {foot} (h 0.672) ===")
    VC = L.DC[(foot, hk)]; V = np.zeros_like(VC); VH = np.zeros_like(VC); r0s = []; ratios = {r: [] for r in (0.15, 0.3, 0.46, 1.0, 2.0)}
    for i in L.ALLI:
        i = int(i); Msrc, r0, sat = halo_os1(i, foot, hk); r0s.append(r0); V[i] = L.dvecN(i, foot, hk, Msrc)
        if L.OKK[i]:
            Mh = m_hse(i, foot, hk); VH[i] = L.dvecN(i, foot, hk, Mh)
            for r in ratios: ratios[r].append(float(np.interp(r, RG, Msrc) / np.interp(r, RG, Mh)))
        L.PREP.clear()
    dC = VC.sum(0); Am, Ax, Ap = nbin / dC, xbin / dC, V.sum(0) / dC
    P("D1 per bin (all 326): bin | measured A | cross A_x | OS1 pred | pred/meas")
    for b in range(8): P(f"   {b}  {Am[b]:7.3f}  {Ax[b]:+7.3f}  {Ap[b]:7.3f}  {Ap[b] / Am[b]:6.2f}")
    P(f"   OS1 halo r0 (Mpc): median {np.median(r0s):.3f}, 16-84% {np.percentile(r0s, 16):.3f}-{np.percentile(r0s, 84):.3f}")
    P("D2 (OS1 halo + baryons) / M_HSE, 106 KT clusters: median [16-84%]")
    for r, v in ratios.items(): P(f"   r = {r:4.2f} Mpc: {np.median(v):.2f} [{np.percentile(v, 16):.2f}, {np.percentile(v, 84):.2f}]")
    o = L.M[f"{foot}|{hk}"]; D3 = {}
    P("D3 KT_all (106): band | measured A +- s | OS1 pred | HSE-lensing pred")
    for bi, b in enumerate(BN):
        idx = BANDS[b]; dk = VC[IK][:, idx].sum(); ms = o[f"KT_all|{b}"]
        a_os1 = V[IK][:, idx].sum() / dk; a_h = VH[IK][:, idx].sum() / dk; s = ms.get("s_IN", ms["s"])
        D3[b] = dict(meas=ms["A"], s=s, os1=a_os1, hse=a_h)
        P(f"   {b:5s}  {ms['A']:.3f} +- {s:.3f}  {a_os1:.3f}  {a_h:.3f}")
    RES[foot] = dict(bins=dict(meas=Am.tolist(), cross=Ax.tolist(), os1=Ap.tolist()), r0_median=float(np.median(r0s)),
                     mass_ratio={str(r): [float(np.median(v)), float(np.percentile(v, 16)), float(np.percentile(v, 84))] for r, v in ratios.items()}, D3=D3)
json.dump(RES, open(os.path.join(HERE, "ib1_diagnostics_results.json"), "w"), indent=1)
open(os.path.join(HERE, "ib1_diagnostics.out"), "w").write("\n".join(OUT) + "\n")

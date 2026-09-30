#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A8_energy -- G3 energy: the canonical (Noether) energy of the interaction sector on the solved static fields, with sign, against the baryons' orbital energy
(1/2) M_b V_f^2, V_f^2 = sqrt(G M_b a0), inside r_e = 0.4 r_ta (this lane's convention, CFG48 Gcommon.r_ta_kpc, read-only) and inside r_e times 1.7 and 3.6
(the CFG4 convention's range, CFG48 referee note: r_ta differ by 1.7-3.6x).  For static fields the Hamiltonian density is -L, so
    E_int(<r_e)  = -(sigma_s a0^2 / 8 pi G) Int_0^{r_e} M(Q) 4 pi r^2 dr        (interaction term alone)
    E_rel(<r_e)  = -(1/8 pi G) Int [ b (dPsi'^2 - 2 dPhi' dPsi') + sigma_s a0^2 M(Q) + b y^2 ] 4 pi r^2 dr   (relative sector = EH_relative + interaction, EXCESS over the decoupled Newtonian value -b y^2, whose 1/r_min point-mass self-energy would otherwise dominate)
Point mass, P2 (nu_mono reported).  Hand indicator (frozen 2): the isolated deep-MOND AQUAL field energy is (1/3) M V_f^2 ln(r_e/r_M).
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A8_energy")
P = R.P
GC = C.load_gcommon()
res = {}
for kn in ("P2", "nu_mono"):
    d = C.Design(C.KERNELS[kn], 1.0, 1.0, +1)
    Qs, ms = d.Qs, d.ms
    Mint = np.concatenate([[Qs[0] * ms[0]], Qs[0] * ms[0] + np.cumsum(0.5 * (ms[1:] + ms[:-1]) * np.diff(Qs))])

    def Mq(Q):
        Q = np.asarray(Q, float)
        return np.where(Q <= Qs[0], Q * ms[0], np.interp(Q, Qs, Mint))
    b = 1.0 * 1.0 / (1.0 + 1.0)                               # beta gamma/(beta+gamma) at beta = gamma = 1
    for Mb in (1e9, 1e10, 1e11, 1e12):
        a0 = C.A0_KPC
        rM = math.sqrt(C.G * Mb / a0)
        Vf2 = math.sqrt(C.G * Mb * a0)
        Eorb = 0.5 * Mb * Vf2
        rta = GC.r_ta_kpc(Mb)
        for label, fac in (("conv1 (0.4 r_ta, lane)", 1.0), ("conv2-low (x1.7)", 1.7), ("conv2-high (x3.6)", 3.6)):
            re = 0.4 * rta * fac
            rr = np.geomspace(1e-3 * rM, re, 6000)
            yN = (rM / rr) ** 2
            Q = np.interp(np.log(yN), np.log(d.y), d.Q)
            dPsi = np.interp(np.log(yN), np.log(d.y), d.dPsi)
            x_ = np.interp(np.log(yN), np.log(d.y), d.x)
            dPhi = dPsi * (1 + 8 * x_)
            Mv = Mq(Q)
            w = 4 * math.pi * rr ** 2
            # units: a0^2/(8 pi G) [(km/s)^4/kpc^2 / ((km/s)^2 kpc/Msun)] * kpc^3 -> Msun (km/s)^2 ; a0-unit fields
            pref = a0 ** 2 / (8 * math.pi * C.G)
            Eint = -pref * np.trapz(Mv * w, rr)
            Lrel = b * (dPsi ** 2 - 2 * dPhi * dPsi) + Mv - (-b * yN ** 2)      # minus the decoupled (Newtonian, m = 0) relative-sector value -b y^2: the point-mass self-energy divergence cancels
            Erel = -pref * np.trapz(Lrel * w, rr)
            hand = (1.0 / 3.0) * Mb * Vf2 * math.log(re / rM)
            res[(kn, Mb, label)] = dict(re_over_rM=re / rM, E_int_over_orb=Eint / Eorb, E_rel_over_orb=Erel / Eorb, hand_over_orb=hand / Eorb)
            if kn == "P2" and Mb in (1e9, 1e12):
                P(f"  {kn} M_b = {Mb:.0e} {label:24s}: r_e/r_M = {re/rM:8.1f}: E_int/(1/2 M V_f^2) = {Eint/Eorb:+10.3f} ; E_rel/(...) = {Erel/Eorb:+10.3f} ; deep-MOND hand (2/3)ln(r_e/r_M) = {hand/Eorb:.2f}")
R.num("energy", {"|".join(map(str, k)): v for k, v in res.items()})
allint = [abs(v["E_int_over_orb"]) for k, v in res.items() if k[0] == "P2"]
allrel = [abs(v["E_rel_over_orb"]) for k, v in res.items() if k[0] == "P2"]
signs = {("+" if v["E_int_over_orb"] > 0 else "-") for k, v in res.items() if k[0] == "P2"}
P(f"  P2: |E_int|/(1/2 M V_f^2) ranges {min(allint):.2f}..{max(allint):.2f};  |E_rel|/(...) ranges {min(allrel):.2f}..{max(allrel):.2f};  sign of E_int over all cases: {signs}")
R.check("G3 energy: the interaction sector's stored energy inside r_e is <= (1/2) M_b V_f^2 in magnitude for every mass and both r_ta conventions", max(allint) <= 1.0, f"max |E_int|/orb = {max(allint):.2f}", kind="result")
R.check("G3 energy: the relative sector's stored energy (EH_relative + interaction) is <= (1/2) M_b V_f^2 in magnitude", max(allrel) <= 1.0, f"max |E_rel|/orb = {max(allrel):.2f}", kind="result")
R.check("the interaction energy has a definite sign on the designed branch (a negative canonical energy is the ghost-like signature; it is reported, not counted as a pass)", len(signs) == 1, f"sign {signs}", kind="result")
worst = max(max(allint), max(allrel))
R.verdict("G3 energy (13a/13b/13c-analogue, field-side)", "FAIL" if worst > 1.0 else "PASS", f"stored energy up to {worst:.1f} x the baryons' orbital energy (sign {signs}); origin: the field, not supplied by the vacuum or the baryons; a NEGATIVE interaction energy would mean the sector lowers the total energy (unbounded from below with the fourth-order vector)")
R.finish(None)

#!/usr/bin/env python3
"""Finite audit of actual FRZ1/FZS1/JNT2 enclosed masses; no spectra/box runs."""
import argparse
import contextlib
import csv
import io
import json
import math
import os
from pathlib import Path
import sys
import time

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"
sys.dont_write_bytecode = True
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
JPATH = ROOT / "closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_hm.py"
ZS = (0.0, 2.2, 3.0, 4.4)
FACS = (1.25, 2.0, 3.0, 5.0)


def exact_cold(mb, r, a0, G, h):
    """Positive root, rationalized for cancellation resistance; Msun/h."""
    t = mb * np.asarray(r) ** 2 * a0 / (G * h)
    return 2 * t / (np.sqrt(mb * mb + 4 * t) + mb)


def residual(total, source, r, a0, G, h):
    """g^2/[gN*(a0+g)] - 1; comoving-scaled a0, nonzero radii."""
    g = G * h * total / r ** 2
    gn = G * h * source / r ** 2
    return g * g / (gn * (a0 + g)) - 1


def stats(rows, key):
    a = [r[key] for r in rows if r[key] is not None]
    return [min(a), max(a)] if a else None


def run(out):
    started = time.monotonic()
    sys.path.insert(0, str(JPATH.parent))
    code = JPATH.read_text()
    J = {"__file__": str(JPATH), "__name__": "jnt2_mass_audit"}
    # Exactly the actual layout definitions; stop before JNT2's execution loops.
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code[:code.index('\nP(f"JNT2 G1')], str(JPATH), "exec"), J)
    Z, F, L, C = J["Z"], J["F"], J["L"], J["C"]
    h, FB, G = F["h"], F["FB"], F["G"]
    rows, profiles = [], {}
    errors = {k: 0.0 for k in (
        "B_independent_reconstruction_rel_patch", "FZS1_reconstruction_rel_patch",
        "JNT2_reconstruction_rel_patch", "raw_law_polynomial_residual",
        "raw_cold_vs_original_phantom_rel_patch", "FZS1_mass_conservation_rel_patch",
        "JNT2_mass_conservation_rel_patch", "join_cold_match_rel_patch",
        "exterior_reference_rel_patch", "baryon_endpoint_budget_rel_patch")}
    min_increment = {"B": 0.0, "FZS1": 0.0, "JNT2": 0.0}
    for z in ZS:
        J["setz"](z)
        for foot in Z["FOOTS"]:
            vst, X, a0 = C.vstar_kms(foot, z), F["Xsh"](foot), F["a0c"](foot)
            for fac in FACS:
                fnS, fnJ = Z["lay_S"](foot, z, fac), J["lay_J"](foot, z, fac)
                for idx, hb in enumerate(L["HB"]):
                    R = Z["rset_com"](hb, foot, z, fac)
                    Z["CUR"][0] = R
                    r, MB, info = F["layout"](hb, foot, mode="B")
                    rr, MR, _ = F["layout"](hb, foot, mode="Rb")
                    Z["CUR"][0] = 0.0
                    assert np.array_equal(r, rr)
                    bar = Z["Bar"](hb, foot, r)
                    CB, CR = MB - bar, MR - bar
                    i = int(np.argmin(abs(r - R)))
                    assert abs(r[i] / R - 1) < 1e-12
                    s = CR[i] / CB[i]
                    independentS = np.where(r <= R, bar + s * CB, MR)
                    rs, MS, _ = fnS(hb)
                    assert np.array_equal(rs, r)
                    rj, MJ, ij = fnJ(hb)
                    above = bool(F["v_vir"](hb) > vst)
                    J_at_R = float(np.interp(R, rj, MJ))
                    independentJ = MR if above else independentS
                    if info["regime"] == "galaxy":
                        mb = np.full_like(r, (1 - FB) * hb["Mta"] / X)
                        raw = exact_cold(mb, r, a0, G, h)
                        cap = (1 - FB) * hb["Mta"]
                        ph = np.minimum(raw, cap)
                        rem = max(cap - ph[-1], 0.0)
                        independentB = bar + ph + rem * r / hb["rta"]
                        pre, W = 0.0, 1.0
                        exterior_baryons = 0.0
                    else:
                        mb = bar.copy()
                        raw = exact_cold(mb, r, a0, G, h)
                        raw[0] = 0.0
                        v = F["v_vir"](hb)
                        pre = min(max(0.5 * (1 - (Z["VST"][foot] / v) ** 2), 0.0), 1.0)
                        W = 1.5 * v * v / (1.5 * v * v + F["CS_IGM"] ** 2)
                        share = (1 - FB) * hb["M200c"]
                        cap = (1 - pre) * share
                        ph = np.minimum(W * raw, cap)
                        rem = max(cap - ph[-1], 0.0)
                        nfw = F["m_nfw"](np.minimum(r, hb["r200c"]) / hb["rs"]) / F["m_nfw"](hb["r200c"] / hb["rs"])
                        outside = np.where(r > hb["r200c"], F["M_L"](hb, r) - hb["M200c"], 0)
                        independentB = bar + pre * share * nfw + ph + rem * r / hb["rta"] + outside
                        exterior_baryons = FB * (hb["Mta"] - hb["M200c"])
                    use = (r > 0) & (r <= R) & (mb > 0)
                    lawres = residual((mb + raw)[use], mb[use], r[use], a0, G, h)
                    original = F["phantom"](mb, r, a0)
                    for key, val in (
                        ("B_independent_reconstruction_rel_patch", np.max(abs(MB - independentB)) / hb["Mta"]),
                        ("FZS1_reconstruction_rel_patch", np.max(abs(MS - independentS)) / hb["Mta"]),
                        ("JNT2_reconstruction_rel_patch", np.max(abs(np.interp(rj, r, independentJ) - MJ)) / hb["Mta"]),
                        ("raw_law_polynomial_residual", np.max(abs(lawres))),
                        ("raw_cold_vs_original_phantom_rel_patch", np.max(abs(raw - original)) / hb["Mta"]),
                        ("FZS1_mass_conservation_rel_patch", abs(MS[-1] / hb["Mta"] - 1)),
                        ("JNT2_mass_conservation_rel_patch", abs(MJ[-1] / hb["Mta"] - 1)),
                        ("join_cold_match_rel_patch", abs((MS[i] - bar[i]) - CR[i]) / hb["Mta"]),
                        ("exterior_reference_rel_patch", np.max(abs(MS[r >= R] - MR[r >= R])) / hb["Mta"]),
                        ("baryon_endpoint_budget_rel_patch", abs(bar[-1] + exterior_baryons - FB * hb["Mta"]) / hb["Mta"])):
                        errors[key] = max(errors[key], float(val))
                    for name, mass in (("B", MB), ("FZS1", MS), ("JNT2", MJ)):
                        min_increment[name] = min(min_increment[name], float(np.min(np.diff(mass)) / hb["Mta"]))
                    # Both tests are disclosed: exact-law source in code, and all explicit Bar baryons.
                    epsB = residual(MB[use], mb[use], r[use], a0, G, h)
                    epsS = residual(MS[use], mb[use], r[use], a0, G, h)
                    epsJ = residual(independentJ[use], mb[use], r[use], a0, G, h)
                    epsAll = residual(MS[use], bar[use], r[use], a0, G, h)
                    ratioS = MS[i] / (mb[i] + raw[i])
                    denom = CR[-1] - CR[i]
                    t = (CR[-1] - CB[i]) / denom if denom > 0 else None
                    row = dict(z=z, foot=foot, f=fac, grid_index=idx, regime=info["regime"], split_reference=above,
                        M200m_Msun_h=hb["M"], M200c_Msun_h=hb["M200c"], Mta_Msun_h=hb["Mta"],
                        Mb_fold_Msun_h=Z["Mb_fold"](hb, foot), Mb_fold_Msun=Z["Mb_fold"](hb, foot) / h,
                        Xsh=X, cosmic_cold_per_baryon=(1-FB)/FB, v200c_kms=F["v_vir"](hb), vstar_kms=vst,
                        R_set_nominal_kpc=R / ((1+z)*h)*1000, R_set_effective_JNT2_kpc=0.0 if above else R / ((1+z)*h)*1000,
                        R_set_over_rta=R/hb["rta"], R_set_over_r200c=R/hb["r200c"],
                        source_baryons_at_R_Msun_h=mb[i], Bar_at_R_Msun_h=bar[i],
                        raw_exact_cold_at_R_Msun_h=raw[i], B_cold_at_R_Msun_h=CB[i], reference_cold_at_R_Msun_h=CR[i],
                        FZS1_cold_at_R_Msun_h=MS[i]-bar[i], JNT2_cold_at_nominal_R_Msun_h=J_at_R-bar[i],
                        cosmic_patch_cold_Msun_h=(1-FB)*hb["Mta"], implemented_nonbar_reservoir_Msun_h=CR[-1],
                        outer_baryons_in_nonbar_reservoir_Msun_h=exterior_baryons,
                        raw_exact_over_cosmic_patch_cold=raw[i]/((1-FB)*hb["Mta"]),
                        raw_exact_over_nonbar_reservoir=raw[i]/CR[-1], B_over_nonbar_reservoir=CB[i]/CR[-1],
                        raw_exact_over_reference_at_R=raw[i]/CR[i], B_over_reference_at_R=CB[i]/CR[i], s=s,
                        exact_B_junction_outer_t=t, pre_fraction=pre, pressure_W=W, rem_Msun_h=rem,
                        B_force_residual_source_at_R=float(epsB[-1]), FZS1_force_residual_source_at_R=float(epsS[-1]),
                        JNT2_force_residual_source_at_R=float(epsJ[-1]), FZS1_force_residual_allbar_at_R=float(epsAll[-1]),
                        B_force_residual_source_maxabs=float(np.max(abs(epsB))), FZS1_force_residual_source_maxabs=float(np.max(abs(epsS))),
                        JNT2_force_residual_source_maxabs=float(np.max(abs(epsJ))), FZS1_force_residual_allbar_maxabs=float(np.max(abs(epsAll))),
                        FZS1_acceleration_over_raw_exact_at_R=float(ratioS),
                        FZS1_velocity_over_raw_exact_at_R=float(math.sqrt(ratioS)),
                        FZS1_patch_mass_rel_error=float(MS[-1]/hb["Mta"]-1), JNT2_patch_mass_rel_error=float(MJ[-1]/hb["Mta"]-1),
                        radial_nodes=len(r), inner_radial_nodes=int(np.sum(use)))
                    rows.append({k: v.item() if isinstance(v, np.generic) else v for k, v in row.items()})
                    if idx in (0, 80, 120, 160, 200, 240, 280, 320) and fac in (1.25, 3.0):
                        key = f"{foot}_z{z:g}_f{fac:g}_i{idx}"
                        profiles[key] = np.column_stack([r, mb, bar, raw, CB, CR, MS, independentJ])
                print(f"computed z={z:g} {foot} f={fac:g}: 321 halo masses", flush=True)
    assert len(rows) == 321 * 4 * 2 * 4
    assert errors["B_independent_reconstruction_rel_patch"] < 1e-12
    assert errors["FZS1_reconstruction_rel_patch"] < 1e-12
    assert errors["JNT2_reconstruction_rel_patch"] < 1e-12
    assert errors["raw_law_polynomial_residual"] < 1e-12
    assert max(abs(x) for x in min_increment.values()) < 1e-12
    assert errors["FZS1_mass_conservation_rel_patch"] < 1e-12
    assert errors["JNT2_mass_conservation_rel_patch"] < 1e-12
    summary = []
    for z in ZS:
        for foot in Z["FOOTS"]:
            for fac in FACS:
                cell = [r for r in rows if r["z"]==z and r["foot"]==foot and r["f"]==fac]
                active = [r for r in cell if not r["split_reference"]]
                summary.append(dict(z=z, foot=foot, f=fac, n_total=len(cell), n_active=len(active),
                    n_active_galaxy=sum(r["regime"]=="galaxy" for r in active),
                    n_active_raw_law_exceeds_cosmic_patch=sum(r["raw_exact_over_cosmic_patch_cold"]>1+1e-12 for r in active),
                    n_active_s_above_1=sum(r["s"]>1+1e-12 for r in active),
                    n_active_s_below_1=sum(r["s"]<1-1e-12 for r in active),
                    s_active=stats(active,"s"), raw_over_cosmic_patch_active=stats(active,"raw_exact_over_cosmic_patch_cold"),
                    B_over_nonbar_active=stats(active,"B_over_nonbar_reservoir"),
                    exact_B_outer_t_active=stats(active,"exact_B_junction_outer_t"),
                    FZS1_acceleration_ratio_at_R_active=stats(active,"FZS1_acceleration_over_raw_exact_at_R"),
                    FZS1_force_residual_at_R_active=stats(active,"FZS1_force_residual_source_at_R"),
                    FZS1_force_residual_maxabs_active=stats(active,"FZS1_force_residual_source_maxabs")))
    benchmark=[]
    q=1+C.XS
    for foot in Z["FOOTS"]:
        for z in ZS:
            vs=C.vstar_kms(foot,z)*1000
            H=C.H0*C.E(z)
            for ratio in (0.1,0.5,1.0,q/(q-1),2.0,10.0):
                v=ratio*vs; mt=v**3/(10*C.G*H); mb=mt/q; radius=v/(10*H)
                gn=C.G*mb/radius**2
                accel=(gn+math.sqrt(gn*gn+4*gn*C.A0[foot]))/2
                direct=accel*radius**2/C.G/mt
                analytic=(1+math.sqrt(1+4*q*q/ratio))/(2*q)
                assert abs(direct/analytic-1)<1e-13
                benchmark.append(dict(foot=foot,z=z,v_over_vstar=ratio,exact_total_over_budget=direct,
                    exact_cold_over_cold_budget=(q*direct-1)/(q-1),deep_total_over_budget=math.sqrt(1/ratio)))
    out.mkdir(parents=True,exist_ok=True)
    with (out/"halo_masses.csv").open("w",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    np.savez_compressed(out/"representative_profiles.npz", **profiles)
    result=dict(assertion_tested="Exact source prefixes and independent algebra agree on enclosed masses and the prescribed normalization on the finite grid; conservation and force-law residual are distinct tests.",
        scope=dict(redshifts=ZS,factors=FACS,footings=Z["FOOTS"],halo_log10M200m_Msun_h=[8,16],halo_count_per_cell=321,rows=len(rows),radial_grid="original 1600 log nodes plus 0 and layout/junction nodes"),
        constants=dict(h=h,FB=FB,Xsh=F["XTAB"],X_crossing=C.XS),checks=errors,min_increment_rel_patch=min_increment,
        summary=summary,common_r200_benchmark=benchmark,
        profile_columns=["r_comoving_Mpc_h","source_baryons_Msun_h","Bar_Msun_h","raw_exact_cold_Msun_h","B_cold_Msun_h","reference_cold_Msun_h","FZS1_total_Msun_h","JNT2_total_Msun_h"],
        elapsed_seconds=time.monotonic()-started)
    (out/"results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(dict(rows=len(rows),checks=errors,elapsed=result["elapsed_seconds"]),indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(); run(args.output)

#!/usr/bin/env python3
"""Bounded XJ1 profile/current audit. Writes only the supplied new result path.

No forest boxes, shell trajectories or numerical field equations are rerun.
The exact proof is in JUNCTION_THEOREM.md; this script checks identities and
one-sided charge densities on the existing FRZ1/XJ1 halo grid.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
import sys
sys.dont_write_bytecode = True
import json, math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface"))
import xj1_lib2 as XL


def exact_checks():
    b, c, T, x = sp.symbols("b c T x")
    t = (T-b)/(T-c)
    E = b + t*(x-c)
    n_i, n_o, v_i, v_o, speed = sp.symbols("n_i n_o v_i v_o speed")
    jump = n_o*(v_o-speed)-n_i*(v_i-speed)
    residuals = {
        "mass_continuity": sp.simplify(E.subs(x,c)-b),
        "total_mass": sp.simplify(E.subs(x,T)-T),
        "outer_slope": sp.simplify(sp.diff(E,x)-t),
        "front_speed": sp.simplify(jump.subs(speed,(n_o*v_o-n_i*v_i)/(n_o-n_i))),
        "required_outer_speed": sp.simplify(jump.subs({v_i:0,v_o:speed*(1-n_i/n_o)})),
    }
    assert all(r == 0 for r in residuals.values())
    # Exact positive examples obey continuity/total mass but have density jumps.
    # Unit outer radius; C_B(r)=T*r, C_R(r)=T*r^2, R=1/2.
    R, Tq = Q(1,2), Q(1)
    tq = (Tq-Tq*R)/(Tq-Tq*R*R)
    inside_slope, outside_slope = Tq, tq*2*Tq*R
    assert tq == Q(2,3) and inside_slope/outside_slope == Q(3,2)
    # Stationary surface + static inside + infall outside leaves nonzero delta source.
    assert outside_slope*(-1) != inside_slope*0
    # Moving front can satisfy charge conservation: speed 2, outer velocity -1.
    assert outside_slope*(-1-2) == inside_slope*(0-2)
    # A second positive static junction requires outflow at a growing front.
    # C_B=r^2, C_R=r at R=1/2, t=3/2, density ratio 2/3.
    tq2=(1-R*R)/(1-R)
    assert tq2 == Q(3,2) and 2*R/tq2 == Q(2,3)
    return {"symbolic_residuals":{k:str(v) for k,v in residuals.items()},
            "exact_examples":{"inflow_compatible_ratio":"3/2", "outflow_required_ratio":"2/3"}}


def transport_checks():
    """Exact checks of the constructive continuity-only path, no field dynamics."""
    a,adot,delta,sr,se,tau=sp.symbols("a adot delta sr se tau")
    slope=(1-a)*sr+a*se
    velocity=-adot*delta/slope
    time=sp.symbols("time")
    schedule=1-sp.exp(-time/tau)
    residuals={
        "integrated_continuity":sp.simplify(adot*delta+velocity*slope),
        "exponential_schedule":sp.simplify(sp.diff(schedule,time)-(1-schedule)/tau),
        "bound_denominator_remainder":sp.simplify(slope-(1-a)*sr-a*se),
    }
    assert all(x==0 for x in residuals.values())
    # Exact capped target C_E=min(2r,1), C_R=r, L=T=tau=1.
    # The endpoint density vanishes outside 1/2; all finite-time mixtures remain positive.
    n=0; worst=Q(0)
    for aq in (Q(0),Q(1,2),Q(3,4),Q(7,8),Q(15,16),Q(255,256)):
        da=1-aq
        for r in (Q(1,8),Q(1,4),Q(1,2),Q(3,4),Q(1)):
            target=min(2*r,Q(1)); diff=target-r
            for target_slope in ((Q(2),Q(0)) if r==Q(1,2) else ((Q(2),) if r<Q(1,2) else (Q(0),))):
                density_slope=(1-aq)+aq*target_slope
                v=-da*diff/density_slope
                assert density_slope>0
                assert da*diff+density_slope*v==0
                assert abs(v)<=abs(diff)
                worst=max(worst,abs(v));n+=1
        assert (1-aq)*0+aq*0==0 and (1-aq)*1+aq*1==1
    # At R=1/2 two one-sided velocities differ but the flux is the same.
    # A finite-time linear schedule a=t (tau=1) gives v=-delta/(1-t) in the cap;
    # the exponential schedule instead gives v=-delta there at every finite time.
    linear=sp.simplify((-delta/(1-time))*(1-time)+delta)
    exponential_cap=sp.simplify(velocity.subs({adot:(1-a)/tau,se:0})+delta/(tau*sr))
    assert linear==0 and exponential_cap==0
    return {"symbolic_residuals":{k:str(v) for k,v in residuals.items()},
            "exact_rational_trace_checks":n,"capped_example_max_abs_velocity_tau1":str(worst),
            "linear_schedule_cap_blowup_identity":str(linear),
            "exponential_schedule_cap_velocity_identity":str(exponential_cap),
            "non_claims":["Continuity and positivity only; no constitutive, momentum, energy or full-current field solution.",
                          "tau is arbitrary and target arrival is asymptotic; neither is a derived settling law."]}


def audit_profiles():
    XL.install()
    Z=XL.X.rec(); F,L=Z["F"],Z["L"]
    layout, Bar, CUR=Z["layout"],Z["Bar"],Z["CUR"]
    rows=[]; by_case={}; max_inner=0.; max_mass=0.; min_increment=0.
    zs=[0.0]+XL.ZB
    for foot in XL.FOOTS:
        for z in zs:
            Z["set_z"](z); vs=XL.X.vstar(foot,z)
            for k in (2,3):
                key=f"{foot}|{z}|k{k}"
                group=[]
                for hb in L["HB"]:
                    if F["v_vir"](hb)>vs:
                        continue
                    r,M,info=XL.exact_fn(foot,z,vs,XL.COL_K[k])(hb)
                    if "R_set" not in info:
                        continue
                    R=info["R_set"]; idx=info["i_set"]; t=info["t"]
                    CUR[0]=R
                    rB,MB,_=layout(hb,foot,mode="B")
                    CUR[0]=0.
                    max_inner=max(max_inner,float(np.max(np.abs(M[:idx+1]-MB[:idx+1]))/hb["Mta"]))
                    max_mass=max(max_mass,abs(float(M[-1]/hb["Mta"]-1)))
                    min_increment=min(min_increment,float(np.min(np.diff(M))/hb["Mta"]))
                    slopes=[]
                    original_grid=F["rgrid"]
                    try:
                        for eps in (1e-4,1e-5,1e-6):
                            nodes=np.array([R*(1-eps),R,R*(1+eps),hb["rta"]])
                            F["rgrid"]=lambda h,rm,nodes=nodes:nodes.copy()
                            rb,mb,_=layout(hb,foot,mode="B")
                            rr,mr,_=layout(hb,foot,mode="Rb")
                            cb=mb-Bar(hb,foot,rb); cr=mr-Bar(hb,foot,rr)
                            b0,bm=np.interp([R,R*(1-eps)],rb,cb)
                            cp,c0=np.interp([R*(1+eps),R],rr,cr)
                            slopes.append(((b0-bm)/(R*eps),t*(cp-c0)/(R*eps)))
                    finally:
                        F["rgrid"]=original_grid
                    si,so=slopes[-1]
                    scale=hb["Mta"]/R
                    q=si/so if so>1e-10*scale else None
                    conv=max(abs(slopes[-1][j]-slopes[-2][j])/max(abs(slopes[-1][j]),abs(slopes[-2][j]),1e-9*scale) for j in (0,1))
                    conv_abs=max(abs(slopes[-1][j]-slopes[-2][j])/scale for j in (0,1))
                    conv_ok=all(abs(slopes[-1][j]-slopes[-2][j])<=1e-3*max(abs(slopes[-1][j]),abs(slopes[-2][j]))+1e-9*scale for j in (0,1))
                    row={"footing":foot,"z":z,"caustic":k,"logM200m":math.log10(hb["M"]),
                         "logMb_physical":math.log10(Z["Mb_fold"](hb,foot)/Z["h"]),
                         "regime":info.get("regime"),"R_set_comoving_Mpch":R,"t":t,
                         "cold_density_inside_over_outside":q,
                         "required_vout_over_front_speed":None if q is None else 1-q,
                         "one_sided_slope_convergence":conv,
                         "one_sided_slope_absolute_change_normalized":conv_abs,
                         "one_sided_slope_mixed_tolerance_pass":conv_ok,
                         "cold_slope_inside":si,"cold_slope_outside":so,
                         "cold_slope_inside_normalized":si/scale,"cold_slope_outside_normalized":so/scale}
                    rows.append(row); group.append(row)
                ratios=[a["cold_density_inside_over_outside"] for a in group if a["cold_density_inside_over_outside"] is not None]
                by_case[key]={"n":len(group),"positive_outer_density":len(ratios),
                    "outflow_required_for_growing_front":sum(q<0.999 for q in ratios),
                    "inflow_compatible_for_growing_front":sum(q>1.001 for q in ratios),
                    "near_equal_density":sum(0.999<=q<=1.001 for q in ratios),
                    "ratio_min_med_max":[float(np.min(ratios)),float(np.median(ratios)),float(np.max(ratios))],
                    "max_slope_convergence":max(a["one_sided_slope_convergence"] for a in group)}
    allq=[a["cold_density_inside_over_outside"] for a in rows if a["cold_density_inside_over_outside"] is not None]
    checks={"interior_equal":max_inner<1e-12,"endpoint_conserved":max_mass<1e-9,
            "monotone_mass":min_increment>=-1e-9,
            "nonnegative_t":all(a["t"]>=-1e-12 for a in rows),
            "nonnegative_cold_slopes":all(min(a["cold_slope_inside_normalized"],a["cold_slope_outside_normalized"])>=-1e-9 for a in rows),
            "stable_one_sided_slopes":all(a["one_sided_slope_mixed_tolerance_pass"] for a in rows)}
    return {"assertion_tested":"XJ1 k=2,3 profiles have exact-law-layout interiors, conserved total mass and nonnegative profile slopes on both footings at z=0 and 12 forest redshifts; diagnose one-sided density jump only.",
            "non_claims":["No field equation solution or full-current junction is established.",
                          "No actual velocity or front-speed history is specified by these snapshot profiles.",
                          "The q<1 count excludes only static interiors, outward moving fronts and pure advective infall taken together.",
                          "Exact-law-layout means source code mode B; equality to the algebraic force law is not independently certified here."],
            "profile_count":len(rows),"checks":checks,"positive_outer_density_count":len(allq),
            "degenerate_outer_density_count":len(rows)-len(allq),"max_interior_error_over_Mta":max_inner,
            "max_endpoint_relative_error":max_mass,"min_mass_increment_over_Mta":min_increment,
            "count_outflow_required_for_growing_front":sum(q<0.999 for q in allq),
            "count_inflow_compatible_for_growing_front":sum(q>1.001 for q in allq),
            "max_slope_convergence":max(a["one_sided_slope_convergence"] for a in rows),
            "max_slope_convergence_positive_outer_density":max(a["one_sided_slope_convergence"] for a in rows if a["cold_density_inside_over_outside"] is not None),
            "max_slope_absolute_change_normalized":max(a["one_sided_slope_absolute_change_normalized"] for a in rows),
            "groups":by_case,"rows":rows}


if __name__=="__main__":
    out={"exact_checks":exact_checks(),"transport_checks":transport_checks(),"profile_audit":audit_profiles()}
    path=Path(sys.argv[1]).resolve()
    assert path.is_relative_to(ROOT/"codex_mass_budget_2026_11_14/latest_review")
    normalize=lambda v:v.item() if isinstance(v,np.generic) else str(v)
    path.write_text(json.dumps(out,indent=2,default=normalize)+"\n")
    p=out["profile_audit"]
    print(json.dumps({k:v for k,v in p.items() if k not in ("groups","rows")},indent=2,default=normalize))
    assert all(p["checks"].values()),p["checks"]

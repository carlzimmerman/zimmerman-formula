#!/usr/bin/env python3
"""Necessary NR medium-emission kinematics. No rate/action/empirical fit inferred."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[4]
    v,w,cs,d,mu = s.symbols("v w cs d mu", real=True)
    gain = w*w/2-v*w*mu
    balance = cs*w+gain-d
    identities = {
        "energy_partition": s.expand((d-cs*w)-gain+balance),
        "angular_equation": s.expand(w*(cs+w/2-d/w-v*mu)-balance),
        "opposite_direction_difference": s.expand(balance.subs(mu,-1)-balance.subs(mu,1)-2*v*w),
        "cold_energy": s.expand(balance.subs(v,0)-(cs*w+w*w/2-d))
    }
    assert all(value == 0 for value in identities.values())
    examples=[]
    c=s.Rational("299792.458")
    recoil=s.Integer(650)
    poisson_mean=s.Rational("2.3077948724637416")
    for speed in (s.Integer(1),s.Integer(10),s.Integer(300),s.Integer(537)):
        cold_release=speed*recoil+recoil**2/2
        examples.append({"cs_kms":int(speed),
                         "parameter_example_only":True,
                         "zero_release_min_v_for_fixed_recoil_kms":str(speed+recoil/2),
                         "cold_release_over_m_km2s2":str(cold_release),
                         "cold_release_over_mc2":str(s.N(cold_release/c**2,25)),
                         "cold_heating_over_mc2":str(s.N(recoil**2/(2*c**2),25)),
                         "mean_required_internal_reservoir_over_mc2":str(s.N(poisson_mean*cold_release/c**2,25))})
    # Positive release allows cold emission: a rational construction supplies
    # a physical root at w=650 for every positive cs example, without squaring.
    cold_residues=[s.simplify(balance.subs({v:0,w:recoil,cs:s.Integer(z["cs_kms"]),d:s.Integer(z["cs_kms"])*recoil+recoil**2/2})) for z in examples]
    assert all(z==0 for z in cold_residues)
    # For Delta>0, a positive root exists for each angle. Check original,
    # unsquared energy balance at a finite exact grid, then 30-digit display.
    grid=[]
    for vv in (0,10,100,650,1000):
        for ss in (10,300,537):
            dd=s.Integer(ss)*650+s.Rational(650**2,2)
            for mm in (-1,0,1):
                root_w=s.Integer(vv)*mm-ss+s.sqrt((ss-s.Integer(vv)*mm)**2+2*dd)
                residue=s.simplify(balance.subs({v:vv,cs:ss,d:dd,mu:mm,w:root_w}))
                assert residue==0 and root_w>0
                grid.append({"v":vv,"cs":ss,"mu":mm,"d":str(dd),"w":str(s.N(root_w,30)),"gain_over_m":str(s.N(dd-ss*root_w,30)),"energy_residue":str(residue)})
    # Reuse already installed Lean and narrowly scoped compiled imports.
    packages=root/"qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/.lake/packages"
    env=dict(os.environ)
    env["LEAN_PATH"]=os.pathsep.join(str(p/".lake/build/lib/lean") for p in sorted(packages.iterdir()) if (p/".lake/build/lib/lean").is_dir())
    lean="/Users/carlzimmerman/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean"
    argv=[lean,str(here/"MediumEmission.lean")]
    run=subprocess.run(argv,env=env,capture_output=True,text=True,timeout=120)
    result={"scope":"positive-energy linear clock dispersion and fixed-mass NR tracer only",
            "exact_symbolic_residues":{key:str(value) for key,value in identities.items()},
            "cold_construction_exact_residues":[str(z) for z in cold_residues],
            "parameter_examples":examples,"positive_release_45_point_exact_grid":grid,
            "lean":{"argv":argv,"LEAN_PATH":env["LEAN_PATH"],"returncode":run.returncode,"stdout":run.stdout,"stderr":run.stderr},
            "non_claims":["No emission rate, angle distribution, classical field action, stability, or cosmological observable derived.","All cs and speed values are illustrative parameter examples.","Fixed NR inertial mass is a stipulated Hamiltonian approximation; changing relativistic rest mass needs a full action."]}
    args.result.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    sys.exit(run.returncode)


if __name__=="__main__":
    main()

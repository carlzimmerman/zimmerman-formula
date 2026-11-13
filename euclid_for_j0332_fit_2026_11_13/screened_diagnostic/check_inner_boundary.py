"""Extend the screened radial grid inward100x, preserving every outer node."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import spherical_screen as model


def main():
    source=HERE/"spherical_screen.py"
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    theta=np.array([.5,1.,1.5,2.,3.])
    R=theta*model.geometry()[0]*1000*model.PC
    rows=[]
    for length in [21.7,1000.]:
        base=model.Problem(length,350,30).solve()
        extended=model.Problem(length,350,30)
        old_r=extended.r
        extra=np.geomspace(old_r[1]/100,old_r[1],701)[:-1]
        r=np.r_[0.,extra,old_r[1:]]
        extended.r=r
        extended.s=r/extended.L
        s=extended.s
        extended.h=np.diff(s)
        extended.sm2=(s[:-1]**2+s[:-1]*s[1:]+s[1:]**2)/3
        extended.H=(s[2:]-s[:-2])/2
        extended.gn=np.r_[0.,model.G*model.MASS*model.mfrac(r[1:])/r[1:]**2/model.A0]
        extended.ys=np.r_[0.,model.law_y(extended.gn[1:])]
        extended.solve()
        aa,ref=base.deflection(R)
        bb,_=extended.deflection(R)
        rows.append({"Lstar_pc":length,"inner_radius_original_pc":old_r[1]/model.PC,
            "inner_radius_extended_pc":r[1]/model.PC,"old_nodes":len(old_r),"extended_nodes":len(r),
            "max_total_deflection_relative_change":float(np.max(np.abs(bb/aa-1))),
            "max_screened_correction_absolute_change":float(np.max(np.abs((bb-aa)/ref))),
            "base_scaled_residual":base.error,"extended_scaled_residual":extended.error})
    assert digest==hashlib.sha256(source.read_bytes()).hexdigest()
    result={"assertion_tested":"At two fixed Lstar values, inward100x grid extension preserving all previous outer nodes leaves the five named deflections stable to observed values",
        "source_sha256":digest,"source_unchanged":True,"runs":rows,
        "non_claims":"Not uniform inner-boundary or full-action error bound"}
    (HERE/"inner_boundary_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()

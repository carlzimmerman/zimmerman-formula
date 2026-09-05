#!/usr/bin/env python3
"""Derive a conditional near-circular nodal-precession prediction from audited Q2.

Known quadrupole mechanics, not a new fundamental law or independent Cassini test.
The exact exponential AQUAL solver supplies the predicted coefficient.
"""
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
import sympy as s

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def derive():
    x,y,z,Q,a,n,I,f = s.symbols("x y z Q a n I f", real=True)
    potential = -Q*(z*z-(x*x+y*y+z*z)/3)/2
    force = s.Matrix([-s.diff(potential,v) for v in (x,y,z)])
    tidal = force.jacobian([x,y,z])
    # Circular unperturbed Kepler orbit. Normal l=(sin I,0,cos I).
    orbit = a*s.Matrix([s.cos(I)*s.cos(f), s.sin(f), -s.sin(I)*s.cos(f)])
    torque = orbit.cross(force.subs(dict(zip((x,y,z),orbit)), simultaneous=True))
    mean_torque = torque.applyfunc(lambda v:s.simplify(s.integrate(s.expand_trig(v),(f,0,2*s.pi))/(2*s.pi)))
    normal_rate = mean_torque/(n*a*a)
    # e_z cross l = (0,sin I,0); node longitude is undefined at sin I=0.
    node_rate = s.simplify(normal_rate[1]/s.sin(I))
    return dict(Q=Q,n=n,I=I,potential=potential,force=force,tidal=tidal,
                mean_torque=mean_torque,normal_rate=normal_rate,node_rate=node_rate)


def node_coefficient_mas_century(q2, period_years):
    year = 365.25*86400
    period = period_years*year
    expression = derive()
    rate = float(expression["node_rate"].subs({expression["Q"]:q2,
                  expression["n"]:2*math.pi/period, expression["I"]:s.pi/3}))*2
    return rate*(100*year)*(180/math.pi)*3600*1000


def main():
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    paths = [HERE/"results.json", Path(__file__), HERE/"test_orbital_prediction.py"]
    records = json.loads(paths[0].read_text())["results"]
    q2 = next(r["Q2_si"] for r in records if r["case"]["name"]=="fine")
    expressions = derive()
    result = {"Q2_from_fine_AQUAL_solve": q2,
              "derived_node_rate": str(expressions["node_rate"]),
              "derived_tidal_tensor": str(expressions["tidal"]),
              "coefficient_mas_per_century_per_orbital_year": node_coefficient_mas_century(q2,1),
              "saturn_like_29_4_year_orbit_coefficient_mas_century": node_coefficient_mas_century(q2,29.4),
              "Park_upper_endpoint_saturn_like_coefficient": node_coefficient_mas_century(5.2e-27,29.4),
              "scope": "Multiply coefficient by cos I; leading secular circular-orbit approximation; no eccentric planetary ephemeris fit",
              "novelty": "Known quadrupole response; newly computed project coefficient; not an independent empirical confirmation"}
    path = HERE/"orbital_prediction.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    digest = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    git = lambda *a:subprocess.check_output(["git",*a],cwd=HERE,text=True).strip()
    manifest = {"schema_version":1,"claim_id":"AQUAL-circular-orbit-node-response",
                "repository":{"commit":git("rev-parse","HEAD"),"dirty":bool(git("status","--porcelain"))},
                "command":"PYTHONDONTWRITEBYTECODE=1 "+sys.executable+" "+str(Path(__file__).resolve()),
                "environment":{"software":[sys.version,"sympy "+s.__version__],"hardware":platform.platform()},
                "mathematics":{"assertion_tested":"Circular orbit averaged torque from the signed quadrupole potential",
                               "coefficient_domain":"exact symbolic derivation, binary64 SI evaluation",
                               "conventions":"Phi=-Q2(z^2-r^2/3)/2; acceleration=-grad Phi; inclination to external-field axis",
                               "inputs":[{"path":str(p),"sha256":digest(p)} for p in paths],
                               "bounds":{"orbit":"circular; first order in Q2/n^2","example_period_years":29.4},
                               "non_claims":["Not a new fundamental law","Not an independent Cassini dataset","Not an eccentric orbit calculation"]},
                "randomness":{"used":False,"generator":"","seed":None},
                "run":{"started_at":started,"runtime_seconds":time.monotonic()-start,"exit_status":0},
                "outputs":[{"path":str(path),"sha256":digest(path)}],
                "checks":[{"name":"tidal_tensor_trace_zero","passed":s.trace(expressions["tidal"])==0}],
                "result":result,"residual_risks":["Inherits the unresolved strict-tolerance PDE check","Nearly circular first-order approximation"]}
    (HERE/"orbital_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()

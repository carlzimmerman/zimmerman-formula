#!/usr/bin/env python3
"""Bounded exact identity and normalization checks for NS-SELF-GRAVITY-001."""
import hashlib
import json
from pathlib import Path
import sys

import sympy as s

checks = []


def equal(name, left, right=0):
    delta = s.simplify(left - right)
    if delta != 0:
        raise AssertionError((name, delta))
    checks.append({"name": name, "passed": True, "domain": "exact SymPy"})


def truth(name, assertion, domain="exact SymPy"):
    if not bool(assertion):
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "domain": domain})


lane = Path(__file__).resolve().parent
project = lane.parents[2]
manifest = json.loads((lane / "inputs/source_manifest.json").read_text())
for record in manifest["sources"]:
    truth("dependency snapshot " + Path(record["snapshot"]).name,
          hashlib.sha256((project / record["snapshot"]).read_bytes()).hexdigest()
          == record["sha256"], "SHA256 bytes")
round_inputs = lane.parent / "inputs"
round_manifest = json.loads((round_inputs / "source_manifest.json").read_text())
used = {"RTM_REPORT.md", "MC_MODES_PROOF.md", "MC_BOUNDARY_PROOF.md", "CE053_FINITE_EDGE.txt"}
for record in round_manifest["sources"]:
    if Path(record["snapshot"]).name in used:
        truth("round source snapshot " + Path(record["snapshot"]).name,
              hashlib.sha256((project / record["snapshot"]).read_bytes()).hexdigest()
              == record["sha256"], "SHA256 bytes")

t, u, v, n, mu, C = s.symbols("t u v n mu C", positive=True)
inner = (1 - t**(3-n))/(n-3)
kernel = 1/t - t**(2-n)/(n-2)
equal("inner mass primitive", s.diff(inner, t), t**(2-n))
equal("inner mass primitive at wall", inner.subs(t, 1))
equal("kernel derivative", s.diff(kernel, t), -(n-3)*inner/t**2)
equal("kernel weighted form", t*kernel, 1-t**(3-n)/(n-2))

first = 1/t + mu*kernel
equal("first Picard exact expression", first, (1+mu)/t-mu*t**(2-n)/(n-2))
equal("first Picard inner source flux", (-t**2*s.diff(first, t)).subs(t, 1), 1)
equal("first Picard reference Poisson source", -s.diff(t**2*s.diff(first, t), t),
      mu*(n-3)*t**(2-n))
equal("weighted first-correction derivative", s.diff(t*(first-1/t), t),
      mu*(n-3)/(n-2)*t**(2-n))

envelope = (C-1)/C**n
equal("certificate maximum derivative", s.diff(envelope, C),
      C**(-n-1)*(n-(n-1)*C))

for index in (s.Rational(7, 2), s.Integer(4), s.Integer(5), s.Integer(6)):
    direct_inner = s.integrate(u**(2-index), (u, 1, v))
    direct_kernel = (index-3)*s.integrate(direct_inner/v**2, (v, t, s.oo))
    equal(f"nested kernel n={index}", direct_kernel, kernel.subs(n, index))
    equal(f"mass integral n={index}", s.integrate(t**(2-index), (t, 1, s.oo)),
          1/(index-3))
    equal(f"first correction weighted norm endpoint n={index}",
          s.limit(t*(first-1/t).subs(n, index), t, s.oo), mu)

certificate_controls = []
for index in (s.Integer(4), s.Integer(5), s.Integer(6)):
    cs = index/(index-1)
    mustar = (index-1)**(index-1)/index**index
    for fraction in (s.Rational(1, 4), s.Rational(1, 2)):
        muv = fraction*mustar
        qv = index*muv*cs**(index-1)
        equal(f"explicit q n={index} fraction={fraction}", qv, fraction)
        truth(f"selfmap certificate n={index} fraction={fraction}", 1+muv*cs**index <= cs)
        truth(f"strict contraction n={index} fraction={fraction}", qv < 1)
        certificate_controls.append({"n": str(index), "mu": str(muv), "C": str(cs), "q": str(qv)})
    equal(f"critical selfmap equality n={index}", 1+mustar*cs**index, cs)
    equal(f"critical q=1 n={index}", index*mustar*cs**(index-1), 1)

G, M0, R0, rhoR, zp = s.symbols("G M0 R0 rhoR Zpower", positive=True)
rhoR_relation = mu*(n-3)*M0/(4*s.pi*R0**3)
equal("dimensional Poisson source", G*M0/R0**3*mu*(n-3)*zp,
      4*s.pi*G*rhoR_relation*zp)
equal("dimensionless mass normalization", 4*s.pi*rhoR_relation*R0**3/(n-3), mu*M0)

rho, K = s.symbols("rho K", positive=True)
P = K*rho**(1+1/n)
z = (n+1)*K*rho**(1/n)
equal("Euler chemical identity dP=rho dz", s.diff(P, rho), rho*s.diff(z, rho))

x, d0, c = s.symbols("x D0 c", positive=True)
hc_t = d0**2*x**3*t**(-6)/(1-x/t**2)**2
hc_1 = d0**2*x**3/(1-x)**2
lower_ratio = rhoR*c**2*t**(-n)/hc_t
equal("causal envelope ratio factor", lower_ratio/(rhoR*c**2/hc_1*t**(6-n)),
      (1-x/t**2)**2/(1-x)**2)
eta = s.symbols("eta", positive=True)
upper_ratio = rhoR*c**2*C**n*t**(-n)*(1+(n-1)/n*eta*C/t)/hc_t
equal("n=7 upper gate ratio tends to zero", s.limit(upper_ratio.subs(n, 7), t, s.oo), 0)

result = {
    "claim_id": "NS-SELF-GRAVITY-001",
    "status": "all declared exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "certificate_controls": certificate_controls,
    "non_claims": [
        "Finite controls do not replace the analytic uniform convergence proof.",
        "The contraction threshold is not an Euler-Poisson nonexistence threshold.",
        "No core/interface match, microscopic carrier, Einstein solution or coupled gauge/gravity stability is certified."
    ]
}
output = Path(sys.argv[1])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2)+"\n")
print(f"{len(checks)} exact checks passed; results written to {output}")

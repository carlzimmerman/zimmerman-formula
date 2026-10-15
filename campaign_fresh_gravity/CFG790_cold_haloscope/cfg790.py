"""CFG790 -- hypothetical cold-energy haloscope: power and photon rates for axion-like (B-field) and dark-photon-like portals.
Criteria FROZEN_CRITERIA.md.  Natural units internally.  Run: python3 cfg790.py  (CFG790_MUTATE=1: B -> 0).  Bounds PROVISIONAL.
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("CFG790_MUTATE") == "1"
OUT = []
def P(s): print(s); OUT.append(s)
HBAR = 6.582e-25                     # GeV s
GEV4_TO_WM2 = 1.602e-10 * (1 / HBAR) * (1 / 1.9733e-16) ** 2     # J * s^-1 * m^-2
TESLA = 1.9535e-16                   # GeV^2
CM = 1 / 1.9733e-14                  # 1 cm in GeV^-1
MSUN, PC = 1.989e30, 3.0857e16
rho_si = 0.01 * MSUN / PC ** 3 * (2.998e8) ** 2 / 1.602e-10     # GeV per m^3
rho = rho_si * 1e-6 / (CM ** 3)       # GeV/cm^3 -> GeV^4
P(f"CFG790  cold-energy haloscope{'  [MUTATE B=0]' if MUT else ''}")
P(f"  K1: 1 GeV^4 = {GEV4_TO_WM2:.3e} W/m^2 (6.26e45); 1 T = {TESLA:.3e} GeV^2; local rho = {rho_si * 1e-6:.3f} GeV/cm^3")
tau_s = 4.43e15 * 3.156e7
Gam = 1 / tau_s
P(f"  K2: Gamma_max = {Gam:.2e} s^-1 (CFG789 7.2e-24)")
B = 0.0 if MUT else 10 * TESLA; A = 10.0
res = {}
for m_eV in (1, 2, 3, 10, 100):
    m = m_eV * 1e-9
    gmax = math.sqrt(64 * math.pi * Gam * HBAR / m ** 3)
    lam_nm = 1239.84 / m_eV
    row = {}
    for lab, g in (("A sky-bound g", gmax), ("A lit. g 1e-12", 1e-12)):
        PA = g ** 2 * B ** 2 * rho / m ** 2 * GEV4_TO_WM2
        Pw = PA * A; N = Pw / (m_eV * 1.602e-19)
        row[lab] = dict(g=g, P_W=Pw, photons_per_day=N * 86400)
    for eps in (1e-12, 1e-14):
        PA = eps ** 2 * rho * GEV4_TO_WM2
        Pw = PA * A; N = Pw / (m_eV * 1.602e-19)
        row[f"B eps {eps:g}"] = dict(P_W=Pw, photons_per_day=N * 86400)
    res[str(m_eV)] = dict(lambda_nm=lam_nm, **row)
    P(f"  m {m_eV:>3} eV (lambda {lam_nm:7.1f} nm): " + "; ".join(f"{k}: P {v['P_W']:.1e} W, {v['photons_per_day']:.1e}/day" for k, v in row.items()))
best = max(v["P_W"] for r in res.values() for k, v in r.items() if isinstance(v, dict))
harvest = "HARVEST CLOSED" if best < 1e-6 else "HARVEST OPEN"
det = sorted({k for r in res.values() for k, v in r.items() if isinstance(v, dict) and v["photons_per_day"] >= 1})
P(f"\n  best power anywhere {best:.1e} W -> {harvest}; factor short of 300 MW: {3e8 / best:.1e}; of 1 W: {1 / best:.1e}")
P(f"  DETECTABLE (>= 1 photon/day, 10 m^2): {det if det else 'none'}")
json.dump(dict(res=res, harvest=harvest, detectable=det, mutate=MUT), open(os.path.join(HERE, f"cfg790_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg790{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)

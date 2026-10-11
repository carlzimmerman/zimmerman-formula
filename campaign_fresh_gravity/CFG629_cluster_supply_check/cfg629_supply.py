"""CFG629: does the merger lanes' case-L omission (unsettled cold energy = 0) explain the cluster-core shortfall?
Projected M(<250 kpc) at t=0 of CFG599 progenitors, settled-only vs settled + unsettled reservoir
(supply = 5.364 M_b, unsettled = supply - settled phantom, NFW c=4 shape as declared in CFG597 M-3 / CFG432; that shape
is an inherited placeholder). Compared with Paraficz+16 strong-lensing M(<250) 2.5e14 / 2.0e14 (PROVISIONAL, recalled).
kappa = 1/2 FITTED; footings never pooled."""
import sys, os, json
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "CFG599_merger_stopwatch_v2")); sys.path.insert(0, os.path.join(H, "..", "CFG597_merger_settling_stopwatch"))
import numpy as np, cfg599_lib as L

def proj(r, rho, R):
    f = 4 * np.pi * r**2 * rho; M = np.r_[0, np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]
    k = r > R; rr = r[k]; w = 1 - np.sqrt(1 - (R / rr)**2)
    return float(np.interp(R, r, M) + np.trapz(f[k] * w, rr))

out = {}
for foot in ["can", "alt"]:
    for name, M, cl, obs in [("main", 1.5e15, False, 2.5e14), ("sub", 1.5e14, True, 2.0e14), ("sub4to1", 3.75e14, True, 2.0e14)]:
        p = L.Progenitor599(M, foot, cloud=cl); r = p.r
        rb = p.rho_g + p.rho_s + p.rho_cc
        supply = 5.364 * p.Mb; Mu = max(supply - p.Mph_tot, 0.0)
        rs = p.r200 / 4; nfw = np.where(r < p.r200, 1 / (np.maximum(r, 1e-3) / rs * (1 + r / rs)**2), 0.0)
        Mn = np.r_[0, np.cumsum(0.5 * (4*np.pi*r[1:]**2*nfw[1:] + 4*np.pi*r[:-1]**2*nfw[:-1]) * np.diff(r))]
        rho_u = Mu * nfw / Mn[-1]
        b, c, u = proj(r, rb, 250), proj(r, p.rho_ph, 250), proj(r, rho_u, 250)
        row = dict(Mb=p.Mb, supply=supply, settled=p.Mph_tot, unsettled=Mu, total_mass_all=p.Mb + supply,
                   proj250_settled_only_over_lensing=(b + c) / obs, proj250_with_unsettled_over_lensing=(b + c + u) / obs,
                   whole_system_mass_over_lensing250=(p.Mb + supply) / obs)
        out[f"{foot}_{name}"] = row
        print(f"{foot} {name:8s} supply {supply:.2e} settled {p.Mph_tot:.2e} unsettled {Mu:.2e} | proj<250 / lensing: "
              f"settled-only {row['proj250_settled_only_over_lensing']:.2f}, +unsettled {row['proj250_with_unsettled_over_lensing']:.2f}; "
              f"whole system / lensing(<250) {row['whole_system_mass_over_lensing250']:.2f}")
json.dump(out, open(os.path.join(H, "cfg629_supply_results.json"), "w"), indent=1)

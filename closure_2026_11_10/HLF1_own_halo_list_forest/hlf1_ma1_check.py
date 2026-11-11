#!/usr/bin/env python3
"""HLF1 AMENDMENT A1 (657e245086): MUTATE MA1 restated. The z = 0 grid with its cells permuted (seed 1, as hlf1_halos.py's MUTATE run)
must give at most 10 % of the own count above 5e13 Msun/h. The finder is hlf1_halos.py's, executed from its own source (prefix up to
the planted-halo known answer). Reported: permuted counts above 1e13, 2e13, 5e13, 1e14.
  nice -n 19 python3 hlf1_ma1_check.py -> hlf1_ma1_check.json / .out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "hlf1_halos.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ KA-A1")
ns = {"__file__": SRC, "__name__": "hlf1_halos_lib"}; exec(compile(code[:cut], SRC, "exec"), ns)
np = ns["np"]; MC = ns["MCELL"]
d0 = np.load(os.path.join(ns["P0"], f"{ns['TAG']}_z0_mesh256.npz"))["dpart"].astype(np.float64); rho1 = 1.0 + d0
_, _, m0 = ns["find_halos"](rho1); M0 = m0 * MC
perm = np.random.default_rng(1).permutation(rho1.ravel()).reshape(rho1.shape)
_, _, mp = ns["find_halos"](perm); Mp = mp * MC
rows = {f"{t:.0e}": dict(own=int((M0 >= t).sum()), permuted=int((Mp >= t).sum())) for t in (1e13, 2e13, 5e13, 1e14)}
r = rows["5e+13"]; bites = bool(r["permuted"] <= 0.10 * r["own"])
res = dict(lane="HLF1", amendment="A1 657e245086", rows=rows, densest_cell_mass=float(rho1.max() * MC), largest_permuted=float(Mp.max()) if len(Mp) else 0.0,
           MA1_restated=dict(own=r["own"], permuted=r["permuted"], bites=bites), note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
json.dump(res, open(os.path.join(HERE, "hlf1_ma1_check.json"), "w"), indent=1)
txt = "\n".join([f"densest cell {res['densest_cell_mass']:.3e} Msun/h; largest permuted object {res['largest_permuted']:.3e}"]
                + [f"above {k}: own {v['own']}, permuted {v['permuted']}" for k, v in rows.items()]
                + [f"MA1 restated (above 5e13): {r['permuted']} against {r['own']} -> {'bites' if bites else 'DOES NOT BITE'}"])
print(txt); open(os.path.join(HERE, "hlf1_ma1_check.out"), "w").write(txt + "\n")

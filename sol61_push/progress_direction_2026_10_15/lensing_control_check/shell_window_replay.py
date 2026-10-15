"""Bounded diagnostic of CFG805 K2; does not recover individual FFT powers.

For shell j replace every unknown mode power by saved P_grav[j], but evaluate
the top-hat at each exact integer-lattice mode. Compare that finite sum with
CFG805's trapezoid over shell means and CFG650's stored actual-mode sigma8.
No simulation, fit, renormalization, low-k extrapolation, or original-file write.
"""
import argparse
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np


def window(x):
    return 3.0 * (np.sin(x) - x * np.cos(x)) / x**3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = here / "input_snapshots/cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json"
    obj = json.loads(source.read_text())
    snap = obj["snap"]["x0.2562"]
    k, power = np.asarray(snap["k"]), np.asarray(snap["P_grav"])
    keep = (k > 0) & np.isfinite(power) & (power > 0)
    k, power = k[keep], power[keep]
    assert keep.all(), "This replay requires every recorded shell to be present."
    assert np.all(np.diff(k) > 0)
    box = obj["L"]
    fundamental = 2 * math.pi / box
    integrand = k**2 * power * window(8*k)**2 / (2*math.pi**2)
    trap_variance = float(np.trapz(integrand, k))
    stored_variance = snap["sigma8_grav"]**2
    rows = []
    # Largest allocation is 129^3 lattice entries, not a 1024^3 field.
    for nmax in (16, 32, 64):
        axis = np.arange(-nmax, nmax+1)
        radius2 = (axis[:, None, None]**2 + axis[None, :, None]**2
                   + axis[None, None, :]**2)
        kval = fundamental * np.sqrt(radius2).ravel()
        upper = (nmax-0.5)*fundamental
        kval = kval[(kval > 0) & (kval <= upper)]
        # measure_pk edges are (0.5,1.5,2.5,...) * fundamental.
        shell = np.floor(kval/fundamental+0.5).astype(int)-1
        assert shell.min() == 0 and shell.max() < len(power)
        variance = float(np.sum(power[shell]*window(8*kval)**2)/box**3)
        prefix = k <= upper
        row = dict(nmax=nmax, allocated_lattice_entries=int((2*nmax+1)**3),
                   retained_modes=int(len(kval)), k_upper_h_per_Mpc=upper,
                   shell_constant_variance=variance,
                   shell_constant_sigma8=math.sqrt(variance),
                   relative_sigma8_difference_from_stored=math.sqrt(variance)/snap["sigma8_grav"]-1,
                   trapezoid_variance_through_same_k_upper=float(np.trapz(integrand[prefix],k[prefix])))
        if nmax == 16:
            row["first_shells"] = []
            for j in range(4):
                mask = shell == j
                row["first_shells"].append(dict(shell=j+1,modes=int(mask.sum()),
                    mean_k=float(kval[mask].mean()),saved_mean_k=float(k[j]),
                    variance=float(np.sum(power[shell[mask]]*window(8*kval[mask])**2)/box**3)))
        rows.append(row)
    result = dict(
        assertion="Compare two non-equivalent sigma8 estimators on the same finite-box shell spectrum.",
        interpretation="Shell-count/window weighting accounts for most of K2 discrepancy; exact attribution requires individual mode powers or stored shell-weighted sums.",
        non_claims=["Not an exact reconstruction of CFG650 actual-mode sigma8.",
                    "Does not validate the lensing transform, nuisance optimization, or old fit scores.",
                    "Does not fill absent modes below the box fundamental or correct frozen K2."],
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_tag=obj["tag"], snapshot="x0.2562", z=snap["z"], box_Mpc_over_h=box,
        fundamental_k_h_per_Mpc=fundamental, first_saved_shell_mean_k=float(k[0]),
        stored_actual_mode_sigma8=snap["sigma8_grav"],
        trapezoid_sigma8=math.sqrt(trap_variance),
        stored_minus_trapezoid_variance=stored_variance-trap_variance,
        shell_constant_replays=rows,
        software=dict(python=sys.version.split()[0],numpy=np.__version__,platform=platform.platform()))
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(trapezoid_sigma8=result["trapezoid_sigma8"],stored_sigma8=snap["sigma8_grav"],
                          shell_constant_sigma8=[row["shell_constant_sigma8"] for row in rows],
                          largest_allocated_entries=rows[-1]["allocated_lattice_entries"])))


if __name__ == "__main__":
    main()

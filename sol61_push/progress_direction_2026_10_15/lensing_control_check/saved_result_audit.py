"""Audit saved mutation/radii and CFG801 residual covariance; no new fit."""
import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np


def definitions(path, marker):
    source = path.read_text()
    assert source.count(marker) == 1
    scope = {"__file__": str(path), "__name__": "audit_definitions"}
    exec(compile(source.split(marker)[0],str(path),"exec"),scope)
    return scope


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    dest = Path(__file__).resolve().parent / "input_snapshots"
    # Pin canonical definitions irrespective of caller's optional lane flags.
    sys.argv = ["audit_definitions"]
    os.environ.pop("CFG801_MUTATE",None)
    os.environ.pop("CFG804_MUTATE",None)
    g = definitions(dest/"cfg801.py",'P(f"CFG801')
    radii, obs = [], []
    for b in range(1,5):
        data = np.loadtxt(dest/f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")
        radii.append(data[:,0]); obs.append(data[:,1]/data[:,4])
    radii, obs = np.array(radii), np.array(obs)
    raw = np.loadtxt(dest/"Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")
    masses = sorted(set(raw[:,0])); covariance = np.zeros((60,60))
    for row in raw:
        b,c = masses.index(row[0]),masses.index(row[1])
        i,j = np.argmin(abs(radii[0]-row[2])),np.argmin(abs(radii[0]-row[3]))
        covariance[15*b+i,15*c+j] = row[4]/row[6]
    model = []
    fixed_masses = [10.36,10.83,11.01,11.18]
    for b,lm in enumerate(fixed_masses):
        mass = 10**lm
        rm = math.sqrt(g["Gpc"]*mass/g["a0"])
        x = radii[b]*1e6/rm
        model.append(mass/rm**2*np.exp(np.interp(np.log(x),np.log(g["X"]),np.log(g["fN"]))))
    residual = obs.reshape(-1)-np.concatenate(model)
    weighted = np.linalg.solve(covariance,residual)
    joint = float(residual@weighted)
    blocks, conditional, additive = [], [], []
    mask = np.ones((60,60),bool)
    for b in range(4):
        sel = np.arange(15*b,15*(b+1))
        rest = np.setdiff1d(np.arange(60),sel)
        blocks.append(float(residual[sel]@np.linalg.solve(covariance[np.ix_(sel,sel)],residual[sel])))
        conditional.append(joint-float(residual[rest]@np.linalg.solve(covariance[np.ix_(rest,rest)],residual[rest])))
        additive.append(float(residual[sel]@weighted[sel]))
        mask[np.ix_(sel,sel)] = False
    corr = covariance / np.sqrt(np.diag(covariance)[:,None]*np.diag(covariance)[None,:])
    baseline = json.loads((dest/"cfg805_results.json").read_text())
    mutation = json.loads((dest/"cfg805_results_MUTATE.json").read_text())
    old = json.loads((dest/"cfg804_results.json").read_text())
    g4 = definitions(dest/"cfg804.py",'P(f"CFG804')
    edge_rows = []
    for name,lms in [("CFG804_D",old["all"]["logMb"]),("CFG805_D",baseline["all"]["logMb_D"])]:
        rows = []
        for lm in lms:
            supply,_ = g4["N_of"](lm)
            ngrid = np.r_[1.0,np.arange(2.0,10.01,.25)]
            rounded = float(ngrid[np.argmin(abs(ngrid-supply))])
            rm = math.sqrt(g4["Gpc"]*10**lm/g4["a0"])/1e6
            rows.append(dict(logMb=lm,N=supply,N_grid=rounded,
                exact_edge_Mpc=g4["edge_of"](supply)*rm,
                implemented_profile_edge_Mpc=g4["edge_of"](rounded)*rm))
        edge_rows.append(dict(model=name,bins=rows))
    result = dict(
        contract="Saved-result arithmetic and exact-source baseline residual diagnostic; no profiling or two-halo fit rerun.",
        mutation_relative_to_canonical_b_D_percent=[100*(m/b-1) for b,m in zip(baseline["all"]["b_D"],mutation["all"]["b_D"])],
        original_all_radii_dchi2=baseline["all"]["dchi2"],
        old_comparison_gap=148.7,
        original_gap_reduction_percent=100*(1-baseline["all"]["dchi2"]/148.7),
        CFG801_baseline=dict(logMb=fixed_masses,joint_chi2=joint,marginal_block_chi2=blocks,
            marginal_block_sum=sum(blocks),signed_additive_partition=additive,
            conditional_bin_increments=conditional,
            heavy_bins_given_light_chi2=joint-blocks[0],
            diagonal_pulls_by_bin=(residual/np.sqrt(np.diag(covariance))).reshape(4,15).tolist(),
            max_cross_bin_absolute_correlation=float(np.max(abs(corr[mask]))),
            covariance_symmetry_max_abs=float(np.max(abs(covariance-covariance.T))),
            covariance_minimum_eigenvalue=float(np.linalg.eigvalsh(covariance)[0])),
        fixed_CFG805_REX_Mpc=[.343,.442,.433,.429],edge_consistency=edge_rows,
        non_claims=["Not a residual diagnostic for CFG805 fitted B+2h or D+2h.",
                    "Conditional increments do not form an additive partition.",
                    "Mass-bin residual concentration does not identify morphology or a gas mechanism.",
                    "No original score, criterion, or scientific code has been modified."])
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(mutation_percent=result["mutation_relative_to_canonical_b_D_percent"],
                         CFG801_joint_chi2=joint,conditional_increments=conditional)))


if __name__ == "__main__":
    main()

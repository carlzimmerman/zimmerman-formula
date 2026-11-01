"""Prepared small-perturbation tests; no state changes during evolution."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import numpy as np

import refinement
import convective_transport as convective


def entropy_perturbation(model, state, amplitude=.01, mass_fraction=.2):
    """Perturb K with exactly zero internal-energy work at fixed geometry.

    This deliberately prepares a nearby initial condition; it is not an
    entropy redistribution step of the physical law. Its entropy change is
    recorded explicitly and is not counted as simulated production.
    """
    if not np.isfinite(amplitude) or amplitude <= 0 or not 0 < mass_fraction <= 1:
        raise ValueError('invalid perturbation amplitude or mass fraction')
    before = np.asarray(state, dtype=float)
    fields = model.fields(before)
    coordinate = (np.arange(model.n)+.5)/(model.n*mass_fraction)
    taper = np.maximum(1-coordinate, 0)
    weights = model.dm*fields['W']*taper
    if weights.sum() <= 0:
        raise ValueError('perturbation has no resolved support')
    shape = 1-2*coordinate
    offset = np.dot(weights, shape)/weights.sum()
    delta = amplitude*model.params.k_star*taper*(shape-offset)
    prepared = before.copy()
    prepared[2*model.n:] += delta
    model.fields(prepared)
    energy_before, energy_after = model.energy(before), model.energy(prepared)
    sigma_before = model.dm*np.cbrt(before[2*model.n:]/model.params.k_star).sum()
    sigma_after = model.dm*np.cbrt(prepared[2*model.n:]/model.params.k_star).sum()
    return prepared, dict(
        kind='prepared_energy_neutral_entropy_mode', amplitude=amplitude,
        support_mass_fraction=mass_fraction, delta_K=delta.tolist(),
        energy_before=energy_before, energy_after=energy_after,
        delta_energy={key:energy_after[key]-energy_before[key] for key in energy_before},
        entropy_before=float(sigma_before), entropy_after=float(sigma_after),
        entropy_preparation_change=float(sigma_after-sigma_before),
        applied_once_before_integration=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--t-end',type=float,default=64)
    parser.add_argument('--amplitude',type=float,default=.01)
    parser.add_argument('--wall-seconds',type=float,default=45)
    args=parser.parse_args()
    raw=args.input.read_bytes(); previous=json.loads(raw)
    material_params=convective.baseline.material.MaterialParameters(**previous['material_parameters'])
    transport_params=convective.ConvectiveParameters(**previous['transport_parameters'])
    model=refinement.FloorAuditedCollapse(previous['n_shells'],material_params,transport=transport_params,
        initial_density=previous['initial_density'],radius=previous['initial_radius'],
        initial_velocity_gradient=previous['initial_velocity_gradient'])
    prepared,audit=entropy_perturbation(model,previous['final_state'],amplitude=args.amplitude)
    audit.update(source=str(args.input.resolve()),source_sha256=hashlib.sha256(raw).hexdigest())
    result=refinement.simulate(model,initial_state=prepared,initial_time=previous['t_reached'],
        t_end=args.t_end,samples=257,wall_seconds=args.wall_seconds,
        rtol=2e-7,atol=1e-9,max_step=.05,max_rhs_calls=300000)
    result['stability_preparation']=audit
    convective.baseline.atomic_json(args.output,result)
    print(json.dumps({key:result[key] for key in ['status','t_reached','max_relative_energy_error']}))
    return 0 if result['status']=='completed' else 2


if __name__=='__main__':
    raise SystemExit(main())

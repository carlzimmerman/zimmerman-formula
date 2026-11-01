"""Distinct outward, instability-gated heat closure for the shell experiment.

This is a phenomenological heat transport hypothesis, not material convection
or parcel exchange. The pinned Fourier operator and its runs are unchanged.
For neighboring cells i,j with center separation delta_r, define

    chi = K/Kstar,
    xi = ell_g max((chi_i-chi_j)/delta_r,0)/(chi_g+(chi_i+chi_j)/2),
    a = xi/(1+xi),
    L = P0 D A/delta_r h_i h_j a max(psi_i-psi_j,0).

Thus only an outward-decreasing entropy coordinate and a hotter inner cell can
produce outward heat exchange. ell_g is a fixed physical length; it does not
scale with the mesh. At fixed geometry each physical face flux is monotone in
the supplying K and antitone in the receiving K. The same shared luminosity
enters neighboring cell energies with opposite signs. The old shock heater
and memory bulk damping, including mechanical work, are inherited unchanged.

Negative intermediate solver K uses chi=max(K,0)/Kstar in the new instability
gate. psi retains the pinned parent's smooth linear continuation in K. This
is a piecewise locally Lipschitz stage extension with a strictly positive gate
denominator, not an accepted-state projection. Parent sparse Radau rejects any
negative accepted K and restarts from the last accepted state with a quarter
step, under its declared caps. A completed run alone makes no settling claim.
"""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path

import numpy as np

import transport as baseline


CLOSURE = "outward_instability_gated_heat"


@dataclass(frozen=True)
class ConvectiveParameters(baseline.TransportParameters):
    stratification_length: float = 0.1
    stratification_scale: float = 0.01

    def __post_init__(self):
        super().__post_init__()
        for name in ("stratification_length", "stratification_scale"):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.ndim != 0 or not np.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be a finite positive scalar")
            object.__setattr__(self, name, float(value))


class ConvectiveCollapse(baseline.TransportCollapse):
    def __init__(self, n_shells, params, transport=None, **sphere_parameters):
        selected = ConvectiveParameters() if transport is None else transport
        if not isinstance(selected, ConvectiveParameters):
            raise ValueError("transport must be ConvectiveParameters")
        super().__init__(n_shells, params, transport=selected, **sphere_parameters)

    def fields(self, y, *, stage_extension=False):
        f = super().fields(y, stage_extension=stage_extension)
        chi = np.maximum(f["K"], 0) / self.params.k_star
        separation = np.diff(f["center_radius"])
        xi = (self.transport.stratification_length
              * np.maximum((chi[:-1] - chi[1:]) / separation, 0)
              / (self.transport.stratification_scale + 0.5 * (chi[:-1] + chi[1:])))
        gate = xi / (1 + xi)
        luminosity = np.zeros(self.n + 1)
        luminosity[1:-1] = (self.params.p0 * self.transport.diffusivity
                            * 4 * np.pi * f["r"][:-1]**2 / separation
                            * f["activation"][:-1] * f["activation"][1:]
                            * gate * np.maximum(f["psi"][:-1] - f["psi"][1:], 0))
        dk_conduction = -np.diff(luminosity) / (self.dm * f["W"])
        f.update(convective_xi=xi, convective_gate=gate, luminosity=luminosity,
                 dk_conduction=dk_conduction,
                 dk=f["dk_original"] + f["dk_damping"] + dk_conduction)
        return f

    def diagnostics(self, t, y):
        result = super().diagnostics(t, y)
        r01, rho01 = self.enclosed_estimator(y, 0.01)
        f = self.fields(y)
        result.update(enclosed_1pct_radius=r01, enclosed_1pct_mean_density=rho01,
                      max_convective_gate=float(f["convective_gate"].max()),
                      active_convective_face_fraction=float(np.mean(f["luminosity"][1:-1] > 0)))
        return result

    def profile(self, y):
        result = super().profile(y)
        f = self.fields(y)
        result.update(convective_xi=f["convective_xi"].tolist(),
                      convective_gate=f["convective_gate"].tolist())
        return result


def simulate(model, **kwargs):
    result = baseline.simulate(model, **kwargs)
    result["closure"] = CLOSURE
    result["transport_units"].update(stratification_length="fixed physical length",
                                     stratification_scale="K/Kstar")
    result["non_claims"].append("Instability-gated heat transport is not resolved material convection")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shells", type=int, default=32)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--diffusivity", type=float, default=0.1)
    parser.add_argument("--damping-strength", type=float, default=1.0)
    parser.add_argument("--memory-activation", type=float, default=0.01)
    parser.add_argument("--stratification-length", type=float, default=0.1)
    parser.add_argument("--stratification-scale", type=float, default=0.01)
    parser.add_argument("--t-end", type=float, default=8.0)
    parser.add_argument("--samples", type=int, default=161)
    parser.add_argument("--wall-seconds", type=float, default=45.0)
    parser.add_argument("--max-rhs-calls", type=int, default=300000)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--atol", type=float, default=1e-9)
    parser.add_argument("--max-step", type=float, default=0.05)
    parser.add_argument("--restart", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    material_params = baseline.material.MaterialParameters(rho_q=1, G=1,
                                                           a0=np.sqrt(8 * np.pi), tau=args.tau)
    transport_params = ConvectiveParameters(
        diffusivity=args.diffusivity, damping_strength=args.damping_strength,
        memory_activation=args.memory_activation,
        stratification_length=args.stratification_length, stratification_scale=args.stratification_scale,
    )
    sphere_parameters = {}
    initial_state, initial_time = None, 0.0
    if args.restart is not None:
        previous = json.loads(args.restart.read_text())
        if (previous.get("closure") != CLOSURE or previous["n_shells"] != args.shells
                or previous["material_parameters"] != asdict(material_params)
                or previous["transport_parameters"] != asdict(transport_params)):
            parser.error("restart must have identical closure, shell count and all material/transport parameters")
        initial_state, initial_time = previous["final_state"], previous["t_reached"]
        sphere_parameters = dict(initial_density=previous["initial_density"],
                                 radius=previous["initial_radius"],
                                 initial_velocity_gradient=previous["initial_velocity_gradient"])
    model = ConvectiveCollapse(args.shells, material_params, transport=transport_params,
                               **sphere_parameters)
    result = simulate(model, t_end=args.t_end, samples=args.samples, rtol=args.rtol, atol=args.atol,
                      wall_seconds=args.wall_seconds, max_rhs_calls=args.max_rhs_calls,
                      max_step=args.max_step, initial_state=initial_state, initial_time=initial_time)
    baseline.atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("closure", "status", "n_shells", "t_reached",
                                                  "elapsed_seconds", "rhs_calls", "max_relative_energy_error")},
                     sort_keys=True))
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())

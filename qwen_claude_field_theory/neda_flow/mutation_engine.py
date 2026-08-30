#!/usr/bin/env python3
"""ALEATORIC MUTATION ENGINE -- the novelty source (the haliflow move). A seeded PRNG samples
UNIFORMLY over the expressible grammar, not over the LLM's literature prior: structural combinations
no model would propose because nothing in its training resembles them. Zero LLM calls -- the gates
only read structure, so skeletons run at machine speed. Seeded by iteration => fully reproducible.
Qwen keeps the interpretive branches; the PRNG owns the exploration frontier."""
import random, json

FIELD_TYPES  = ["scalar", "vector", "stf_tensor", "khronon", "multiplier", "metric"]
KINETICS     = ["none", "standard", "degenerate", "higher_derivative"]
CONNECTIONS  = ["riemannian", "riemannian", "teleparallel", "nonmetricity"]   # riemannian 2x weight
SCALAR_SECTORS = ["propagating", "instantaneous", "constrained", "none"]
MOND_REAL    = ["aux_legendre_chi", "constraint_first_q", "nonlocal_F+"]
SOURCE_POOL  = ["R", "R3", "spatial_einstein", "weyl_E", "chi", "P_i", "q", "multiplier",
                "inv_laplacian", "elliptic_kernel_f", "mu(y)", "a_mu", "u_mu", "K_ij", "theta",
                "C_tensor", "C_invariant_1", "torsion_T", "nonmetricity_Q", "rho"]
NONLOCAL     = ["none", "none", "spatial"]                                    # temporal excluded (P6)
SCREEN       = [None, None, "e^-y"]

def random_skeleton(seed):
    """One schema-complete candidate sampled uniformly over the grammar. Deterministic per seed."""
    rng = random.Random(seed)
    n_fields = rng.randint(1, 3)
    fields = [{"name": f"F{i}", "type": rng.choice(FIELD_TYPES), "kinetic": rng.choice(KINETICS),
               "timelike_background": rng.random() < 0.25} for i in range(n_fields)]
    fields.insert(0, {"name": "g", "type": "metric", "kinetic": "standard",
                      "timelike_background": False})
    n_coup = rng.randint(1, 3)
    coups = []
    for j in range(n_coup):
        pf = rng.random() < 0.3
        coups.append({"label": f"c{j}", "sources": rng.sample(SOURCE_POOL, rng.randint(1, 3)),
                      "order_in_phi": rng.choice([0, 1, 2, 2]),
                      "preferred_frame": pf,
                      "screened_by": ("e^-y" if pf else rng.choice(SCREEN)),
                      "lapse_weighted": False,                               # P3: never
                      "nonlocal": rng.choice(NONLOCAL)})
    conn = rng.choice(CONNECTIONS)
    cand = {
        "name": f"ALEATORIC-{seed}",
        "family": "aleatoric",
        "connection": conn,
        "scalar_sector": rng.choice(SCALAR_SECTORS),
        "fields": fields, "couplings": coups,
        "mond_realization": rng.choice(MOND_REAL),
        "kinetic_normalization_source": "independent",
        "claimed_mechanism": f"Aleatoric grammar sample (seed {seed}): structure IS the claim; "
                             f"connection={conn}. Judged purely by the deterministic gates.",
        "predicted_weak_field": "To be determined by the gates; no narrative prediction is asserted.",
        "inequivalence_argument": f"Uniform grammar sample, seed {seed}: mechanism fingerprint is "
                                  f"checked against every dead class and prior candidate by the "
                                  f"dedup layer; structural novelty is enforced there, not asserted here.",
    }
    if sum(1 for f in fields if f["type"] == "metric") >= 2:
        cand["bimetric_spec"] = {"interaction": rng.choice(["hassan_rosen", "composite", "bimond_connection"]),
                                 "matter_metric": "g",
                                 "mond_source": rng.choice(["nonlinear_helicity0", "composite_matter",
                                                            "connection_invariants"]),
                                 "m_FP": "~H0"}
    return cand


def crossover(mechanism_library, seed):
    """Random recombination of two VERIFIED mechanisms into a random family skeleton -- the other
    novelty axis: proven parts in never-tried combinations."""
    rng = random.Random(10**9 + seed)
    cand = random_skeleton(10**9 + seed)
    picks = rng.sample(mechanism_library, min(2, len(mechanism_library)))
    cand["name"] = f"CROSSOVER-{seed}"
    cand["claimed_mechanism"] = ("Crossover of verified mechanisms: " +
                                 " x ".join(p["id"] for p in picks) + ". " +
                                 " | ".join(p["mechanism"][:120] for p in picks))
    return cand

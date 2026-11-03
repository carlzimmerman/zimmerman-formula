#!/usr/bin/env python3
"""Writes mw_targets.json: Bovy & Rix K_z table and R0 as X5's chain loads them (X5's loader, read-only). kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
os.environ["OMP_NUM_THREADS"] = "1"; sys.dont_write_bytecode = True
RB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(RB, "X5_mw_joint_baryons"))
import x5_lib as L
ns = L.load_p4()
json.dump(dict(R0=float(ns["R0_MW"]), BR_R=[float(x) for x in ns["BR_R"]], BR_K=[float(x) for x in ns["BR_K"]], BR_E5=[float(x) for x in ns["BR_E5"]]), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mw_targets.json"), "w"), indent=0)

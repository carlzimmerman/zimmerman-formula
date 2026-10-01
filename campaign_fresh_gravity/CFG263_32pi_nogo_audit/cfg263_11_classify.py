"""CFG263 final step: apply the FROZEN classifier and door rule (cfg263_lib.classify / door, written before any run)
to the flags produced by scripts 01-08, plus the door-rule inputs below. Writes the table into results.json under 'CLASSIFICATION'.

Door-rule inputs are judgments backed by a record search (grep over sonnet55_push/puzzle_32pi, sol61_push,
campaign_fresh_gravity/closure_map; see README 'Door search'). Each carries its reason.
"""
import json
import os
from cfg263_lib import Checks, run_main, classify, door, HERE


ROUTES = {
    "NG-G": dict(route="a symmetry of the gravity-coupled action that acts on the a0-sector's vacuum constant (e.g. sequestering)",
                 specific_route=False, route_not_in_record=False, route_u_algebraic=True, route_no_inserted_target=False,
                 why="no named mechanism ties a0 to the constant; sequestering is in the record (closure_map/ACTIONS_AND_NOGOS.md:37, XR20 T4 'not tied')"),
    "NG-E": dict(route="an area-first horizon route a0^2 A_dS = (3/8) c^4",
                 specific_route=False, route_not_in_record=True, route_u_algebraic=True, route_no_inserted_target=False,
                 why="pi-allowed (E5) but the 3/8 must be supplied; no published or proposed mechanism; same class as 'density' (E5b)"),
    "NG-X1-i": dict(route="'4 = D' (trace) and the other D-dependent labels rejected only through the shared-D-lift premise",
                    specific_route=False, route_not_in_record=False, route_u_algebraic=True, route_no_inserted_target=False,
                    why="labels without a mechanism (X1 README:91-100, :117); 'a0^2 = G rho/D' has no action"),
    "NG-X1-ii": dict(route="Noether-charge condition at the a0 radius in u-units, G Q(r)/r = -4 pi/3",
                     specific_route=True, route_not_in_record=True, route_u_algebraic=True, route_no_inserted_target=False,
                     why="u-algebraic but it is G rho r^2 = 1 at r = 1/(2 a0), i.e. the puzzle restated (X1_4c)"),
    "NG-K": dict(route="(a) SUSY-breaking (F-term) vacuum energy; (b) a thermal (Bose) origin of the RAR nu",
                 specific_route=False, route_not_in_record=True, route_u_algebraic=False, route_no_inserted_target=False,
                 why="(a) no equation links a0 to the F-term; (b) computed here: W_v = pi^3/(30 g^3), transcendental, never 4 (K8)"),
    "NG-L": dict(route="u-algebraic SdS principles ('curvature = density')",
                 specific_route=True, route_not_in_record=False, route_u_algebraic=True, route_no_inserted_target=False,
                 why="K_Sigma = rho_Lambda is unattainable at every SdS horizon (L6; lane L E10); kappa^2 = c G rho needs c = 1/4 inserted"),
    "NG-N": dict(route="none (class as worded)", specific_route=False, route_not_in_record=False, route_u_algebraic=False, route_no_inserted_target=False,
                 why="the T(a) structure knows only a and H: outputs q H, excluded for any q algebraic, in any units"),
    "NG-P12": dict(route="none (class as worded; strengthened under NEC)", specific_route=False, route_not_in_record=False, route_u_algebraic=False, route_no_inserted_target=False,
                   why="P5/P5c: any static-patch normalisation under NEC gives |kappa| r_h >= (8pi-1)/2"),
    "NG-B3": dict(route="preferred-frame coupling ratio: forced kernel a0^2 = G_N rho_v with Lambda = 8 pi G_cosm rho_v gives kappa^2 = G_N/G_cosm; kappa = 1/2 needs G_cosm = 4 G_N",
                  specific_route=True, route_not_in_record=True, route_u_algebraic=True, route_no_inserted_target=False,
                  why="G_cosm/G_N is a free coupling ratio (set to 4 by hand); in the lambda-model G_cosm = 2G/(3 lambda - 1) needs lambda = 1/2 (G_N = G) or 1/3 < lambda < 1/2 (sol61's G_N), inside the negative-kinetic window 1/3 < lambda < 1 (S8); BBN allows 0.92-1.04"),
    "NG-S61": dict(route="none (class as worded)", specific_route=False, route_not_in_record=False, route_u_algebraic=False, route_no_inserted_target=False,
                   why="explicitly scoped to the canonical-clock action; re-derived"),
}


def main():
    C = Checks("CLASSIFICATION")
    R = json.load(open(os.path.join(HERE, "results.json")))
    flags = {
        "NG-G": R["NG-G"]["flags"], "NG-E": R["NG-E"]["flags"],
        "NG-X1-i": R["NG-X1"]["flags_X1_i"], "NG-X1-ii": R["NG-X1"]["flags_X1_ii"],
        "NG-K": R["NG-K"]["flags"], "NG-L": R["NG-L"]["flags"], "NG-N": R["NG-N"]["flags"],
        "NG-P12": R["NG-P12B3"]["flags_P12"], "NG-B3": R["NG-P12B3"]["flags_B3"], "NG-S61": R["NG-S61"]["flags"],
    }
    table = {}
    for k, fl in flags.items():
        cls = classify(fl)
        d, reason = door({**fl, **ROUTES[k]})
        table[k] = {"class": cls, "door": d, "door_reason": reason, "route_considered": ROUTES[k]["route"], "why": ROUTES[k]["why"]}
        print(f"{k:10s} {cls:30s} door={'YES' if d else 'no'}  [{reason}]")
    C.check("no_ERROR_class", all(v["class"] != "ERROR" for v in table.values()), "no audited no-go has a false load-bearing step")
    print(f"re-opened doors: {[k for k, v in table.items() if v['door']] or 'none'}")
    C.check("classes_from_frozen_classifier", all(table[k]["class"] == classify(flags[k]) for k in table), "every class is the frozen classifier's output on the scripted flags")
    C.value("re_opened_doors", ",".join(k for k, v in table.items() if v["door"]) or "none")
    return C.write({"table": table})


if __name__ == "__main__":
    run_main(main)

#!/usr/bin/env python3
"""AELLA (the whirlwind) -- EXHAUSTIVE ARCHITECTURE-CLASS SWEEP -- no LLM, no sampling: enumerate EVERY structural class the
grammar can express and run the deterministic gates on a representative of each. The trusted/theorem
gates are functions of structure only, so each verdict covers the WHOLE class. Output: the complete
map of the expressible space -- killed classes (with the killing gate) and the genuinely open ones."""
import sys, json, itertools, collections
import os
NEDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "neda_flow")
sys.path.insert(0, NEDA); os.chdir(NEDA)   # gates/state resolve from Neda; reports written back below
import candidate_manager as cm, evaluator as ev, gate_templates as gt

DEAD = json.load(open("state/DEAD_CLASSES.json"))["classes"]

def rep(geometry, conn, frame, pf, loc, mond, backing, norm, bint=None, bsrc=None):
    """Minimal representative candidate for one structural class."""
    fields=[{"name":"g","type":"metric","kinetic":"standard","timelike_background":False}]
    if geometry=="bimetric":
        fields.append({"name":"f","type":"metric","kinetic":"standard","timelike_background":False})
    if frame=="non_propagating":
        fields.append({"name":"u","type":"vector","kinetic":"none","timelike_background":True})
    elif frame=="propagating":
        fields.append({"name":"u","type":"vector","kinetic":"standard","timelike_background":True})
    if backing=="multiplier":
        fields.append({"name":"lam","type":"multiplier","kinetic":"none","timelike_background":False})
        sector="constrained"
    elif backing=="degenerate":
        fields.append({"name":"chi","type":"scalar","kinetic":"degenerate","timelike_background":False})
        sector="constrained"
    else:
        fields.append({"name":"chi","type":"scalar","kinetic":"standard","timelike_background":False})
        sector="propagating"
    coups=[{"label":"mond","sources":["chi","mu(y)"],"order_in_phi":2,"preferred_frame":False,
            "screened_by":None,"lapse_weighted":False,"nonlocal":("spatial" if loc=="nonlocal" else "none")}]
    if frame!="none" and pf!="none":
        coups.append({"label":"slip","sources":["u_mu","chi"],"order_in_phi":1,"preferred_frame":True,
                      "screened_by":("e^-y" if pf=="screened" else None),"lapse_weighted":False,"nonlocal":"none"})
    c={"name":"SWEEP","family":geometry,"connection":conn,"scalar_sector":sector,
       "fields":fields,"couplings":coups,"mond_realization":mond,
       "kinetic_normalization_source":norm,
       "claimed_mechanism":"sweep representative; degeneracy/constraint structure as declared",
       "predicted_weak_field":"n/a","inequivalence_argument":"exhaustive-sweep representative"}
    if geometry=="bimetric":
        c["bimetric_spec"]={"interaction":bint,"matter_metric":"g","mond_source":bsrc,"m_FP":"~H0"}
    return c

def verdict(c):
    canon=cm.canonicalize(c)
    for dc in DEAD:
        if ev.matches_dead_class(canon,dc): return ("DEAD-CLASS", dc["class_id"])
    g0=ev.gate_G0(c,canon)
    if g0["status"]=="KILL": return ("KILL-G0", g0["certificate"][:60])
    for gate in ("G4","G5","G6","G8"):
        v=gt.run(gate,c)
        if v and v["status"]=="KILL": return (f"KILL-{gate}", v["certificate"][:60])
    for gate in ("G1","G2","G3"):
        v=gt.run(gate,c)
        if v and v["status"]=="KILL": return (f"KILL-{gate}", v["certificate"][:60])
    return ("OPEN", "")

rows=[]; seen=set()
MONDS=["aux_legendre_chi","constraint_first_q","nonlocal_F+"]
# ---- single metric
for conn,frame,pf,loc,mond,backing,norm in itertools.product(
        ["riemannian","teleparallel","nonmetricity"], ["none","non_propagating","propagating"],
        ["none","unscreened","screened"], ["local","nonlocal"], MONDS,
        ["none","multiplier","degenerate"], ["independent","screened_coupling"]):
    if frame=="none" and pf!="none": continue
    c=rep("single",conn,frame,pf,loc,mond,backing,norm)
    key=cm.mechanism_fingerprint(c)[0]
    if key in seen: continue
    seen.add(key)
    v,why=verdict(c)
    rows.append({"class":{"geom":"single","conn":conn,"frame":frame,"pf":pf,"loc":loc,"mond":mond,
                          "backing":backing,"norm":norm},"verdict":v,"why":why})
# ---- bimetric
for bint,bsrc,loc,mond,norm in itertools.product(
        ["hassan_rosen","composite","bimond_connection","other"],
        ["linear_massive_graviton","nonlinear_helicity0","composite_matter","connection_invariants"],
        ["local","nonlocal"], MONDS, ["independent"]):
    c=rep("bimetric","riemannian","none","none",loc,mond,"none",norm,bint,bsrc)
    key=cm.mechanism_fingerprint(c)[0]
    if key in seen: continue
    seen.add(key)
    v,why=verdict(c)
    rows.append({"class":{"geom":"bimetric","interaction":bint,"mond_source":bsrc,"loc":loc,
                          "mond":mond},"verdict":v,"why":why})

tally=collections.Counter(r["verdict"] for r in rows)
opens=[r for r in rows if r["verdict"]=="OPEN"]
json.dump({"total_classes":len(rows),"tally":dict(tally),"open_classes":opens},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","aella_flow","reports","EXHAUSTIVE_SWEEP.json"),"w"), indent=1)
print(f"TOTAL structural classes enumerated: {len(rows)}")
for k,v in sorted(tally.items(), key=lambda x:-x[1]): print(f"  {k:14s}: {v}")
print(f"\n=== THE OPEN CLASSES ({len(opens)}) -- the genuinely unkilled territory ===")
for r in opens: print("  ", json.dumps(r["class"]))

#!/usr/bin/env python3
"""ORACLE REGRESSION TEST — the machine must reproduce verdicts we derived BY HAND this session.
This is the answer to 'how do we know it works': run known-verdict architectures, require agreement.
If any row flips, the evaluator changed its mind about established physics -> DO NOT TRUST until audited."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import candidate_manager as cm, evaluator as ev, gate_templates as gt

def C(**k):
    for d,v in dict(name="x",family="x",mond_realization="x",claimed_mechanism="x",fields=[],couplings=[]).items():
        k.setdefault(d,v)
    return k

CASES = [
 ("AeST unscreened vector",
  C(family="screened-preferred-frame",
    fields=[{"name":"A","type":"vector","kinetic":"standard","timelike_background":True}],
    couplings=[{"label":"a2","sources":["u_mu","a_mu"],"order_in_phi":2,"preferred_frame":True,
                "screened_by":None,"lapse_weighted":False,"nonlocal":"none"}]),"KILL"),
 ("lapse-weighted MOND",
  C(mond_realization="aux_legendre_chi",
    couplings=[{"label":"m","sources":["chi","lapse"],"order_in_phi":2,"preferred_frame":False,
                "screened_by":None,"lapse_weighted":True,"nonlocal":"none"}]),"KILL"),
 ("temporal-nonlocal escape",
  C(couplings=[{"label":"t","sources":["box_ret"],"order_in_phi":2,"preferred_frame":False,
                "screened_by":None,"lapse_weighted":False,"nonlocal":"temporal"}]),"KILL"),
 ("P7 collision",
  C(kinetic_normalization_source="screened_coupling",
    fields=[{"name":"T","type":"khronon","kinetic":"degenerate","timelike_background":True}],
    couplings=[{"label":"a","sources":["a_mu","mu(y)"],"order_in_phi":2,"preferred_frame":True,
                "screened_by":"e^-y","lapse_weighted":False,"nonlocal":"none"}]),"KILL"),
 ("khronometric e^-y SCREENED survivor",
  C(family="screened-preferred-frame",kinetic_normalization_source="independent",
    mond_realization="aux_legendre_chi",
    fields=[{"name":"T","type":"khronon","kinetic":"standard","timelike_background":True}],
    couplings=[{"label":"a2","sources":["a_mu","mu(y)"],"order_in_phi":2,"preferred_frame":True,
                "screened_by":"e^-y","lapse_weighted":False,"nonlocal":"none"}]),"PASS"),
]

def machine_verdict(cand):
    canon = cm.canonicalize(cand)
    dead = json.load(open(os.path.join(os.path.dirname(__file__),"..","state","DEAD_CLASSES.json")))
    if any(ev.matches_dead_class(canon,d) for d in dead["classes"]):
        return "KILL"
    return "KILL" if ev.gate_G0(cand,canon)["status"]=="KILL" else "PASS"

def main():
    bad=[]
    for name,cand,expect in CASES:
        v=machine_verdict(cand)
        if v!=expect: bad.append((name,v,expect))
    # G1 constitutive identity
    if gt.run("G1",C(mond_realization="aux_legendre_chi"))["status"]!="PASS":
        bad.append(("aux-Legendre G1","!=PASS","PASS"))
    if bad:
        print("ORACLE FAIL:",bad); sys.exit(1)
    print(f"ORACLE OK: {len(CASES)+1}/{len(CASES)+1} machine verdicts match hand-derived physics")

if __name__=="__main__": main()

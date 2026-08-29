import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import candidate_manager as cm, evaluator as ev

good = {"name":"t","family":"screened-preferred-frame","mond_realization":"aux_legendre_chi",
  "claimed_mechanism":"x","kinetic_normalization_source":"independent",
  "fields":[{"name":"T","type":"khronon","kinetic":"standard","timelike_background":True}],
  "couplings":[{"label":"a2","sources":["a_mu","mu(y)"],"order_in_phi":2,"preferred_frame":True,
                "screened_by":"e^-y","lapse_weighted":False,"nonlocal":"none"}]}
bad = json.loads(json.dumps(good)); bad["couplings"][0]["screened_by"]=None
lapse = json.loads(json.dumps(good)); lapse["couplings"][0]["lapse_weighted"]=True

c0 = ev.gate_G0(good, cm.canonicalize(good)); assert c0["status"]=="PASS", c0
c1 = ev.gate_G0(bad, cm.canonicalize(bad));  assert c1["status"]=="KILL", c1
c2 = ev.gate_G0(lapse, cm.canonicalize(lapse)); assert c2["status"]=="KILL", c2
h1, h2 = cm.arch_hash(good), cm.arch_hash(json.loads(json.dumps(good)))
assert h1==h2
ren = json.loads(json.dumps(good)); ren["fields"][0]["name"]="S"   # rename collapses
assert cm.arch_hash(ren)==h1
# dead-class DC-002 signature: propagating timelike vector
aest = {"name":"a","family":"x","mond_realization":"y","claimed_mechanism":"z",
  "fields":[{"name":"A","type":"vector","kinetic":"standard","timelike_background":True}],"couplings":[]}
dc = json.load(open(os.path.join(os.path.dirname(__file__),"..","state","DEAD_CLASSES.json")))
hit = any(ev.matches_dead_class(cm.canonicalize(aest), c) for c in dc["classes"])
assert hit, "AeST-like candidate should match DC-002"
# script-gate contract
cert = ev.run_gate_script("TEST-0001","G1",
  'print(\'CERTIFICATE_JSON: {"gate":"G1","status":"OPEN","certificate":"smoke"}\')')
assert cert["status"]=="OPEN", cert
print("SMOKE OK: G0 pass/kill, canonical hash, rename-collapse, dead-class match, script contract")

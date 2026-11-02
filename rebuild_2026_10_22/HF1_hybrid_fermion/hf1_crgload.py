"""Load CRG1's clean-room modules read-only, inputs from CRG1, caches into this lane. kappa = 1/2 FITTED; not theory closed."""
import os, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CRG = os.path.join(RB, "CRG1_clean_room_regrade")
sys.dont_write_bytecode = True
def crg():
    if "crg1_core" in sys.modules: return
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read(); a = 'INP = os.path.join(HERE, "inputs")'; assert s.count(a) == 1
    s = s.replace(a, f'INP = {os.path.join(CRG, "inputs")!r}').replace('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(HERE, "cache_crg", "p")!r}').replace('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(HERE, "cache_crg", "c")!r}')
    m = types.ModuleType("crg1_core"); m.__file__ = p; sys.modules["crg1_core"] = m; exec(compile(s, p, "exec"), m.__dict__); sys.path.insert(0, os.path.join(CRG, "v1"))

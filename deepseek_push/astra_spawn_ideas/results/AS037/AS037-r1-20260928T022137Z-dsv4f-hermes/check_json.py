import json, sys, mpmath as mp
src = open('compute_as037.py').read()
# strip the final print and instead dump with a checker
src = src.replace("print(json.dumps(out, indent=1, sort_keys=True))",
                  "pass\ncheck_json(out)")
checker = '''
def check_json(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if not isinstance(k, str):
                print("NON-STRING KEY at", path, ":", repr(k)[:80]); sys.exit(1)
            check_json(v, path + "/" + k[:40])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            check_json(v, path + "[%d]" % i)
    elif isinstance(o, str):
        return
    elif o is None or isinstance(o, (bool, int, float)):
        return
    else:
        try:
            json.dumps(o)
        except Exception as e:
            print("BAD VALUE at", path, ":", type(o), repr(o)[:120], "->", e); sys.exit(1)
'''
src = src.replace("import sympy as sp", "import sympy as sp\n" + checker)
exec(compile(src, 'compute_as037_check.py', 'exec'), {'__name__': '__main__'})
print("ALL VALUES JSON-SAFE")

"""CFG237 MUTATE dispatcher: runs M1..M8 (env MUTATE=k) on the script(s) that carry each mutation; a control BITES when the script exits 1.
M1 class move -> CFG237_classes; M2 alpha_CO x2 -> main; M3 common-mode +0.30 dex -> main and c7; M4 swap flat/rival -> power; M5 band on the stars -> main;
M6 sigma_int 0.30 -> power; M7 R_e x1.5 -> main; M8 g_obs x1.5 -> main. Exit 0 iff every mutation bites (every designated script exits 1)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = {"1": ["CFG237_classes.py"], "2": ["CFG237_main.py"], "3": ["CFG237_main.py", "CFG237_c7.py"], "4": ["CFG237_power.py"],
        "5": ["CFG237_main.py"], "6": ["CFG237_power.py"], "7": ["CFG237_main.py"], "8": ["CFG237_main.py"]}
allbite = True
lines = []
for k, scripts in PLAN.items():
    for s in scripts:
        env = dict(os.environ); env["MUTATE"] = k
        p = subprocess.run([sys.executable, os.path.join(HERE, s)], env=env, capture_output=True, text=True)
        bite = p.returncode == 1
        allbite &= bite
        lines.append(f"M{k} {s}: exit {p.returncode} -> {'BITES' if bite else 'DOES NOT BITE'}")
        print(lines[-1])
open(os.path.join(HERE, "CFG237_MUTATE.out"), "w").write("\n".join(lines) + f"\nALL BITE: {allbite}\n")
print("ALL BITE:", allbite)
sys.exit(0 if allbite else 1)

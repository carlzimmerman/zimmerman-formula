"""AS3 gate G-MAT: AS2's as2_gmat.run() unchanged, executed by import."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
_AS2 = Path(__file__).resolve().parent.parent / "AS2_fg_cpr_scheme"
if str(_AS2) not in sys.path:
    sys.path.insert(0, str(_AS2))
import as2_gmat

if __name__ == "__main__":
    print("MODE: NORMAL (AS2 G-MAT by import, unchanged)")
    ok, _, _ = as2_gmat.run()
    print("\nCHECKS FAILED:", as2_gmat.fails if as2_gmat.fails else "none")
    sys.exit(0 if ok else 1)

"""Re-grade AC23 with its own frozen grade.py, swapping in the corrected main rows.
Builds a tree in argv[1]: stored AC23 parts/ka1 (read-only copies) + reruns/ac23_main_corrected/*.json,
then runs AC23 grade.py's source with only its D path changed. Run from the repo root."""
import shutil, sys
from pathlib import Path
src = Path('action_search_2026_11_05/AC23_fresh_slow_roots')
fix = Path('closure_2026_11_06/FRW_RECONCILIATION_CHAIN/reruns/ac23_main_corrected')
T = Path(sys.argv[1]); (T / 'parts').mkdir(parents=True, exist_ok=True)
for p in (src / 'parts').glob('*.json'): shutil.copy(p, T / 'parts' / p.name)
shutil.copytree(src / 'ka1', T / 'ka1', dirs_exist_ok=True); shutil.copy(src / 'witnesses.json', T / 'witnesses.json')
for p in fix.glob('*.json'): shutil.copy(p, T / 'parts' / p.name)
code = (src / 'grade.py').read_text().replace(
    "D = Path('action_search_2026_11_05/AC23_fresh_slow_roots')", f"D = Path({str(T)!r})")
assert f"D = Path({str(T)!r})" in code
exec(compile(code, 'AC23/grade.py[corrected tree]', 'exec'), {'__name__': '__main__'})

"""Execute unchanged CFG782 mathematics, redirecting only its two output paths."""
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[2]
src = root/'campaign_fresh_gravity/CFG782_unbinding_selector/cfg782.py'
out = Path(sys.argv[1]).resolve()
text = src.read_text()
# HERE is used in these two writes; preserve its original value for input resolution.
old = 'os.path.join(HERE, f"cfg782'
assert text.count(old) == 2
text = text.replace(old, 'os.path.join('+repr(str(out))+', f"cfg782')
exec(compile(text, str(src), 'exec'), {'__file__':str(src), '__name__':'__main__'})

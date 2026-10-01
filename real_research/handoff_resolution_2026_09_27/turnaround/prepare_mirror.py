from pathlib import Path
import shutil,json,hashlib,subprocess,sys
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
mirror=out/'mirror'; mirror.mkdir(exist_ok=True)
# Copy small scientific source/data artifacts only; no source/output symlinks.
folders=['real_research/derivation_chain_2026','real_research/cross_thread_review_2026_09_26','real_research/dark_energy_2026','real_research/acceleration_trigger_2026','real_research/dark_sector_2026','real_research/dark_fluid_kick_2026','real_research/blind_kernel_2026','real_research/generated_phantom_2026','real_research/data/lensing_rar/brouwer2021_rar','hunt_2026']
hashes={}
for folder in folders:
 for p in (root/folder).rglob('*'):
  if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts: continue
  if p.suffix not in ('.py','.json','.out','.txt','.dat','.csv','.md'): continue
  if p.stat().st_size>10000000: continue
  if p.name.startswith('XR36_') and p.suffix in ('.out','.json'): continue
  dst=mirror/p.relative_to(root); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dst)
  hashes[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(out/'mirror_sources.json').write_text(json.dumps({'base_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'input_hashes':hashes},indent=2))
print('copied',len(hashes),'files',mirror)

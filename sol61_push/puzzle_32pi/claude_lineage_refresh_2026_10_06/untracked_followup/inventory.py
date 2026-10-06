"""Scoped untracked inventory and dirty-log prefix comparison; no science execution."""
from pathlib import Path
import subprocess,json,hashlib,collections,zipfile,datetime
r=Path.cwd();p=r/'sol61_push/puzzle_32pi/claude_lineage_refresh_2026_10_06/untracked_followup';scopes=['sonnet55_push/puzzle_32pi','campaign_fresh_gravity']
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def sha(b):return hashlib.sha256(b).hexdigest()
head=git('rev-parse','HEAD');files=git('ls-files','--others','--exclude-standard','--',*scopes).splitlines();records=[]
source_suffixes={'.py','.md','.lean','.json','.toml','.yaml','.yml','.tex','.c','.cpp','.h','.jl','.r','.ipynb'}
for f in files:
 q=r/f;sz=q.stat().st_size
 with q.open('rb') as g:header=g.read(128)
 row=dict(path=f,bytes=sz,suffix=q.suffix,header_128_sha256=sha(header),header_has_NUL=b'\x00' in header,is_source_candidate=q.suffix.lower() in source_suffixes)
 if q.suffix=='.npz':
  with zipfile.ZipFile(q) as z:
   members=z.infolist();names=[i.filename for i in members]
   row['archive_member_count']=len(names);row['archive_suffix_counts']=dict(collections.Counter(Path(i).suffix for i in names));row['archive_catalog_sha256']=sha('\n'.join(names).encode());row['archive_member_sample']=names[:12];row['uncompressed_bytes_total']=sum(i.file_size for i in members)
  row['classification']='NumPy array zip archive; member-directory read only, no array execution/loading'
 elif q.suffix=='.bin':row['classification']='binary simulation product by suffix/location/names and sampled byte header, not scientific source'
 elif q.suffix=='.out':row['classification']='untracked execution log';row['full_sha256']=sha(q.read_bytes());row['full_text']=q.read_text(errors='replace')
 else:row['classification']='unclassified; needs source review'
 records.append(row)
dirty=[]
for f in ['campaign_fresh_gravity/CFG4_clusters.out','campaign_fresh_gravity/CFG4_galaxy_law.out','campaign_fresh_gravity/CFG4_galaxy_law_MUTATE.out']:
 q=r/f;cur=q.read_bytes();old=subprocess.check_output(['git','show',head+':'+f]);dirty.append(dict(path=f,current_sha256=sha(cur),committed_sha256=sha(old),current_bytes=len(cur),committed_bytes=len(old),current_is_exact_committed_prefix=old.startswith(cur),current_lines=len(cur.splitlines()),committed_lines=len(old.splitlines()),last_source_log_commit=git('log','-1','--format=%H',head,'--',f),interpretation='prefix truncation only if exact prefix test true; no new completed outcome inferred'))
out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),pinned_HEAD=head,HEAD_at_end=git('rev-parse','HEAD'),scopes=scopes,extension_counts=dict(collections.Counter(x['suffix'] for x in records)),scope_counts=dict(collections.Counter(x['path'].split('/')[0] for x in records)),source_candidate_suffixes=sorted(source_suffixes),source_candidates=[x['path'] for x in records if x['is_source_candidate']],inventory=records,dirty_log_comparison=dirty,limits='git untracked --exclude-standard, ignores omitted; binary contents not scientifically audited or regenerated; header hashes are not whole-file hashes; no inference of when/by whom products were generated or scientific antecedent validity; no source writes',original_snapshot_sha256=sha((p.parent/'SOURCE_UPDATE.json').read_bytes()))
(p/'INVENTORY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(extensions=out['extension_counts'],source_candidates=out['source_candidates'],dirty_prefix_tests=[(x['path'],x['current_is_exact_committed_prefix']) for x in dirty],HEAD=head)))

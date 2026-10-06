"""Read-only bounded Git/source lineage refresh; never executes scientific sources."""
from pathlib import Path
import subprocess,json,hashlib,datetime
root=Path.cwd();owned=root/'sol61_push/puzzle_32pi/claude_lineage_refresh_2026_10_06'
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def dig(b):return hashlib.sha256(b).hexdigest()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();head=git('rev-parse','HEAD')
prior=json.loads((root/'sol61_push/puzzle_32pi/projected_external_field_2026_10_06/SOURCE_AUDIT.json').read_text())
checkpoints={'sonnet55_push/puzzle_32pi':'6988a2ecbab63393c26a160f81ee15a4391d6a0a','campaign_fresh_gravity':'be5eee875ba98ad4246ee3e854094fd5050cfd5b'}
files=[r['path'] for r in prior['files'] if r['path'].startswith(('sonnet55_push/','campaign_fresh_gravity/'))]
# Pin the imported solver and source harness/certification dependency, without running it.
files+=['campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_edge_harness.py','campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/CFG355_veto_certificates.lean']
old={r['path']:r for r in prior['files']};records=[]
for f in files:
 cur=(root/f).read_bytes();blob=subprocess.check_output(['git','show',head+':'+f]);last=git('log','-1','--format=%H',head,'--',f)
 records.append(dict(path=f,sha256=dig(cur),pinned_HEAD_blob_sha256=dig(blob),matches_pinned_HEAD=cur==blob,last_file_commit=last,matches_prior_source_snapshot=(dig(cur)==old[f]['current_sha256']) if f in old else None))
logs={scope:git('log','--format=%H %s',base+'..'+head,'--',scope).splitlines() for scope,base in checkpoints.items()}
ancestry={scope:subprocess.run(['git','merge-base','--is-ancestor',base,head]).returncode==0 for scope,base in checkpoints.items()}
scopes=list(checkpoints);dirty=git('status','--porcelain','--untracked-files=no','--',*scopes).splitlines();untracked=git('ls-files','--others','--exclude-standard','--',*scopes).splitlines()
out=dict(start_UTC=start,end_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),pinned_HEAD=head,HEAD_at_end=git('rev-parse','HEAD'),source_checkpoints=checkpoints,checkpoints_are_ancestors=ancestry,tracked_commits_since_checkpoint=logs,tracked_dirty=dirty,untracked_count=len(untracked),untracked_names_not_scientific_evidence=True,files=records,prior_snapshot='sol61_push/puzzle_32pi/projected_external_field_2026_10_06/SOURCE_AUDIT.json',prior_snapshot_sha256=dig((root/'sol61_push/puzzle_32pi/projected_external_field_2026_10_06/SOURCE_AUDIT.json').read_bytes()),commands=['git rev-parse HEAD','git log --format=%H %s CHECKPOINT..PINNED_HEAD -- SCOPE','git merge-base --is-ancestor CHECKPOINT PINNED_HEAD','git status --porcelain --untracked-files=no -- TWO_SCOPES','git ls-files --others --exclude-standard -- TWO_SCOPES','git show PINNED_HEAD:FILE','git log -1 --format=%H PINNED_HEAD -- FILE'],limits='only two named tracked scopes and ten named source/README/criteria/harness/Lean files; no scientific reruns, fetches, branch mutation or author edits',claim='No newer tracked scientific source under these scopes in the inspected interval if both tracked logs are empty; no claim about all Claude activity')
(owned/'SOURCE_UPDATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(pinned_HEAD=head,HEAD_at_end=out['HEAD_at_end'],new_scoped_commits=sum(map(len,logs.values())),changed_named_current_sources=[r['path'] for r in records if not r['matches_pinned_HEAD']],dirty=dirty,untracked_count=len(untracked))))

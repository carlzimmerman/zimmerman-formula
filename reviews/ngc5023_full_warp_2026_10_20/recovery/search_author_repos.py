#!/usr/bin/env python3
"""Bounded metadata-only search of author's public model/software repositories."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

HERE=Path(__file__).resolve().parent
records=[]

def get(url,name):
    req=urllib.request.Request(url,headers={'User-Agent':'NGC5023-public-model-recovery/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=25) as f:
            raw=f.read(2_000_001)
            if len(raw)>2_000_000:raise RuntimeError('metadata response byte bound')
            resolved=f.url
        p=HERE/name;p.write_bytes(raw)
        records.append({'url':url,'resolved_url':resolved,'path':str(p.name),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        return json.loads(raw)
    except Exception as e:
        records.append({'url':url,'error':repr(e)})
        return None

repos=get('https://api.github.com/users/PeterKamphuis/repos?per_page=100','author_repos.json')
hits=[]
if repos:
    for repo in repos:
        if repo['name'] in ['FAT','pyFAT-astro','pyHIARD','TRM_errors','Disk_Simulations']:
            branch=repo['default_branch']
            tree=get('https://api.github.com/repos/'+repo['full_name']+'/git/trees/'+branch+'?recursive=1','tree_'+repo['name']+'.json')
            if tree:
                selected=[v for v in tree.get('tree',[]) if any(t in v['path'].lower().replace('_','').replace(' ','') for t in ['5023','8286'])]
                hits.append({'repo':repo['full_name'],'branch':branch,'tree_sha':tree.get('sha'),'truncated':tree.get('truncated'),'object_filename_matches':selected,'paths_checked':len(tree.get('tree',[]))})
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Fresh metadata-only author-repository recovery path, distinct from prior article/archive searches. No files executed or installed.','records':records,'search_results':hits,'limit':'Filename matching only; no claim every blob, repository history or nonpublic attachment was searched. No matched file by itself authenticates the 2013preferredmodel.'}
(HERE/'AUTHOR_REPOSITORY_SEARCH.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(hits,indent=2))

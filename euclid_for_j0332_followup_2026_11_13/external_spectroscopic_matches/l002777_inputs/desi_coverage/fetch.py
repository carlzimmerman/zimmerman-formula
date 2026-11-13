"""Small public metadata requests with byte/time caps and provenance."""
import argparse,hashlib,json,time,urllib.request,urllib.error
from pathlib import Path
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent


def fetch(label,url,limit=3000000):
    start=time.monotonic()
    record={'url':url,'method':'GET','started_utc':datetime.now(timezone.utc).isoformat(),
            'max_bytes':limit,'timeout_seconds':30}
    request=urllib.request.Request(url,headers={'User-Agent':'Astronomy-public-data-audit/1.0'})
    try:
        response=urllib.request.urlopen(request,timeout=30)
    except urllib.error.HTTPError as error:
        response=error
    except Exception as error:
        record.update(error=repr(error),elapsed_seconds=time.monotonic()-start)
        (HERE/(label+'.provenance.json')).write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record));return
    with response:
        data=response.read(limit+1)
        record.update(status=response.status,final_url=response.geturl(),headers=dict(response.headers),
            observed_bytes=len(data),truncated=len(data)>limit,elapsed_seconds=time.monotonic()-start)
    if len(data)>limit:data=data[:limit]
    target=HERE/label
    target.write_bytes(data)
    record.update(output=str(target),sha256=hashlib.sha256(data).hexdigest())
    (HERE/(label+'.provenance.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='headers'}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('label');parser.add_argument('url')
    parser.add_argument('--max-bytes',type=int,default=3000000)
    args=parser.parse_args();fetch(args.label,args.url,args.max_bytes)

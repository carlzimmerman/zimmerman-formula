"""Bounded public-data fetch with per-attempt provenance; no bulk products."""
import argparse,datetime,hashlib,json,time,urllib.request
from pathlib import Path

class PublicGetRedirects(urllib.request.HTTPRedirectHandler):
    def http_error_308(self,req,fp,code,msg,headers):
        return self.http_error_302(req,fp,302,msg,headers)

def main():
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('output');p.add_argument('--max-bytes',type=int,default=12000000);p.add_argument('--byte-range');args=p.parse_args()
    dest=Path(args.output);assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();rec=dict(url=args.url,output=str(dest),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),max_bytes=args.max_bytes,timeout_seconds=45)
    try:
        headers={'User-Agent':'Scientific reproducibility audit; bounded single-table request'}
        if args.byte_range:headers['Range']='bytes='+args.byte_range;rec['requested_byte_range']=args.byte_range
        request=urllib.request.Request(args.url,headers=headers)
        with urllib.request.build_opener(PublicGetRedirects()).open(request,timeout=45) as response:
            data=response.read(args.max_bytes+1);rec.update(status=response.status,final_url=response.url,headers=dict(response.headers))
            if args.byte_range and response.status!=206:raise ValueError('Server did not honor bounded range request')
        if len(data)>args.max_bytes:raise ValueError('Response exceeded byte cap')
        dest.write_bytes(data);rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),success=True)
    except Exception as e:rec.update(success=False,error=repr(e))
    rec['seconds']=time.monotonic()-start;dest.with_name(dest.name+'.provenance.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
    return 0 if rec['success'] else 1

if __name__=='__main__':raise SystemExit(main())

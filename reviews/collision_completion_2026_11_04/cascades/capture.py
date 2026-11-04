"""Always record observed process RSS/runtime even if an experiment raises."""
import sys,time,resource,json,runpy,traceback
from pathlib import Path
def main():
 metric,script,*args=sys.argv[1:];start=time.monotonic();status='completed';error=None
 try:
  sys.argv=[script]+args;runpy.run_path(script,run_name='__main__')
 except BaseException as exc:
  status='failed';error=repr(exc);raise
 finally:
  Path(metric).write_text(json.dumps(dict(status=status,error=error,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
if __name__=='__main__':main()

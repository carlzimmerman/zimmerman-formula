import ctypes, sys, time, os, json
pid = int(sys.argv[1]); out = sys.argv[2]
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")
class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
mx = 0.0; series = []
while True:
    ru = _RU()
    if _LP.proc_pid_rusage(pid, 2, ctypes.byref(ru)) != 0: break
    f = ru.footprint / 1e9; mx = max(mx, f); series.append((round(time.time()), round(f, 2), round(ru.resident / 1e9, 2)))
    if len(series) % 20 == 0: json.dump(dict(max_fp_gb=mx, series=series[-4000:]), open(out, "w"))
    time.sleep(0.5)
json.dump(dict(max_fp_gb=mx, series=series[-4000:]), open(out, "w"))

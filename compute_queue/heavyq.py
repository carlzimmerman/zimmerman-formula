#!/usr/bin/env python3
"""heavyq: a preemptible heavy-compute queue for this repo.  One heavy job runs at a time; it yields (checkpoint, exit) when the
machine is needed by the lanes in progress, and is resumed with its resume_cmd when the room returns.

The owner's request (2026-10-23): heavy compute saves progress, makes room for the work in progress, and picks back up when that
lands, so the machine is always computing but no lane waits on a large run.

  nohup python3 compute_queue/heavyq.py daemon >/dev/null 2>&1 &     (from the repo root; one instance per queue dir: pidfile lock)
  python3 compute_queue/heavyq.py status [--json]
  python3 compute_queue/heavyq.py add --id ID --cmd CMD --resume-cmd CMD --est-gb G [--cwd DIR] [--priority P] [--threads T]
                                      [--done-file F] [--retries N] [--grace S] [--env K=V ...] [--hold] [--note TEXT]
  python3 compute_queue/heavyq.py pause ID | resume ID | remove ID
  touch compute_queue/YIELD          (the running job checkpoints and exits; nothing starts while the file exists)

Rules (defaults below; any key can be overridden in <queue dir>/config.json, which is re-read every poll):
  start  the highest-priority queued/paused job that is not held (strict head of line; ties by queue order), when no queue job
         runs, no known heavy run is live (the 1024^3 engines/launchers, as chain960.sh's heavy() gate), free+inactive >=
         max(est_gb, learned peak) + headroom_gb (8), disk free >= disk_min_gb (30), no other process has a footprint >
         other_proc_gb (4), no YIELD file, and all of that has held for clear_s.  First run: cmd.  Every later run: resume_cmd.
  yield  SIGTERM to the job's process group when free+inactive < floor_gb (6), swap used grew > swap_grow_gb (2) since the run
         started, YIELD exists, another process has a footprint > other_proc_gb, a known heavy run appears, disk free <
         disk_min_gb, or `pause ID`.  SIGKILL when the group has not exited grace_s (300) after the SIGTERM.  -> paused.
  abort  SIGKILL at once: job footprint > hard_abort_gb (52) -> failed; swap growth > swap_kill_gb (4, CFG960's frozen rule)
         or disk free < disk_kill_gb (5) -> paused (counts as a retry).
Memory is read the macOS way (RSS under-reports because pages are compressed): per-process phys_footprint from libproc, summed
over the job's process group; vm_stat free+inactive; sysctl vm.swapusage.  Jobs run under nohup + nice in their own process
group (start_new_session) through a small shim that records the exit code, so they survive a daemon restart and are adopted
by the next daemon.  Stdlib only.  What a job must do: JOB_CONTRACT.md.
"""
import argparse, ctypes, fcntl, json, os, re, shutil, signal, subprocess, sys, time, traceback
from contextlib import contextmanager

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ME = os.path.abspath(__file__)
GB = 1e9
YIELD_EXIT = 75          # EX_TEMPFAIL: "checkpoint written, resumable"
ACTIVE = ("running", "yielding")
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
               "NUMBA_NUM_THREADS", "HEAVYQ_THREADS")
DEFAULTS = dict(
    headroom_gb=8.0,       # start needs free+inactive >= est_gb + headroom_gb
    floor_gb=6.0,          # yield when free+inactive < floor_gb
    swap_grow_gb=2.0,      # yield when swap used grew more than this since the run started
    swap_kill_gb=4.0,      # SIGKILL at once beyond this growth (CFG960's frozen abort rule), even inside the grace period
    other_proc_gb=4.0,     # yield (and do not start) while any other process has a footprint above this
    hard_abort_gb=52.0,    # SIGKILL at once when the job's footprint exceeds this -> failed
    disk_min_gb=30.0,      # start needs disk free >= this; a running job yields below it
    disk_kill_gb=5.0,      # SIGKILL at once below this (no room left for a checkpoint)
    grace_s=300,           # SIGTERM -> SIGKILL
    clear_s=120,           # all start gates must stay clear this long before a start / resume (no flapping)
    poll_s=10,
    status_s=30,
    nice=5,
    default_threads=12,    # leaves 4 of 16 cores to the lanes
    max_retries=3,         # restarts after a crash / lost run / emergency kill before the job is marked failed
    external_heavy_regex=r"cfg6[0-9][0-9]_pm\.py|run_65[04]\.py|cfg596_pm|cfg960_sctm_pm\.py|run_960\.py|llama-server",
    ignore_proc_regex="",  # processes never counted by the other_proc_gb rule (matched on the full command line)
)


# ----------------------------------------------------------------------------------------------------- machine probes (macOS)
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")


class _RU(ctypes.Structure):   # rusage_info_v2 (flavor 2), as run_960.py; plus the start time used to recognise our own pid
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in (
        "user_time", "system_time", "pkg_idle_wkups", "interrupt_wkups", "pageins", "wired", "resident", "footprint",
        "start_abstime", "exit_abstime")] + [("pad", ctypes.c_uint64 * 40)]


def proc_info(pid):
    """(phys_footprint GB, start abstime) or None when the process is gone or not ours (root processes are unreadable)."""
    ru = _RU()
    if _LP.proc_pid_rusage(int(pid), 2, ctypes.byref(ru)) != 0:
        return None
    return ru.footprint / GB, int(ru.start_abstime)


def vm_free():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    ps = int(re.search(r"page size of (\d+) bytes", out).group(1))

    def pages(name):
        m = re.search(r"^%s:\s+(\d+)\." % re.escape(name), out, re.M)
        return int(m.group(1)) if m else 0
    f, i = pages("Pages free"), pages("Pages inactive")
    return dict(free_gb=f * ps / GB, inactive_gb=i * ps / GB, free_inactive_gb=(f + i) * ps / GB)


def swap_usage():
    out = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout

    def val(key):
        m = re.search(key + r" = ([\d.]+)([KMGT])", out)
        if not m:
            return 0.0
        return float(m.group(1)) * {"K": 2 ** 10, "M": 2 ** 20, "G": 2 ** 30, "T": 2 ** 40}[m.group(2)] / GB
    return dict(swap_used_gb=val("used"), swap_total_gb=val("total"))


def ps_rows(exclude=()):
    """[(pid, pgid, command)] for every process."""
    p = subprocess.Popen(["ps", "-axo", "pid=,pgid=,command="], stdout=subprocess.PIPE, text=True)
    out = p.communicate()[0]
    rows = []
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        pid, pgid = int(parts[0]), int(parts[1])
        if pid == p.pid or pid in exclude:
            continue
        rows.append((pid, pgid, parts[2] if len(parts) > 2 else ""))
    return rows


def short(cmd, n=70):
    toks = cmd.split()
    if not toks:
        return "?"
    s = " ".join([os.path.basename(toks[0])] + toks[1:])
    return s if len(s) <= n else s[:n - 3] + "..."


def group_alive(pgid):
    try:
        os.killpg(int(pgid), 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:   # the group id now belongs to someone else's processes: ours is gone
        return False


def snapshot(cfg, job_pgid=None):
    s = dict(t=time.time())
    s.update(vm_free())
    s.update(swap_usage())
    s["disk_free_gb"] = shutil.disk_usage(REPO).free / GB
    me = os.getpid()
    ign = re.compile(cfg["ignore_proc_regex"]) if cfg["ignore_proc_regex"] else None
    hv = re.compile(cfg["external_heavy_regex"]) if cfg["external_heavy_regex"] else None
    job_fp, job_n, big, heavy = 0.0, 0, [], []
    for pid, pgid, cmd in ps_rows():
        info = proc_info(pid)
        fp = info[0] if info else None
        if job_pgid and pgid == job_pgid:
            job_n += 1
            job_fp += fp or 0.0
            continue
        if pid == me or "heavyq.py" in cmd:
            continue
        if fp is not None and fp > cfg["other_proc_gb"] and not (ign and ign.search(cmd)):
            big.append(dict(pid=pid, footprint_gb=round(fp, 2), cmd=short(cmd)))
        if hv and hv.search(cmd):
            heavy.append(dict(pid=pid, footprint_gb=round(fp, 2) if fp is not None else None, cmd=short(cmd)))
    s.update(job_footprint_gb=job_fp, job_nproc=job_n, other_big=big, external_heavy=heavy)
    return s


# ----------------------------------------------------------------------------------------------------- files
def now_iso(t=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t if t is not None else time.time()))


def atomic_write_json(path, obj):
    tmp = "%s.tmp.%d" % (path, os.getpid())
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def qdir_default():
    return os.path.abspath(os.environ.get("HEAVYQ_DIR") or HERE)


def load_config(qdir):
    cfg = dict(DEFAULTS)
    user = read_json(os.path.join(qdir, "config.json"), {}) or {}
    cfg.update({k: v for k, v in user.items() if k in DEFAULTS})
    return cfg


def resolve(path):
    return os.path.normpath(path if os.path.isabs(path) else os.path.join(REPO, path))


class Store:
    """queue.json, edited only under an flock on queue.lock (daemon and CLI), replaced atomically."""

    def __init__(self, qdir):
        self.qdir = qdir
        self.path = os.path.join(qdir, "queue.json")
        self.lock = os.path.join(qdir, "queue.lock")

    def read(self):
        return read_json(self.path, None) or dict(version=1, jobs=[])

    @contextmanager
    def edit(self):
        os.makedirs(self.qdir, exist_ok=True)
        with open(self.lock, "a") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            try:
                data = self.read()
                before = json.dumps(data, sort_keys=True)
                yield data
                if json.dumps(data, sort_keys=True) != before:
                    atomic_write_json(self.path, data)
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)


def find(data, jid):
    for j in data["jobs"]:
        if j["id"] == jid:
            return j
    return None


def active_job(data):
    for j in data["jobs"]:
        if j["state"] in ACTIVE:
            return j
    return None


def event(job, text):
    ev = job.setdefault("events", [])
    ev.append("%s %s" % (now_iso(), text))
    del ev[:-30]


def daemon_pid(qdir):
    """pid of the live daemon for this queue dir, or None (the daemon holds an exclusive flock on heavyq.pid)."""
    path = os.path.join(qdir, "heavyq.pid")
    if not os.path.exists(path):
        return None
    with open(path, "a+") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except OSError:
            f.seek(0)
            txt = f.read().strip()
            return int(txt) if txt.isdigit() else -1
        fcntl.flock(f, fcntl.LOCK_UN)
        return None


# ----------------------------------------------------------------------------------------------------- the daemon
class Daemon:
    def __init__(self, qdir):
        self.qdir = qdir
        self.store = Store(qdir)
        self.logs = os.path.join(qdir, "logs")
        self.yield_path = os.path.join(qdir, "YIELD")
        self.popen = {}           # job id -> Popen of its shim (only for jobs this daemon launched; reaped here)
        self.stop = False
        self.clear_since = None
        self.blockers = []
        self.last_status = 0.0
        self.dirty = True

    def log(self, msg):
        line = "%s %s" % (now_iso(), msg)
        print(line, flush=True)
        with open(os.path.join(self.qdir, "heavyq.log"), "a") as f:
            f.write(line + "\n")

    def rc_path(self, job):
        return os.path.join(self.logs, "%s.rc.json" % job["id"])

    # ---------------------------------------------------------------- lifecycle
    def run(self):
        os.makedirs(self.logs, exist_ok=True)
        self.pidf = open(os.path.join(self.qdir, "heavyq.pid"), "a+")
        for _ in range(10):
            try:
                fcntl.flock(self.pidf, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                time.sleep(0.2)
        else:
            self.pidf.seek(0)
            print("heavyq: a daemon already runs for %s (pid %s); not starting a second one" % (
                os.path.relpath(self.qdir, REPO), self.pidf.read().strip() or "?"), file=sys.stderr)
            sys.exit(3)
        self.pidf.seek(0)
        self.pidf.truncate()
        self.pidf.write(str(os.getpid()))
        self.pidf.flush()
        signal.signal(signal.SIGTERM, self._on_stop)
        signal.signal(signal.SIGINT, self._on_stop)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        cfg = load_config(self.qdir)
        self.log("daemon start pid %d, queue dir %s" % (os.getpid(), os.path.relpath(self.qdir, REPO)))
        with self.store.edit() as data:
            self.adopt(data, cfg)
        while not self.stop:
            cfg = load_config(self.qdir)
            try:
                self.tick(cfg)
            except Exception:
                self.log("tick error (daemon keeps running):\n" + traceback.format_exc())
            t_end = time.time() + float(cfg["poll_s"])
            while not self.stop and time.time() < t_end:
                time.sleep(min(0.25, max(0.0, t_end - time.time())))
        self.log("daemon stop (a running job is left running; the next daemon adopts it)")
        try:
            data = self.store.read()
            self.write_status(data, snapshot(cfg, (active_job(data) or {}).get("pgid")), cfg, stopped=True)
        except Exception:
            pass

    def _on_stop(self, signum, frame):
        self.stop = True

    def adopt(self, data, cfg):
        for job in data["jobs"]:
            if job["state"] not in ACTIVE:
                continue
            if group_alive(job["pgid"]):
                info = proc_info(job["pid"])
                if info is None or job.get("start_abs") is None or info[1] == job["start_abs"]:
                    self.log("adopted %s job %s (pgid %d)" % (job["state"], job["id"], job["pgid"]))
                    event(job, "adopted by daemon %d" % os.getpid())
                    continue
            self.finish(job, cfg)

    # ---------------------------------------------------------------- one poll
    def tick(self, cfg):
        with self.store.edit() as data:
            job = active_job(data)
            snap = snapshot(cfg, job["pgid"] if job else None)
            if job:
                self.blockers = []
                self.supervise(job, snap, cfg)
            if not active_job(data):
                self.maybe_start(data, snap, cfg)
            if self.dirty or time.time() - self.last_status >= float(cfg["status_s"]):
                self.write_status(data, snap, cfg)

    def signal_job(self, job, sig):
        try:
            os.killpg(job["pgid"], sig)
        except ProcessLookupError:
            pass

    def yield_reasons(self, job, snap, cfg):
        r = []
        if job.get("hold"):
            r.append("pause requested")
        if os.path.exists(self.yield_path):
            r.append("YIELD file present")
        if snap["free_inactive_gb"] < cfg["floor_gb"]:
            r.append("free+inactive %.1f GB < floor %.1f GB" % (snap["free_inactive_gb"], cfg["floor_gb"]))
        growth = snap["swap_used_gb"] - job["swap0_gb"]
        if growth > cfg["swap_grow_gb"]:
            r.append("swap growth %.2f GB > %.1f GB since the run started" % (growth, cfg["swap_grow_gb"]))
        if snap["other_big"]:
            r.append("other process footprint > %.0f GB: %s" % (cfg["other_proc_gb"], ", ".join(
                "%d %s %.1f GB" % (p["pid"], p["cmd"][:40], p["footprint_gb"]) for p in snap["other_big"][:3])))
        if snap["external_heavy"]:
            r.append("known heavy run live: %s" % ", ".join("%d %s" % (p["pid"], p["cmd"][:40]) for p in snap["external_heavy"][:3]))
        if snap["disk_free_gb"] < cfg["disk_min_gb"]:
            r.append("disk free %.1f GB < %.0f GB" % (snap["disk_free_gb"], cfg["disk_min_gb"]))
        return r

    def supervise(self, job, snap, cfg):
        p = self.popen.get(job["id"])
        if p is not None and p.poll() is not None:
            self.popen.pop(job["id"], None)          # reap our shim so the group can empty
        if not group_alive(job["pgid"]):
            self.finish(job, cfg)
            return
        now = time.time()
        fp = snap["job_footprint_gb"]
        job["footprint_gb"] = round(fp, 3)
        job["peak_gb"] = round(max(job.get("peak_gb", 0.0), fp), 3)
        growth = snap["swap_used_gb"] - job["swap0_gb"]
        kill = None
        if fp > cfg["hard_abort_gb"]:
            kill = ("hard_abort", "footprint %.2f GB > hard limit %.1f GB" % (fp, cfg["hard_abort_gb"]))
        elif growth > cfg["swap_kill_gb"]:
            kill = ("swap_kill", "swap growth %.2f GB > %.1f GB" % (growth, cfg["swap_kill_gb"]))
        elif snap["disk_free_gb"] < cfg["disk_kill_gb"]:
            kill = ("disk_kill", "disk free %.1f GB < %.1f GB" % (snap["disk_free_gb"], cfg["disk_kill_gb"]))
        if kill and not job.get("kill_kind"):
            self.signal_job(job, signal.SIGKILL)
            job["kill_kind"], job["kill_reason"] = kill
            self.log("SIGKILL %s: %s" % (job["id"], kill[1]))
            event(job, "SIGKILL: " + kill[1])
            self.dirty = True
            return
        if job["state"] == "running":
            reasons = self.yield_reasons(job, snap, cfg)
            if reasons:
                if any(x.startswith(("free+inactive", "swap growth")) for x in reasons) and job["peak_gb"] > job["est_gb"]:
                    job["est_gb_learned"] = round(1.1 * job["peak_gb"], 2)   # the job itself was the consumer: start it with room next time
                self.signal_job(job, signal.SIGTERM)
                job.update(state="yielding", yield_sent_t=now, yield_sent_at=now_iso(now), yield_reason="; ".join(reasons))
                self.log("yield %s (SIGTERM to pgid %d): %s" % (job["id"], job["pgid"], job["yield_reason"]))
                event(job, "SIGTERM: " + job["yield_reason"])
                self.dirty = True
        elif job["state"] == "yielding" and not job.get("kill_kind"):
            grace = float(job.get("grace_s") or cfg["grace_s"])
            if now - job["yield_sent_t"] > grace:
                self.signal_job(job, signal.SIGKILL)
                job["kill_kind"], job["kill_reason"] = "grace", "no exit %.0f s after SIGTERM" % grace
                self.log("SIGKILL %s: %s" % (job["id"], job["kill_reason"]))
                event(job, "SIGKILL: " + job["kill_reason"])
                self.dirty = True

    def finish(self, job, cfg):
        """The job's process group is gone: decide done / paused / failed."""
        now = time.time()
        rcinfo = read_json(self.rc_path(job))
        rc = rcinfo["rc"] if rcinfo and rcinfo.get("run") == job.get("runs") else None
        rc_txt = "exit %s" % rc if rc is not None else "no exit record (killed or lost)"
        kind = job.get("kill_kind")
        done_file = job.get("done_file")
        done_present = bool(done_file) and os.path.exists(os.path.join(resolve(job["cwd"]), done_file))
        retry = False
        if kind == "hard_abort":
            new, why = "failed", "hard abort: %s" % job["kill_reason"]
        elif rc == 0 and done_present:
            new, why = "done", "exit 0, done_file present"
        elif job["state"] == "yielding":
            new, why = "paused", "yielded (%s); %s" % (job.get("yield_reason"), rc_txt)
            job["yields"] = job.get("yields", 0) + 1
            if kind:
                job["kills"] = job.get("kills", 0) + 1
                why += "; " + job["kill_reason"]
            elif rc not in (0, YIELD_EXIT):
                why += " (contract: expected exit %d after SIGTERM)" % YIELD_EXIT
        elif kind:
            new, why, retry = "paused", "emergency kill: %s" % job["kill_reason"], True
        elif rc == 0:
            new, why = ("done", "exit 0") if not done_file else ("failed", "exit 0 but done_file %s missing" % done_file)
        elif rc == YIELD_EXIT:
            new, why = "paused", "the job yielded on its own (exit %d)" % YIELD_EXIT
        else:
            new, why, retry = "paused", ("crashed, " if rc is not None else "") + rc_txt, True
        if retry:
            left = job.get("retries_left", cfg["max_retries"])
            if left > 0:
                job["retries_left"] = left - 1
                why += "; restart with resume_cmd (%d retries left)" % (left - 1)
            else:
                new, why = "failed", why + "; no retries left"
        if job.get("started_t"):
            job["runtime_s"] = round(job.get("runtime_s", 0.0) + now - job["started_t"], 1)
        job["last_exit"] = dict(run=job.get("runs"), rc=rc, at=now_iso(now), why=why)
        job["state"] = new
        for k in ("pid", "pgid", "start_abs", "started_t", "swap0_gb", "kill_kind", "kill_reason", "yield_sent_t",
                  "footprint_gb"):
            job.pop(k, None)
        if new == "done":
            job["done_at"] = now_iso(now)
        self.popen.pop(job["id"], None)
        self.clear_since = None
        self.dirty = True
        self.log("%s -> %s: %s" % (job["id"], new, why))
        event(job, "%s: %s" % (new, why))

    def maybe_start(self, data, snap, cfg):
        cands = [(i, j) for i, j in enumerate(data["jobs"]) if j["state"] in ("queued", "paused") and not j.get("hold")]
        if not cands:
            self.blockers, self.clear_since = ["no runnable job"], None
            return
        _, job = min(cands, key=lambda t: (-t[1].get("priority", 0), t[0]))
        need = max(job["est_gb"], job.get("est_gb_learned", 0.0)) + cfg["headroom_gb"]
        b = []
        if os.path.exists(self.yield_path):
            b.append("YIELD file present")
        if snap["external_heavy"]:
            b.append("known heavy run live: " + ", ".join("%d %s" % (p["pid"], p["cmd"][:40]) for p in snap["external_heavy"][:3]))
        if snap["other_big"]:
            b.append("other process footprint > %.0f GB: %s" % (cfg["other_proc_gb"], ", ".join(
                "%d %s %.1f GB" % (p["pid"], p["cmd"][:40], p["footprint_gb"]) for p in snap["other_big"][:3])))
        if snap["free_inactive_gb"] < need:
            b.append("free+inactive %.1f GB < %.1f GB (est %.1f + headroom %.1f) for %s" % (
                snap["free_inactive_gb"], need, need - cfg["headroom_gb"], cfg["headroom_gb"], job["id"]))
        if snap["free_inactive_gb"] < cfg["floor_gb"]:   # never start into a yield (only bites if floor_gb > est + headroom)
            b.append("free+inactive %.1f GB < floor %.1f GB" % (snap["free_inactive_gb"], cfg["floor_gb"]))
        if snap["disk_free_gb"] < cfg["disk_min_gb"]:
            b.append("disk free %.1f GB < %.0f GB" % (snap["disk_free_gb"], cfg["disk_min_gb"]))
        if b:
            if b != self.blockers:
                self.dirty = True
            self.blockers, self.clear_since = b, None
            return
        now = time.time()
        if self.clear_since is None:
            self.clear_since = now
        if now - self.clear_since < float(cfg["clear_s"]):
            self.blockers = ["gates clear for %.0f of %s s (next: %s)" % (now - self.clear_since, cfg["clear_s"], job["id"])]
            return
        self.launch(job, snap, cfg)

    def launch(self, job, snap, cfg):
        resume = job.get("runs", 0) > 0
        cmd = job["resume_cmd"] if resume else job["cmd"]
        run = job.get("runs", 0) + 1
        threads = str(job.get("threads") or cfg["default_threads"])
        env = dict(os.environ)
        env.update({k: threads for k in THREAD_VARS})
        env.update(job.get("env") or {})
        env.update(HEAVYQ_JOB_ID=job["id"], HEAVYQ_RUN=str(run), HEAVYQ_RESUME="1" if resume else "0",
                   HEAVYQ_YIELD_EXIT=str(YIELD_EXIT))
        os.makedirs(self.logs, exist_ok=True)
        rcp = self.rc_path(job)
        if os.path.exists(rcp):
            os.remove(rcp)
        argv = ["nohup", "nice", "-n", str(cfg["nice"]), sys.executable, ME, "_shim", rcp, str(run), cmd]
        try:
            with open(os.path.join(self.logs, "%s.log" % job["id"]), "a") as lf:
                lf.write("\n=== heavyq %s run %d at %s (threads %s): %s\n" % ("RESUME" if resume else "START", run, now_iso(),
                                                                             threads, cmd))
                lf.flush()
                p = subprocess.Popen(argv, cwd=resolve(job["cwd"]), stdin=subprocess.DEVNULL, stdout=lf,
                                     stderr=subprocess.STDOUT, env=env, start_new_session=True, close_fds=True)
        except OSError as e:
            job["state"] = "failed"
            job["last_exit"] = dict(run=run, rc=None, at=now_iso(), why="launch failed: %s" % e)
            self.log("%s -> failed: launch failed: %s" % (job["id"], e))
            self.dirty = True
            return
        self.popen[job["id"]] = p
        info = proc_info(p.pid)
        now = time.time()
        job.update(state="running", pid=p.pid, pgid=p.pid, start_abs=info[1] if info else None, started_t=now,
                   started_at=now_iso(now), swap0_gb=round(snap["swap_used_gb"], 3), runs=run, footprint_gb=0.0)
        job.pop("yield_reason", None)
        job.pop("yield_sent_at", None)
        self.blockers = []
        self.dirty = True
        what = "resume" if resume else "start"
        self.log("%s %s run %d (pgid %d, need %.1f GB, free+inactive %.1f GB): %s" % (
            what, job["id"], run, p.pid, max(job["est_gb"], job.get("est_gb_learned", 0.0)), snap["free_inactive_gb"], cmd))
        event(job, "%s run %d pgid %d" % (what, run, p.pid))

    def write_status(self, data, snap, cfg, stopped=False):
        job = active_job(data)
        running = None
        if job:
            running = dict(id=job["id"], state=job["state"], pid=job["pid"], run=job.get("runs"),
                           footprint_gb=round(snap["job_footprint_gb"], 3), peak_gb=job.get("peak_gb"),
                           est_gb=job["est_gb"], est_gb_learned=job.get("est_gb_learned"), nproc=snap["job_nproc"],
                           started_at=job.get("started_at"), run_s=round(time.time() - job.get("started_t", time.time()), 1),
                           swap_growth_gb=round(snap["swap_used_gb"] - job.get("swap0_gb", snap["swap_used_gb"]), 3),
                           yield_reason=job.get("yield_reason"), yield_sent_at=job.get("yield_sent_at"))
        st = dict(
            updated=now_iso(), daemon=dict(pid=os.getpid(), state="stopped" if stopped else "running"),
            machine={k: round(snap[k], 2) for k in ("free_inactive_gb", "free_gb", "inactive_gb", "swap_used_gb",
                                                       "swap_total_gb", "disk_free_gb")},
            running=running, next_start_blockers=[] if job else self.blockers,
            yield_file=os.path.exists(self.yield_path), other_big=snap["other_big"], external_heavy=snap["external_heavy"],
            queue=[summary(j) for j in data["jobs"]], config=cfg)
        atomic_write_json(os.path.join(self.qdir, "status.json"), st)
        self.last_status = time.time()
        self.dirty = False


def summary(j):
    return dict(id=j["id"], state=j["state"], hold=bool(j.get("hold")), priority=j.get("priority", 0), est_gb=j["est_gb"],
                est_gb_learned=j.get("est_gb_learned"), runs=j.get("runs", 0), yields=j.get("yields", 0),
                peak_gb=j.get("peak_gb"), runtime_s=j.get("runtime_s"), last_exit=j.get("last_exit"))


# ----------------------------------------------------------------------------------------------------- the shim
def shim(rc_path, run, cmd):
    """Runs inside the job's process group (leader).  Ignores SIGTERM/SIGINT itself (the handler is not inherited, so the job
    gets the default action unless it installs its own), waits for the job and for anything else left in the group, then
    records the exit code so a daemon that did not launch the job (restart, adoption) can still read it."""
    got = dict(term=0)

    def on_sig(signum, frame):
        got["term"] += 1
    signal.signal(signal.SIGTERM, on_sig)
    signal.signal(signal.SIGINT, on_sig)
    child = subprocess.Popen(["/bin/bash", "-c", cmd])
    rc = child.wait()
    me, pg = os.getpid(), os.getpgid(0)
    t0 = time.time()
    while True:   # a wrapper may exit before the programs it started (they got the same SIGTERM): wait for the group
        others = [pid for pid, pgid, _ in ps_rows(exclude=(me,)) if pgid == pg]
        if not others:
            break
        if time.time() - t0 < 2:
            print("=== heavyq shim: waiting for %d process(es) left in the job's group" % len(others), flush=True)
        time.sleep(1)
    atomic_write_json(rc_path, dict(run=int(run), rc=rc, term_signals_seen=got["term"], ended=now_iso()))
    print("=== heavyq run %s exit %s at %s" % (run, rc, now_iso()), flush=True)
    return 0


# ----------------------------------------------------------------------------------------------------- CLI
def cmd_status(qdir, as_json):
    st = read_json(os.path.join(qdir, "status.json"))
    data = Store(qdir).read()
    pid = daemon_pid(qdir)
    if as_json:
        print(json.dumps(dict(daemon_pid=pid, status=st, queue=data), indent=1))
        return 0
    if pid:
        age = time.time() - os.path.getmtime(os.path.join(qdir, "status.json")) if st else None
        print("daemon: running (pid %s)%s" % (pid, ", status %.0f s old" % age if age is not None else ""))
    else:
        print("daemon: NOT running   (start: nohup python3 compute_queue/heavyq.py daemon >/dev/null 2>&1 &)")
    if st:
        m = st["machine"]
        print("machine: free+inactive %.1f GB | swap used %.1f of %.1f GB | disk free %.0f GB | YIELD file %s" % (
            m["free_inactive_gb"], m["swap_used_gb"], m["swap_total_gb"], m["disk_free_gb"], "PRESENT" if st["yield_file"] else "absent"))
        r = st.get("running")
        if r:
            print("running: %s [%s] pid %s run %s, footprint %.2f GB (peak %s, est %s), %.0f s, swap growth %.2f GB%s" % (
                r["id"], r["state"], r["pid"], r["run"], r["footprint_gb"], r["peak_gb"], r["est_gb"], r["run_s"],
                r["swap_growth_gb"], ("; yielding: " + r["yield_reason"]) if r.get("yield_reason") else ""))
        elif st.get("next_start_blockers"):
            print("next start: " + " | ".join(st["next_start_blockers"]))
        for p in st.get("other_big", []):
            print("  other process > limit: %(pid)s %(cmd)s %(footprint_gb)s GB" % p)
    jobs = data["jobs"]
    if not jobs:
        print("queue: empty")
        return 0
    print("queue (%d):" % len(jobs))
    print("  %-18s %-9s %-4s %4s %7s %5s %6s  %s" % ("id", "state", "hold", "prio", "est_gb", "runs", "yields", "last exit"))
    for j in jobs:
        le = j.get("last_exit") or {}
        print("  %-18s %-9s %-4s %4s %7.1f %5d %6d  %s" % (j["id"], j["state"], "yes" if j.get("hold") else "", j.get("priority", 0),
                                                          j["est_gb"], j.get("runs", 0), j.get("yields", 0), le.get("why", "")[:70]))
    return 0


def cmd_add(qdir, a):
    cfg = load_config(qdir)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", a.id):
        sys.exit("heavyq add: id must be 1-64 of [A-Za-z0-9_.-]")
    if not (0 < a.est_gb < cfg["hard_abort_gb"]):
        sys.exit("heavyq add: est_gb must be > 0 and below the hard abort (%.0f GB)" % cfg["hard_abort_gb"])
    cwd = resolve(a.cwd)
    if not os.path.isdir(cwd):
        sys.exit("heavyq add: cwd %s does not exist" % a.cwd)
    rel = os.path.relpath(cwd, REPO)
    env = {}
    for kv in a.env or []:
        k, sep, v = kv.partition("=")
        if not sep:
            sys.exit("heavyq add: --env wants K=V")
        env[k] = v
    job = dict(id=a.id, cmd=a.cmd, resume_cmd=a.resume_cmd, cwd=rel if not rel.startswith("..") else cwd, est_gb=float(a.est_gb),
               priority=int(a.priority), threads=int(a.threads or cfg["default_threads"]), state="queued", hold=bool(a.hold),
               retries_left=int(a.retries if a.retries is not None else cfg["max_retries"]), runs=0, yields=0,
               added_at=now_iso())
    for k, v in (("done_file", a.done_file), ("grace_s", a.grace), ("note", a.note)):
        if v:
            job[k] = v
    if env:
        job["env"] = env
    with Store(qdir).edit() as data:
        if find(data, a.id):
            sys.exit("heavyq add: id %s already in the queue (remove it first)" % a.id)
        event(job, "added")
        data["jobs"].append(job)
    print("added %s (est %.1f GB, priority %d, threads %d%s)" % (a.id, job["est_gb"], job["priority"], job["threads"],
                                                               ", HELD" if a.hold else ""))
    if not daemon_pid(qdir):
        print("note: the daemon is not running; nothing starts until it is")
    return 0


def cmd_pause(qdir, jid):
    with Store(qdir).edit() as data:
        j = find(data, jid)
        if not j:
            sys.exit("heavyq pause: no job %s" % jid)
        if j["state"] in ("done", "failed"):
            sys.exit("heavyq pause: %s is %s" % (jid, j["state"]))
        j["hold"] = True
        event(j, "pause requested (hold)")
        st = j["state"]
    if st in ACTIVE:
        print("%s: hold set; the daemon sends SIGTERM at its next poll and the job checkpoints (resume with: heavyq.py resume %s)" % (jid, jid))
        if not daemon_pid(qdir):
            print("warning: the daemon is not running, so nothing will signal the job until it is started")
    else:
        print("%s: held (%s); it will not start until: heavyq.py resume %s" % (jid, st, jid))
    return 0


def cmd_resume(qdir, jid):
    cfg = load_config(qdir)
    with Store(qdir).edit() as data:
        j = find(data, jid)
        if not j:
            sys.exit("heavyq resume: no job %s" % jid)
        j["hold"] = False
        msg = "hold cleared"
        if j["state"] == "failed":
            j["state"] = "paused" if j.get("runs", 0) > 0 else "queued"
            j["retries_left"] = cfg["max_retries"]
            msg = "re-queued from failed as %s" % j["state"]
        event(j, "resume: " + msg)
        st = j["state"]
    print("%s: %s; state %s%s" % (jid, msg, st, " (runs resume_cmd when the gates allow)" if st == "paused" else ""))
    return 0


def cmd_remove(qdir, jid):
    with Store(qdir).edit() as data:
        j = find(data, jid)
        if not j:
            sys.exit("heavyq remove: no job %s" % jid)
        if j["state"] in ACTIVE:
            sys.exit("heavyq remove: %s is %s; `heavyq.py pause %s` first, remove it once it is paused" % (jid, j["state"], jid))
        data["jobs"].remove(j)
    print("removed %s (its log and checkpoints are left in place)" % jid)
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["_shim"]:
        return shim(*argv[1:4])
    ap = argparse.ArgumentParser(description="preemptible heavy-compute queue (see the module docstring and JOB_CONTRACT.md)")
    ap.add_argument("--qdir", default=None, help="queue directory (default: this folder, or $HEAVYQ_DIR)")
    sub = ap.add_subparsers(dest="action", required=True)
    sub.add_parser("daemon")
    s = sub.add_parser("status")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("add")
    s.add_argument("--id", required=True)
    s.add_argument("--cmd", required=True, help="first-run command (bash -c, in --cwd)")
    s.add_argument("--resume-cmd", required=True, help="command for every later run (continues from the checkpoint)")
    s.add_argument("--est-gb", type=float, required=True, help="peak footprint in GB (not RSS)")
    s.add_argument("--cwd", default=".", help="working directory, relative to the repo root (default: the repo root)")
    s.add_argument("--priority", type=int, default=0, help="higher runs first")
    s.add_argument("--threads", type=int, default=None)
    s.add_argument("--done-file", default=None, help="path (relative to cwd) that exists only when the job is complete")
    s.add_argument("--retries", type=int, default=None)
    s.add_argument("--grace", type=float, default=None, help="seconds from SIGTERM to SIGKILL for this job")
    s.add_argument("--env", action="append", help="K=V for the job's environment (repeatable)")
    s.add_argument("--hold", action="store_true", help="add held: it does not start until `resume ID`")
    s.add_argument("--note", default=None)
    for name in ("pause", "resume", "remove"):
        sub.add_parser(name).add_argument("id")
    a = ap.parse_args(argv)
    qdir = os.path.abspath(a.qdir) if a.qdir else qdir_default()
    os.makedirs(qdir, exist_ok=True)
    if a.action == "daemon":
        Daemon(qdir).run()
        return 0
    if a.action == "status":
        return cmd_status(qdir, a.json)
    if a.action == "add":
        return cmd_add(qdir, a)
    return dict(pause=cmd_pause, resume=cmd_resume, remove=cmd_remove)[a.action](qdir, a.id)


if __name__ == "__main__":
    sys.exit(main())

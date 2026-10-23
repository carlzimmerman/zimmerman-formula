#!/usr/bin/env python3
"""Full-cycle test of heavyq with the dummy job (compute_queue/test/dummy_job.py, 0.55 GB footprint, one thread).

It uses a throwaway queue dir (compute_queue/test/_work/q, gitignored), never compute_queue/queue.json, and runs no science.
  0  reference: the dummy run uninterrupted
  1  daemon start; a second daemon on the same queue dir is refused (pidfile lock)
  2  add the job; it starts (own process group, nice 5, footprint read from libproc)
  3  forced yield: touch YIELD -> SIGTERM -> checkpoint -> exit 75 -> paused; it stays paused while YIELD exists
  4  rm YIELD -> automatic resume with resume_cmd from the checkpoint step
  5  `remove` of a running job is refused; `pause` -> checkpoint -> held (stays paused with the gates clear); `resume` -> resumes
  6  daemon restart while the job runs: the job keeps running and the new daemon adopts it
  7  completion: result identical (acc chain and buffer SHA-256) to the uninterrupted reference; `remove` the finished job
  8  a job that ignores SIGTERM is SIGKILLed after its grace and paused; the memory floor (set through a live config.json
     edit) blocks the start and, when violated during a run, yields the job
Writes test_cycle.out (this transcript) and test_cycle_result.json next to this script.
  python3 compute_queue/test/test_cycle.py
"""
import json, os, shutil, signal, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CQ = os.path.dirname(HERE)
REPO = os.path.dirname(CQ)
HQ = os.path.join(CQ, "heavyq.py")
PY = sys.executable
WORK = os.path.join(HERE, "_work")
QD = os.path.join(WORK, "q")
MB, STEPS, SLEEP = 512, 60, 0.2
JOB = "dummy"
REL = lambda p: os.path.relpath(p, REPO)
DUMMY_ARGS = "--mb %d --steps %d --step-sleep %s" % (MB, STEPS, SLEEP)
CMD = "python3 compute_queue/test/dummy_job.py --work %s %s" % (REL(os.path.join(WORK, "queued")), DUMMY_ARGS)

T0 = time.time()
OUT = []
CHECKS = []
FACTS = {}


def say(msg):
    line = "[%6.1f s] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    OUT.append(line)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail))
    say("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        raise SystemExit("test failed at: " + name)


def rj(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def job(jid=JOB):
    for j in (rj(os.path.join(QD, "queue.json"), {}) or {}).get("jobs", []):
        if j["id"] == jid:
            return j
    return None


def state(jid=JOB):
    j = job(jid)
    return j["state"] if j else None


def set_config(**extra):
    cfg = dict(poll_s=0.5, status_s=1, clear_s=3, grace_s=60)   # test timings only; memory/disk/footprint rules keep defaults
    cfg.update(extra)
    tmp = os.path.join(QD, "config.json.tmp.test")
    with open(tmp, "w") as f:
        json.dump(cfg, f)
    os.replace(tmp, os.path.join(QD, "config.json"))


def step():
    return (rj(os.path.join(WORK, "queued", "progress.json"), {}) or {}).get("step", 0)


def hq(*args):
    return subprocess.run([PY, HQ, "--qdir", QD] + list(args), capture_output=True, text=True, cwd=REPO)


def wait(pred, timeout, what):
    t = time.time()
    while time.time() - t < timeout:
        v = pred()
        if v:
            return v
        time.sleep(0.1)
    check(what, False, "timed out after %.0f s (state %s, step %s)" % (timeout, state(), step()))


def group_members(pgid):
    out = subprocess.run(["ps", "-axo", "pid=,pgid=,nice=,command="], capture_output=True, text=True).stdout
    rows = []
    for line in out.splitlines():
        p = line.split(None, 3)
        if len(p) >= 3 and int(p[1]) == pgid:
            rows.append((int(p[0]), int(p[2]), p[3] if len(p) > 3 else ""))
    return rows


def start_daemon(tag):
    f = open(os.path.join(WORK, "daemon_%s.stdout" % tag), "w")
    p = subprocess.Popen([PY, HQ, "--qdir", QD, "daemon"], cwd=REPO, stdout=f, stderr=subprocess.STDOUT)
    wait(lambda: os.path.exists(os.path.join(QD, "status.json")) and rj(os.path.join(QD, "status.json"), {}).get("daemon", {}).get("pid") == p.pid,
         20, "daemon %s up" % tag)
    return p


def job_log():
    try:
        with open(os.path.join(QD, "logs", JOB + ".log")) as f:
            return f.read()
    except FileNotFoundError:
        return ""


def main():
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(QD)
    set_config()
    say("heavyq full-cycle test; throwaway queue dir %s; dummy %s; config: poll 0.5 s, status 1 s, clear 3 s, grace 60 s"
        % (REL(QD), DUMMY_ARGS))

    # 0 reference
    t = time.time()
    r = subprocess.run([PY, os.path.join(HERE, "dummy_job.py"), "--work", os.path.join(WORK, "ref")] + DUMMY_ARGS.split(),
                       capture_output=True, text=True)
    ref = rj(os.path.join(WORK, "ref", "result.json"))
    check("0 reference run (uninterrupted) completes", r.returncode == 0 and ref is not None,
          "%.1f s, acc %s..., buf_sha256 %s..." % (time.time() - t, ref["acc"][:16], ref["buf_sha256"][:16]))

    d1 = d2 = None
    pgids = []
    try:
        # 1 daemon + lock
        d1 = start_daemon("1")
        r = hq("daemon")
        check("1 second daemon on the same queue dir refused", r.returncode == 3 and "already runs" in r.stderr, r.stderr.strip()[:100])
        st = rj(os.path.join(QD, "status.json"))
        m = st["machine"]
        FACTS["machine_at_start"] = m
        say("machine: free+inactive %.1f GB, swap used %.2f GB, disk free %.0f GB; other processes > 4 GB: %d; known heavy runs: %d"
            % (m["free_inactive_gb"], m["swap_used_gb"], m["disk_free_gb"], len(st["other_big"]), len(st["external_heavy"])))

        # 2 add + start
        r = hq("add", "--id", JOB, "--cmd", CMD, "--resume-cmd", CMD + " --resume", "--est-gb", "1.0", "--priority", "5",
               "--threads", "1", "--done-file", REL(os.path.join(WORK, "queued", "result.json")), "--note", "heavyq cycle test")
        check("2 add", r.returncode == 0, r.stdout.strip())
        wait(lambda: state() == "running", 30, "2 job started")
        j = job()
        pgids.append(j["pgid"])
        wait(lambda: step() >= 8, 60, "2 job progressing")
        mem = group_members(j["pgid"])
        dpg = os.getpgid(d1.pid)
        check("2 job in its own process group at nice 5", j["pgid"] != dpg and mem and all(n == 5 for _, n, _ in mem),
              "pgid %d (daemon pgid %d); members %s" % (j["pgid"], dpg, [(pid, n, c.split()[0].split('/')[-1]) for pid, n, c in mem]))
        time.sleep(1.2)
        st = rj(os.path.join(QD, "status.json"))
        fp = st["running"]["footprint_gb"]
        FACTS["footprint_gb_running"] = fp
        check("2 footprint read (libproc phys_footprint over the group) and < 2 GB", 0.4 < fp < 2.0, "%.3f GB at step %d" % (fp, step()))

        # 3 forced yield via YIELD
        open(os.path.join(QD, "YIELD"), "w").close()
        ty = time.time()
        wait(lambda: state() == "paused", 60, "3 yield -> paused")
        j = job()
        lat = time.time() - ty
        ck = int(job_log().split("checkpoint written at step ")[-1].split(";")[0])
        FACTS["yield1"] = dict(latency_s=round(lat, 1), checkpoint_step=ck, rc=j["last_exit"]["rc"], why=j["last_exit"]["why"])
        check("3 YIELD file -> SIGTERM -> checkpoint -> exit 75 -> paused",
              j["last_exit"]["rc"] == 75 and os.path.exists(os.path.join(WORK, "queued", "ckpt.bin")),
              "%.1f s; checkpoint at step %d; %s" % (lat, ck, j["last_exit"]["why"]))
        check("3 job process group gone after the yield", not group_members(pgids[-1]), "pgid %d" % pgids[-1])
        time.sleep(5)
        st = rj(os.path.join(QD, "status.json"))
        check("3 stays paused while YIELD exists", state() == "paused" and step() == ck and "YIELD file present" in st["next_start_blockers"],
              "blockers %s" % st["next_start_blockers"])

        # 4 automatic resume
        os.remove(os.path.join(QD, "YIELD"))
        tr = time.time()
        wait(lambda: state() == "running" and job()["runs"] == 2, 60, "4 automatic resume")
        pgids.append(job()["pgid"])
        wait(lambda: "resumed from checkpoint at step %d" % ck in job_log(), 30, "4 resumed from the checkpoint step")
        check("4 YIELD removed -> resume_cmd from the checkpoint", True,
              "%.1f s after rm (clear_s 3); log: 'resumed from checkpoint at step %d'" % (time.time() - tr, ck))

        # 5 remove refused while running; pause / resume CLI
        wait(lambda: step() >= ck + 8, 60, "5 progressing after resume")
        r = hq("remove", JOB)
        check("5 remove of a running job refused", r.returncode != 0 and state() == "running", r.stderr.strip()[:110])
        r = hq("pause", JOB)
        wait(lambda: state() == "paused", 60, "5 pause -> paused")
        j = job()
        ck2 = int(job_log().split("checkpoint written at step ")[-1].split(";")[0])
        check("5 `pause` -> checkpoint -> exit 75 -> paused (held)", j["last_exit"]["rc"] == 75 and j["hold"],
              "checkpoint at step %d; %s" % (ck2, j["last_exit"]["why"]))
        time.sleep(5)
        check("5 held job does not restart with the gates clear", state() == "paused" and step() == ck2,
              "blockers %s" % rj(os.path.join(QD, "status.json"))["next_start_blockers"])
        r = hq("resume", JOB)
        wait(lambda: state() == "running" and job()["runs"] == 3, 60, "5 resume -> running")
        pgids.append(job()["pgid"])
        wait(lambda: "resumed from checkpoint at step %d" % ck2 in job_log(), 30, "5 resumed from the second checkpoint")
        check("5 `resume` -> resume_cmd from the checkpoint", True, r.stdout.strip())

        # 6 daemon restart with the job running
        s0 = step()
        d1.send_signal(signal.SIGTERM)
        d1.wait(20)
        alive = bool(group_members(pgids[-1]))
        time.sleep(1.5)
        check("6 daemon stopped; the job keeps running without it", alive and step() > s0 and state() == "running",
              "steps %d -> %d while no daemon ran" % (s0, step()))
        d2 = start_daemon("2")
        wait(lambda: any("adopted by daemon %d" % d2.pid in e for e in job()["events"]), 20, "6 adopted")
        st = rj(os.path.join(QD, "status.json"))
        check("6 new daemon adopts the running job", st["running"] and st["running"]["pid"] == pgids[-1],
              "running pid %s, footprint %.3f GB" % (st["running"]["pid"], st["running"]["footprint_gb"]))

        # 7 completion and identity
        wait(lambda: state() == "done", 120, "7 completion")
        j = job()
        res = rj(os.path.join(WORK, "queued", "result.json"))
        FACTS["final_job"] = dict(runs=j["runs"], yields=j["yields"], peak_gb=j["peak_gb"], runtime_s=j.get("runtime_s"),
                                  last_exit=j["last_exit"])
        check("7 job done (exit 0, done_file present) after 3 runs and 2 yields",
              j["runs"] == 3 and j["yields"] == 2 and j["last_exit"]["rc"] == 0, j["last_exit"]["why"])
        same = res == ref
        FACTS["result_queued"], FACTS["result_reference"] = res, ref
        check("7 final result identical to the uninterrupted run", same,
              "acc %s, buf_sha256 %s (both runs)" % (res["acc"], res["buf_sha256"]) if same else "%s vs %s" % (res, ref))
        check("7 no process left in any of the job's groups", not any(group_members(g) for g in pgids), "pgids %s" % pgids)
        r = hq("remove", JOB)
        check("7 remove the finished job", r.returncode == 0 and job() is None, r.stdout.strip())

        # 8 a job that breaks the contract (ignores SIGTERM): grace kill; and the memory floor rule through a live config edit
        SJ = "stubborn"
        scmd = "python3 compute_queue/test/dummy_job.py --work %s --mb 64 --steps 100000 --step-sleep 0.05 --ignore-term" % (
            REL(os.path.join(WORK, "stubborn")))
        r = hq("add", "--id", SJ, "--cmd", scmd, "--resume-cmd", scmd + " --resume", "--est-gb", "0.2", "--threads", "1",
               "--grace", "3")
        wait(lambda: state(SJ) == "running", 30, "8 stubborn job started")
        pgids.append(job(SJ)["pgid"])
        time.sleep(1)
        open(os.path.join(QD, "YIELD"), "w").close()
        ty = time.time()
        wait(lambda: state(SJ) == "paused", 30, "8 grace kill -> paused")
        j = job(SJ)
        check("8 job ignoring SIGTERM is SIGKILLed after its grace (3 s) and paused",
              j["kills"] == 1 and j["last_exit"]["rc"] is None and "no exit 3 s after SIGTERM" in j["last_exit"]["why"],
              "%.1f s; %s" % (time.time() - ty, j["last_exit"]["why"]))
        check("8 its process group is gone", not group_members(pgids[-1]), "pgid %d" % pgids[-1])
        set_config(floor_gb=1000)
        os.remove(os.path.join(QD, "YIELD"))
        time.sleep(4)
        bl = rj(os.path.join(QD, "status.json"))["next_start_blockers"]
        check("8 floor rule blocks the start (config.json re-read live)", state(SJ) == "paused" and any("floor 1000" in b for b in bl),
              "blockers %s" % bl)
        set_config()
        wait(lambda: state(SJ) == "running" and job(SJ)["runs"] == 2, 30, "8 resumes once the floor is restored")
        pgids.append(job(SJ)["pgid"])
        time.sleep(1)
        set_config(floor_gb=1000)
        wait(lambda: state(SJ) == "paused", 30, "8 floor yield -> paused")
        j = job(SJ)
        check("8 free+inactive below the floor -> SIGTERM (ignored) -> SIGKILL -> paused",
              j["kills"] == 2 and "< floor 1000.0 GB" in j["last_exit"]["why"], j["last_exit"]["why"])
        hq("pause", SJ)
        r = hq("remove", SJ)
        set_config()
        check("8 held + removed", r.returncode == 0 and job(SJ) is None, r.stdout.strip())
    finally:
        for p in (d1, d2):
            if p and p.poll() is None:
                p.send_signal(signal.SIGTERM)
                p.wait(20)
        for g in pgids:
            try:
                os.killpg(g, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        try:
            with open(os.path.join(QD, "heavyq.log")) as f:
                dlog = f.read().splitlines()
        except FileNotFoundError:
            dlog = []
        say("daemon event log (%s):" % REL(os.path.join(QD, "heavyq.log")))
        for line in dlog:
            OUT.append("    " + line)
            print("    " + line)
        say("job log (%s):" % REL(os.path.join(QD, "logs", JOB + ".log")))
        for line in job_log().splitlines():
            if line.strip():
                OUT.append("    " + line)
                print("    " + line)
        ok = bool(CHECKS) and all(c["ok"] for c in CHECKS)
        say("RESULT: %s (%d/%d checks)" % ("PASS" if ok else "FAIL", sum(c["ok"] for c in CHECKS), len(CHECKS)))
        with open(os.path.join(HERE, "test_cycle.out"), "w") as f:
            f.write("\n".join(OUT) + "\n")
        with open(os.path.join(HERE, "test_cycle_result.json"), "w") as f:
            json.dump(dict(result="PASS" if ok else "FAIL", date=time.strftime("%Y-%m-%d %H:%M"), dummy=DUMMY_ARGS,
                           checks=CHECKS, facts=FACTS), f, indent=1)
            f.write("\n")
        if ok:
            shutil.rmtree(WORK, ignore_errors=True)   # 0.5 GB of buffers/checkpoints; the transcript keeps the evidence
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

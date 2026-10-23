#!/usr/bin/env python3
"""heavyq test job: a deterministic, memory-holding computation that follows compute_queue/JOB_CONTRACT.md.

State: a buffer of --mb MiB filled from SHAKE-256(seed, block index) and a SHA-256 chain value `acc`.
Step s:  d = SHA-256(acc || s || buffer);  acc = d;  the 1 MiB block of the buffer chosen by d is overwritten with SHAKE-256(d).
Result:  result.json with the final acc and SHA-256(buffer) -- any lost, repeated or reordered step changes both.

Contract behaviour:
  SIGTERM / SIGINT -> finish the current step, write the checkpoint atomically (whole state: step, acc, buffer), exit 75.
  --resume         -> result present: exit 0 at once; checkpoint present: continue from it (bit-identical, the checkpoint is
                      the complete state); neither: start fresh.
  outputs          -> written to a temporary file in the same folder, fsynced, then os.replace()d.
  est_gb           -> about --mb MiB + 40 MB (0.55 GB at the default 512).
  python3 dummy_job.py --work DIR [--mb 512] [--steps 60] [--step-sleep 0.2] [--resume]
"""
import argparse, hashlib, json, os, signal, sys, time

MiB = 1 << 20
YIELD_EXIT = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75"))


def atomic_write(path, chunks):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        for c in chunks:
            f.write(c)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--mb", type=int, default=512)
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--step-sleep", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=20261023)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--ignore-term", action="store_true", help="TEST ONLY: break the contract (ignore SIGTERM) to exercise the grace kill")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    ckpt, result, progress = (os.path.join(a.work, n) for n in ("ckpt.bin", "result.json", "progress.json"))
    stop = dict(sig=None)

    def on_signal(signum, frame):
        stop["sig"] = signum
    signal.signal(signal.SIGTERM, signal.SIG_IGN if a.ignore_term else on_signal)
    signal.signal(signal.SIGINT, on_signal)

    if a.resume and os.path.exists(result):
        print("result already present: nothing to do", flush=True)
        return 0
    seed = a.seed.to_bytes(8, "little")
    buf = bytearray(a.mb * MiB)
    mv = memoryview(buf)
    if a.resume and os.path.exists(ckpt):
        with open(ckpt, "rb") as f:
            hdr = json.loads(f.readline())
            assert (hdr["mb"], hdr["seed"], hdr["steps"]) == (a.mb, a.seed, a.steps), "checkpoint is for other parameters"
            assert f.readinto(buf) == len(buf), "short checkpoint"
        assert hashlib.sha256(mv).hexdigest() == hdr["buf_sha256"], "checkpoint body does not match its header"
        step, acc = hdr["step"], bytes.fromhex(hdr["acc"])
        print("resumed from checkpoint at step %d" % step, flush=True)
    else:
        for i in range(a.mb):
            mv[i * MiB:(i + 1) * MiB] = hashlib.shake_256(seed + i.to_bytes(8, "little")).digest(MiB)
        step, acc = 0, hashlib.sha256(seed).digest()
        print("fresh start (%d MiB, %d steps)" % (a.mb, a.steps), flush=True)

    while step < a.steps:
        if stop["sig"] is not None:
            hdr = dict(step=step, acc=acc.hex(), mb=a.mb, seed=a.seed, steps=a.steps, buf_sha256=hashlib.sha256(mv).hexdigest())
            atomic_write(ckpt, [(json.dumps(hdr) + "\n").encode(), mv])
            print("signal %d: checkpoint written at step %d; exit %d" % (stop["sig"], step, YIELD_EXIT), flush=True)
            return YIELD_EXIT
        h = hashlib.sha256(acc)
        h.update(step.to_bytes(8, "little"))
        h.update(mv)
        d = h.digest()
        off = int.from_bytes(d[:8], "little") % a.mb
        mv[off * MiB:(off + 1) * MiB] = hashlib.shake_256(d).digest(MiB)
        acc, step = d, step + 1
        atomic_write(progress, [json.dumps(dict(step=step)).encode()])
        if a.step_sleep:
            time.sleep(a.step_sleep)

    res = dict(steps=a.steps, mb=a.mb, seed=a.seed, acc=acc.hex(), buf_sha256=hashlib.sha256(mv).hexdigest())
    atomic_write(result, [(json.dumps(res, indent=1) + "\n").encode()])
    if os.path.exists(ckpt):
        os.remove(ckpt)
    print("done: acc %s buf_sha256 %s" % (res["acc"][:16], res["buf_sha256"][:16]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

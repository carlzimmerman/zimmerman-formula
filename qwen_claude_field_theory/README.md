# qwen_claude_field_theory — 100 ideas, one per session, overnight

Built 2026-08-17 after the session that produced the AeST no-go. These are the ideas and
reframings that were *not* pursued, written so a local worker can attack them one at a time
without stalling.

## Run it

```bash
export OLLAMA_KEEP_ALIVE=24h
export WORKER_MODEL=qwen3.8:27b-mlx        # optional
bash qwen_claude_field_theory/runloop.sh
```

Stop with `touch qwen_claude_field_theory/STOP`, or Ctrl-C.

The endpoint is **locked to localhost and fails closed** — the loop refuses to start if
`ANTHROPIC_BASE_URL` is not local. It never touches a paid API.

## Why it should not stall

The first autoloop burned itself on open-ended idea generation. This one is different:

- **Fixed list.** 100 concrete ideas, each with a pre-registered PASS/KILL condition. No
  generation step, so nothing to spiral on.
- **Hard 25-minute cap per idea** (`ITER_TIMEOUT`), plus an explicit 20-minute self-imposed
  time box in the protocol. `NOT COMPUTED` is an accepted, ledgered outcome — a graded
  partial beats a hung session.
- **Fresh context per idea.** Each session reads `PROTOCOL.md` and *one* idea spec. It is
  told not to read the other 99.
- **Real data paths, verified to exist**, listed in `PROTOCOL.md`. If a path is missing the
  worker grades `NOT COMPUTED` and moves on instead of hunting.
- **The dispatcher can see its own completions.** `next_idea.py` reads the ledger and skips
  finished ids; verified by simulation that it advances I001 → I003 → I005 as rows land.

## Reserved

**I001, I003, I012 and I037 are excluded from the loop** — Claude is running those four
directly (EFE factorisation, disc corrections to the local law, the RAR's real requirement on
s, and whether the dust is forced irrotational). The dispatcher skips them, so the local
worker will never duplicate that work. Their results will land in the main repo, not here.

## Where the value is

Not evenly spread. If you only get through part of it:

- **Section A (I001–I015)** attacks the live 233× incompatibility. **I001** (does the EFE
  factorise against a density-dependent a₀), **I003** (disc corrections to the local law) and
  **I012** (does the RAR really need s ≥ 0.558 once Υ is refitted) are the three that could
  reopen the framework's relativistic home.
- **I037** — whether the dark sector's dust is *forced* to be irrotational — is the single
  highest-value item in the file. If vorticity is allowed, centrifugal support evades all
  five dust filters at once, because it is not a pressure.
- **I099 and I100** always produce output, so the run ends on something useful whatever
  else happens.

## Layout

```
PROTOCOL.md    the rules + the six framework facts + verified data paths
IDEAS.md       the 100 ideas
next_idea.py   dispatcher -- run this FIRST each session
LEDGER.md      memory; one row per idea
runloop.sh     the overnight loop (fail-closed, local only)
runs/          the worker's scripts and logs
```

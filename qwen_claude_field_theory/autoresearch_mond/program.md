# AUTORESEARCH MOND — Zimmerman theory cooker (persistent, Qwen-proposes / computer-judges)

MISSION: KEEP COOKING. search -> test -> kill -> learn -> mutate -> repeat, with permanent memory,
until all required gates PASS or the remaining grammar is proven closed. Full spec: Carl's 34-section
directive (2026-08-29); immutable law: global_protocol.md (= CRISPY_FRIED_CHICKEN_RECIPE.md copy).

## LAUNCH (manual, token-free — no Claude needed)
    cd qwen_claude_field_theory/autoresearch_mond
    ollama serve &            # if not already running; model 'Qwen-Physics' must be installed
    python3 runner.py 50      # run 50 iterations (omit arg = run until stopped; Ctrl+C = clean stop)
    # env overrides: QWEN_MODEL, OLLAMA_URL, QWEN_CTX, AR_MAX_GATES (default 5 = G1..G5), AR_CHECKPOINT
Results: database/*.jsonl (append-only), reports/checkpoint_*.md, survivors/, kills/, gate_scripts/.
Resume is automatic (GLOBAL_STATE.json). Never restarts science from iteration 1.

## HONEST SCOPE (read before trusting any output)
- Tier 1 (evaluator.py): G0 order/structural rules + P1-P7 + dead-class dedup are FULLY deterministic.
- Tier 2 (G1..G12): the derivation agent WRITES a sympy script per gate; the SCRIPT is executed and
  its printed CERTIFICATE_JSON is the judge; the referee agent then attacks it. A gate PASS is
  therefore "PASS(script)": the script itself could be wrong, so **SURVIVOR = SURVIVOR_PENDING_AUDIT.
  Nothing is 'viable' until a human/Claude audits the committed gate scripts** (they are all saved in
  gate_scripts/ for exactly this). Qwen never grades its own candidate; synthesis rules enter the
  knowledge graph as PROPOSED and only a human/Claude promotes them to BINDING.
- Single-candidate kills never auto-generalize to class kills (DEAD_CLASSES signatures are added only
  with a class-level argument).

## SEEDED KNOWLEDGE (sec 26 — agents do not rediscover)
state/DEAD_CLASSES.json: 108k pincer theorem, AeST alpha_2 kill, lapse-weighting kill (x2), quadratic-
carrier order-counting kill, disformal kill, sigma-Legendre no-go, 2-DOF MMG kill, CCG, UV-deformation.
state/SURVIVORS.json: khronometric e^-y self-screened (CONDITIONAL; G8 Lambda_sc = make-or-break) and
nonlocal DEFW/F+ (OPEN). state/KNOWLEDGE_GRAPH.json: 8 BINDING rules. state/OPEN_GATES.json: the
frontier, led by sec-33's objective: separate screened PF response from kinetic normalization.

## STOP CONDITIONS
SUCCESS (all gates PASS + audit) | STRUCTURAL NO-GO (grammar exhausted + theorem) | BLOCKED
(infrastructure; resumes later) | HUMAN OVERRIDE (Ctrl+C). Never stops because a candidate "looks
promising" and never because Qwen says it is sufficient.

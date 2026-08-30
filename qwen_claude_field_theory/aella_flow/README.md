# AELLA — the whirlwind (exhaustive architecture-class sweep)
Zero-LLM brute force done right: the structural axes of the grammar are FINITE, and Neda's trusted/
theorem gates are functions of structure only — so instead of sampling forever, Aella ENUMERATES every
expressible architecture class, gates one representative of each, and the verdict covers the whole
class. Output: `reports/EXHAUSTIVE_SWEEP.json` — the complete map (killed classes + the open set).

Run:  `python3 sweep.py`   (seconds; no Ollama, no tokens)
Division of labor: **Aella** maps the space exhaustively at the class level · **Neda** (neda_flow) runs
the interpretive LLM branches + aleatoric probes within it · **Claude** hostile-audits the open set.
Aella imports Neda's `candidate_manager/evaluator/gate_templates` — one gate codebase, two engines.

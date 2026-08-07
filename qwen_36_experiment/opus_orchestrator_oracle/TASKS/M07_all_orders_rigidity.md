# M07 — Is the (v/c)² suppression an all-orders statement?
COST: M | KILLS FAST: YES | script: `mi_all_orders_rigidity_2026.py`

## The task
On the open list, never run. The (v/c)² suppression was established at leading order. If it holds **to all
orders**, the whole u-contraction class is closed by theorem and the corpus can stop testing members. If it
fails at some order, that order is exactly where to look.

## Do
1. Set up the u-contraction expansion on the exact circular dS worldline (the embedding is in
   `mi_circular_dS_response_2026.py` — reuse it).
2. Compute the suppression factor at successive orders in (v/c). Does it stay (v/c)², or does a term at
   higher order come in unsuppressed?
3. Look for a structural reason: the corpus's sign obstruction is spec(□_u) ≤ 0 while |a|² > 0. Is that an
   all-orders statement? If so, prove it.
4. State the theorem with hypotheses, or exhibit the order at which it breaks.

## Settles if / refuted if
SETTLED: all-orders ⇒ a real theorem, and M05/M08 become unnecessary for this class.
REFUTED: an unsuppressed higher-order term ⇒ that is the mechanism's address; compute its coefficient.

## Known walls
Generic K needs |K| ~ 3.8e5–3.8e7 against ‖K‖ ≤ 1 — it is the **prefactor**, not the kernel choice. And that
prefactor IS the Frenet torsion. One fact, three faces.

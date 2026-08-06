# DOOR D1 — Collect the CTP variational prize
STATUS: OPEN | RANK: 5 | COST: M | KILLS FAST: no (a standalone advance)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
The corpus's standing obstacle is that the MI law is **not variational** — a retarded kernel cannot come from
an in-out action. But it **can** in the in-in (Schwinger-Keldysh) formulation: varying the closed-time-path
effective action gives retarded equations of motion. tn18 announces exactly this and does not do it: review
found its kernel is **exactly even** (`max|K(t)-K(-t)|/max|K| = 7.72e-14`), its action is a single symmetric
double integral, and grep finds **no z_+, no z_-, no branch index** in 488 lines.

## Why it works with the framework
It repairs the framework's own stated motivation without touching a0 or the phenomenology, and it directly
addresses the 2026-08-01 no-go ("the law is not variational in a disc") rather than routing around it. This is
the door I would rank highest for *theoretical* payoff independent of the coefficient.

## Concrete first calculation
1. Write `S[z_+, z_-]` with genuine plus/minus branches and the Keldysh rotation
   `z_cl = (z_+ + z_-)/2`, `z_q = z_+ - z_-`.
2. Vary `delta S / delta z_q` and evaluate on the diagonal `z_+ = z_- = z`.
3. Verify **symbolically** that the retarded kernel `K_R` survives in the EOM and the imaginary/noise part
   `K_I` drops out of the mean equation (it should reappear as noise, which is the physically right place).
4. Check the four Keldysh propagators are consistent: `G_R - G_A = G_> - G_<`.

## Settles if / refuted if
CONFIRMS: a genuinely retarded MI equation of motion from a variational principle ⇒ **the "not variational"
no-go is dissolved for the CTP class**, which is a real, standalone, publishable advance.
KILLS: an obstruction appears even in CTP ⇒ that obstruction is much deeper than previously known and is worth
stating as a theorem.

## Known walls — do not rediscover
A time-symmetric (even) kernel has **zero quadrature** and sits exactly on the passivity boundary — that is
what a *quadratic in-out* action gives you, and it is why tn18's kernel came out even. The whole point of CTP
is to escape that, so if your CTP kernel is also even, you have not implemented CTP.

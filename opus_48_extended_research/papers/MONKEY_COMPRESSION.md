# Monkeys, Hamlet, and the Price of a Prompt: Language Models as Search-Space Compressors in Generate-and-Test Discovery

**Carl P. Zimmerman** — Briar Creek Tech

2026-08-14

---

## Abstract

The infinite monkey theorem is true and useless: a million monkeys typing 2 keystrokes per second on a 27-key keyboard need an expected $10^{186063}$ years to produce Hamlet, because blind sampling has neither a prior nor a verifier. Interposing a large language model between the monkeys and the page collapses the expected wait to 2,400 years for the prompt "write hamlet" and to about three minutes for "hamlet" — a compression of roughly $10^{186060}$ in expected time — because training has already absorbed the target's improbability into the weights, leaving the monkeys to find only its *address*. We work the arithmetic exactly (every number in this note is reproduced by a committed script), derive the informational floor on prompt length (the address cannot be shorter than the bits of the target *not* already in the model), and then make the serious point the joke carries: the same two ingredients that rescue the monkeys — a prior that proposes only well-formed candidates, and a verifier that scores each one against data — convert blind exploration into feasible generate-and-test search. This is a legitimate discovery methodology with one non-negotiable caveat: the fit that terminates a search is not evidence, because search-until-fit guarantees a fit; evidence is what the surviving candidate does on data it was never searched against. We state the caveat's discipline (pre-registration, committed verification scripts, out-of-sample confrontation) and its application to LLM-assisted hypothesis generation, taking no position here on the correctness of any particular hypothesis so found.

---

## 1. The theorem and its arithmetic

Émile Borel's dactylographic monkeys (1913) and Eddington's popularization (1927) established the canonical statement: a monkey striking keys uniformly at random will, with probability approaching 1 as time goes to infinity, type any given finite text — including Hamlet. The theorem is correct. The interesting quantity is the expected wait, which the theorem's popular form politely omits.

Model the setup as a 27-key keyboard (26 letters plus the space bar), struck uniformly at random, output examined as a sliding window over the keystroke stream. For a target string of $N$ characters, the expected number of keystrokes before the target first appears is, to excellent approximation for non-self-overlapping strings,

$$W(N) \approx 27^{N}.$$

Take Hamlet at approximately 130,000 characters (case-folded, punctuation dropped — every simplification here is a *gift* to the monkeys). Then

$$W = 27^{130000} \approx 10^{186077} \ \text{keystrokes}.$$

Give the monkeys every advantage: one million of them, each typing 2 keystrokes per second, i.e. $2 \times 10^{6}$ keystrokes per second in aggregate, roughly $6.3 \times 10^{13}$ per year. The expected wait is

$$T_{\text{Hamlet}} \approx \frac{10^{186077}}{2\times 10^{6} \ \text{s}^{-1}} \approx 10^{186071} \ \text{s} \approx 3\times 10^{186063} \ \text{years},$$

about $10^{186053}$ times the age of the universe ($1.38\times 10^{10}$ yr). Note how little the monkeys matter: their entire aggregate typing rate removed seven units from an exponent of 186,077. Giving every atom in the observable universe ($\sim 10^{80}$) a keyboard would still leave the exponent above 185,990. The problem is not throughput. The problem is that blind sampling pays the full information price of the target at every attempt.

## 2. A language model between the monkeys and the page

Now interpose a trained large language model: the monkeys type into a prompt box, and any prompt that elicits the complete text of Hamlet counts as success. The target string shrinks from the play to the *prompt*, and the arithmetic collapses:

| Monkeys must type | $N$ | Expected keystrokes | Expected time (1M monkeys, 2 keys/s) |
|---|---|---|---|
| Hamlet directly (no LLM) | 130,000 | $10^{186077}$ | $\sim 3\times 10^{186063}$ years |
| "write hamlet in full" | 20 | $27^{20} \approx 4.2\times 10^{28}$ | $\sim 6.7\times 10^{14}$ yr ($\approx$ 49,000 universe ages) |
| "write hamlet" | 12 | $27^{12} \approx 1.5\times 10^{17}$ | $\approx$ 2,400 years |
| 8 characters | 8 | $27^{8} \approx 2.8\times 10^{11}$ | $\approx$ 1.6 days |
| "hamlet" | 6 | $27^{6} \approx 3.9\times 10^{8}$ | $\approx$ 3.2 minutes |

Three features of this table deserve to be made explicit.

**(a) The compression is astronomical and real.** From typing Hamlet to typing "write hamlet" the expected time falls by a factor of order $10^{186060}$. Nothing about probability theory changed; what changed is that the model's training already performed the search through character space and cached the result. In the terminology of the compression literature, a language model *is* a compressor (this is not a metaphor: LLMs are literally competitive with, and often superior to, purpose-built compressors on text, cf. Delétang et al. 2023), and a prompt is a *codeword*: a short address that the model decompresses into a long, structured output.

**(b) Each character of prompt costs a factor of 27.** "write hamlet in full" versus "hamlet" is 14 characters of politeness costing a factor of $27^{14} \approx 10^{20}$ in expected time — the difference between three minutes and 49,000 ages of the universe. In a random-search regime, verbosity is not a style choice; it is an exponential tax.

**(c) The residual wait is the address, not the target.** The six characters of "hamlet" carry $6 \log_2 27 \approx 28.5$ bits. That is the entire remaining price of a 130,000-character work — because the work is among the most heavily replicated texts in the training distribution, it possesses one of the shortest addresses of any large object in the model. The improbability did not vanish. It was pre-paid, once, at training time.

## 3. The shortest prompt and the informational floor

How short can the prompt go? The mechanical arithmetic says each character removed divides the wait by 27, but there is a floor, and it is informational rather than mechanical: **the prompt must carry at least the bits of the target that are not already in the model.** Formally, the shortest reliable prompt is a conditional description length — the analogue of conditional Kolmogorov complexity $K(\text{target} \mid \text{model})$ — and it shrinks as the mutual information between model and target grows.

Three regimes illustrate the floor:

1. **Famous target** (Hamlet): the corpus contains the object many times over; the address is a single token of its common name; about 28 bits suffice. Below that, reliability decays — a 4-character fragment has too many alternative continuations, and the monkeys' hit no longer deterministically yields the play.

2. **Obscure target** (a string the model has never seen — a random hex block, an unpublished result): the mutual information is zero; no short address exists; the prompt must contain essentially the target itself, and the monkeys are back to paying full freight. *No language model can shorten the address of something it has not compressed.*

3. **The degenerate limit**: a model fine-tuned to emit the target unconditionally has moved 100% of the specification into the weights; the shortest prompt is the empty string; monkeys are unnecessary. The classic theorem is the opposite pole — a bare typewriter holds 0% of the specification and the keystrokes must carry it all.

Prompt length is therefore a *measurement*: it reads off how much of a target's description already resides in the machine. This also gives a precise meaning to fame: an object is famous, relative to a model, exactly to the extent that its address is short. And it locates the honest limit of the parlor trick in Section 2 — eliciting Hamlet from a model that memorized Hamlet is retrieval, not creation. The interesting case is the one where the model has *not* memorized the target, which brings us to the actual point.

## 4. Why the theorem is useless, and generate-and-test is not

The infinite monkey theorem describes a search with two properties, each independently fatal:

- **No prior.** Every keystroke is uniform; the sampler spends almost all its measure on strings that could not possibly be the target — ungrammatical, unpronounceable, not even word-like. The search space is character space, size $27^{N}$.
- **No verifier.** Nothing in the setup says "warmer." A monkey that produces Act I Scene I verbatim and then one typo receives exactly the same feedback as one producing static: none. Partial progress cannot accumulate.

Infinity is the price of lacking both. Now repair them separately:

- A **prior** restricts proposals to well-formed candidates. A language model prompted for, say, "a simple formula relating an acceleration scale to cosmological quantities" does not emit random strings; it emits dimensionally sensible combinations of the relevant constants — the manifold its training compressed. The effective search space drops from $27^{N}$ to the (vastly smaller) set of coherent candidates, plausibly $10^{3}$–$10^{6}$ objects for a constrained physics ansatz rather than $10^{186077}$ strings.
- A **verifier** scores each candidate against something the proposer cannot fake: data, a proof checker, a compiler, an experiment. With a verifier, expected search time stops being (space size) $\times$ (per-draw cost) and becomes (space size / acceptable hits) $\times$ (per-test cost) — and partial structure *can* accumulate across iterations, because the verifier's feedback steers the next round of proposals.

With both in place, blind exploration becomes **generate-and-test**, and the economics change from "longer than the universe" to "weeks of iteration": thousands of candidates, minutes per test. This is not a novelty of the LLM era. It is evolution's algorithm — mutation is dumb, selection is smart — and it is Simon's and Campbell's blind-variation-plus-selective-retention account of discovery, with the LLM playing chemistry (constraining which variations are well-formed enough to try) and the data playing selection. What the LLM adds is purely quantitative: a very strong, very broad prior available for a few cents per proposal. But quantitative changes of $10^{5}$ or more in proposal quality are qualitative changes in what a single investigator can search.

## 5. The caveat that carries all the weight

Generate-and-test has a failure mode exactly as old as the method, and it must be stated as bluntly as the method's power: **search-until-fit guarantees a fit.** If candidates are drawn until one matches the data, the terminal match is a *selection event*, not a *measurement*. Its nominal significance is meaningless, because the look-elsewhere effect has been maximized by construction: the procedure conditions on success.

The discipline that rescues the method is standard and non-optional:

1. **The fit that ends the search is a hypothesis, never a result.** It earns exactly nothing from the data that selected it.
2. **Evidence is out-of-sample behavior.** The surviving candidate must be confronted with data it was never searched against — new surveys, held-out regimes, independent observables — and it must be *allowed to fail* there.
3. **Pre-register what failure looks like** before the confronting data arrive: frozen estimators, committed thresholds, hash-stamped analysis choices. Otherwise the search quietly continues inside the "confirmation."
4. **Publish the verifier, not just the verdict.** Every load-bearing quantitative claim should ship with a runnable script that reproduces it from stated inputs, so that the selection pressure operating on the candidate is public and re-runnable.
5. **Record the kills.** A generate-and-test program that reports only survivors is indistinguishable from noise mining; the retraction and dead-end record is what makes the survivor count interpretable.

None of this is specific to language models. What is specific to language models is the *rate*: a prior this strong makes candidates so cheap that the look-elsewhere exposure grows faster than in any previous instrument, and the discipline above correspondingly matters more, not less. The LLM changed the economics of proposing. It changed nothing about the epistemology of confirming.

## 6. A case study, stated carefully

The author's own research program in galaxy-scale gravity — an acceleration scale tied to the cosmological constant, with a specific interpolation kernel and a redshift dependence — originated in precisely this loop: extended, deliberately unconstrained exploratory prompting of large language models, with each emitted candidate confronted against public kinematic data (SPARC rotation curves and the radial acceleration relation) by scripts written for that purpose, most candidates dying on contact, and one reframing surviving repeated confrontation.

This note is about the *method*, and it takes no position here on the correctness of that surviving hypothesis. What makes the case study usable as evidence about the method is only this: the program's public record (Zenodo DOIs and a version-controlled repository) exhibits the discipline of Section 5 in both directions — pre-registered, hash-frozen predictions awaiting adversarial data (Gaia DR4; Rubin/LSST); committed verification scripts for quantitative claims; and, importantly, *published retractions and withdrawn claims* where the verifier subsequently went the other way, including a public retraction of early overclaims. Survivorship reporting is the failure mode; a kill ledger is the countermeasure; the method is only as honest as its ledger.

The generalizable claim is modest and, we think, robust: **an individual investigator equipped with a strong generative prior and a ruthless, automated verifier can now conduct hypothesis searches that were previously the exclusive economics of large groups** — and the value of what such searches produce is decided entirely downstream, by out-of-sample confrontation, exactly as it always was.

## 7. Limits of the analogy

For completeness, the ways the monkey framing understates or misstates the real situation:

- **LLM sampling is not uniform**, so "expected keystrokes" for prompts mixes two regimes: the monkeys' uniform search *for* the prompt, and the model's highly non-uniform conditional distribution *given* the prompt. The table in Section 2 treats elicitation as deterministic at the given prompt; in reality reliability degrades smoothly as prompts shorten (Section 3), and a fully honest account would multiply by the elicitation probability. This refines the constants, not the exponents.
- **Verbatim reproduction of a 130,000-character text** in one pass also runs against context-window and copying-fidelity limits in current systems; the honest deployment retrieves the text rather than recites it. This strengthens rather than weakens the section-3 point: models are best treated as *address resolvers*, with the canonical object fetched from ground truth.
- **The verifier bounds everything.** Generate-and-test inherits the quality of its verifier. A weak verifier (noisy data, flexible post-hoc fitting, unfalsifiable scoring) converts the method into an efficient generator of plausible junk. The method's output is never better than the hardest test the survivor has passed.
- **The prior can be a cage.** A model proposes from what it has compressed; a search steered by an LLM prior will preferentially rediscover the vicinity of the known. Genuinely unprecedented structure — the zero-mutual-information regime of Section 3 — is exactly where the prior gives no discount, and where the method degrades gracefully back toward monkeys.

## 8. Conclusion

The monkey theorem's answer to "how long?" is an exponent with six digits: $10^{186063}$ years for a million monkeys to type Hamlet. Putting a trained language model between the monkeys and the page reduces the task to typing an address, and the arithmetic falls to minutes — because training pre-paid the improbability, once, into the weights. The serious content of the joke is a two-ingredient recipe as old as evolution: a prior that proposes only viable candidates, and a verifier that cannot be argued with. Together they turn blind typing into feasible search; and the single discipline that keeps the result honest is refusing to count the fit that ended the search as evidence for the thing it found. Proposal has become nearly free. Confirmation has not, and that asymmetry is now the entire game.

---

## Appendix A: the arithmetic, verified

All numbers in this note are computed, with tolerances, by the committed script `monkey_compression_check.py` (exit 0), published alongside this PDF. Conventions: 27-key uniform keyboard; expected wait $W(N)=27^{N}$ keystrokes for an $N$-character target (sliding window, non-self-overlapping approximation); aggregate rate $R = 10^{6} \times 2 = 2\times10^{6}$ keystrokes/s; Julian year $3.156\times10^{7}$ s; age of universe $1.38\times10^{10}$ yr; Hamlet length $1.3\times10^{5}$ characters (any figure in the range 120,000–180,000 commonly quoted for the play changes the exponent by under 40%, i.e. between $10^{171000}$ and $10^{258000}$ keystrokes — nothing in the argument is sensitive to this choice).

Key values: $\log_{10} 27 = 1.431364$. $W(130000) = 10^{186077.3}$ keystrokes $= 10^{186071.0}$ s $= 10^{186063.5}$ yr. $W(20) = 4.24\times10^{28}$ keystrokes $= 2.12\times10^{22}$ s $= 6.72\times10^{14}$ yr $= 4.87\times10^{4}$ universe ages. $W(12) = 1.501\times10^{17}$ keystrokes $= 7.50\times10^{10}$ s $= 2378$ yr. $W(8) = 2.82\times10^{11}$ keystrokes $= 1.41\times10^{5}$ s $= 1.63$ days. $W(6) = 3.874\times10^{8}$ keystrokes $= 193.7$ s $= 3.23$ min. Monkeys needed for "write hamlet" in one expected day: $W(12)/(86400 \times 2) = 8.7\times10^{11}$. Bits in "hamlet": $6\log_{2}27 = 28.5$. Politeness factor, "write hamlet in full" vs "hamlet": $27^{14} = 1.09\times10^{20}$. Time compression, Hamlet-direct vs "write hamlet": $10^{186063.5}/2378 \approx 10^{186060.1}$.

## References

- Borel, É. (1913). "Mécanique Statistique et Irréversibilité." *J. Phys. 5e série*, 3, 189–196. (The dactylographic monkeys.)
- Eddington, A. S. (1928). *The Nature of the Physical World*. Macmillan. (The popularized form.)
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell Syst. Tech. J.*, 27, 379–423, 623–656.
- Kolmogorov, A. N. (1965). "Three approaches to the quantitative definition of information." *Problems Inform. Transmission*, 1(1), 1–7. (Conditional description length; the floor of Section 3.)
- Campbell, D. T. (1960). "Blind variation and selective retention in creative thought as in other knowledge processes." *Psychol. Rev.*, 67(6), 380–400.
- Simon, H. A. (1962). "The Architecture of Complexity." *Proc. Am. Phil. Soc.*, 106(6), 467–482.
- Delétang, G., et al. (2023). "Language Modeling Is Compression." arXiv:2309.10668.
- Zimmerman, C. P. (2026). "The Completion." Zenodo, DOI 10.5281/zenodo.21895046 (v9). (Case-study program of Section 6; cited for its methodology ledger — pre-registrations, committed verification scripts, and retraction record at https://github.com/carlzimmerman/zimmerman-formula — not as evidence for its physics claims.)

*License: CC-BY-4.0. Every quantitative claim in this note is reproduced by the committed script published with it.*

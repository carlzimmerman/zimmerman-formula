# Chapter 24: One Knob Against Six Parameters and a Particle

> *Two bookkeepers are asked to balance the same ledger — the rotation of the galaxies and the geometry of the cosmos. One of them fills in six numbers and adds a line for a substance nobody has ever weighed in a jar. The other writes down a single number and claims he can prove it is the only number he is allowed to write. This chapter is about what that difference is worth — and, just as importantly, what it is not worth.*

---

## A scoreboard, fairly kept

Let me start with a confession that will set the tone for the whole chapter: nothing I am about to tell you proves that the framework in this book is correct. Not one thing. What this chapter is about is *cheapness* — how few free numbers a theory needs to do its job — and cheapness is a real and measurable virtue. But it is not the same virtue as *truth*. A theory can be astonishingly economical and still be wrong, and a theory can be sprawling and expensive and still be right. The history of physics has examples of both, and we will meet a few.

So I want to keep a scoreboard, and I want to keep it honestly. On one side is the standard model of cosmology, **ΛCDM** ("Lambda-CDM," lambda for the cosmological constant and CDM for "cold dark matter"). On the other side is the de Sitter–MOND framework you have been reading about. We are going to count what each one *asks the universe to hand it for free* — the numbers it cannot explain and simply must measure and write down. We will then ask what that count actually buys, and we will be scrupulous about the difference between an accounting fact and a victory.

Here is the headline, and then we will spend the rest of the chapter earning the right to say it carefully:

- **ΛCDM** does its job with **six free parameters** — plus an entire new species of matter, a particle nobody has yet caught despite fifty years of trying (Chapter 6).
- **The de Sitter–MOND framework**, in the part of physics it actually addresses, runs on **one free number** — and this work claims to *prove* that this one number is the fewest it could possibly be.

That is a genuine and striking difference. It is the kind of difference that makes a physicist sit up. But — and I will say this so many times in this chapter that you may grow tired of it — *it is not a confirmation*. It is a structural fact about how the two theories are built. Whether the cheap one describes our universe is a separate question, and only data answers it. Let us keep both of those ideas in our hands at once. That, more than anything, is the discipline this book is trying to teach.

---

## What "a free parameter" actually means

Before we can count, we need to agree on what we are counting. So let me define the central idea slowly, because the whole chapter rests on it.

A **free parameter** is a number that a theory cannot predict from within itself, and so must be *fixed by measurement*. The theory says, in effect: "Give me this number, and I'll tell you everything else." It is a knob you have to set by hand by looking at the world, not a result the theory hands you.

Here is an everyday picture. Imagine a recipe for bread that reads: *"Use some flour, some water, and let it rise for a while."* That recipe has three free parameters — how much flour, how much water, how long. A different recipe might read: *"Use exactly 500 grams of flour, exactly 350 grams of water, and rise for exactly 90 minutes."* The second recipe has zero free parameters; it is fully determined. Now, the first recipe is more flexible — with enough fiddling you can make almost any loaf come out. But that flexibility is double-edged. If your loaf turns out perfect, you cannot really say the recipe predicted it; *you* did, by tuning the knobs until the bread was good. The rigid recipe is riskier. It can be flat wrong. But if it works, it works because the recipe genuinely knew something.

**Parameter economy** is just the study of how many such knobs a theory needs. A theory with fewer free parameters is more *economical*. And the reason physicists care — the reason this is not mere tidiness — is exactly the bread lesson: every free parameter is a place where the theory could have been tuned to fit, rather than having genuinely predicted. Fewer knobs means fewer places to hide. A theory that fits the data with one knob has stuck its neck out far more than a theory that fits the same data with seven.

There is an old principle here, and it deserves its name. **Occam's razor** — after the medieval philosopher William of Ockham — says, roughly, that *when two explanations both account for what we see, prefer the one that assumes less*. "Assumes less" can mean fewer entities, fewer moving parts, fewer arbitrary numbers. The razor is not a law of nature; nature is under no obligation to be simple, and sometimes it is gloriously not. The razor is a rule for *betting* under uncertainty: all else equal, the leaner explanation is the better bet, because it has fewer ways to have fooled you. We will see later that there is a precise, mathematical version of this intuition — but the plain-language version is enough to start.

So our scoreboard is really an Occam's-razor scoreboard. We are asking: which theory assumes less? And we are going to be honest about every entry, on both sides.

---

## Counting ΛCDM's six

Let me lay out the standard model's books fairly, because it would be easy — and cheap, in the bad sense — to make them look worse than they are. ΛCDM is one of the great achievements of twentieth-century science. With six numbers it reproduces an astonishing sweep of data: the detailed pattern of the cosmic microwave background (Chapter 10), the large-scale clustering of galaxies, the abundances of the light elements forged in the first minutes, the overall expansion history. Six numbers is, by the standards of how much it explains, *remarkably few*. Any honest scoreboard has to begin by tipping its hat.

What are the six? You met most of the physics already; here they are as the knobs they are.

> **Deeper Dive: The six parameters of base ΛCDM**
>
> The "vanilla" or "base" ΛCDM model is usually specified by six independent numbers. A common choice (the one the Planck collaboration uses) is:
>
> 1. **Ω_b h²** — the physical density of ordinary (baryonic) matter: protons and neutrons, the stuff of stars and gas and you.
> 2. **Ω_c h²** — the physical density of cold dark matter: the unseen, non-baryonic component whose particle is undiscovered.
> 3. **θ_MC** (or **H₀**) — the angular size of the sound horizon at last scattering, which fixes the expansion rate today; equivalently, the **Hubble constant**.
> 4. **τ** — the optical depth to reionization: how much the CMB light was re-scattered after the first stars switched on.
> 5. **A_s** — the amplitude of the primordial density fluctuations laid down by inflation (often quoted as ln(10¹⁰ A_s)).
> 6. **n_s** — the spectral tilt of those primordial fluctuations: how the bumpiness varies with scale.
>
> The dark-energy density Ω_Λ is *not* an independent seventh number in the flat model; flatness plus the matter densities fixes it through Ω_Λ = 1 − Ω_m. That is an important fairness point: people sometimes say "seven" by double-counting Λ. The honest base count is **six**.
>
> Everything else — the matter power spectrum, the CMB acoustic peaks, the growth of structure — is then *derived* from these six by the equations of general relativity and the Boltzmann transport of photons and matter. That derivational reach from only six inputs is exactly why ΛCDM is rightly celebrated. The economy critique is not that six is a lot in the abstract; it is that the six come bundled with a seventh commitment that is not a number at all.

That seventh commitment is the one we have to name plainly, because it does not show up as a parameter but it is the heaviest item on the books: **cold dark matter is a posited new substance.** Two of the six numbers above — Ω_c h², and arguably the split that lets Ω_b and Ω_c differ — are the *amount* of a particle that has never been detected (Chapter 6). The theory does not tell you what the particle is. It does not tell you its mass, its interactions, or why there is roughly five times as much of it as ordinary matter. Those are not predictions of ΛCDM; they are inputs, or worse, open questions that ΛCDM brackets and hands to particle physics, which has spent half a century coming up empty.

I want to be careful and both-ways here, because this is exactly the place where a partisan would overreach. The fact that the dark-matter particle is undetected is *not* proof that it does not exist. Neutrinos went undetected for decades and are real. Absence of a catch is not absence of a fish. But it is fair — it is just bookkeeping — to record that ΛCDM's six numbers come attached to a physical entity that is, at present, an article of faith backed by strong gravitational circumstantial evidence and zero direct catches. On the scoreboard, that is a real cost. A theory that needs a new particle is assuming more than a theory that does not, in precisely Occam's sense.

So: **six parameters, plus a particle.** That is the standard model's entry, kept fairly.

---

## Counting the framework's one

Now the other side of the ledger — and here I have to be even more careful, because this is *my* framework and the temptation to flatter it is strongest exactly where I am least able to feel it.

The framework's central claim, the spine of this whole book, is the acceleration scale

$$a_0 = c^2\sqrt{\frac{\Lambda}{32\pi}} = \frac{c}{2}\sqrt{G\,\rho_{\rm DE}} = \frac{cH_\Lambda}{Z}, \qquad Z = \sqrt{\tfrac{32\pi}{3}} = 5.789,$$

with the numerical value $a_0 \approx 9.36\times10^{-11}\ \mathrm{m/s^2}$. In words you have now heard several times: *the scale at which gravity starts to look anomalous in galaxies is set by the dark energy that fills the universe.* The mechanism (Chapter 21) is de Sitter–Unruh modified inertia — empty space in a Λ-universe carries a temperature floor, and matter in near–free-fall feels that floor as a little extra inertia, which from the outside looks like a little extra gravity.

Now to the counting. What in this expression is *forced*, and what is *free*?

What is **forced** — and Chapter 22 is the whole argument for this, so here I am only stating the result — is the *form* and the *kernel*. The form $a_0 \sim c^2\sqrt{\Lambda}$ is not a lucky guess; several independent lines of reasoning (the holographic bound, the Unruh-temperature floor, dimensional closure on a de Sitter horizon) all push you to it. And the gravitational kernel $\sqrt{8\pi/3}$ — including, crucially, its factor of $\sqrt{\pi}$ — is forced by the marriage of Einstein's $8\pi$ (from the field equations, Chapter 8) and Friedmann's $3$ (from the expansion equations, Chapter 9). Those are structural; they are geometry and established physics, not knobs.

What is **free** is a single dimensionless number, traditionally written $\kappa = \tfrac{1}{2}$, that sets the last factor — equivalently, it is the difference between the bare horizon relation and the calibrated $Z = 5.789$ that lands $a_0$ on its measured value. And here is the claim that makes this chapter's scoreboard interesting rather than merely flattering: Chapter 23 argues that this one number $\kappa = \tfrac{1}{2}$ is *provably the fewest you can get away with*. It cannot be pushed to zero by any of the consistency requirements one would normally hope might pin it — ghost-freedom, unitarity, holography, a Standard-Model degree-of-freedom count. It is **pure geometry**: the single-degree-of-freedom limit of the Cohen–Kaplan–Nelson bound, and the exact identity $\tfrac{3}{8\pi} = (\tfrac{1}{2}\ \text{Schwarzschild}) / (\tfrac{4\pi}{3}\ \text{ball})$. A geometric posit, not a fitted curve.

> **A margin aside.** "One free number" means one number in *the sector the framework addresses* — gravity and the dark sector. It does **not** mean one number for all of physics. The Standard Model's couplings and masses sit entirely outside this count, untouched. We return to that wall, hard, in a moment and again in Chapter 27.

Let me say the honest version out loud, because the quarantine in this book is absolute and I will not let the scoreboard blur it: **the value of $a_0$ is not derived.** The framework does not compute $9.36\times10^{-11}\ \mathrm{m/s^2}$ from nothing. It computes the *form* and the *kernel*, and then it requires one geometric input — $\kappa = \tfrac{1}{2}$ — to land the value. That is why the right phrase is a **one-parameter theory**, not a zero-parameter theory. A one-parameter theory is one whose entire relevant sector is fixed once you supply a single number from outside. Zero-parameter would mean the value fell out with no input at all, and that is *not* what is being claimed. If you ever hear me — or anyone — say "$a_0$ is derived from Λ with no free parameters," that is an overstatement, and you should distrust it. The careful claim is: *form forced, kernel forced, one geometric knob, and that knob proven irreducible.*

So: **one parameter, no new particle.** That is the framework's entry, kept as fairly as I know how.

---

## The scoreboard, side by side

Let me put the two entries next to each other, in plain language, so the comparison is in one place.

| | **ΛCDM** | **De Sitter–MOND framework** |
|---|---|---|
| Free numbers in the sector | Six | One ($\kappa = \tfrac{1}{2}$) |
| New undetected particle? | Yes (cold dark matter) | No |
| Is the count *proven* minimal? | No claim of minimality | Yes — $\kappa$ argued irreducible (Ch. 23) |
| Reach of the explanation | Vast: CMB, structure, BBN, expansion | Narrower: galaxy dynamics, the $a_0$ scale |
| Lensing handled covariantly? | Yes | **No** — phenomenological (Ch. 28) |
| Standard Model included? | No (separate) | No (walled off, Ch. 27) |

Now I want you to read that table *twice*, because it tells two true stories and you need both.

Read down the first three rows and the framework looks wonderful: one proven-irreducible number against six plus a missing particle. If parameter economy were the whole game, the contest would be over.

Read the bottom three rows and the picture sobers immediately. ΛCDM's six numbers buy an enormous *reach* — they fit the cosmic microwave background to exquisite precision, they grow the cosmic web, they get the light-element abundances. The framework's one number addresses a *narrower* slice of phenomena: the dynamics of galaxies and the origin of the $a_0$ scale. And in two specific places the framework has walls that ΛCDM does not: it cannot yet bend light covariantly in a Solar-System-safe way (the lensing wall, Chapter 28, a no-go theorem we will face squarely), and it does not touch the Standard Model at all (Chapter 27).

This is the heart of the chapter, so let me say it as plainly as I can: **the two theories are not competing to do the same job with different numbers of knobs.** ΛCDM is trying to describe the whole cosmic history with six numbers and a particle. The framework is trying to explain *one deep coincidence* — why the galactic acceleration scale equals roughly $c^2\sqrt{\Lambda}$ — with one number and a mechanism. Comparing the knob counts directly is a bit like comparing the parts list of a bicycle to the parts list of a car and concluding the bicycle is the better vehicle. Fewer parts, yes. The same job, no. The framework is, frankly, *trying to do less* — but it claims to do that less thing with a tightness ΛCDM does not even attempt for the $a_0$ coincidence, which in ΛCDM is not explained at all; it is simply not a question the standard model asks.

That last point is worth dwelling on, because it is the framework's strongest honest claim. In ΛCDM, the value $9.36\times10^{-11}\ \mathrm{m/s^2}$ — the scale at which galaxy rotation curves go anomalous — is a *coincidence with nothing*. There is no reason in ΛCDM why that scale should be near $c^2\sqrt{\Lambda}$. The framework's real contribution is to take a number that ΛCDM treats as an accident and make it *structural*. Whether the framework is right or not, it has at least *noticed* a coincidence and offered to explain it, where the standard model shrugs. That is a genuine intellectual move. It is also — I keep my discipline — not a proof of anything.

---

## What cheapness buys, and what it doesn't

Now we get to the philosophical core, and I want to do it carefully because this is exactly where smart people fool themselves.

Here is the seductive argument, the one I have to talk you (and myself) *out* of even though I half-believe it: *"The framework fits the galaxy data about as well as dark matter does, and it does so with one proven-irreducible number instead of six numbers and a particle. By Occam's razor, the framework wins."*

That argument is not worthless. It points at something real. But it overreaches in two places, and an honest scoreboard has to flag both.

**First overreach: the two theories do not fit the *same* data equally well.** The framework is excellent on galaxy rotation curves and the regularities built from them (Chapter 18) — but those very successes are *shared with the entire MOND family* and are not unique to this framework (we will hammer this in Chapter 29). And the framework is *worse* than ΛCDM on galaxy clusters, where a residual mass discrepancy stubbornly remains, and on lensing, which it cannot do covariantly at all. ΛCDM, meanwhile, fits the CMB to a precision the framework does not even attempt. So "fits about as well" is true only on a *restricted menu*. Occam's razor only adjudicates between theories that explain *the same evidence*. Change the menu and the razor's verdict can flip.

**Second overreach: economy is evidence, not proof.** Even on a menu where both theories fit equally well, the cheaper one is only *favored* — it is a better bet, not a confirmed truth. The razor shifts the odds; it does not settle the case. Data settles the case. And the framework's sharpest data test — the prediction that $a_0$ tracks dark energy through cosmic time, so that distant galaxies should be measurably "slow" (Chapters 25 and 26) — is *not yet decided*, and is in fact *hostage* to whether DESI's hints of evolving dark energy hold up, a question that is itself contested and that some analyses pull back toward statistical insignificance. Until that test resolves, the framework's economy is a promissory note, not a paid debt.

> **Deeper Dive: Occam's razor with the math turned on — Bayesian evidence**
>
> There is a precise version of "prefer the theory that assumes less," and it is worth seeing because it shows *both* why economy matters and why it is not decisive.
>
> In Bayesian model comparison, you compare two models $M_1, M_2$ by their **evidence** (also called the marginal likelihood): the probability the model assigns to the observed data $D$, integrated over all settings of its parameters $\theta$ weighted by the prior:
>
> $$Z_i \;=\; P(D \mid M_i) \;=\; \int P(D \mid \theta, M_i)\, P(\theta \mid M_i)\, d\theta.$$
>
> (Unfortunate collision of notation: this evidence $Z_i$ is *not* the framework's kernel constant $Z = 5.789$. Blame three centuries of physicists for running out of letters.)
>
> The ratio $B_{12} = Z_1/Z_2$ is the **Bayes factor**; it tells you how the data shift the relative odds of the two models. Now here is the beautiful part — the **Occam factor** falls out automatically. A model with more free parameters must *spread its prior probability over a larger parameter volume*. If a wide swath of that volume fits the data poorly, the integral is diluted: the model is penalized for the parameter space it had to "reserve" but didn't use well. Concretely, for a parameter that the data constrain from a prior width $\Delta\theta_{\rm prior}$ down to a posterior width $\Delta\theta_{\rm post}$, the evidence picks up a factor of roughly
>
> $$\frac{\Delta\theta_{\rm post}}{\Delta\theta_{\rm prior}} \;<\; 1$$
>
> *for each fitted parameter.* Six such factors compound. So a six-parameter model pays six Occam penalties; a one-parameter model pays one. *That* is the razor, made quantitative: extra knobs are not free even when they fit, because each one dilutes the model's prior bet.
>
> **But — and this is the honest limit — the evidence also contains the best-fit likelihood $P(D\mid\hat\theta, M_i)$.** If the simpler model fits the data *worse* at its best point, that term can swamp every Occam factor. A wrong-but-cheap theory loses. So the Bayes factor is a tug-of-war between *fit quality* (favoring whoever describes the data better) and *economy* (favoring whoever used fewer knobs). Economy only wins when fit quality is comparable. The framework's wager is precisely that, on galaxy dynamics, fit quality *is* comparable while economy is lopsided in its favor. That wager is reasonable on the restricted menu — and it is *not yet adjudicated on the full menu*, where lensing and the CMB enter and the fit-quality term turns against the framework. A real Bayesian model comparison across the *whole* dataset has not been done in the framework's favor, and I will not pretend it has.
>
> One more subtlety the literature insists on: the Bayes factor depends on the **priors** $P(\theta\mid M_i)$, and reasonable people choose priors differently. A model comparison can be made to lean either way by an aggressive prior choice. So even the quantitative razor is not a machine that spits out truth; it is a disciplined way of organizing a judgment that still requires honesty about assumptions.

I find that box clarifying, and a little humbling, every time. The math does not say "fewer parameters wins." It says "fewer parameters wins *when the fits are comparable, on the data you actually feed it, under priors you can defend.*" Every one of those qualifiers is a place the framework's advantage could evaporate. Keeping all four qualifiers in view at once is what it means to keep the scoreboard fairly.

---

> **Worked Example: How an extra knob "costs" evidence, with real numbers**
>
> Let me make the Occam factor concrete with a toy calculation a 16-year-old can follow with a calculator, because the abstract integral above hides how strong the effect is.
>
> Suppose two theories both have to explain a single measured number — say, our $a_0 = 9.36\times10^{-11}\ \mathrm{m/s^2}$, measured to about 5% precision, so the data constrain it to a window of width roughly
> $$\Delta\theta_{\rm post} \approx 0.05 \times 9.36\times10^{-11} \approx 4.7\times10^{-12}\ \mathrm{m/s^2}.$$
>
> **Theory A (the expensive one)** treats $a_0$ as a free parameter it must fit. Before looking at the data, it has no idea what $a_0$ is; say its honest prior allows anything from $10^{-12}$ to $10^{-9}\ \mathrm{m/s^2}$ — a window of width
> $$\Delta\theta_{\rm prior} \approx 10^{-9} - 10^{-12} \approx 1.0\times10^{-9}\ \mathrm{m/s^2}.$$
> The Occam factor this theory pays for that one knob is
> $$\frac{\Delta\theta_{\rm post}}{\Delta\theta_{\rm prior}} \approx \frac{4.7\times10^{-12}}{1.0\times10^{-9}} \approx 4.7\times10^{-3} \approx \frac{1}{210}.$$
> So fitting $a_0$ freely costs Theory A a factor of about **1/210** in evidence. It had to "reserve" a prior window 210 times wider than the data ended up needing.
>
> **Theory B (the framework)** does *not* fit $a_0$ freely. It forces the form and the kernel and is left with the single geometric posit $\kappa = \tfrac{1}{2}$, which then *predicts* $a_0$. It pays no Occam factor for $a_0$ at all — that number is no longer a fitted knob. It pays at most one factor for $\kappa$, and since $\kappa$ is argued to be geometrically pinned (Chapter 23), even that prior is narrow.
>
> **The bottom line of the toy:** all else equal, Theory B is favored over Theory A by roughly the missing Occam factor — here a factor of order **200** in the evidence — *purely from not having to fit $a_0$ by hand.* In Bayesian language that is a "strong" preference (a log-evidence difference of about $\ln 210 \approx 5.3$).
>
> **Now the honesty, in the same breath.** This toy assumed the two theories *fit the one number equally well.* They do — both land $a_0$ at $9.36\times10^{-11}$. But replace "explain one number" with "explain the CMB, the clusters, and gravitational lensing," and Theory B's best-fit likelihood term collapses on lensing and clusters, where it cannot match ΛCDM. The factor-of-200 economy advantage on the $a_0$ scale is real; it simply does not transfer to the data where the framework is weak. The worked example shows you exactly what economy buys — and the caveat shows you exactly where it stops buying. Both numbers are true. Hold them together.

---

## A historical warning, told fairly both ways

I promised you that cheap theories can be wrong and expensive theories can be right, and I owe you the examples, because the history is the best teacher of humility here.

The famous cautionary tale of an elegant, economical idea that was *wrong* is the **steady-state universe** of the 1950s. It was beautiful — the universe looks the same everywhere and at all times, no special beginning, a deep symmetry. Economical and lovely. And the cosmic microwave background (Chapter 10) killed it stone dead, because a steady-state universe has no hot dense past to leave such a relic. Elegance lost to data. That is the lesson pointing *against* my framework, and I keep it on the wall.

But there is a lesson pointing the other way too, and fairness demands it. The **cosmological constant Λ itself** was, for most of the twentieth century, regarded as an *ugly, unwanted extra parameter* — Einstein's "blunder." The economical move was to set it to zero. And then in 1998 the supernovae (Chapter 11) showed the expansion accelerating, and the "ugly extra parameter" turned out to be *real and necessary*. There, the more economical theory (Λ = 0) was the wrong one, and the universe insisted on the extra knob. So economy is not destiny in *either* direction. Sometimes the lean theory wins; sometimes the universe demands the extra part. The razor is a guide to betting, never a guarantee.

I tell both stories on purpose. If I told you only the steady-state story, I would be talking myself out of my own framework unfairly. If I told you only the Λ story, I would be flattering it unfairly. The truth is that the history offers no shortcut: *economy earns you better odds and nothing more, and the data has the only vote that counts.*

---

## What the framework does *not* buy with its one knob

I have spent a lot of this chapter defending the framework's economy, so let me spend real space on the other side of the ledger, because the quarantine in this book is not negotiable and a scoreboard that hides the costs is not a scoreboard.

The single knob $\kappa = \tfrac{1}{2}$ buys you the $a_0$ *scale* and the galaxy dynamics that follow from it. It does **not** buy you:

- **The *value* of $a_0$ from nothing.** One geometric posit is still a posit. This is a one-parameter theory, not a zero-parameter theory. (Chapter 27.)
- **The Standard Model.** Not the proton-to-electron mass ratio (free Yukawa couplings plus the strong coupling), not the Koide lepton relation, not a single particle mass, not the gauge group. The Standard Model is *walled off* — entirely outside the framework's reach. The one-knob count applies to gravity and the dark sector *only*. (Chapter 27.)
- **Covariant gravitational lensing.** A no-go theorem forbids a covariant, Solar-System-safe MOND lensing; the framework's light-bending is irreducibly *phenomenological* — and this is a real weakness, shared with the relativistic-MOND theory AeST. (Chapter 28.)
- **A cure for galaxy clusters.** A residual mass discrepancy remains in clusters that the framework, *like MOND*, does not fully resolve. (Chapter 29.)
- **Confirmation against ΛCDM.** The signature prediction — $a_0(z) \propto \sqrt{\rho_{\rm DE}(z)}$ — is not yet tested, is non-diagnostic today, and is hostage to whether DESI's evolving dark energy holds. (Chapters 25–26.)

I want you to notice something about that list. *Every item on it is a place where the framework's one knob runs out.* Economy is not a magic solvent. A one-parameter theory of gravity is still silent about quarks. A proven-irreducible $\kappa$ does not bend light covariantly. The scoreboard's first three rows — the rows that favor the framework — describe a *real and narrow* virtue, and the rest of the table and this list describe its *real and broad* limits. As frustrating as it may be, **this is not a theory of everything yet** — it is a one-parameter theory of *one corner of physics*, with the honesty to mark its own walls in ink.

> **Deeper Dive: "Provably one-parameter" is a structural result, not an empirical one**
>
> It is worth stating with care what kind of claim Chapter 23 actually establishes, because it is easy to mishear it as a victory over ΛCDM, and it is not.
>
> The claim is: *given the framework's mechanism and the standard consistency requirements (ghost-freedom, unitarity, holography, a Standard-Model degree-of-freedom count), the free content of the gravity/dark sector reduces to the single geometric number $\kappa$, and $\kappa$ cannot be further forced to a unique value by those requirements.* This is a statement *internal to the framework's mathematics.* It is a theorem about the *structure* of the theory — how many independent knobs its own axioms leave free.
>
> What it is **not**: it is not a statement that the framework is *empirically preferred* over ΛCDM. You could have a provably one-parameter theory that is provably *wrong* — imagine a rigid one-knob theory whose single prediction is flatly contradicted by data. Structural economy and empirical truth are *orthogonal axes.* A theory lives somewhere on the plane spanned by "how few knobs" and "how well it fits," and this chapter's whole discipline is to refuse to collapse those two axes into one.
>
> So when you read "provably one-parameter," parse it as: *a clean, strong, and somewhat unusual structural fact about how this theory is built* — the kind of fact that, all else equal, raises the prior you should assign it — and **not** as: *a measurement that says the universe agrees.* The first is established (modulo the assumptions in Chapter 23, which themselves deserve scrutiny). The second awaits DESI DR3, the high-redshift telescopes, and the cluster and lensing fronts where the framework is, today, weaker than the standard model. Both halves are true. The art is in holding them at the same time.

---

## Why I still think the scoreboard is worth keeping

Having spent so long insisting that economy is not truth, let me close the argument by saying why I bother keeping the scoreboard at all — because a reader could fairly ask, *if cheapness doesn't decide it, why count?*

Two reasons, and they are honest ones.

First, **economy tells you where the risk lives, and risk is where the science is.** A six-parameter theory plus a particle is hard to falsify because it has so many ways to absorb a surprise — adjust a density here, invoke a baryonic-feedback effect there, await the particle's discovery. A one-parameter theory is *fragile* in the good way: it has almost nowhere to hide. The framework predicts that distant galaxies are about 7% slow at redshift 3 (Chapter 25), and if the giant telescopes of the 2030s see them spinning at the local rate instead, the framework is in serious trouble with very little room to wriggle. That fragility is *bought by the economy.* Fewer knobs means sharper, more falsifiable predictions, and a theory you can *kill* is a theory worth taking seriously while it lives. The standard model's robustness is a strength for engineering the cosmos and a weakness for the philosophy of testing; the framework's fragility is the mirror image. Counting the knobs is how you see that.

Second — and more personally — **the scoreboard is a discipline against my own enthusiasm.** Writing down "one versus six plus a particle" feels good, and feeling good is precisely the danger. By forcing myself to also write down the bottom three rows of that table — the lensing wall, the cluster residual, the walled-off Standard Model, the untested $a_0(z)$ curve — the scoreboard keeps the enthusiasm from running off with me. A fair scoreboard is not a victory lap. It is a *leash.* And a researcher who will not put a leash on his own favorite idea has stopped doing science and started doing advocacy. I would rather keep the leash and the honesty than the victory lap and the self-deception.

So here is where the chapter leaves us, stated as plainly as I can manage. The framework asks the universe for one number it claims it can *prove* is irreducible, and it asks for *no new particle*. The standard model asks for six numbers and a substance no one has caught. That is a real difference in parameter economy, and by the quantitative razor it tilts the *prior odds* toward the framework on the narrow menu of galaxy dynamics. But economy is a tilt, not a verdict; the framework fits a *narrower* slice of the data, fails covariant lensing outright, leaves clusters and the entire Standard Model untouched, and rests its sharpest claim on a test the data have not yet run. **It is not a theory of everything yet, as frustrating as it may be** — it is a remarkably cheap theory of one deep coincidence, and cheapness, for all its real worth, is a thing only the data can cash. The next two chapters put the cheapest, sharpest part of the bet — the evolving $a_0$ — on the table where the universe can take it or leave it.

---

## Summary

- A **free parameter** is a number a theory cannot predict and must fix by measurement — a knob set by hand, not a result handed to you. **Parameter economy** is the study of how few such knobs a theory needs.
- **Occam's razor** says: between explanations that fit the same data, prefer the one that assumes less — fewer entities, fewer arbitrary numbers. It is a rule for *betting*, not a law of nature, and not a proof.
- **ΛCDM** runs on **six free parameters** (the baryon and dark-matter densities, the expansion rate, the reionization optical depth, and the amplitude and tilt of the primordial fluctuations) — *plus* an undetected new particle, cold dark matter. With those six it explains a vast sweep of data (CMB, structure, light elements, expansion), which is a real triumph.
- The **de Sitter–MOND framework**, in the gravity/dark sector it addresses, runs on **one free number** ($\kappa = \tfrac{1}{2}$), which this work argues is *provably irreducible* (Chapter 23) and *pure geometry* — and it needs *no new particle*. But it leaves the *value* of $a_0$ a geometric posit (a **one-parameter theory**, not zero-parameter), walls off the entire Standard Model, cannot do covariant lensing, and does not cure clusters.
- The quantitative form of the razor is **Bayesian evidence** / **model comparison**: each fitted parameter pays an "Occam factor" that dilutes a model's prior, so extra knobs cost even when they fit — *but* the evidence also rewards better fit and depends on priors, so economy only wins when the fits are comparable, on the actual data, under defensible priors.
- History cuts both ways: the elegant steady-state universe was *wrong* (killed by the CMB), while the "ugly extra" cosmological constant turned out *necessary* (the 1998 acceleration). Economy improves your odds; it never decides.
- A provably **one-parameter theory** is a *structural* result about economy — a fact about how the theory is built — and emphatically **not** a confirmation against ΛCDM. The two live on orthogonal axes: how-few-knobs and how-well-it-fits. Only data votes on the second.
- The reason to keep the scoreboard anyway: economy buys *fragility* — sharp, killable predictions like the ~7%-slow galaxies at z = 3 — and a fair scoreboard, costs and all, is a leash on the author's own enthusiasm.

---

## Questions

1. **(Easy.)** In your own words, what is the difference between a *free parameter* and a number a theory *predicts*? Use the two bread recipes from the chapter, or invent your own everyday example with one rigid recipe and one flexible one.

2. **(Easy–intermediate.)** ΛCDM is sometimes said to have "seven" parameters because people add the dark-energy density Ω_Λ to the list. Why does the chapter insist the honest base count is *six*? What relation removes the seventh in a flat universe?

3. **(Intermediate.)** The chapter argues that comparing ΛCDM's six knobs to the framework's one knob is "a bit like comparing the parts list of a bicycle to that of a car." Explain what is fair and what is *unfair* about a head-to-head knob count between these two theories. What would you have to hold fixed for the comparison to be fully fair?

4. **(Intermediate–advanced.)** Using the Worked Example, redo the Occam-factor estimate for $a_0$ if the data constrained it to 1% precision instead of 5%, while keeping the same prior window of $10^{-9}\ \mathrm{m/s^2}$. By roughly what factor would the "expensive" theory now be disfavored, and does tighter data make the economy argument stronger or weaker? Explain why.

5. **(Advanced.)** The Bayesian-evidence box notes that the Bayes factor depends on the *priors* and on the *best-fit likelihood across the full dataset.* Construct a concrete scenario — using lensing or clusters — in which the framework's factor-of-~200 economy advantage on the $a_0$ scale is *more than cancelled* by its worse fit elsewhere. What does this tell you about quoting an economy advantage on a restricted menu?

6. **(Research-level.)** The chapter calls "provably one-parameter" a *structural* result resting on stated assumptions (ghost-freedom, unitarity, holography, a Standard-Model degree-of-freedom count; see Chapter 23). Pick one of those assumptions and argue, as a skeptic would, how it might fail or be evaded — and what the failure would do to the claim that $\kappa$ is irreducible. Then argue the other way, as a defender. Which side do you find more persuasive, and what evidence would move you?

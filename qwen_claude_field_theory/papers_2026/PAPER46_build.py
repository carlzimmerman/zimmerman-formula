#!/usr/bin/env python3
"""PAPER46 builder: generates PAPER46_prediction_ledger_2026.tex from the data arrays of the Kepler Grade Prediction Chart
(explainers/kepler_grade_prediction_chart.html), so the paper and the chart cannot drift apart.
Usage: python3 PAPER46_build.py        (writes the .tex; compile with tectonic; then PAPER46_audit.py)
Every non-ASCII character must be in the MAP below; an unmapped character aborts the build (never silently dropped)."""
import json, os, re, subprocess, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CHART = os.path.join(REPO, "explainers", "kepler_grade_prediction_chart.html")
OUT = os.path.join(HERE, "PAPER46_prediction_ledger_2026.tex")

# ---------------------------------------------------------------- unicode -> LaTeX
M = r"\ensuremath{%s}"
MAP = {
 "α": M % r"\alpha", "β": M % r"\beta", "γ": M % r"\gamma", "δ": M % r"\delta", "ε": M % r"\epsilon", "η": M % r"\eta",
 "θ": M % r"\theta", "κ": M % r"\kappa", "λ": M % r"\lambda", "μ": M % r"\mu", "ν": M % r"\nu", "ξ": M % r"\xi",
 "π": M % r"\pi", "ρ": M % r"\rho", "σ": M % r"\sigma", "τ": M % r"\tau", "φ": M % r"\phi", "χ": M % r"\chi", "ψ": M % r"\psi",
 "Ψ": M % r"\Psi", "Φ": M % r"\Phi", "Ω": M % r"\Omega", "Σ": M % r"\Sigma", "Δ": M % r"\Delta", "Λ": M % r"\Lambda",
 "Γ": M % r"\Gamma", "Ξ": M % r"\Xi", "ω": M % r"\omega", "ς": M % r"\varsigma",
 "≥": M % r"\geq", "≤": M % r"\leq", "≈": M % r"\approx", "≳": M % r"\gtrsim", "≲": M % r"\lesssim", "≠": M % r"\neq",
 "×": M % r"\times", "→": M % r"\rightarrow", "←": M % r"\leftarrow", "±": M % r"\pm", "∝": M % r"\propto", "√": M % r"\sqrt{\,}",
 "∞": M % r"\infty", "−": "-", "–": "--", "—": "---", "’": "'", "‘": "`", "“": "``", "”": "''", "·": M % r"\cdot",
 "°": r"\textdegree{}", "…": r"\ldots{}", "‰": r"\textperthousand{}", "∂": M % r"\partial", "∫": M % r"\int", "∑": M % r"\sum",
 "²": r"\textsuperscript{2}", "³": r"\textsuperscript{3}", "¹": r"\textsuperscript{1}", "⁴": r"\textsuperscript{4}",
 "⁻": r"\textsuperscript{-}", "⁶": r"\textsuperscript{6}", "⁸": r"\textsuperscript{8}",
 "₀": r"\textsubscript{0}", "₁": r"\textsubscript{1}", "₂": r"\textsubscript{2}", "₃": r"\textsubscript{3}",
 "ₐ": r"\textsubscript{a}", "½": M % r"\tfrac{1}{2}", "⅓": M % r"\tfrac{1}{3}", "¼": M % r"\tfrac{1}{4}",
 "☉": M % r"\odot", "⊙": M % r"\odot", "†": M % r"\dagger", "‡": M % r"\ddagger", "∼": M % r"\sim", "~": r"\textasciitilde{}",
 "ℓ": M % r"\ell", "ħ": M % r"\hbar", "∥": M % r"\parallel", "⊥": M % r"\perp", "∈": M % r"\in", "∣": M % r"\mid",
 "Å": r"\AA{}", "é": r"\'e", "á": r"\'a", "ö": r'\"o', "ü": r'\"u', "ø": r"\o{}", "ß": r"\ss{}", "í": r"\'i", "ñ": r"\~n",
 " ": "~", " ": r"\,", " ": r"\,", "≡": M % r"\equiv", "⇒": M % r"\Rightarrow", "→": M % r"\rightarrow",
 "∑": M % r"\sum", "∆": M % r"\Delta", "§": r"\S{}", "Θ": M % r"\Theta", "Ṗ": M % r"\dot{P}", "″": M % r"{}^{\prime\prime}", "₈": r"\textsubscript{8}", "×": M % r"\times", "Ω": M % r"\Omega", "π": M % r"\pi", "Ⅱ": "II",
}
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "^": r"\^{}"}
UNMAPPED = set()


def esc(text):
    out = []
    for ch in text:
        if ch == "\u0302" and out:                      # combining circumflex: gamma + U+0302 -> \hat{gamma}
            prev = out.pop()
            inner = prev[len("\\ensuremath{"):-1] if prev.startswith("\\ensuremath{") else prev
            out.append(M % (r"\hat{" + inner + "}"))
            continue
        if ch in SPECIAL:
            out.append(SPECIAL[ch])
        elif ch == "~":
            out.append(MAP["~"])
        elif ord(ch) < 128:
            out.append(ch)
        elif ch in MAP:
            out.append(MAP[ch])
        else:
            UNMAPPED.add(ch)
            out.append("?")
    return "".join(out)


# ---------------------------------------------------------------- inline html -> latex
class Inline(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag == "sub": self.out.append(r"\textsubscript{")
        elif tag == "sup": self.out.append(r"\textsuperscript{")
        elif tag == "b" or tag == "strong": self.out.append(r"\textbf{")
        elif tag == "i" or tag == "em": self.out.append(r"\textit{")
        elif tag == "br": self.out.append(r"\newline ")

    def handle_endtag(self, tag):
        if tag in ("sub", "sup", "b", "strong", "i", "em"): self.out.append("}")

    def handle_data(self, data):
        self.out.append(esc(data))


def inl(html):
    p = Inline()
    p.feed(html or "")
    return "".join(p.out).strip()


# ---------------------------------------------------------------- chart data via node
def chart_data():
    src = open(CHART, encoding="utf-8").read()
    js = re.search(r"<script>(.*)</script>", src, re.S).group(1)
    head = js.split("renderFuture(); renderConf(); renderDepo();")[0]
    stub = ("var document={getElementById:function(){return {}},querySelectorAll:function(){return []}};" + head +
            "\nconsole.log(JSON.stringify({FUTURE:FUTURE,CONF:CONF,DEPO:DEPO,DNC:DNC,NON:NON}));")
    r = subprocess.run(["node", "-e", stub], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("node failed: " + r.stderr[:400])
    return json.loads(r.stdout), src


# ---------------------------------------------------------------- static html block -> latex (neutrino section, legend, box)
class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs), [], parent

    def cls(self):
        return self.attrs.get("class", "")


class Tree(HTMLParser):
    VOID = {"br", "meta", "link", "img", "input", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [])
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in self.VOID:
            self.cur = n

    def handle_endtag(self, tag):
        c = self.cur
        while c is not None and c.tag != tag:
            c = c.parent
        if c is not None and c.parent is not None:
            self.cur = c.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def inner_html(n):
    s = []
    for c in n.children:
        if isinstance(c, str):
            s.append(c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        else:
            at = "".join(f' {k}="{v}"' for k, v in c.attrs.items())
            s.append(f"<{c.tag}{at}>" + (inner_html(c) if c.tag not in Tree.VOID else "") + (f"</{c.tag}>" if c.tag not in Tree.VOID else ""))
    return "".join(s)


def text_of(n):
    return "".join(c if isinstance(c, str) else text_of(c) for c in n.children)


def rows_of(table):
    rows = []
    for sec in table.children:
        if isinstance(sec, str): continue
        if sec.tag in ("thead", "tbody"):
            for tr in sec.children:
                if isinstance(tr, str) or tr.tag != "tr": continue
                rows.append((sec.tag, [(c.tag, inl(inner_html(c))) for c in tr.children if not isinstance(c, str)]))
    return rows


def table_latex(table):
    rows = rows_of(table)
    ncol = max(len(r[1]) for r in rows)
    spec = "".join(r">{\raggedright\arraybackslash}p{\dimexpr(\linewidth-%d\tabcolsep)/%d\relax}" % (2 * ncol, ncol) for _ in range(ncol))
    out = [r"{\footnotesize\begin{longtable}{%s}" % spec, r"\toprule"]
    head = [r for r in rows if r[0] == "thead"]
    for r in head:
        out.append(" & ".join(r"\textbf{%s}" % c[1] for c in r[1]) + r" \\")
    out += [r"\midrule", r"\endhead"]
    for r in rows:
        if r[0] == "thead": continue
        cells = [c[1] for c in r[1]] + [""] * (ncol - len(r[1]))
        out.append(" & ".join(cells) + r" \\")
    out += [r"\bottomrule", r"\end{longtable}}"]
    return "\n".join(out)


def block_latex(n):
    """render a block-level html node (div/h3/p/table wrappers) to latex"""
    out = []
    for c in n.children:
        if isinstance(c, str):
            if c.strip(): out.append(inl(c))
            continue
        if c.tag == "h3":
            out.append(r"\subsection*{%s}" % inl(inner_html(c)))
        elif c.tag == "p":
            out.append(inl(inner_html(c)) + "\n")
        elif c.tag == "div" and "tblwrap" in c.cls():
            for t in c.children:
                if not isinstance(t, str) and t.tag == "table": out.append(table_latex(t))
        elif c.tag == "div" and "callout" in c.cls():
            out.append(r"\begin{quote}\small " + inl(inner_html(c)) + r"\end{quote}")
        elif c.tag == "div" and "cards" in c.cls():
            out.append(r"\begin{itemize}")
            for card in c.children:
                if isinstance(card, str) or card.tag != "div": continue
                b = [x for x in card.children if not isinstance(x, str)]
                head = inl(inner_html(b[0])) if b else ""
                body = inl(inner_html(b[1])) if len(b) > 1 else ""
                out.append(r"\item \textbf{%s} %s" % (head, body))
            out.append(r"\end{itemize}")
    return "\n\n".join(out)


def section_html(src, start_marker, end_marker):
    a = src.index(start_marker) + len(start_marker)
    b = src.index(end_marker, a)
    t = Tree()
    t.feed(src[a:b])
    return t.root


# ---------------------------------------------------------------- document
def future_longtable(group):
    rows = group["rows"]
    out = [r"\subsection*{%s}" % inl(group["h"])]
    if group.get("n"):
        out.append(inl(group["n"]) + "\n")
    out.append(r"""{\scriptsize\begin{longtable}{>{\raggedright\arraybackslash}p{1.9cm}>{\raggedright\arraybackslash}p{3.6cm}>{\raggedright\arraybackslash}p{6.1cm}>{\raggedright\arraybackslash}p{8.3cm}c}
\toprule
\textbf{When} & \textbf{Test} & \textbf{Framework predicts} & \textbf{Rivals; what counts against it; status} & \textbf{Grade}\\
\midrule\endhead""")
    for r in rows:
        when = inl(r["d"]) + (r"\newline {\itshape " + inl(r["s"]) + "}" if r.get("s") else "")
        test = r"\textbf{" + inl(r["t"]) + "}" + (r"\newline " + inl(r["u"]) if r.get("u") else "")
        last = r"\textbf{Rivals.} " + inl(r["r"]) + r"\newline \textbf{Counts against.} " + inl(r["k"])
        if r.get("w"):
            last += r"\newline \textbf{Note.} " + inl(r["w"])
        last += r"\newline {\itshape " + inl(r["src"]) + "}"
        out.append(" & ".join([when, test, inl(r["p"]), last, r["g"]]) + r" \\ \addlinespace[2pt]")
    out.append(r"\bottomrule\end{longtable}}")
    return "\n".join(out)


def conf_longtable(group):
    labels = {"pass": "pass", "fail": "FAILS", "nd": "not diagnostic", "void": "void"}
    out = [r"\subsection*{%s}" % inl(group["h"]),
           r"""{\footnotesize\begin{longtable}{>{\raggedright\arraybackslash}p{4.4cm}>{\raggedright\arraybackslash}p{11.6cm}>{\raggedright\arraybackslash}p{2.0cm}>{\raggedright\arraybackslash}p{3.4cm}}
\toprule\textbf{Test} & \textbf{Outcome} & \textbf{Result} & \textbf{Source}\\\midrule\endhead"""]
    for r in group["rows"]:
        out.append(" & ".join([inl(r["t"]), inl(r["o"]), labels[r["r"]], inl(r["s"])]) + r" \\")
    out.append(r"\bottomrule\end{longtable}}")
    return "\n".join(out)


def main():
    data, src = chart_data()
    F, C, D, DNC, NON = data["FUTURE"], data["CONF"], data["DEPO"], data["DNC"], data["NON"]
    nF = sum(len(g["rows"]) for g in F)
    cnt = {k: sum(1 for g in F for r in g["rows"] if r["g"] == k) for k in ("K1", "K2", "K3", "K4")}
    nC = sum(len(g["rows"]) for g in C)
    nuc = section_html(src, "<h2>Neutrino predictions in detail</h2>", "<h2>Already confronted</h2>")
    legend = section_html(src, '<div class="legend">', "<h2>Coming up</h2>")
    meta = {"nF": nF, "cnt": cnt, "nC": nC, "nD": len(D), "nDNC": len(DNC), "nNON": len(NON)}

    T = []
    T.append(r"""\documentclass[10pt]{article}
\usepackage[landscape,margin=0.6in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{booktabs,longtable,array}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={A Dated, Graded Ledger of the Testable Predictions of a Vacuum-Tied MOND Framework, with Its Confronted Record and Retracted Claims (Working Note)}}
\setlist{nosep,leftmargin=1.3em}
\setlength{\parskip}{3pt}\setlength{\parindent}{0pt}
\sloppy
\begin{document}
\begin{center}
{\Large\bfseries A Dated, Graded Ledger of the Testable Predictions of a Vacuum-Tied MOND Framework,\\ with Its Confronted Record and Retracted Claims}\\[4pt]
{\large Working note}\\[4pt]
{\small The authors --- 2026-10-11, version 1.0. AI-assisted compilation; not peer reviewed.}
\end{center}
""")
    T.append(r"""\begin{abstract}
\noindent We collect, in one dated ledger, every testable prediction we could find in the working record of a programme built on the law $a_0=\kappa c\sqrt{G\rho_\Lambda}$ with $\kappa=\tfrac12$ \emph{fitted}, together with the numbers the rivals predict, the result that would count against each prediction, and what has already been confronted with data. Each of %(nF)d future tests carries a grade: K1 (the number was fixed before the data exist, by frozen criteria or a sealed hash, with a date and a stated kill condition; %(k1)d tests), K2 (sharp but capped by systematics, conditional, or nearly shared by the rivals; %(k2)d), K3 (open: no usable data, no date, or a forecast only; %(k3)d) and K4 (speculative or numerology-era predictions that could still be checked but have no derivation and are mostly retracted in the record; %(k4)d). We also list %(nC)d confronted results, including the failures, %(nD)d public deposits with their status, and the claims that must not be cited. The dated releases in the next months are the ALMA cubes of 2026-11-06 and 2026-11-28 and Gaia DR4 on 2026-12-02. The neutrino sector, which is entirely conditional and rests on a coincidence that the record itself calls generic, is set out in detail. Nothing here says the data favour the framework, $\kappa$ is not derived, the cold energy's mass is still required, and the theory is not closed.
\end{abstract}
""" % {"nF": nF, "k1": cnt["K1"], "k2": cnt["K2"], "k3": cnt["K3"], "k4": cnt["K4"], "nC": nC, "nD": len(D)})
    T.append(r"""\section{Scope and standing terms}
The acceleration scale is $a_0=\kappa c\sqrt{G\rho_\Lambda}$ with $\kappa=\tfrac12$ fitted (the current estimate is $0.42\pm0.10$, CFG493). Two footings, canonical $a_0=9.3603\times10^{-11}$ and alternative $1.1312\times10^{-10}$\,m\,s$^{-2}$, are never pooled and are written ``can / alt''. The cold energy's mass is still required and no dark-matter particle is proposed. Verdicts use raw data against framework-native predictions only; rows whose machinery is calibrated on $\Lambda$CDM carry no verdict weight. The flat law $a_0(z)=\mathrm{const}$ is the framework's distinctive high-redshift law, $a_0\propto H(z)$ is its rival, and $\Lambda$CDM has no $a_0$ (its emergent scale is the proxy).

\textbf{Method.} The ledger was compiled on 2026-10-11 from nine read-only sweeps of the programme's repository (the predictions ledgers, the Gaia DR4 pre-registration and its 21 amendments, lanes CFG1--CFG700, the atomos kill sheet, \texttt{real\_research}, \texttt{hunt\_2026}, the multi-model exploration folders, git history since April, and memory notes). Some lane folders were only keyword-screened, so the list is thorough but not guaranteed complete. Release dates for Euclid, Rubin, JUNO, LISA and 4MOST are taken from the record's own inventories and were not independently verified. Rows from AI exploration branches are tagged BRANCH and are non-authoritative; rows tied to the retired modified-inertia arm are tagged MI-ARM and are not live; rows from the old clock-host candidate are tagged CANDIDATE-CONDITIONAL.

\textbf{Grades.} """ )
    T.append(block_latex(legend) if False else
             r"\begin{itemize}\item \textbf{K1}, the Kepler grade: a number fixed before the data exist (frozen criteria or a sealed hash), a date, and a stated result that counts against it.\item \textbf{K2}: capped. The number is sharp, but the test cannot reach $3\sigma$ with today's systematics, the rivals predict nearly the same, or it is conditional on an assumption.\item \textbf{K3}: open. A real prediction with no usable data, no date, or only a forecast.\item \textbf{K4}, ``Kepler slop'': speculative or numerology-era predictions. Dated and testable, so they could still land, but no derivation backs them and the record has retracted or downgraded several. They are never to be cited as framework results.\end{itemize}")
    T.append(r"""\section{Calendar of dated releases}
\begin{center}\footnotesize\begin{tabular}{ll}
\toprule 2026-10-11 to 13 & Framework-native cosmic shear, 1024$^3$ run (CFG596), verdict pending\\
2026-11-06 & ALMA U4\_27928, CO at $z=1.42$ (sealed predictions, CFG571)\\
2026-11-28 & ALMA GS4\_24110, deep [CI] at $z=2.00$ (sealed predictions; part already scored on other public data)\\
2026-12-02 & Gaia DR4: wide binaries (pre-registration, 21 amendments) and Milky Way vertical force and curve (sealed, CFG553)\\
2026-12-17 & ALMA Big Wheel at $0.24''$ (no sealed prediction)\\
2027--2028 & Rubin SNe $w(z)$ gate, JUNO $\theta_{12}$, DESI DR3\\
2030s & LISA, DUNE and Hyper-K, LEGEND-1000, CMB-S4\\
\bottomrule\end{tabular}\end{center}
""")
    T.append(r"\section{Future tests}" + "\n" +
             "Sorted by date within each group. Rows are generated from the same data file as the public chart, so the two cannot differ.")
    for g in F:
        if g["h"].startswith("K4"): continue
        T.append(future_longtable(g))
    T.append(r"\section{Neutrino predictions in detail}")
    T.append(block_latex(nuc))
    T.append(r"\section{K4: Kepler slop}")
    for g in F:
        if g["h"].startswith("K4"):
            T.append(future_longtable(g))
    T.append(r"\section{Already confronted}" + "\n" +
             "What the record says so far. ``Not diagnostic'' means the test could not separate the readings, which is different from a pass.")
    for g in C:
        T.append(conf_longtable(g))
    T.append(r"\section{Published deposits}" + "\n" + "What is on the public record with a DOI or a committed hash, and where each stands.")
    lab = {"open": "open", "sup": "superseded", "nd": "note", "pass": "done"}
    T.append(r"""{\footnotesize\begin{longtable}{>{\raggedright\arraybackslash}p{5.2cm}>{\raggedright\arraybackslash}p{13.0cm}>{\raggedright\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{2.4cm}}
\toprule\textbf{Deposit} & \textbf{What it registered} & \textbf{Status} & \textbf{Source}\\\midrule\endhead""")
    for d in D:
        T.append(" & ".join([inl(d[0]), inl(d[1]), lab[d[2]], inl(d[3])]) + r" \\")
    T.append(r"\bottomrule\end{longtable}}")
    T.append(r"\section{Claims not to cite}" + "\n" + "Withdrawn, superseded or void claims that still sit in older files of the programme.")
    T.append(r"\begin{itemize}" + "\n" + "\n".join(r"\item \textbf{%s} %s" % (inl(a), inl(b)) for a, b in DNC) + "\n" + r"\end{itemize}")
    T.append(r"\section{What the framework does not predict}" + "\n" + "Statements the framework does not make, listed so they are never claimed as tests.")
    T.append(r"\begin{itemize}" + "\n" + "\n".join(r"\item \textbf{%s} %s" % (inl(a), inl(b)) for a, b in NON) + "\n" + r"\end{itemize}")
    T.append(r"""\section{Limits and use}
This ledger is a record of what the programme has committed to, not an argument that the framework is right. Several rows are conditional on assumptions that are not derived ($\kappa=\tfrac12$, the supply of cold energy, the identification of the lightest neutrino mass with the vacuum-energy scale, the non-supersymmetric AdS conjecture). The programme's own census describes the framework as viable but with essentially no distinctive, modified-gravity-impossible evidence in hand. A survival of a test is never a confirmation. The dated sealed predictions (the Milky Way vertical force and curve, the ALMA gas masses, the dark-energy evolution statement) carry SHA-256 hashes in the repository and are never edited after sealing; any change goes in a new dated file.

\textbf{AI assistance.} The sweeps and this compilation were produced with Anthropic's Claude; the numbers were read from committed files, and the build script regenerates every table from the chart data. Rows from other AI models' exploration folders are labelled as such.

\textbf{Reproducibility.} The repository at \url{https://github.com/carlzimmerman/zimmerman-formula} holds the public chart (\texttt{explainers/kepler\_grade\_prediction\_chart.html}), this paper's builder (\texttt{PAPER46\_build.py}) and its audit (\texttt{PAPER46\_audit.py}).
\end{document}
""")
    open(OUT, "w", encoding="utf-8").write("\n\n".join(T))
    if UNMAPPED:
        os.remove(OUT)
        sys.exit("UNMAPPED characters (add to MAP): " + " ".join(sorted(UNMAPPED)) + "  " + " ".join(f"U+{ord(c):04X}" for c in sorted(UNMAPPED)))
    json.dump(meta, open(os.path.join(HERE, "PAPER46_build_meta.json"), "w"), indent=1)
    print("wrote", os.path.basename(OUT), meta)


if __name__ == "__main__":
    main()

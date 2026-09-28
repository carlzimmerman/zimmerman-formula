"""Shared helpers for the citation-index build (paths, scope, text segmentation, name normalisation)."""
from __future__ import annotations

import functools
import gzip
import io
import json
import os
import re
import subprocess
import threading
import tokenize
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
CITE_DIR = HERE.parent                      # citations/
REPO = Path(os.environ.get("CITE_REPO", CITE_DIR.parent)).resolve()   # repository root (override for testing)
DATA = CITE_DIR / "data"
REGISTRY = HERE / "registry"

# ---------------------------------------------------------------- scope
# What is scanned: every git-TRACKED Python script and notebook, minus the prefixes below.
EXCLUDE_PREFIXES = (
    "ai_slop/extended_research/",        # excluded at the author's request (biology material; not touched)
    "ai_slop/TruthFlow/hermes_agent/",   # vendored third-party agent framework: credited as software, not scanned
    "ai_slop/HermesFlow/hermes_agent/",  # second vendored copy of the same framework
    "citations/",                        # the index and its own build scripts
)
SCAN_SUFFIXES = (".py", ".ipynb")


@functools.lru_cache(maxsize=None)
def build_ref() -> str:
    """The commit the index is built from. run_all.py pins it once (CITE_REF) so every stage reads the same commit
    even if HEAD moves during the build. Files are read as committed there, never from the working tree, so
    uncommitted edits (other sessions' work in progress) never enter the index."""
    return os.environ.get("CITE_REF") or subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                                        capture_output=True, text=True, check=True).stdout.strip()


def head_commit() -> str:
    return build_ref()


def committed_files(suffixes: tuple[str, ...] | None = None) -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-tree", "-r", "-z", "--name-only", build_ref()],
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    return sorted(p for p in out.split("\0") if p and (suffixes is None or p.endswith(suffixes)))


def tracked_files() -> list[str]:
    return [p for p in committed_files(SCAN_SUFFIXES) if not p.startswith(EXCLUDE_PREFIXES)]


_blob_lock = threading.Lock()
_blob_proc = None


def read_committed(path: str) -> bytes | None:
    """A file's bytes as committed at build_ref(); None when the file is not in that commit."""
    global _blob_proc
    with _blob_lock:
        if _blob_proc is None:
            _blob_proc = subprocess.Popen(["git", "-C", str(REPO), "cat-file", "--batch"],
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        _blob_proc.stdin.write(f"{build_ref()}:{path}\n".encode("utf-8"))
        _blob_proc.stdin.flush()
        head = _blob_proc.stdout.readline().decode("utf-8", "replace").split()
        if len(head) != 3 or head[1] != "blob":
            return None
        data = _blob_proc.stdout.read(int(head[2]))
        _blob_proc.stdout.read(1)                  # the newline that ends each object
        return data


def read_source(path: str) -> tuple[str | None, list[tuple[int, str]]]:
    """Return (python_code, extra_prose_segments). Notebooks: code cells joined; markdown cells as prose."""
    raw = read_committed(path)
    if raw is None:
        return None, []
    text = raw.decode("utf-8", "replace")
    if not path.endswith(".ipynb"):
        return text, []
    try:
        nb = json.loads(text)
    except Exception:
        return text, []
    code, prose = [], []
    for i, cell in enumerate(nb.get("cells", [])):
        src = cell.get("source", "")
        src = "".join(src) if isinstance(src, list) else str(src)
        if cell.get("cell_type") == "code":
            code.append(src)
        else:
            prose.append((0, src))
    return "\n".join(code), prose


def prose_segments(src: str) -> list[tuple[int, str]]:
    """(line, text) of every comment and string literal. Falls back to whole lines if tokenizing fails."""
    segs: list[tuple[int, str]] = []
    try:
        fmid = getattr(tokenize, "FSTRING_MIDDLE", None)
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING) or (fmid is not None and tok.type == fmid):
                segs.append((tok.start[0], tok.string))
        return segs
    except Exception:
        return [(i, line) for i, line in enumerate(src.splitlines(), 1)]


def strip_accents(s: str) -> str:
    s = s.replace("ł", "l").replace("Ł", "L").replace("ø", "o").replace("Ø", "O").replace("ß", "ss")
    s = s.replace("æ", "ae").replace("Æ", "Ae").replace("đ", "d").replace("Đ", "D").replace("ı", "i")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


PARTICLES = {"de", "van", "von", "der", "den", "le", "la", "di", "del", "da", "dos", "du", "ten", "ter", "'t",
             "des", "della", "dal", "el", "al", "st", "st."}


def norm_family(s: str) -> str:
    """Accent/case-folded family name without particles, apostrophes, hyphens or spaces."""
    s = strip_accents(s).lower().replace("’", "'")
    parts = [p for p in re.split(r"[\s]+", s) if p]
    while len(parts) > 1 and parts[0] in PARTICLES:
        parts = parts[1:]
    return re.sub(r"[^a-z]", "", "".join(parts))


def slugify(s: str) -> str:
    s = strip_accents(s).lower().replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def dump_json(obj, path: Path, gz: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True)
    if gz:                                  # mtime=0: identical content gives identical bytes (no spurious diffs)
        with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as fh:
            fh.write(data.encode("utf-8"))
    else:
        path.write_text(data + "\n", encoding="utf-8")


def load_json(path: Path):
    if str(path).endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(path.read_text(encoding="utf-8"))


def own_author_families() -> set[str]:
    """Family names of the repository's own author(s), read from CITATION.cff at build time (never hard-coded)."""
    fams = set()
    cff = REPO / "CITATION.cff"
    if cff.exists():
        in_authors = False
        for line in cff.read_text(encoding="utf-8").splitlines():
            if re.match(r"^authors:", line):
                in_authors = True
                continue
            if in_authors and re.match(r"^\S", line):
                in_authors = False
            m = re.search(r"family-names:\s*\"?([^\"]+)\"?", line)
            if in_authors and m:
                fams.add(norm_family(m.group(1)))
    return fams


def own_author_given_initials() -> set[str]:
    out = set()
    cff = REPO / "CITATION.cff"
    if cff.exists():
        for m in re.finditer(r"given-names:\s*\"?([^\"\n]+)\"?", cff.read_text(encoding="utf-8")):
            out.add(strip_accents(m.group(1)).strip()[:1].lower())
    return out


# ---------------------------------------------------------------- keeping the author's identity out of the index
@functools.lru_cache(maxsize=None)
def own_identity() -> dict:
    """The repository author's name and the repository's owner handle, read from CITATION.cff at build time.
    Used only to keep them OUT of the index and its committed data (never hard-coded here)."""
    out = {"given": "", "family": "", "owner": "", "repo": ""}
    cff = REPO / "CITATION.cff"
    if not cff.exists():
        return out
    txt = cff.read_text(encoding="utf-8")
    g = re.search(r"given-names:\s*\"?([^\"\n]+)", txt)
    f = re.search(r"family-names:\s*\"?([^\"\n]+)", txt)
    u = re.search(r"repository-code:\s*\"?https?://(?:www\.)?github\.com/([^/\"\s]+)/([^/\"\s]+)", txt)
    if g:
        out["given"] = g.group(1).strip()
    if f:
        out["family"] = f.group(1).strip()
    if u:
        out["owner"], out["repo"] = u.group(1), re.sub(r"\.git$", "", u.group(2))
    return out


def _own_name_rx():
    me = own_identity()
    if not (me["given"] and me["family"]):
        return None
    first, fam = re.escape(me["given"].split()[0]), re.escape(me["family"])
    return re.compile(rf"(?i)\b{first}\b(?:\s+[A-Z]\.?)*\s+{fam}\b")


def own_leak_patterns() -> list:
    """(label, regex) pairs for what must never appear in a committed index file."""
    me = own_identity()
    pats = [("a local filesystem path", re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[a-z][A-Za-z0-9._-]*/"))]
    rx = _own_name_rx()
    if rx:
        pats.append(("the repository author's name", rx))
        pats.append(("the repository author's first name as a possessive",
                     re.compile(rf"\b{re.escape(me['given'].split()[0])}(?:'{{1,2}}|\u2019)s\b")))
    if me["owner"]:
        pats.append(("the repository owner's handle", re.compile(rf"(?i)\b{re.escape(me['owner'])}\b")))
    return pats


def mentions_own_repository(text: str) -> bool:
    me = own_identity()
    return bool(me["owner"]) and re.search(rf"(?i)github\.com/{re.escape(me['owner'])}/", text) is not None


def scrub_text(s: str) -> str:
    """Replace the repository URL, the owner handle, the author's name and local paths with neutral placeholders."""
    me = own_identity()
    if me["owner"]:
        s = re.sub(rf"(?i)https?://(?:www\.)?github\.com/{re.escape(me['owner'])}/[^\s)\]}}\"',;]*", "[this repository]", s)
        s = re.sub(rf"(?i)\b{re.escape(me['owner'])}\b", "[repository owner]", s)
    rx = _own_name_rx()
    if rx:
        s = rx.sub("[repository author]", s)
        s = re.sub(rf"\b{re.escape(me['given'].split()[0])}(?:'{{1,2}}|\u2019)s\b", "the author's", s)
    return re.sub(r"/Users/[A-Za-z0-9._-]+/|/home/[a-z][A-Za-z0-9._-]*/", "~/", s)


def is_own_author(a: dict) -> bool:
    """True for an author record that is the repository's own author (family name + compatible initial, or the
    full name written in one field, as some publishers do)."""
    fam, given = a.get("family") or "", a.get("given") or ""
    if norm_family(fam) in own_author_families() and (not given or strip_accents(given)[:1].lower() in own_author_given_initials()):
        return True
    rx = _own_name_rx()
    full = re.sub(r"\s+", " ", f"{given} {fam} {a.get('name') or ''}".replace("\xa0", " "))
    return bool(rx and rx.search(full))


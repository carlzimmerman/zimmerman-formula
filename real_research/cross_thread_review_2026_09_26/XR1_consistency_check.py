#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR1 -- CROSS-LANE CONSISTENCY CHECK for the dark-sector / vacuum-gate construction lanes.

WHAT IT DOES.  Reads XR1_registry.json (every stage that feeds a headline verdict: its switch cell (p, x_c0), a0 footing,
kernel, phantom operator, gate variable, carrier, epoch and imports) and re-derives the load-bearing attributes from the
SOURCE (ast / regex -- nothing is executed or imported) and from results JSON (committed version via `git show HEAD:`,
falling back to the working tree only for untracked pending lanes).  Then, per headline verdict, it asks whether all
contributing stages share cell, footing, kernel, operator, gate variable and epoch, and prints a mismatch table.

WHY.  L381's Harvey step ran with L370's default switch cell (SW_DEF = "p1_x1.5") while importing particle-mesh retentions
computed at p = 2, x_c0 = 2 (withdrawn, 3151d88f2); the same inheritance then showed up in L373 and AT3.  The cell is set
in one file and consumed three imports away, so it has to be traced in the code, not read from docstrings.

CHECKS (rc = 0 iff all hold)
  D   every derivable registry attribute equals what the source / JSON gives now (registry drift -> rc = 1);
  E   the task's known claims hold in the code (L373 p2_x2.0 in PM and Harvey; the L388 chain p1_x2.5 throughout; AT3's
      current source at p1_x2.5; DE3's cell) and in the results JSON (DE1 F1, DE2 W2/window, DE3 x_lens, L380/L381/L364);
  C1  CONTROL: the known L381 mismatch is detected from the source (cells {p1_x1.5, p2_x2.0}), not from the registry;
  C2  CONTROL (negative): the same-cell chains (L388+L389+L390, L373) are NOT flagged for a cell conflict;
  C3  no cell override sits inside an `if __name__ == "__main__"` block of a spawn-started Pool script.
REPORTED (never change rc): the per-verdict flag table (CELL-CONFLICT, CELL-EXCLUDED, CELL-OMITTED, FOOTING-PARTIAL,
  KERNEL-MIXED, EPOCH-MIXED, CARRIER-MIXED, OPERATOR-MIXED, GATEVAR-MIXED), source/output freshness, SW_DEF consumers,
  downstream uses.
MUTATE=1 corrupts one registry entry in memory (L381's Harvey cell set to p2_x2.0, as if someone had papered over the
  mismatch): check D must catch it and the script must exit 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR1_consistency_check.py
(read-only everywhere; single-threaded; a few seconds)
"""
import ast, json, os, re, subprocess, sys, time, hashlib, glob

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
REG = json.load(open(os.path.join(HERE, "XR1_registry.json")))
ST, V, CROSS = REG["stages"], REG["verdicts"], REG["cross"]
P = print
FAIL = []                                                    # (check, message): any entry -> rc = 1


def fail(tag, msg):
    FAIL.append((tag, msg)); P(f"  ** {tag}: {msg}")


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


# ------------------------------------------------------------------------------------------------ file access (read-only)
_SRC, _AST = {}, {}


def src(path):
    if path not in _SRC:
        fp = os.path.join(REPO, path)
        _SRC[path] = open(fp, encoding="utf-8", errors="replace").read() if os.path.exists(fp) else None
    return _SRC[path]


def tree(path):
    if path not in _AST:
        s = src(path)
        try:
            _AST[path] = ast.parse(s) if s is not None else None
        except SyntaxError as e:
            _AST[path] = e
    t = _AST[path]
    if isinstance(t, SyntaxError) or t is None:
        raise RuntimeError(f"cannot parse {path}: {t}")
    return t


def line_of(path, pat):
    s = src(path)
    if s is None:
        return None
    for i, ln in enumerate(s.splitlines(), 1):
        if pat in ln:
            return i
    return None


def git_state(path):
    if not os.path.exists(os.path.join(REPO, path)):
        return "absent"
    r = subprocess.run(["git", "status", "--porcelain", "--", path], cwd=REPO, capture_output=True, text=True).stdout.strip()
    return "committed" if not r else ("untracked" if r.startswith("??") else "modified")


_JS = {}


def jload(path):
    """committed JSON (git show HEAD:path); the working tree only for untracked files.  Returns (data, origin)."""
    if path in _JS:
        return _JS[path]
    st = git_state(path)
    out = (None, "absent")
    if st in ("committed", "modified"):
        r = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO, capture_output=True, text=True)
        if r.returncode == 0:
            out = (json.loads(r.stdout), "HEAD" + (" (working tree modified)" if st == "modified" else ""))
    elif st == "untracked":
        out = (json.load(open(os.path.join(REPO, path))), "working tree (untracked, pending lane)")
    _JS[path] = out
    return out


def jpath(d, path):
    for k in path:
        d = d[k]
    return d


def cellname(p, x):
    return f"p{float(p):g}_x{float(x):.1f}"


def parse_cell_text(s):
    m = re.search(r"p\s*=\s*([\d.]+),\s*x_c0\s*=\s*([\d.]+)", s)
    return cellname(m.group(1), m.group(2)) if m else None


# ------------------------------------------------------------------------------------------------ ast helpers
def const(node, consts=None):
    try:
        return ast.literal_eval(node)
    except Exception:
        if consts is not None and isinstance(node, ast.Name) and node.id in consts:
            return consts[node.id]
        raise


def module_consts(path):
    """top-level NAME = literal (tuple unpacking included)."""
    out = {}
    for n in tree(path).body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                try:
                    if isinstance(t, ast.Name):
                        out[t.id] = const(n.value)
                    elif isinstance(t, ast.Tuple) and isinstance(n.value, ast.Tuple) and len(t.elts) == len(n.value.elts):
                        for a, b in zip(t.elts, n.value.elts):
                            if isinstance(a, ast.Name):
                                try:
                                    out[a.id] = const(b)
                                except Exception:
                                    pass
                except Exception:
                    pass
    return out


def placed_assignments(path):
    """every assignment in the file with its placement: 'top' (module body), 'main' (inside if __name__ == '__main__'),
    'def' (inside a function), 'block' (other module-level block)."""
    res = []

    def walk(node, where):
        for ch in ast.iter_child_nodes(node):
            w = where
            if isinstance(ch, ast.If) and "__name__" in ast.unparse(ch.test) and "__main__" in ast.unparse(ch.test):
                w = "main"
            elif isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                w = "def"
            elif isinstance(ch, (ast.If, ast.For, ast.While, ast.With, ast.Try)) and where == "top":
                w = "block"
            if isinstance(ch, ast.Assign):
                for t in ch.targets:
                    for e in (t.elts if isinstance(t, ast.Tuple) else [t]):
                        val = None
                        if isinstance(t, ast.Tuple) and isinstance(ch.value, ast.Tuple) and len(t.elts) == len(ch.value.elts):
                            val = ch.value.elts[t.elts.index(e)]
                        elif not isinstance(t, ast.Tuple):
                            val = ch.value
                        res.append(dict(target=e, value=val, full_value=ch.value, lineno=ch.lineno, where=where))
            walk(ch, w)
    walk(tree(path), "top")
    return res


def target_str(e):
    try:
        return ast.unparse(e)
    except Exception:
        return "?"


def uses_spawn_pool(path):
    s = src(path) or ""
    return ("Pool(" in s) and ('get_context("fork")' not in s) and ("set_start_method(\"fork\"" not in s)


# ------------------------------------------------------------------------------------------------ derivations
def d_sw_def(spec):
    c = module_consts(spec["file"])
    v, table = c.get("SW_DEF"), c.get("SWITCH", {})
    if v not in table:
        raise RuntimeError(f"SW_DEF {v!r} not in SWITCH table of {spec['file']}")
    p, x = table[v]
    if cellname(p, x) != v:
        raise RuntimeError(f"SW_DEF key {v} does not match its (p, x_c0) = {table[v]}")
    return v, f"{spec['file']}:{line_of(spec['file'], 'SW_DEF = ')} SW_DEF = {v!r}"


def sw_assignments(path):
    """assignments that bind SW_DEF in a file: ('unpack', line) for the tuple-unpack from L70/L's namespace, ('set', value,
    line) for anything else."""
    out = []
    for a in placed_assignments(path):
        e = a["target"]
        name = e.id if isinstance(e, ast.Name) else (ast.literal_eval(e.slice) if isinstance(e, ast.Subscript) and isinstance(e.slice, ast.Constant) else None)
        if name != "SW_DEF":
            continue
        fv = a["full_value"]
        if isinstance(fv, ast.GeneratorExp) or (isinstance(fv, ast.Subscript) and "SW_DEF" in ast.unparse(fv)):
            out.append(("unpack", a["lineno"], a["where"]))
        else:
            out.append(("set", a["value"], a["lineno"], a["where"]))
    return out


def d_sw_inherit(spec):
    base, bev = derive(spec["base"])
    sets = [s for s in sw_assignments(spec["file"]) if s[0] == "set"]
    unp = [s for s in sw_assignments(spec["file"]) if s[0] == "unpack"]
    if sets:
        consts = module_consts(spec["file"])
        v = const(sets[-1][1], consts)
        return v, f"{spec['file']}:{sets[-1][2]} SW_DEF set to {v!r} (overrides the inherited value)"
    if not unp:
        raise RuntimeError(f"{spec['file']}: no SW_DEF binding found")
    return base, f"{spec['file']}:{unp[0][1]} SW_DEF unpacked from L370's namespace, never reassigned -> {base!r}  [{bev}]"


def d_reps_adapter(spec):
    t = tree(spec["file"])
    fn = next((n for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and n.name == spec["func"]), None)
    if fn is None:
        raise RuntimeError(f"{spec['file']}: function {spec['func']} not found")
    strs = []
    for n in ast.walk(fn):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            strs.append((n.value, getattr(n, "lineno", fn.lineno)))
    hits = [(s, ln) for s, ln in strs if re.search(r"SW_DEF\s*=", s) or "SWITCH" in s]
    if hits:
        if not spec.get("cell_const"):
            raise RuntimeError(f"{spec['file']}: adapter inserts SW_DEF but no cell_const is registered")
        v = module_consts(spec["file"])[spec["cell_const"]]
        return v, f"{spec['file']}:{hits[0][1]} adapter inserts 'SW_DEF = <cell>' into L371's source; job cell {spec['cell_const']} = {v!r}"
    base, bev = derive(spec["base"])
    return base, f"{spec['file']}:{fn.lineno} {spec['func']}(): none of its {len(strs)} string constants (the source replacements) mentions SW_DEF/SWITCH -> inherits {base!r}  [{bev}]"


def d_module_cell(spec):
    c = module_consts(spec["file"])
    p, x = c[spec["p"]], c[spec["x"]]
    base = cellname(p, x)
    ev = [f"{spec['file']}:{line_of(spec['file'], spec['x'] + ', ' + spec['p']) or line_of(spec['file'], spec['p'])} {spec['p']} = {p}, {spec['x']} = {x}"]
    eff = {"p": p, "x": x}
    hazards = []
    for imp in spec.get("importers", []):
        for a in placed_assignments(imp):
            e = a["target"]
            if isinstance(e, ast.Attribute) and e.attr in (spec["p"], spec["x"]):
                try:
                    v = const(a["value"])
                except Exception:
                    v = "?"
                key = "p" if e.attr == spec["p"] else "x"
                ev.append(f"{imp}:{a['lineno']} {target_str(e)} = {v!r} [{a['where']}]")
                if a["where"] == "top":
                    eff[key] = v
                elif a["where"] == "main" and uses_spawn_pool(imp):
                    hazards.append(f"{imp}:{a['lineno']} override inside __main__ guard of a spawn-Pool script: workers keep {base}")
                else:
                    eff[key] = v
    for h in hazards:
        fail("C3", h)
    return cellname(eff["p"], eff["x"]), "; ".join(ev)


def d_g_assign(spec):
    t = tree(spec["file"])
    fn = next((n for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and n.name == spec["func"]), None)
    if fn is None:
        raise RuntimeError(f"{spec['file']}: {spec['func']} not found")
    g_line, swk_ok = None, False
    for n in ast.walk(fn):
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Subscript) and isinstance(tg.slice, ast.Constant) and tg.slice.value == "SW_DEF":
                    g_line = n.lineno
                if isinstance(tg, ast.Name) and tg.id == "SWK" and isinstance(n.value, ast.JoinedStr):
                    u = ast.unparse(n.value)
                    swk_ok = ("P_GATE" in u and "X_C0" in u)
    if g_line and swk_ok:
        v, ev = derive(spec["mesh"])
        return v, f"{spec['file']}:{g_line} G['SW_DEF'] = SWK built from the mesh module's P_GATE/X_C0 -> {v!r}  [{ev}]"
    v, ev = d_sw_def({"file": ST["L370.harvey"]["file"]})
    return v, f"{spec['file']}: no G['SW_DEF'] assignment in {spec['func']}() -> L370 default {v!r}"


def d_exec_slice(spec):
    s72 = src(spec["src"])
    i0, i1 = s72.index(spec["start"]), s72.index(spec["end"])
    sl = s72[i0:i1]
    if not re.search(r"SW_DEF\b.*=\s*\(L70\[k\]", sl.replace("\n", " ")) and "SW_DEF, Grid, phantom_felt = (L70[k]" not in sl:
        raise RuntimeError(f"{spec['src']}: the executed slice no longer unpacks SW_DEF from L70")
    base, bev = derive(spec["base"])
    t = tree(spec["file"])
    consts = module_consts(spec["file"])
    exec_line = None
    for n in ast.walk(t):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "exec" and len(n.args) >= 2 \
                and isinstance(n.args[1], ast.Name) and n.args[1].id == spec["ns"]:
            exec_line = n.lineno
    ov, table_add = None, []
    for a in placed_assignments(spec["file"]):
        e = a["target"]
        if isinstance(e, ast.Subscript) and isinstance(e.value, ast.Name) and e.value.id == spec["ns"] \
                and isinstance(e.slice, ast.Constant) and e.slice.value == "SW_DEF":
            ov = (const(a["value"], consts), a["lineno"])
        if isinstance(e, ast.Subscript) and "SWITCH" in ast.unparse(e):
            try:
                table_add.append(const(e.slice, consts))
            except Exception:
                pass
    if ov is None:
        return base, f"{spec['file']}:{exec_line} exec of {os.path.basename(spec['src'])} slice binds SW_DEF from L70; no {spec['ns']}['SW_DEF'] override -> {base!r}  [{bev}]"
    v, ln = ov
    if exec_line is not None and ln < exec_line:
        raise RuntimeError(f"{spec['file']}:{ln} override precedes the exec at line {exec_line}: the slice would reset it to {base}")
    table70 = module_consts(ST["L370.harvey"]["file"]).get("SWITCH", {})
    if v not in table70 and v not in table_add:
        raise RuntimeError(f"{spec['file']}: override {v!r} is not in L370's SWITCH table and is never added")
    return v, f"{spec['file']}:{ln} {spec['ns']}['SW_DEF'] = {v!r} after the exec at line {exec_line} (SWITCH entry added: {v in table_add})"


def d_shear_key(spec):
    cells = sorted({cellname(a, b) for a, b in re.findall(r'TM\[f"p=([\d.]+), x_c0=([\d.]+)/', src(spec["file"]))})
    if len(cells) != 1:
        raise RuntimeError(f"{spec['file']}: shear keys {cells}")
    return cells[0], f"{spec['file']}:{line_of(spec['file'], 'TM[f\"p=')} shear gate reads L364 T_max key {cells[0]}"


def d_json_cell(spec):
    d, origin = jload(spec["file"])
    if d is None:
        return "absent", f"{spec['file']} absent"
    c = jpath(d, spec["path"])
    return cellname(c["p"], c["x_c0"]), f"{spec['file']} [{origin}] cell p = {c['p']}, x_c0 = {c['x_c0']}, x_lens = {c.get('x_lens')}"


def d_str_const_cell(spec):
    v = module_consts(spec["file"])[spec["name"]]
    return parse_cell_text(v), f"{spec['file']}:{line_of(spec['file'], spec['name'] + ',') or line_of(spec['file'], spec['name'] + ' =')} {spec['name']} = {v!r}"


def d_cell_in_line(spec):
    ln = line_of(spec["file"], spec["pattern"])
    if ln is None:
        raise RuntimeError(f"{spec['file']}: pattern not found")
    return parse_cell_text(src(spec["file"]).splitlines()[ln - 1]), f"{spec['file']}:{ln}"


def d_row_cells(spec):
    ln = line_of(spec["file"], spec["pattern"])
    if ln is None:
        raise RuntimeError(f"{spec['file']}: pattern not found")
    txt = src(spec["file"]).splitlines()[ln - 1]
    return sorted({cellname(a, b) for a, b in re.findall(r"p=([\d.]+), x_c0=([\d.]+)", txt)}), f"{spec['file']}:{ln}"


def d_switch_table(spec):
    t = module_consts(spec["file"])["SWITCH"]
    return sorted(t), f"{spec['file']}:{line_of(spec['file'], 'SWITCH = {')} SWITCH keys {sorted(t)}"


def d_a0_in_lines(spec):
    feet, lines = set(), []
    for i, ln in enumerate(src(spec["file"]).splitlines(), 1):
        if spec["contains"] in ln:
            f = re.findall(r'A0K?\[["\'](canonical|alt)["\']\]', ln)
            if f:
                feet |= set(f); lines.append(i)
    order = [f for f in ("canonical", "alt") if f in feet]
    return order, f"{spec['file']}: lines {lines[:6]}{'...' if len(lines) > 6 else ''} use {order}"


def d_signature(spec):
    miss = [s for s in spec["all"] if line_of(spec["file"], s) is None]
    if miss:
        raise RuntimeError(f"{spec['file']}: signature missing {miss}")
    return spec.get("id", "__confirmed__"), f"{spec['file']}:{line_of(spec['file'], spec['all'][0])}"


def d_literal(spec):
    ln = line_of(spec["file"], spec["pattern"])
    if ln is None:
        raise RuntimeError(f"{spec['file']}: literal not found")
    return spec["value"], f"{spec['file']}:{ln}"


DERIV = dict(sw_def=d_sw_def, sw_inherit=d_sw_inherit, reps_adapter=d_reps_adapter, module_cell=d_module_cell,
             g_assign=d_g_assign, exec_slice=d_exec_slice, shear_key=d_shear_key, json_cell=d_json_cell,
             str_const_cell=d_str_const_cell, cell_in_line=d_cell_in_line, row_cells=d_row_cells, switch_table=d_switch_table,
             a0_in_lines=d_a0_in_lines, signature=d_signature, literal=d_literal)


def derive(spec):
    return DERIV[spec["kind"]](spec)


# ================================================================================================================ run
P(__doc__.split("CHECKS")[0].strip())
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
P(f"\n  registry inspected {REG['inspected_at']} at {REG['git_head'][:9]}; now HEAD {head}; {len(ST)} stages, {len(V)} verdicts")
if MUTATE:
    P("\n  *** MUTATE=1: the registry's L381 Harvey cell is corrupted to 'p2_x2.0' in memory (hides the known mismatch); "
      "check D must fail and rc must be 1 ***")
    ST["L381.harvey"]["cell"] = "p2_x2.0"

banner("FILES: git state and hash against the registry snapshot (informational -- lanes are being edited live)")
changed = []
for p, meta in sorted(REG["files"].items()):
    fp = os.path.join(REPO, p)
    h = hashlib.sha256(open(fp, "rb").read()).hexdigest() if os.path.exists(fp) else None
    st = git_state(p)
    if h != meta["sha256"] or st != meta["git"]:
        changed.append(p)
        P(f"    changed since registry: {p}  [{meta['git']} -> {st}]")
P(f"    {len(REG['files']) - len(changed)}/{len(REG['files'])} files identical to the snapshot")
for p in CROSS["absent_expected"]:
    P(f"    expected absent (stopped, not committed): {p} -> {'absent' if not os.path.exists(os.path.join(REPO, p)) else 'PRESENT'}")

banner("D  REGISTRY vs SOURCE: every derivable attribute re-derived from the code / results JSON")
EFF = {}                                                     # stage -> effective attributes (derived where derivable)
EVID = {}                                                    # stage -> {attr: evidence string with file:line}
SRCOF = {}                                                   # stage -> {attr: 'derived'|'registry'}
for sid, s in ST.items():
    eff = {k: s.get(k) for k in ("cell", "rows", "footing", "kernel", "operator", "gate_variable")}
    how = {k: "registry" for k in eff}
    for attr, spec in s.get("derive", {}).items():
        try:
            val, ev = derive(spec)
        except Exception as e:                               # a stage we cannot verify is a failure of D
            fail("D", f"{sid}.{attr}: cannot derive ({e})")
            continue
        if attr == "operator_sig":
            P(f"    {sid:20s} operator signature present  [{ev}]")
            continue
        reg = s.get(attr)
        if val == "__confirmed__":
            P(f"    {sid:20s} {attr:13s} = {reg!s:24s} signature confirmed  [{ev}]")
            how[attr] = "derived"
            continue
        EVID.setdefault(sid, {})[attr] = ev
        same = (sorted(val) == sorted(reg)) if isinstance(val, list) and isinstance(reg, list) else (val == reg)
        if same:
            P(f"    {sid:20s} {attr:13s} = {val!s:24s} OK  [{ev}]")
        else:
            fail("D", f"{sid}.{attr}: registry says {reg!r}, source gives {val!r}  [{ev}]")
        eff[attr] = val; how[attr] = "derived"
    EFF[sid], SRCOF[sid] = eff, how

banner("E  THE TASK'S KNOWN CLAIMS, verified in code and results JSON")
for eid, ex in CROSS["expect"].items():
    got = {sid: EFF[sid]["cell"] for sid in ex["stages"]}
    ok = all(v == ex["cell"] for v in got.values()) and all(SRCOF[sid]["cell"] == "derived" for sid in ex["stages"])
    P(f"  [{'PASS' if ok else 'FAIL'}] {eid}: expected {ex['cell']} in {ex['stages']}; derived {got}")
    if not ok:
        fail("E", f"{eid}: {got}")
for c in CROSS["json_claims"]:
    try:
        if c["kind"] == "de1_f1":
            d, origin = jload(c["file"])
            rows = [r for r in d["numbers"]["F1"] if r["foot"] == c["foot"] and abs(r["lMb"] - c["lMb"]) < 1e-9]
            fails = [r["shift_dex"] != 0.0 for r in rows]
            ok = bool(rows) and all(f == c["expect_fail"] for f in fails)
            msg = "; ".join(f"{r['kernel']}: shift {r['shift_dex']:+.3f} dex, edge {r['re_kpc']:.1f} vs r_flag {r['rflag_kpc']:.1f} kpc" for r in rows)
            wd = subprocess.run(["git", "diff", "--quiet", "--", c["file"]], cwd=REPO).returncode
            if wd:
                wt = json.load(open(os.path.join(REPO, c["file"])))["numbers"]["F1"]
                wk = sorted({r["kernel"] for r in wt})
                msg += f"  | working tree (uncommitted) kernels {wk}: " + "; ".join(
                    f"{r['kernel']} {r['shift_dex']:+.3f}" for r in wt if r["foot"] == c["foot"] and abs(r["lMb"] - c["lMb"]) < 1e-9)
        elif c["kind"] == "check_measured":
            d, origin = jload(c["file"])
            k = next(k for k in d["checks"] if k.startswith(c["check_prefix"]))
            ok = d["checks"][k]["ok"] and c["contains"] in d["checks"][k]["measured"]; msg = d["checks"][k]["measured"]
        elif c["kind"] == "text":
            ln = line_of(c["file"], c["contains"]) or line_of(c["alt_file"], c["alt_contains"])
            ok = ln is not None; msg = f"found at line {ln}"; origin = "source/README"
        elif c["kind"] == "number":
            d, origin = jload(c["file"]); v = jpath(d, c["path"]); ok = abs(v - c["value"]) <= c["tol"]; msg = f"{v}"
        elif c["kind"] == "list":
            d, origin = jload(c["file"]); v = jpath(d, c["path"]); ok = v == c["value"]; msg = f"{v}"
        elif c["kind"] == "keys":
            d, origin = jload(c["file"]); v = list(jpath(d, c["path"]).keys()); ok = sorted(v) == sorted(c["value"]); msg = f"{v}"
        P(f"  [{'PASS' if ok else 'FAIL'}] {c['id']} ({os.path.basename(c['file'])}, {origin}): {msg}")
        if not ok:
            fail("E", c["id"])
    except Exception as e:
        fail("E", f"{c['id']}: {e}")

# ------------------------------------------------------------------------------------------------ cross-lane exclusions
d1, _ = jload(CROSS["flagship_exclusions"]["file"])
EXCL = {}
bad = [r for r in d1["numbers"]["F1"] if r["shift_dex"] != 0.0]
if bad:
    EXCL[CROSS["flagship_exclusions"]["cell"]] = sorted({f"{r['foot']} M_b 1e{r['lMb']:g}" for r in bad})

# ================================================================================================================ verdicts
KNORM = {"nu_mono": "nu_mono", "nu_RAR": "nu_RAR", "generated(nu_mono)": "nu_mono",
         "nu_mono (committed edge) / per-kernel (working tree)": "nu_mono", "nu_RAR+nu_mono": "both", "n/a": None}
SEV = ["CELL-CONFLICT", "CELL-EXCLUDED", "CELL-OMITTED", "FOOTING-PARTIAL", "KERNEL-MIXED", "EPOCH-MIXED", "CARRIER-MIXED",
       "OPERATOR-MIXED", "GATEVAR-MIXED"]


def analyse(vid, eff_of):
    v = V[vid]
    flags, detail = {}, {}
    sts = [(sid, ST[sid], eff_of[sid]) for sid in v["stages"]]
    sw = [(sid, s, e) for sid, s, e in sts if s.get("switch_dependent", True)]
    explicit = {e["cell"]: sid for sid, s, e in sw if e["cell"] not in ("none", "per-row", "n/a", None, "absent")}
    cells_by_stage = {sid: e["cell"] for sid, s, e in sw}
    rows = [set(e.get("rows") or []) for sid, s, e in sw if e["cell"] == "per-row"]
    none = [sid for sid, s, e in sw if e["cell"] == "none"]
    ex_cells = sorted(explicit)
    if len(ex_cells) > 1:
        flags["CELL-CONFLICT"] = ", ".join(f"{sid}={c}" for sid, c in cells_by_stage.items() if c in ex_cells)
    elif ex_cells and rows and any(ex_cells[0] not in r for r in rows if not any(" " in x for x in r)):
        flags["CELL-CONFLICT"] = f"fixed {ex_cells[0]} vs per-row stages"
    if none and (ex_cells or rows):
        flags["CELL-OMITTED"] = ", ".join(none) + f" run without the switch while {', '.join(ex_cells) or 'per-row cells'} is claimed"
    if len(ex_cells) == 1 and ex_cells[0] in EXCL:
        flags["CELL-EXCLUDED"] = f"{ex_cells[0]} fails the flat-a0 flagship (DE1 F1: {', '.join(EXCL[ex_cells[0]])})"
    fsets = {sid: tuple(e["footing"]) for sid, s, e in sts if isinstance(e["footing"], list)}
    if fsets and len(set(fsets.values())) > 1:
        flags["FOOTING-PARTIAL"] = "; ".join(f"{sid} {'/'.join(f)}" for sid, f in fsets.items() if len(f) == 1)
    ks = {sid: KNORM.get(e["kernel"], e["kernel"]) for sid, s, e in sts}
    single = {k for k in ks.values() if k not in (None, "both")}
    if len(single) > 1:
        grp = {}
        for sid, k in ks.items():
            if k not in (None, "both"):
                grp.setdefault(k, []).append(sid)
        flags["KERNEL-MIXED"] = "; ".join(f"{k}: {', '.join(v_)}" for k, v_ in sorted(grp.items(), key=lambda kv: len(kv[1])))
    ep = [f"{sid}: {i['quantity']} from {i['from_stage']} computed at z = {i['computed_z']} used at z = {i['used_z']}"
          for sid, s, e in sts for i in s.get("imports", []) if i.get("computed_z") != i.get("used_z")]
    if ep:
        flags["EPOCH-MIXED"] = "; ".join(ep)
    tr = {}
    for sid, s, e in sts:
        if s.get("trigger", "n/a") != "n/a":
            tr.setdefault(s["trigger"], []).append(sid)
    if len(tr) > 1:
        flags["CARRIER-MIXED"] = "; ".join(f"{t}: {', '.join(v_)}" for t, v_ in tr.items())
    ops = {}
    for sid, s, e in sts:
        if s.get("operator_relevant", True) and e["operator"] not in ("none", None):
            for o in e["operator"].split("+"):
                ops.setdefault(o, []).append(sid)
    if len(ops) > 1:
        flags["OPERATOR-MIXED"] = "; ".join(f"{o}: {', '.join(v_)}" for o, v_ in ops.items())
    gv = {}
    for sid, s, e in sw:
        if e["cell"] not in ("none", "n/a") and e["gate_variable"] not in ("n/a", None):
            gv.setdefault(e["gate_variable"], []).append(sid)
    if len(gv) > 1:
        flags["GATEVAR-MIXED"] = "; ".join(f"{g}: {', '.join(v_)}" for g, v_ in gv.items())
    return flags, sorted(set(cells_by_stage.values()) - {"none"})


banner("THE MISMATCH TABLE (one row per headline verdict; flags in severity order; cells from the SOURCE where derivable)")
ABBR = {"CELL-CONFLICT": "CELL!", "CELL-EXCLUDED": "EXCL", "CELL-OMITTED": "omit", "FOOTING-PARTIAL": "foot", "KERNEL-MIXED": "kern",
        "EPOCH-MIXED": "epoch", "CARRIER-MIXED": "carr", "OPERATOR-MIXED": "op", "GATEVAR-MIXED": "gvar"}
RES = {}
P(f"  {'verdict':11s} {'status':44s} {'cells (switch-dependent stages)':34s} flags")
for vid, v in V.items():
    flags, cells = analyse(vid, EFF)
    RES[vid] = flags
    st = v["status"].split(" (")[0].split(":")[0]
    fl = " ".join(ABBR[k] for k in SEV if k in flags) or "-"
    P(f"  {vid:11s} {v['status'][:44]:44s} {', '.join(cells)[:34]:34s} {fl}")
P("  key: CELL! = stages at different (p, x_c0); EXCL = cell fails DE1's flagship; omit = a switch-dependent stage run switch-free;"
  "\n       foot = single-footing stage in a two-footing verdict; kern = nu_mono vs nu_RAR; epoch = imported at one z, used at "
  "another;\n       carr = carrier trigger differs between stages (matter-only vs phantom-inclusive x~, or an imposed core shape);"
  "\n       op = different phantom operators; gvar = different switch-variable conventions")

banner("DETAIL, live and pending verdicts first (WITHDRAWN/SUPERSEDED listed for the record)")
order = sorted(V, key=lambda k: (0 if V[k]["status"].startswith(("STANDS", "SCOPED", "PENDING")) else 1,
                                 min([SEV.index(f) for f in RES[k]] or [99])))
for vid in order:
    if not RES[vid]:
        continue
    P(f"\n  {vid} -- {V[vid]['claim']}\n    status: {V[vid]['status']}  [{V[vid]['status_source']}]")
    for k in SEV:
        if k in RES[vid]:
            P(f"    {k:15s} {RES[vid][k]}")
    if any(k in RES[vid] for k in ("CELL-CONFLICT", "CELL-OMITTED", "CELL-EXCLUDED")):
        for sid in V[vid]["stages"]:
            if not ST[sid].get("switch_dependent", True):
                continue
            ev = EVID.get(sid, {}).get("cell") or EVID.get(sid, {}).get("rows")
            if not ev:
                ev = "; ".join(f"{e['file']}:{line_of(e['file'], e['pattern'])}" for e in ST[sid].get("evidence", [])[:2]) + " (registry)"
            P(f"      cell of {sid:18s} {str(EFF[sid]['cell'] if EFF[sid]['cell'] != 'per-row' else EFF[sid].get('rows')):26s} <- {ev[:190]}")

banner("CONTROLS")
f81, c81 = analyse("L381", EFF)
derived81 = all(SRCOF[s]["cell"] == "derived" for s in V["L381"]["stages"])
ok1 = "CELL-CONFLICT" in f81 and set(c81) == {"p1_x1.5", "p2_x2.0"} and derived81
P(f"  [{'PASS' if ok1 else 'FAIL'}] C1 CONTROL: L381's mismatch detected from the source: cells {c81}, both derived: {derived81}")
P(f"         L381.harvey: {EFF['L381.harvey']['cell']} (L381 harvey() -> L371 -> L370 SW_DEF);  L380.pm: {EFF['L380.pm']['cell']} (L377 constants, no override in L379/L380)")
if not ok1:
    fail("C1", f"L381 not flagged: {f81}")
if MUTATE:
    reg_only = {sid: dict(EFF[sid], cell=ST[sid]["cell"]) for sid in ST}
    fm, cm = analyse("L381", reg_only)
    P(f"         (MUTATE) trusting the corrupted registry alone would give cells {cm} and flags {sorted(fm) or 'none'} for L381 "
      f"-- the mismatch would be hidden; check D is what catches it")
for vid in ("L388_chain", "L373"):
    fx, cx = analyse(vid, EFF)
    ok2 = "CELL-CONFLICT" not in fx
    P(f"  [{'PASS' if ok2 else 'FAIL'}] C2 CONTROL (negative): {vid} has no cell conflict: cells {cx}; other flags {sorted(fx) or 'none'}")
    if not ok2:
        fail("C2", f"{vid}: {fx.get('CELL-CONFLICT')}")

banner("C3  SPAWN SAFETY: cell overrides of imported modules and where they sit (Pool uses 'spawn' on this macOS python)")
hz = 0
lane_files = sorted(set(sum((glob.glob(os.path.join(REPO, "real_research", d, "*.py")) for d in
                             ("dark_sector_2026", "merger_infall_2026", "g03_audit_2026", "generated_phantom_2026",
                              "acceleration_trigger_2026", "dark_energy_2026")), [])))
for fp in lane_files:
    rel = os.path.relpath(fp, REPO)
    try:
        asg = placed_assignments(rel)
    except Exception as e:
        P(f"    (unparsable, skipped) {rel}: {e}")
        continue
    for a in asg:
        e = a["target"]
        nm = e.attr if isinstance(e, ast.Attribute) else (e.slice.value if isinstance(e, ast.Subscript) and isinstance(e.slice, ast.Constant) else None)
        if nm in ("P_GATE", "X_C0", "SW_DEF") and not (isinstance(e, ast.Name)):
            spawn = uses_spawn_pool(rel)
            haz = a["where"] == "main" and spawn
            hz += haz
            P(f"    {rel}:{a['lineno']}  {target_str(e)}  [{a['where']}{', spawn Pool' if spawn else ''}]  {'HAZARD' if haz else 'reaches workers / not in a worker'}")
P(f"  [{'PASS' if hz == 0 else 'FAIL'}] C3 no switch-cell override inside a __main__ guard of a spawn-Pool script ({hz} found)")
if hz:
    fail("C3", f"{hz} spawn hazards")

banner("SW_DEF CONSUMERS: every script that executes L370's machinery, and the cell its Harvey/lensing maps actually use")
for fp in sorted(glob.glob(os.path.join(REPO, "real_research", "*", "*.py"))):
    rel = os.path.relpath(fp, REPO)
    s = src(rel) or ""
    if "L370_boosted_infall_mergers" not in s or "cross_thread_review" in rel:
        continue
    sids = [sid for sid, st_ in ST.items() if st_["file"] == rel and sid.endswith((".harvey", ".elgordo"))]
    cells = sorted({EFF[x]["cell"] for x in sids}) or ["(reads results only / not a registered stage)"]
    P(f"    {rel}: {', '.join(cells)}")

banner("FRESHNESS: is the output on disk from the source on disk? (informational)")
for rel in CROSS["freshness"]:
    fp = os.path.join(REPO, rel)
    if not os.path.exists(fp):
        P(f"    {rel}: absent"); continue
    base = fp[:-3]
    outs = [x for x in (base + ".out", base + "_results.json") if os.path.exists(x)]
    try:
        doc = ast.get_docstring(tree(rel), clean=False) or ""
    except Exception:
        doc = ""
    pre = doc.split("CHECKS")[0].strip()
    msgs = []
    if os.path.exists(base + ".out"):
        o = open(base + ".out", encoding="utf-8", errors="replace").read().lstrip()
        if pre and not o.startswith(pre):
            k = next((i for i, (a, b) in enumerate(zip(o, pre)) if a != b), min(len(o), len(pre)))
            msgs.append(f"HEADER-MISMATCH: the .out was printed by a different version of the docstring (first difference near "
                        f"\"{pre[max(0, k - 30):k + 40].strip()[:70]}\")")
    for x in outs:
        if os.path.getmtime(fp) > os.path.getmtime(x) + 1:
            msgs.append(f"source newer than {os.path.basename(x)} ({time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(fp)))} > "
                        f"{time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(x)))})")
    P(f"    {rel} [{git_state(rel)}]: " + ("; ".join(msgs) if msgs else "consistent"))
at3j = ST["AT3.harvey"]["file"][:-3] + "_results.json"
if os.path.exists(os.path.join(REPO, at3j)):
    dj = json.load(open(os.path.join(REPO, at3j)))
    keys = sorted({k.split("|")[0] for k in dj["numbers"].get("G1", {})})
    P(f"    AT3 results JSON on disk: y_v0 grid {keys} ({'the FAST grid: SLUG has no _FAST suffix, so a smoke run wrote the main name' if keys == ['0.01', '0.1'] else 'main grid'})")

banner("DOWNSTREAM USES (informational)")
for d in CROSS["downstream"]:
    P(f"    {d['file']}:{line_of(d['file'], d['pattern'])}  {d['note']}")

banner("VERDICT")
n_flag = {k: sum(1 for r in RES.values() if k in r) for k in SEV}
live = [v for v in V if V[v]["status"].startswith(("STANDS", "SCOPED", "PENDING"))]
P(f"  {len(V)} verdicts ({len(live)} live or pending); flagged: " + ", ".join(f"{k} {n}" for k, n in n_flag.items() if n))
P(f"  live verdicts with a CELL-CONFLICT: {[v for v in live if 'CELL-CONFLICT' in RES[v]] or 'none'}; "
  f"with CELL-EXCLUDED: {[v for v in live if 'CELL-EXCLUDED' in RES[v]] or 'none'}")
P(f"  checks D/E/C1/C2/C3: {'all pass' if not FAIL else str(len(FAIL)) + ' failure(s): ' + '; '.join(t for t, _ in FAIL)}   [{time.time() - T0:.1f}s]")
rc = 1 if FAIL else 0
P(f"rc={rc}")
sys.exit(rc)

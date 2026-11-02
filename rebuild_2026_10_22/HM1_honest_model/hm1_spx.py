# HM1: SP3's x, with Gnedin as an option and per-galaxy E for IC 1613. SP3 read only. kappa = 1/2 FITTED, unused; not theory closed.
_tx = open(os.environ["HM1_SP3X"]).read()
_a = '_Mf = contract(_rg, _Mbg, _M0, _Mb / float(_M0[-1]))[0]'; assert _tx.count(_a) == 1
if os.environ.get("HM1_GN"): _tx = _tx.replace(_a, '_Mf = contract(_rg, _Mbg, _M0, _Mb / float(_M0[-1]), gnedin=(0.85, 0.8, _R2))[0]')
_a = '_E.append(math.log10((_r["V"] * 1e3) ** 2 / _Rr) - math.log10(GE * _Mb / _Rr ** 2 + GE * _Mc / _Rr ** 2))'; assert _tx.count(_a) == 1
_tx = _tx.replace(_a, _a + '; _ZO["sp3"].setdefault("ltE", {}).setdefault(_tg, {})[_r["name"]] = _E[-1]')
exec(_tx)

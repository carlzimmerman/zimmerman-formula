import os
os.environ["DW2_CAND"] = "share|0.872|linear"; os.environ["DW2_COLDX"] = "1"
_p = "{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cand_max.py")); _g = dict(__file__=_p, __name__="cand_max"); exec(compile(open(_p).read(), _p, "exec"), _g)
NAME = _g["NAME"]; g = _g["g"]

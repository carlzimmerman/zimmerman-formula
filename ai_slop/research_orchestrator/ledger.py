"""Legacy score ledger retired; original SQLite file remains historical evidence."""
from engine import Store
class Ledger:
    def __init__(self,*args,**kwargs):
        raise RuntimeError('Use engine.Store; legacy scores are unreviewed historical records')

# Symbol identity correction

The first run passed17/18 checks. Its characteristic-polynomial equality
failed because SymPy charpoly replaced the requested real-assumption symbol
with a same-name symbol without those assumptions. A minimal reproduction
showed `p.gen == lam` is false; the printed difference consists of cancelling
terms belonging to distinct symbol identities. The check now uses the exact
determinant det(lam I-A), preserving the intended equality and tolerance.
The initial script, JSON and log remain saved; final runs use the corrected
script hash. This changes no equation, numerical input or verdict criterion.

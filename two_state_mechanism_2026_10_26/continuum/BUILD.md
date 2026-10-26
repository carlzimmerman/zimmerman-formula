# Rebuilding the external scattering dependency

Downloaded public source archives (versions, URLs and hashes in SOFTWARE.json):
UKRmol-in3.3.0, UKRmol-out3.3.0.1. The latter extracts as `ukrmol-out-3.3.0`.
GBTOlib is bundled inside the inner-region archive. We use the shipped source,
not the inconsistent GBTOlib version number on the release webpage.
No source-code physics changes were made to UKRmol+.

Build in a temporary directory. On this macOS ARM machine:

```
cmake -S /private/tmp/ukrmol-build/ukrmol-in-3.3.0 -B /private/tmp/ukrmol-build/build \
  -DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk \
  -DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-15 \
  -DCMAKE_Fortran_COMPILER=/opt/homebrew/bin/gfortran \
  -DCMAKE_Fortran_FLAGS='-fdefault-integer-8 -fallow-argument-mismatch' \
  -DBLAS_LIBRARIES=/opt/homebrew/opt/openblas/lib/libopenblas.dylib \
  -DLAPACK_LIBRARIES=/opt/homebrew/opt/openblas/lib/libopenblas.dylib \
  -DWITH_MPI=OFF -DWITH_GIT=OFF \
  -DUKRMOL_OUT_DIR=/private/tmp/ukrmol-build/ukrmol-out-3.3.0
cmake --build /private/tmp/ukrmol-build/build -j 4
```

The first configure failed because GCC could not find macOS libSystem without
an explicit SDK. A subsequent attempt used the wrong extraction-directory name
for the outer package. Both were corrected; final compilation succeeded.
The default H2+ photoionization integral test timed out after240s. This is not a
benchmark pass. Smaller specified continuum calculations were then attempted.

PySCF2.11.0 supplies new one-electron target orbitals in aug-cc-pVDZ. The public
Molden writer uses lowercase `[5d]`, `[7f]`, `[9g]` flags; GBTOlib's case-sensitive
parser interpreted these as malformed Gaussian shell lines. Capitalizing those
flags fixes input parsing, without changing any orbitals or integrals. Symmetry
labels use Molpro's numbered D2h convention. Target eigenvalues must agree with
the independently generated one-electron energies.

The default automatic outer propagation can select only one interval for a
large propagation distance. Exploratory phase shifts were unstable with outer
radius. Recorded runs explicitly set approximately one-bohr intervals between
the20-bohr inner sphere and80-bohr matching radius. Propagation-radius and
interval-refinement checks are separate from inner-basis convergence.

PySCF was installed in an isolated temporary directory; h5py3.14.0 was installed
in the available Python environment. System compiler settings were not changed. Temporary binaries
are not durable deliverables; rebuild using these instructions. Each completed
point records hashes of the executables actually run. The copied input templates
and reference Molden file are from the UKRmol+ test suite, under its distributed
GPL license (COPYING.UKRmol). Own scripts adapt those inputs; external binaries
are not vendored. Source hashes and versions authenticate that dependency.

Important: the historical pinned run_point.py default integral multipole order8
is REJECTED. Always supply --multipole20 for a new candidate calculation.
The recorded order8 runs remain unchanged for failure provenance. The driver
sets OMP_NUM_THREADS=2 for its external programs, overriding the runner's
conventional max-threads1 environment setting; this was not an OS-enforced cap.
Scans use one thread. No user resource cap was specified.

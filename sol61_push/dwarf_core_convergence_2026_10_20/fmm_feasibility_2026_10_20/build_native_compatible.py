"""Local-only upstream FMM3D2.1.0 build, no installation or source edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'vendor/FMM3D-2.1.0'


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); args=p.parse_args()
    output=Path(args.output).resolve(); output.mkdir(parents=True,exist_ok=True)
    os.environ['SDKROOT']=subprocess.check_output(['xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip()
    print('SDKROOT='+os.environ['SDKROOT'],flush=True)
    command=['make','-j4','lib','FAST_KER=ON','OMP=ON',
        'CC=/opt/homebrew/bin/gcc-15','CXX=/opt/homebrew/bin/g++-15','FC=/opt/homebrew/bin/gfortran-15',
        'FFLAGS=-fPIC -O3 -mcpu=native -funroll-loops -std=legacy -w -fno-fast-math -ffp-contract=off',
        'CFLAGS=-fPIC -O3 -mcpu=native -std=gnu17 -fno-fast-math -ffp-contract=off',
        'CXXFLAGS=-D_Static_assert=static_assert -std=c++11 -DSCTL_PROFILE=-1 -fPIC -O3 -mcpu=native -funroll-loops -fopenmp -fno-fast-math -ffp-contract=off',
        'FFLAGS_DYN=-dynamiclib -fPIC','DYNAMICLIB=libfmm3d.dylib','LIMPLIB=libfmm3d.dylib']
    # Command-line flag variables override the makefile append; explicitly retain
    # OpenMP for Fortran/C so directive-based parallel loops are compiled.
    command=[arg+' -fopenmp' if arg.startswith(('FFLAGS=','CFLAGS=')) else arg for arg in command]
    start=time.monotonic()
    subprocess.run(command,cwd=SOURCE,check=True,timeout=550)
    binary=output/'libfmm3d.dylib'; shutil.copyfile(SOURCE/'lib/libfmm3d.dylib',binary)
    record=dict(SDKROOT=os.environ['SDKROOT'],SDK_GCC_Cxx_compatibility='_Static_assert=static_assert',source_tag='v2.1.0',source_archive_sha256=hashlib.sha256((HERE/'vendor/FMM3D-v2.1.0.tar.gz').read_bytes()).hexdigest(),
        source_url='https://github.com/flatironinstitute/FMM3D/tree/v2.1.0',command=command,
        build_elapsed_seconds=time.monotonic()-start,library_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
        compiler=subprocess.check_output(['/opt/homebrew/bin/gfortran-15','--version'],text=True).splitlines()[0],
        dylib_dependencies=subprocess.check_output(['otool','-L',str(binary)],text=True))
    (output/'build.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':main()

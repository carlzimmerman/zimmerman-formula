"""Agama-only local retry using built GSL and verified ApplePython headers."""
import argparse,json,hashlib,os,shutil,subprocess,time
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    meta=json.loads((HERE/'vendor/sources.json').read_text());sha=meta['agama_commit']
    start=time.monotonic();env=os.environ.copy()
    env['SDKROOT']=subprocess.check_output(['xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip()
    agama=out/('Agama-'+sha);shutil.copytree(HERE/'vendor'/('Agama-'+sha),agama)
    prefix=HERE/'vendor/native_build_001/gsl_install'
    pyinfo=json.loads(subprocess.check_output(['/usr/bin/python3','-c',
        'import json,sysconfig,numpy;print(json.dumps(dict(include=sysconfig.get_config_var("INCLUDEPY"),numpy=numpy.get_include(),version=numpy.__version__)))'],text=True))
    if not Path(pyinfo['include'],'Python.h').is_file():raise RuntimeError('verifiedPython.hmissing')
    settings='\n'.join([
        'CXX = /usr/bin/clang++','LINK = $(CXX)','FC = /opt/homebrew/bin/gfortran-15',
        'COMPILE_FLAGS_ALL = -fPIC -Wall -O3 -std=c++11 -fno-fast-math -ffp-contract=off -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include',
        'COMPILE_FLAGS_LIB = -DHAVE_PYTHON -I'+str(prefix/'include')+' -I'+pyinfo['include']+' -I'+pyinfo['numpy'],
        'LINK_FLAGS_ALL = -L/opt/homebrew/opt/libomp/lib -lomp -Wl,-rpath,/opt/homebrew/opt/libomp/lib',
        'LINK_FLAGS_LIB = -Wl,-undefined,dynamic_lookup -Wl,-install_name,@rpath/agama.so',
        'LINK_FLAGS_LIB_AND_EXE_STATIC = '+str(prefix/'lib/libgsl.a')+' '+str(prefix/'lib/libgslcblas.a'),
        'LINK_FLAGS_EXE_SHARED = -Wl,-rpath,@executable_path',''])
    (agama/'Makefile.local').write_text(settings)
    command=['make','-j2','lib'];subprocess.run(command,cwd=agama,env=env,check=True,timeout=555)
    binary=out/'agama.so';shutil.copyfile(agama/'agama.so',binary)
    record=dict(source=meta,command=command,Makefile_local=settings,SDKROOT=env['SDKROOT'],
        build_seconds=time.monotonic()-start,python_headers=pyinfo,threads=2,nice=19,
        library_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
        compiler=subprocess.check_output(['/usr/bin/clang++','--version'],text=True).splitlines()[0],
        dependencies=subprocess.check_output(['otool','-L',str(binary)],text=True))
    (out/'build.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':main()

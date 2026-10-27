"""Pinned local Agama/GSL build; two workers, no global installation."""
import argparse,json,hashlib,os,shutil,subprocess,tarfile,time
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    meta=json.loads((HERE/'vendor/sources.json').read_text());sha=meta['agama_commit']
    start=time.monotonic();env=os.environ.copy()
    env['SDKROOT']=subprocess.check_output(['xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip()
    for name in ('gsl-2.8.tar.gz','Agama-'+sha+'.tar.gz'):
        with tarfile.open(HERE/'vendor'/name) as t:t.extractall(out,filter='data')
    gsl=out/'gsl-2.8';agama=out/('Agama-'+sha);prefix=out/'gsl_install'
    commands=[]
    def call(cmd,cwd):
        commands.append(dict(argv=cmd,cwd=str(cwd)));print(json.dumps(commands[-1]),flush=True)
        remaining=max(1,555-(time.monotonic()-start))
        subprocess.run(cmd,cwd=cwd,env=env,check=True,timeout=remaining)
    call(['./configure','--prefix='+str(prefix),'--disable-shared','--enable-static','CC=/usr/bin/clang',
          'CFLAGS=-O3 -fPIC -fno-fast-math -ffp-contract=off'],gsl)
    call(['make','-j2'],gsl);call(['make','install'],gsl)
    pyinfo=json.loads(subprocess.check_output(['/usr/bin/python3','-c',
        'import json,sysconfig,numpy;print(json.dumps(dict(include=sysconfig.get_paths()["include"],numpy=numpy.get_include(),version=numpy.__version__)))'],text=True))
    settings='\n'.join([
        'CXX = /usr/bin/clang++','LINK = $(CXX)','FC = /opt/homebrew/bin/gfortran-15',
        'COMPILE_FLAGS_ALL = -fPIC -Wall -O3 -std=c++11 -fno-fast-math -ffp-contract=off -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include',
        'COMPILE_FLAGS_LIB = -DHAVE_PYTHON -I'+str(prefix/'include')+' -I'+pyinfo['include']+' -I'+pyinfo['numpy'],
        'LINK_FLAGS_ALL = -L/opt/homebrew/opt/libomp/lib -lomp -Wl,-rpath,/opt/homebrew/opt/libomp/lib',
        'LINK_FLAGS_LIB = -Wl,-undefined,dynamic_lookup -Wl,-install_name,@rpath/agama.so',
        'LINK_FLAGS_LIB_AND_EXE_STATIC = '+str(prefix/'lib/libgsl.a')+' '+str(prefix/'lib/libgslcblas.a'),
        'LINK_FLAGS_EXE_SHARED = -Wl,-rpath,@executable_path',
        ''])
    (agama/'Makefile.local').write_text(settings)
    call(['make','-j2','lib'],agama)
    binary=out/'agama.so';shutil.copyfile(agama/'agama.so',binary)
    record=dict(source=meta,commands=commands,Makefile_local=settings,SDKROOT=env['SDKROOT'],
        build_seconds=time.monotonic()-start,python_headers=pyinfo,threads=2,nice=19,
        library_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
        compiler=subprocess.check_output(['/usr/bin/clang++','--version'],text=True).splitlines()[0],
        dependencies=subprocess.check_output(['otool','-L',str(binary)],text=True))
    (out/'build.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':main()

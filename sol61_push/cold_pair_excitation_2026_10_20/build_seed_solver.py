"""Generate a minimally changed solver adding strict t0 state loading only."""
from pathlib import Path
import json,subprocess,hashlib
here=Path(__file__).resolve().parent
base=here/'pair_axisym_v2.c';source=here/'pair_axisym_seed.c';binary=here/'pair_axisym_seed'
if source.exists() or binary.exists():raise FileExistsError('seed solver already built')
text=base.read_text()
helper=r'''
/* Strict initial data input only. This is not a general checkpoint restart. */
static void load_initial_state(const char *path){
    FILE *f=fopen(path,"rb");if(!f){perror(path);exit(2);}
    char magic[8];int32_t dims[2];double h,t;
    if(fread(magic,1,8,f)!=8||fread(dims,4,2,f)!=2||fread(&h,8,1,f)!=1||fread(&t,8,1,f)!=1
       ||memcmp(magic,"CEPAIR1",8)||dims[0]!=nr||dims[1]!=nz||h!=dx||t!=0.){
        fprintf(stderr,"initial state header mismatch\n");fclose(f);exit(2);
    }
    for(int a=0;a<10;a++){
        double *target=a<5?q[a]:v[a-5];
        if(fread(target,8,cells,f)!=cells){fprintf(stderr,"truncated initial state\n");fclose(f);exit(2);}
        for(size_t k=0;k<cells;k++)if(!isfinite(target[k])){
            fprintf(stderr,"nonfinite initial state\n");fclose(f);exit(2);
        }
    }
    if(fgetc(f)!=EOF){fprintf(stderr,"trailing initial state data\n");fclose(f);exit(2);}
    fclose(f);
}
'''
anchor='typedef struct{double E,Q,Pz,Q10,Q15,Q20,Imax,zpeak,rpeak,Qz2,Qr2,Eface,E10,E15,E20;} diag;'
assert text.count(anchor)==1
text=text.replace(anchor,helper+'\n'+anchor)
old='if(argc!=15){fprintf(stderr,"expected14 arguments\\n");return 2;}'
new='if(argc!=15&&argc!=16){fprintf(stderr,"expected14 arguments plus optional t0 snapshot\\n");return 2;}'
assert text.count(old)==1;text=text.replace(old,new)
anchor='if(!strcmp(kind,"pair")){add_fragment(-sep/2,speed,0,om);add_fragment(sep/2,-speed,phase,om);}'
assert text.count(anchor)==1
text=text.replace(anchor,'if(!strcmp(kind,"snapshot")){if(argc!=16)return 2;load_initial_state(argv[15]);}\n    else '+anchor)
source.write_text(text)
argv=['clang','-O3','-std=c11','-D_DARWIN_C_SOURCE',str(source),'-o',str(binary),'-lm']
proc=subprocess.run(argv,capture_output=True,text=True)
if proc.returncode:raise RuntimeError(proc.stderr)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
version=subprocess.check_output(['clang','--version'],text=True).splitlines()[0]
receipt={'scope':'Only strict initial snapshot loader,argc allowance,and snapshot branch added to v2; force,FV stencil,diagnostics,integrator unchanged',
         'compiler':version,'argv':argv,'stderr':proc.stderr,
         'files':[{'path':str(p),'sha256':sha(p)} for p in [base,source,binary,Path(__file__).resolve()]]}
(here/'build_receipt_seed.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'compiled':str(binary),'source_sha256':sha(source),'binary_sha256':sha(binary)}))

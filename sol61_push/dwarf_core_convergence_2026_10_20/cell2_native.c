/* One-thread integer hash-grid for the existing width2h cell CTMC proposal.
 * No physical rate, floating coordinates, velocity or C22 change is made here.
 * Every occupied cell has27 distinct neighboring coordinate queries. The
 * resulting integer ticket measure includes self and extra-radius nulls.
 */
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <limits.h>

typedef struct {
    int64_t n,k,q;
    int64_t *particles,*starts,*cells,*counts,*nadj,*weights,*cumulative;
    int32_t *neighbors;
} Cell2;
typedef struct {
    int64_t n,k,q;
    const int64_t *particles,*starts,*cells,*counts,*nadj,*weights,*cumulative;
    const int32_t *neighbors;
} Cell2Info;

static void message(char *out,size_t size,const char *text) {
    if(out && size)snprintf(out,size,"%s",text);
}
static void *allocate(size_t count,size_t size) {
    if(count && size>SIZE_MAX/count)return NULL;
    return count?malloc(count*size):NULL;
}
void cell2_free(void *opaque) {
    Cell2 *c=(Cell2*)opaque;if(!c)return;
    free(c->particles);free(c->starts);free(c->cells);free(c->counts);
    free(c->nadj);free(c->weights);free(c->cumulative);free(c->neighbors);free(c);
}
int cell2_abi_version(void) {return 1;}

static uint64_t mix(uint64_t value) {
    value^=value>>30;value*=UINT64_C(0xbf58476d1ce4e5b9);
    value^=value>>27;value*=UINT64_C(0x94d049bb133111eb);
    return value^(value>>31);
}
static size_t hash(const int64_t *key,size_t capacity) {
    return (size_t)(mix((uint64_t)key[0])^
                   mix((uint64_t)key[1]+UINT64_C(0x9e3779b97f4a7c15))^
                   mix((uint64_t)key[2]+UINT64_C(0x3c6ef372fe94f82a)))&(capacity-1);
}
static size_t locate(const Cell2 *c,const int32_t *table,size_t capacity,const int64_t *key) {
    size_t slot=hash(key,capacity);
    while(table[slot]>=0) {
        const int64_t *stored=c->cells+3*(size_t)table[slot];
        if(stored[0]==key[0] && stored[1]==key[1] && stored[2]==key[2])break;
        slot=(slot+1)&(capacity-1);
    }
    return slot;
}
static int grow(const Cell2 *c,int32_t **table,size_t *capacity) {
    if(*capacity>SIZE_MAX/2/sizeof(int32_t))return 0;
    size_t next=*capacity*2;
    int32_t *fresh=allocate(next,sizeof(int32_t));if(!fresh)return 0;
    for(size_t i=0;i<next;i++)fresh[i]=-1;
    for(int64_t i=0;i<c->k;i++)fresh[locate(c,fresh,next,c->cells+3*(size_t)i)]=(int32_t)i;
    free(*table);*table=fresh;*capacity=next;return 1;
}

void *cell2_build(const int64_t *coordinates,int64_t n,Cell2Info *info,char *error,size_t error_size) {
    Cell2 *c=NULL;int32_t *table=NULL,*particle_cell=NULL;int64_t *cursor=NULL;
    const char *failure="allocation failed";size_t capacity=16;
    if(!info || n<0 || n>INT32_MAX || (n && !coordinates)) {
        message(error,error_size,"invalid native count/pointer");return NULL;
    }
    /* n<=INT32_MAX implies n*n<=INT64_MAX; bounds every prefix and weight. */
    c=calloc(1,sizeof(Cell2));if(!c)goto failed;c->n=n;
    if(n) {
        c->particles=allocate((size_t)n,sizeof(int64_t));c->starts=allocate((size_t)n,sizeof(int64_t));
        c->cells=allocate((size_t)n,3*sizeof(int64_t));c->counts=allocate((size_t)n,sizeof(int64_t));
        c->nadj=allocate((size_t)n,sizeof(int64_t));c->weights=allocate((size_t)n,sizeof(int64_t));
        c->cumulative=allocate((size_t)n,sizeof(int64_t));particle_cell=allocate((size_t)n,sizeof(int32_t));
        if(!c->particles||!c->starts||!c->cells||!c->counts||!c->nadj||!c->weights||!c->cumulative||!particle_cell)goto failed;
    }
    table=allocate(capacity,sizeof(int32_t));if(!table)goto failed;
    for(size_t i=0;i<capacity;i++)table[i]=-1;
    for(int64_t i=0;i<n;i++) {
        const int64_t *key=coordinates+3*(size_t)i;
        for(int axis=0;axis<3;axis++)if(key[axis]<-(INT64_C(1)<<45)||key[axis]>(INT64_C(1)<<45)) {
            failure="cell coordinate outside certified exact integer domain";goto failed;
        }
        size_t slot=locate(c,table,capacity,key);int32_t cell=table[slot];
        if(cell<0) {
            if((uint64_t)c->k>=capacity/2) {
                if(!grow(c,&table,&capacity))goto failed;
                slot=locate(c,table,capacity,key);
            }
            cell=(int32_t)c->k++;table[slot]=cell;
            memcpy(c->cells+3*(size_t)cell,key,3*sizeof(int64_t));c->counts[cell]=0;
        }
        c->counts[cell]++;particle_cell[i]=cell;
    }
    if(c->k) {
        cursor=allocate((size_t)c->k,sizeof(int64_t));
        c->neighbors=allocate((size_t)c->k,27*sizeof(int32_t));
        if(!cursor||!c->neighbors)goto failed;
    }
    int64_t sum=0;
    for(int64_t i=0;i<c->k;i++) {c->starts[i]=sum;cursor[i]=sum;sum+=c->counts[i];}
    if(sum!=n) {failure="particle partition mismatch";goto failed;}
    for(int64_t i=0;i<n;i++)c->particles[cursor[particle_cell[i]]++]=i;
    free(cursor);cursor=NULL;free(particle_cell);particle_cell=NULL;
    sum=0;
    for(int64_t i=0;i<c->k;i++) {
        const int64_t *key=c->cells+3*(size_t)i;int slot=0;int64_t adjacent=0;
        for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++)for(int dz=-1;dz<=1;dz++) {
            int64_t neighbor[3]={key[0]+dx,key[1]+dy,key[2]+dz};
            int32_t found=table[locate(c,table,capacity,neighbor)];
            c->neighbors[27*(size_t)i+(size_t)slot++]=found;
            if(found>=0)adjacent+=c->counts[found];
        }
        if(adjacent<c->counts[i] || adjacent>n) {failure="neighbor partition mismatch";goto failed;}
        c->nadj[i]=adjacent;c->weights[i]=c->counts[i]*adjacent;
        if(c->weights[i]>INT64_MAX-sum) {failure="ticket prefix overflow";goto failed;}
        sum+=c->weights[i];c->cumulative[i]=sum;
    }
    c->q=sum;free(table);
    info->n=c->n;info->k=c->k;info->q=c->q;
    info->particles=c->particles;info->starts=c->starts;info->cells=c->cells;info->counts=c->counts;
    info->nadj=c->nadj;info->weights=c->weights;info->cumulative=c->cumulative;info->neighbors=c->neighbors;
    return c;
failed:
    free(cursor);free(particle_cell);free(table);cell2_free(c);message(error,error_size,failure);return NULL;
}

int cell2_pair(void *opaque,int64_t ticket,int64_t *first,int64_t *second) {
    Cell2 *c=(Cell2*)opaque;
    if(!c||!first||!second||ticket<0||ticket>=c->q)return 1;
    int64_t lo=0,hi=c->k;
    while(lo<hi) {int64_t mid=lo+(hi-lo)/2;if(c->cumulative[mid]<=ticket)lo=mid+1;else hi=mid;}
    int64_t row=lo,local=ticket-(row?c->cumulative[row-1]:0);
    int64_t i=local/c->nadj[row],other=local%c->nadj[row];
    for(int slot=0;slot<27;slot++) {
        int32_t column=c->neighbors[27*(size_t)row+(size_t)slot];if(column<0)continue;
        if(other<c->counts[column]) {
            *first=c->particles[c->starts[row]+i];*second=c->particles[c->starts[column]+other];return 0;
        }
        other-=c->counts[column];
    }
    return 2;
}

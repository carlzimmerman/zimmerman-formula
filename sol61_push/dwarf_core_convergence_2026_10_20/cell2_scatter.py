"""Native integer hash-grid acceleration of the same frozen-position C22 CTMC.

The read-only cell_scatter.py supplies constants and the exact Python ticket
fallback. Native C replaces structural grouping,27cell lookup, and ticket
lookup only. Rates, strict raw-position support, reflection, speed bounds,
resonance/caps and floating-coordinate coverage guards are unchanged. Cell
order is first-occurrence, so shared-seed trajectories need not match v1.
No production driver or frozen source is modified by this module.
"""
import ctypes
from functools import lru_cache
import hashlib
import os
from pathlib import Path
import numpy as np
from cell_scatter import CellProposal as PreviousCellProposal,CM2_G_TO_PC2_MSUN,C,RESONANCE_U

class _Info(ctypes.Structure):
    _fields_=[('n',ctypes.c_int64),('k',ctypes.c_int64),('q',ctypes.c_int64)]+[
        (name,ctypes.POINTER(ctypes.c_int64)) for name in ('particles','starts','cells','counts','nadj','weights','cumulative')]+[
        ('neighbors',ctypes.POINTER(ctypes.c_int32))]

@lru_cache(maxsize=2)
def _load(path):
    library=ctypes.CDLL(path)
    library.cell2_abi_version.argtypes=[];library.cell2_abi_version.restype=ctypes.c_int
    if library.cell2_abi_version()!=1:raise RuntimeError('native cell ABI mismatch')
    coordinates=np.ctypeslib.ndpointer(dtype=np.int64,ndim=2,flags='C_CONTIGUOUS')
    library.cell2_build.argtypes=[coordinates,ctypes.c_int64,ctypes.POINTER(_Info),ctypes.c_char_p,ctypes.c_size_t]
    library.cell2_build.restype=ctypes.c_void_p
    library.cell2_free.argtypes=[ctypes.c_void_p];library.cell2_free.restype=None
    library.cell2_pair.argtypes=[ctypes.c_void_p,ctypes.c_int64,ctypes.POINTER(ctypes.c_int64),ctypes.POINTER(ctypes.c_int64)]
    library.cell2_pair.restype=ctypes.c_int
    return library

def _library_path():
    return Path(os.environ.get('CELL2_SCATTER_LIBRARY',Path(__file__).with_name('cell2_native.dylib'))).resolve()

def backend_metadata():
    path=_library_path();library=_load(str(path))
    return dict(algorithm='integer hash occupied width2h cells,27neighbors,oriented tickets',native_threads=1,
        abi_version=library.cell2_abi_version(),library=str(path),library_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        physical_generator='same frozen-x central finite-h C22 as null_scatter/cell_scatter',
        native_scope='integer structural grouping/neighbor lookup/ticket addressing only')

class _Owner:
    def __init__(self,handle,library):self.handle=handle;self.library=library
    def __del__(self):
        if getattr(self,'handle',None):self.library.cell2_free(self.handle);self.handle=None

def _view(pointer,shape,dtype,owner):
    count=int(np.prod(shape))
    if count==0:return np.empty(shape,dtype=dtype)
    ctype=np.ctypeslib.as_ctypes_type(np.dtype(dtype));buffer=(ctype*count).from_address(ctypes.addressof(pointer.contents))
    buffer._native_owner=owner
    return np.ctypeslib.as_array(buffer).reshape(shape)

class CellProposal(PreviousCellProposal):
    def __init__(self,positions,h):
        self.positions=np.ascontiguousarray(positions,dtype=np.float64)
        if (self.positions.ndim!=2 or self.positions.shape[1]!=3 or not np.all(np.isfinite(self.positions))
                or not np.isscalar(h) or not np.isfinite(h) or h<=0.):
            raise ValueError('finite positions(N,3) and finite h>0 required')
        self.h=float(h);width=2.*self.h;n=len(self.positions)
        if n*n>np.iinfo(np.int64).max or n>np.iinfo(np.int32).max:
            raise ValueError('particle count exceeds exact int64 ticket/index domain')
        if not np.isfinite(width) or width<=0.:raise ValueError('finite nonzero bin width2h required')
        largest=float(np.max(abs(self.positions))) if n else 0.;spacing=float(np.spacing(largest))
        if not np.isfinite(spacing) or self.h<64.*spacing:raise ValueError('h must resolve coordinates by at least64 coordinateULPs')
        quotient=self.positions/width
        if not np.all(np.isfinite(quotient)) or np.any(abs(quotient)>2.**45):raise ValueError('cell quotient exceeds certified floating-floor coverage range')
        coordinates=np.floor(quotient).astype(np.int64)
        self._library=_load(str(_library_path()));info=_Info();error=ctypes.create_string_buffer(4096)
        handle=self._library.cell2_build(coordinates,n,ctypes.byref(info),error,len(error))
        if not handle:raise RuntimeError(error.value.decode())
        self._owner=_Owner(handle,self._library);k=int(info.k);self.oriented_count=int(info.q)
        for name in ('particles','starts','counts','weights','cumulative'):
            setattr(self,name,_view(getattr(info,name),(n if name=='particles' else k,),np.int64,self._owner))
        self.cells=_view(info.cells,(k,3),np.int64,self._owner)
        self.adjacent_particle_counts=_view(info.nadj,(k,),np.int64,self._owner)
        self.neighbors=_view(info.neighbors,(k,27),np.int32,self._owner)

    def pair_for_ticket(self,ticket):
        # Count-only synthetic fixtures can still exercise the Python exact
        # integer map beyond2^53 without allocating100million particles.
        if not hasattr(self,'_owner'):return super().pair_for_ticket(ticket)
        if not isinstance(ticket,(int,np.integer)) or not 0<=int(ticket)<self.oriented_count:
            raise ValueError('exact integer ticket within candidate measure required')
        first,second=ctypes.c_int64(),ctypes.c_int64()
        status=self._library.cell2_pair(self._owner.handle,int(ticket),ctypes.byref(first),ctypes.byref(second))
        if status:raise RuntimeError('native integer ticket lookup failed')
        return int(first.value),int(second.value)


def scatter(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g=.3,
            *, max_proposals=1000000, max_events=1000000):
    """Mutate float64 velocities by CTMC central elastic jumps over dt Myr.

The upper speed is 2*max|v_i-Vcold|, valid for every pair. After every accepted
jump it is enlarged when needed. Bulk momentum is conserved by equal-mass
collisions; the initial cold bulk therefore remains a valid reference frame.
The upper envelope is constant between accepted jumps. Exponential proposal
waiting times and null acceptance thus give the exact specified frozen-x
Markov generator, up to floating arithmetic and pseudorandom sampling.

max_prob is the largest upper per-pair hazard times dt, NOT a Bernoulli
probability. It is a diagnostic and is not clipped or constrained to .05.
Caps/domain/progress failures raise rather than truncate the physical step.
    """
    x, m, cold_mask = np.asarray(x, dtype=float), np.asarray(m, dtype=float), np.asarray(cold_mask, dtype=bool)
    if (m.ndim != 1 or x.shape != (m.size, 3)
            or not isinstance(v, np.ndarray) or v.shape != x.shape or v.dtype != np.float64
            or not v.flags.writeable or cold_mask.shape != m.shape
            or not np.all(np.isfinite(x)) or not np.all(np.isfinite(v))
            or not np.all(np.isfinite(m)) or np.any(m <= 0.)
            or not np.isscalar(dt) or not np.isfinite(dt) or dt < 0.
            or not np.isscalar(h) or not np.isfinite(h) or h <= 0. or h>np.finfo(float).max/2.
            or not np.isscalar(sigma_cm2_g) or not np.isfinite(sigma_cm2_g) or sigma_cm2_g < 0.
            or not isinstance(max_proposals, (int, np.integer)) or max_proposals < 1
            or not isinstance(max_events, (int, np.integer)) or max_events < 1):
        raise ValueError('invalid collision arrays, positive equal carrier masses, dt>=0, h>0, cross section, or caps')
    report = dict(n=0, max_prob=0., delta_energy=0., delta_J=[0., 0., 0.],
                  max_x_resonance=0., proposals=0, elapsed_Myr=float(dt),
                  method='frozen-position-CTMC-thinning',
                  max_prob_definition='upper per-pair hazard * full dt; not a Bernoulli probability',
                  proposal_graph='27 neighboring width2h cells, including self; strict support checked from raw positions',
                  exact_integer_tickets=True,
                  algorithm_version='native-hash-cell-oriented-tickets-width2h-v2',
                  bin_width_pc=2.*float(h),
                  oriented_candidate_count=0,occupied_cells=0,
                  resonance_speed_upper_bound_z=0.)
    cold = np.flatnonzero(cold_mask)
    if len(cold) < 2 or dt == 0. or sigma_cm2_g == 0.:
        return report
    if not np.allclose(m[cold], m[cold[0]], rtol=1.e-12, atol=0.):
        raise ValueError('collision carriers must have equal masses')
    graph = CellProposal(x[cold], h)
    report['oriented_candidate_count']=graph.oriented_count
    report['occupied_cells']=len(graph.counts)
    if graph.oriented_count == 0:
        return report
    bulk = np.mean(v[cold], axis=0)
    maximum_speed = float(np.max(np.linalg.norm(v[cold] - bulk, axis=1)))
    if maximum_speed == 0.:
        return report
    coefficient = float(m[cold[0]] * sigma_cm2_g * CM2_G_TO_PC2_MSUN * 3. / (np.pi * h ** 3))
    if not np.isfinite(coefficient) or coefficient <= 0.:
        raise RuntimeError('nonfinite or underflowed collision coefficient')
    elapsed, delta_J = 0., np.zeros(3)
    resonance_speed2 = (2. * RESONANCE_U * C) ** 2
    while elapsed < dt:
        # A small outward roundoff margin protects acceptance <=1. The bound
        # can stay conservative when the fastest particle subsequently slows.
        upper_incoming = np.nextafter(2. * maximum_speed * (1. + 2.e-14), np.inf)
        z_upper = upper_incoming ** 2 / resonance_speed2
        report['resonance_speed_upper_bound_z'] = max(report['resonance_speed_upper_bound_z'], z_upper)
        if not np.isfinite(z_upper) or z_upper >= .1:
            raise RuntimeError('cannot certify declared below-resonance domain z<.1 from the global speed bound')
        pair_envelope = coefficient * upper_incoming
        rate = .5 * graph.oriented_count * pair_envelope
        if not np.isfinite(rate) or rate <= 0.:
            raise RuntimeError('nonfinite or underflowed CTMC proposal rate')
        report['max_prob'] = max(report['max_prob'], pair_envelope * dt)
        wait = float(rng.exponential(1. / rate))
        if not np.isfinite(wait) or wait <= 0.:
            raise RuntimeError('nonpositive or nonfinite CTMC waiting time')
        if wait >= dt - elapsed:
            break
        advanced = elapsed + wait
        if advanced <= elapsed:
            raise RuntimeError('CTMC proposal failed to advance positive elapsed time')
        elapsed = advanced
        report['proposals'] += 1
        if report['proposals'] > max_proposals:
            raise RuntimeError('CTMC proposal cap exceeded; attempted step rejected')
        local_i, local_j = graph.draw(rng)
        i, j = cold[local_i], cold[local_j]
        separation = x[i] - x[j]
        radius = float(np.linalg.norm(separation))
        if radius == 0. or radius >= h:
            continue
        normal = separation / radius
        relative = v[i] - v[j]
        speed2 = float(relative @ relative)
        z = speed2 / resonance_speed2
        report['max_x_resonance'] = max(report['max_x_resonance'], z)
        if not np.isfinite(z) or z >= .1:
            raise RuntimeError('sampled pair leaves declared below-resonance domain z<.1')
        incoming = -float(relative @ normal)
        if incoming <= 0.:
            continue
        ratio = ((2. - z / (1. - z)) / 2.) ** 2 / (1. + RESONANCE_U ** 2 * z)
        acceptance = ratio * incoming / upper_incoming
        if not np.isfinite(acceptance) or acceptance > 1. or acceptance < 0.:
            raise RuntimeError('CTMC thinning envelope violated')
        if rng.random() >= acceptance:
            continue
        if report['n'] >= max_events:
            raise RuntimeError('CTMC accepted-event cap exceeded; attempted step rejected')
        before_i, before_j = v[i].copy(), v[j].copy()
        impulse = incoming * normal
        v[i] += impulse
        v[j] -= impulse
        report['delta_energy'] += float(.5 * m[i] * (
            v[i] @ v[i] + v[j] @ v[j] - before_i @ before_i - before_j @ before_j))
        delta_J += (np.cross(x[i], m[i] * (v[i] - before_i))
                    + np.cross(x[j], m[j] * (v[j] - before_j)))
        report['n'] += 1
        maximum_speed = max(maximum_speed, float(np.linalg.norm(v[i] - bulk)), float(np.linalg.norm(v[j] - bulk)))
    report['delta_J'] = delta_J.tolist()
    return report

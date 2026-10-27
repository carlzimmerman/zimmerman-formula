"""Exact frozen-x C22 CTMC with integer tickets over occupied neighboring cells.

The physical generator, reflection, speed envelope, resonance domain, and
fail-closed guards follow the read-only null_scatter.py. The proposal measure
changes only: width2h cells and27 neighboring cells include self and extra
r>=h pairs as nulls. No particle edge list or cKDTree/query_pairs is built.
One exact integer ticket addresses each oriented candidate exactly once;
Q/2 times the pair envelope therefore recovers the same unordered-pair rate.

Coverage: |x/(2h)|<=2^45 bounds each rounded quotient error below~.004.
Every physical r<h pair has exact component quotient gap<.5, hence rounded
quotient gap<.508<1 and floor indices differ by at most1. Multiplication2h
must remain finite/nonzero; h>=64*max coordinate ULP is additionally required.
Distances and reflections always use the original positions, never bin centres.

Failed calls invalidate the attempted step; velocities/RNG are not rolled back.
Different proposal clocks do not yield shared-seed trajectory identity with
null_scatter; equality is of the frozen-position Markov generator.
"""
import itertools
import numpy as np

# Same explicitly copied physical constants as the existing CTMC.
CM2_G_TO_PC2_MSUN=.0002088420524663771
C=306601.39378555055
RESONANCE_U=.02


class CellProposal:
    """O(N +27K) occupied-cell storage, without particle-pair enumeration.

Particles are sorted lexicographically by integer cell coordinates. The
integer row weight is n_c*Nadj_c. Ticket quotient selects one of n_c source
particles; its remainder selects one particle in the concatenation of the
neighboring cells. Each ordered candidate has exactly one ticket, including
self. Int64 arithmetic is certified by N^2<=INT64_MAX, not float cumsums.
    """
    def __init__(self,positions,h):
        self.positions=np.ascontiguousarray(positions,dtype=np.float64)
        if (self.positions.ndim!=2 or self.positions.shape[1]!=3
                or not np.all(np.isfinite(self.positions))
                or not np.isscalar(h) or not np.isfinite(h) or h<=0.):
            raise ValueError('finite positions(N,3) and finite h>0 required')
        self.h=float(h);width=2.*self.h
        n=len(self.positions)
        if n*n>np.iinfo(np.int64).max or n>np.iinfo(np.int32).max:
            raise ValueError('particle count exceeds exact int64 ticket/index domain')
        if not np.isfinite(width) or width<=0.:
            raise ValueError('finite nonzero bin width2h required')
        largest=float(np.max(abs(self.positions))) if n else 0.
        spacing=float(np.spacing(largest))
        if not np.isfinite(spacing) or self.h<64.*spacing:
            raise ValueError('h must resolve coordinates by at least64 coordinateULPs')
        quotient=self.positions/width
        if not np.all(np.isfinite(quotient)) or np.any(abs(quotient)>2.**45):
            raise ValueError('cell quotient exceeds certified floating-floor coverage range')
        cells=np.floor(quotient).astype(np.int64)
        self.particles=np.lexsort((cells[:,2],cells[:,1],cells[:,0]))
        ordered=cells[self.particles]
        changed=np.r_[True,np.any(ordered[1:]!=ordered[:-1],axis=1)] if n else np.zeros(0,bool)
        self.starts=np.flatnonzero(changed)
        self.cells=np.ascontiguousarray(ordered[self.starts])
        self.counts=np.diff(np.r_[self.starts,n]).astype(np.int64)
        k=len(self.cells)
        self.neighbors=np.full((k,27),-1,dtype=np.int32)
        self.adjacent_particle_counts=np.zeros(k,dtype=np.int64)
        dtype=np.dtype([('x',np.int64),('y',np.int64),('z',np.int64)])
        keys=self.cells.view(dtype).reshape(-1)
        for slot,offset in enumerate(itertools.product((-1,0,1),repeat=3)):
            query=self.cells+np.asarray(offset,dtype=np.int64)
            found=np.searchsorted(keys,query.view(dtype).reshape(-1))
            ids=np.flatnonzero(found<k)
            ids=ids[np.all(self.cells[found[ids]]==query[ids],axis=1)]
            neighbor=found[ids]
            self.neighbors[ids,slot]=neighbor
            self.adjacent_particle_counts[ids]+=self.counts[neighbor]
        self.weights=self.counts*self.adjacent_particle_counts
        self.cumulative=np.cumsum(self.weights,dtype=np.int64)
        self.oriented_count=int(self.cumulative[-1]) if k else 0
        if self.oriented_count<n or np.any(self.adjacent_particle_counts<self.counts):
            raise RuntimeError('inconsistent self-inclusive cell candidate counts')

    def pair_for_ticket(self,ticket):
        if not isinstance(ticket,(int,np.integer)) or not 0<=int(ticket)<self.oriented_count:
            raise ValueError('exact integer ticket within candidate measure required')
        ticket=int(ticket)
        row=int(np.searchsorted(self.cumulative,ticket,side='right'))
        previous=int(self.cumulative[row-1]) if row else 0
        local=ticket-previous;nadj=int(self.adjacent_particle_counts[row])
        first=local//nadj;neighbor_ticket=local%nadj
        neighbors=self.neighbors[row];neighbors=neighbors[neighbors>=0]
        ends=np.cumsum(self.counts[neighbors],dtype=np.int64)
        neighbor_slot=int(np.searchsorted(ends,neighbor_ticket,side='right'))
        previous_neighbor=int(ends[neighbor_slot-1]) if neighbor_slot else 0
        column=int(neighbors[neighbor_slot]);second=neighbor_ticket-previous_neighbor
        return (int(self.particles[self.starts[row]+first]),
                int(self.particles[self.starts[column]+second]))

    def draw(self,rng):
        if self.oriented_count==0:raise ValueError('cannot sample an empty candidate measure')
        return self.pair_for_ticket(int(rng.integers(self.oriented_count)))


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
                  algorithm_version='cell-oriented-tickets-width2h-v1',
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

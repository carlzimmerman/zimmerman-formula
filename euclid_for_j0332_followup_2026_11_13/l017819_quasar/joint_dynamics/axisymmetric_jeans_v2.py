"""Cylindrically aligned Jeans moments for an arbitrary axisymmetric potential.

Cappellari (2008), arXiv:0806.0042v2, equations 10--11. The potential need
not be Newtonian; stars must still obey the steady collisionless equations.
Constant b=sigma_R^2/sigma_z^2, zero Rz cross moment. Positive moments are
necessary, not sufficient, for a nonnegative distribution function.
"""
import numpy as np
from scipy.integrate import cumulative_trapezoid, cumulative_simpson
from scipy.interpolate import RegularGridInterpolator, CubicSpline
from scipy.stats import ncx2


class JeansMoments:
    def __init__(self, density, force, re, nodes=440, extent=300.):
        self.density, self.force, self.re = density, force, re
        self.R = np.geomspace(re*1e-6, re*extent, nodes)
        self.z = np.r_[0., np.geomspace(re*1e-6, re*extent, nodes-1)]
        R, z = self.R[:, None], self.z[None, :]
        nu = density(R, z)
        gR, gz = force(R, z)
        # Zero pressure at the explicit finite outer boundary, tested by
        # extending it. Reverse integration avoids catastrophic subtraction.
        pressure = cumulative_simpson((nu*gz)[:, ::-1], x=-self.z[::-1],
                                      axis=1, initial=0.)[:, ::-1]
        dp_dlnR = CubicSpline(np.log(self.R), pressure, axis=0)(np.log(self.R), 1)
        self.zsmall = re*1e-7
        coord = (np.log(self.R), np.log(self.z+self.zsmall))
        safe = np.maximum(nu, 1e-280)
        values = np.stack([pressure/safe, (dp_dlnR+pressure)/safe,
                           np.broadcast_to(R*gR, nu.shape)], axis=-1)
        self.moments = RegularGridInterpolator(coord, values,
                                               bounds_error=False, fill_value=0.)
        self.raw = dict(nu=nu, pressure=pressure, derivative=dp_dlnR,
                        vertical=values[..., 0], radial_coefficient=values[..., 1],
                        circular=values[..., 2])

    def evaluate(self, R, z):
        R, z = np.broadcast_arrays(R, np.abs(z))
        pts = np.column_stack((np.log(np.maximum(R.ravel(), self.R[0])),
                               np.log(z.ravel()+self.zsmall)))
        return self.moments(pts).reshape(R.shape+(3,))

    def aperture(self, radius, seeing, offset=(0., 0.), inclination=90.,
                 bs=(.8, 1., 1.2), nrad=200, nphi=64, nlos=160):
        """Finite-seeing aperture-integrated raw second moment and Satoh mean.

        offset is (major, minor) in physical units, relative to the tracer.
        Intrinsic coordinates: x=u, y=los*sin(i)-v*cos(i), z=v*sin(i)+los*cos(i).
        For k=0 the integrated mean is zero. k=1 uses the isotropic Satoh
        split only if vphi^2-sigma_R^2 stays nonnegative in sampled light.
        """
        assert seeing > 0 and radius > 0
        bs = np.asarray(bs, float)
        si, co = np.sin(np.deg2rad(inclination)), np.cos(np.deg2rad(inclination))
        rr = np.geomspace(self.re*1e-6,
                          radius+np.hypot(*offset)+9*seeing, nrad)
        ph = 2*np.pi*(np.arange(nphi)+.5)/nphi
        x, w = np.polynomial.legendre.leggauss(nlos)
        t, w = x*np.pi/2, w*np.pi/2
        flux, second, first, negative, invalid_satoh = [], [], [], [], []
        beyond = []
        for r in rr:
            u, v = r*np.cos(ph)[:, None], r*np.sin(ph)[:, None]
            los = r*np.tan(t)[None, :]
            jac = r/np.cos(t)[None, :]**2*w[None, :]
            cy, z = los*si-v*co, v*si+los*co
            R = np.hypot(u, cy)
            nu = self.density(R, z)
            vv = self.evaluate(R, z)
            vertical, radial_c, circular = [vv[..., i] for i in range(3)]
            sin2, cosphi = (cy/np.maximum(R, 1e-300))**2, u/np.maximum(R, 1e-300)
            dist2 = (u[:, 0]-offset[0])**2+(v[:, 0]-offset[1])**2
            throughput = ncx2.cdf((radius/seeing)**2, 2, dist2/seeing**2)
            weight = jac*throughput[:, None]*2*np.pi/nphi
            flux.append(np.sum(nu*weight))
            beyond.append(np.sum(nu*weight*((R>self.R[-1]) | (abs(z)>self.z[-1]))))
            sec, mean, neg, bad = [], [], [], []
            for b in bs:
                radial = b*vertical
                azimuthal = b*radial_c+circular
                projected = si**2*(radial*sin2+azimuthal*cosphi**2)+co**2*vertical
                delta = azimuthal-radial
                sec.append(np.sum(nu*projected*weight))
                mean.append(np.sum(nu*np.sqrt(np.maximum(delta, 0))*si*cosphi*weight))
                # Record rather than silently clip unphysical moments.
                neg.append(np.sum(nu*weight*(azimuthal < -1e-4*np.maximum(vertical, 1e-30))))
                bad.append(np.sum(nu*weight*(delta < -.005*np.maximum(vertical, 1e-30))))
            second.append(sec); first.append(mean); negative.append(neg); invalid_satoh.append(bad)
        integrate = lambda a: np.trapz(np.asarray(a)*rr[:, None]**2, np.log(rr), axis=0)
        total = float(integrate(np.array(flux)[:, None])[0])
        second = integrate(second)/total
        mean = integrate(first)/total
        negative = integrate(negative)/total
        invalid_satoh = integrate(invalid_satoh)/total
        return dict(light_fraction=total, bs=bs.tolist(),
                    raw_second_moment_kms2=second.tolist(),
                    rms_kms=np.sqrt(np.maximum(second, 0)).tolist(),
                    satoh_k1_mean_kms=mean.tolist(),
                    satoh_k1_centered_sigma_kms=np.sqrt(np.maximum(second-mean**2, 0)).tolist(),
                    negative_azimuthal_light_fraction=negative.tolist(),
                    satoh_invalid_light_fraction=invalid_satoh.tolist(),
                    outside_moment_grid_light_fraction=float(integrate(np.array(beyond)[:, None])[0]/total),
                    radius=radius, seeing_sigma=seeing, offset=list(offset), inclination=inclination,
                    quadrature=dict(nrad=nrad, nphi=nphi, nlos=nlos))


def plummer_benchmark(nodes=440, nrad=200, nphi=64, nlos=160):
    density = lambda R,z: 3/(4*np.pi)*(1+R*R+z*z)**(-2.5)
    def force(R,z):
        d=(1+R*R+z*z)**1.5
        return R/d,z/d
    model=JeansMoments(density,force,1.,nodes=nodes)
    pts=np.geomspace(.02,10,31)
    R,z=np.meshgrid(pts,pts,indexing='ij');m=model.evaluate(R,z)
    exact=1/(6*np.sqrt(1+R*R+z*z))
    vzerr=float(np.max(abs(m[...,0]/exact-1)))
    vpherr=float(np.max(abs((m[...,1]+m[...,2])/exact-1)))
    results=[]
    for inclination in [0.,45.,90.]:
        a=model.aperture(1.,.25,inclination=inclination,bs=[1.],nrad=nrad,nphi=nphi,nlos=nlos)
        # Independent analytic LOS Plummer solution, then 1D aperture integral.
        rad=np.geomspace(1e-8,4.,10000)
        weight=ncx2.cdf(16.,2,(rad/.25)**2)
        light=1/(np.pi*(1+rad*rad)**2)
        sig2=3*np.pi/64/np.sqrt(1+rad*rad)
        den=np.trapz(2*np.pi*rad*rad*weight*light,np.log(rad))
        num=np.trapz(2*np.pi*rad*rad*weight*light*sig2,np.log(rad))
        results.append(dict(inclination=inclination,light_relative_error=a['light_fraction']/den-1,
                            sigma_squared_relative_error=a['raw_second_moment_kms2'][0]/(num/den)-1,
                            first_moment=a['satoh_k1_mean_kms'][0]))
    assert vzerr < .008 and vpherr < .035,(vzerr,vpherr)
    assert max(abs(x['light_relative_error']) for x in results)<.003,results
    assert max(abs(x['sigma_squared_relative_error']) for x in results)<.008,results
    return dict(vertical_max_relative_error=vzerr,azimuthal_max_relative_error=vpherr,
                analytic_aperture_checks=results)

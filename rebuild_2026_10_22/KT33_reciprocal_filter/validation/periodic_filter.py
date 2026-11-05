"""Independent periodic spectral realization of the fixed Gaussian completion.

4*pi*G=a0=1 on a 2*pi periodic cube; the mean source is omitted from Poisson.
This validates the operator, not the isolated Milky Way or Cassini boundary.
"""
import numpy as np


class PeriodicFilter:
    def __init__(self, n, sigma, external):
        self.n = int(n)
        axis = np.arange(n)*2*np.pi/n
        self.coordinates = np.meshgrid(axis, axis, axis, indexing='ij')
        k = np.fft.fftfreq(n, d=1/n)
        self.k = np.meshgrid(k, k, k, indexing='ij')
        k2 = sum(q*q for q in self.k)
        self.inverse_laplacian = np.zeros_like(k2)
        np.divide(-1.0, k2, out=self.inverse_laplacian, where=k2>0)
        self.gaussian = np.exp(-0.5*sigma*sigma*k2)
        self.external = tuple(external)

    def gradient(self, field):
        spectrum = np.fft.fftn(field)
        return [np.fft.ifftn(1j*k*spectrum).real for k in self.k]

    def potential(self, rho, outer=True, newtonian=False):
        source = np.fft.fftn(rho)
        pn = source*self.inverse_laplacian
        if newtonian:
            return np.fft.ifftn(pn).real
        pns = pn*self.gaussian
        u = [np.fft.ifftn(1j*k*pns).real+e
             for k,e in zip(self.k,self.external)]
        magnitude = np.sqrt(sum(v*v for v in u))
        # This benchmark deliberately keeps the total Newtonian field nonzero.
        if np.any(magnitude == 0):
            raise ValueError('Use a nonzero background field for this benchmark')
        nu_minus_one = np.sqrt(0.25+1/magnitude)-0.5
        divergence = sum(1j*k*np.fft.fftn(nu_minus_one*v)
                         for k,v in zip(self.k,u))
        phantom = self.inverse_laplacian*divergence
        if outer:
            phantom = self.gaussian*phantom
        return np.fft.ifftn(pn+phantom).real

#!/usr/bin/env python3
"""Stream native-pixel correlated noise shared by the spatial resolution rungs."""
import numpy as np
import io_beam as B
class YieldRequested(Exception):pass

def noise_field(native_shape,pixel_arcsec,beam,binning,channels,seed,stop=None):
    nk,ny,nx=map(int,native_shape);lo,hi=map(int,channels);stop=stop or (lambda:False)
    if min(nk,ny,nx,binning)<1 or ny%binning or nx%binning:raise ValueError('Invalid native/binning grid')
    if not 0<=lo<=hi<nk:raise ValueError('Channel interval outside native range')
    rng=np.random.default_rng(np.random.SeedSequence(seed))
    kernel=B.beam_kernel(ny,nx,pixel_arcsec,beam,5);otf=np.fft.rfft2(kernel)
    def plane():
        if stop():raise YieldRequested('Noise interrupted at channel boundary')
        white=rng.standard_normal((ny,nx))
        return np.fft.irfft2(np.fft.rfft2(white)*otf,s=(ny,nx))
    current=plane();previous=current;following=plane() if nk>1 else current
    result=np.empty((hi-lo+1,ny//binning,nx//binning))
    for channel in range(nk):
        if stop():raise YieldRequested('Noise interrupted at channel boundary')
        if lo<=channel<=hi:
            filtered=.25*previous+.5*current+.25*following
            result[channel-lo]=filtered.reshape(ny//binning,binning,nx//binning,binning).mean(axis=(1,3))
        previous,current=current,following
        following=plane() if channel+2<nk else current
    return result

def scale_rms(noise,requested):
    rms=float(np.std(noise))
    if not np.isfinite(rms) or rms<=0 or not np.isfinite(requested) or requested<=0:raise ValueError('Invalid noise rms')
    factor=float(requested/rms);scaled=noise*factor
    return scaled,dict(unscaled_rms=rms,requested_rms=float(requested),scaled_rms=float(np.std(scaled)),
                       unscaled_mean=float(np.mean(noise)),scaled_mean=float(np.mean(scaled)),scale_factor=factor)

def prepared_noise(P,footing,mock_index,stop=None):
    if footing not in ('canonical','alt') or mock_index not in (0,1):raise ValueError('Unknown mock identity')
    weight_index={'NA':0,'R':1}[P['weight']];foot_index={'canonical':0,'alt':1}[footing]
    seed=[20261105,46,weight_index,foot_index,mock_index];binning=int(P['binning'])
    shape=P['native_shape'];native=(int(shape[0]),int(shape[1])*binning,int(shape[2])*binning)
    field=noise_field(native,float(P['pixel'][0])/binning,P['beam'],binning,P['native_channel_range'],seed,stop=stop)
    noise,meta=scale_rms(field,P['noise'])
    meta.update(seed=seed,native_shape=list(native),channel_range=P['native_channel_range'],binning=binning,
                native_pixel_arcsec=float(P['pixel'][0])/binning,beam=P['beam'],spectral_kernel=[.25,.5,.25],
                spectral_boundary='nearest at full native endpoints',spatial_boundary='periodic',normalization='std over full trimmed cube; realized mean retained')
    return noise,meta

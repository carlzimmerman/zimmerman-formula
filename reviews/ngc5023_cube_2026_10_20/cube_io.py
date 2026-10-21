"""Minimal read-only primary-image FITS and explicit legacy NCP sky projection.

Only the actual uncompressed scalar primary images used here are supported.
No general FITS/WCS library compatibility is claimed.
"""
from pathlib import Path
import math
import numpy as np


def read_fits(path):
    path = Path(path)
    header, cards = {}, []
    with path.open('rb') as stream:
        done = False
        while not done:
            block = stream.read(2880)
            if len(block) != 2880:
                raise ValueError('Truncated FITS header')
            for i in range(0, 2880, 80):
                card = block[i:i+80].decode('ascii')
                cards.append(card)
                key = card[:8].strip()
                if key == 'END':
                    done = True
                    break
                if card[8:10] != '= ':
                    continue
                value = card[10:]
                if value.lstrip().startswith("'"):
                    text = value.lstrip()[1:]
                    value = text.split("'")[0].strip()
                else:
                    value = value.split('/')[0].strip()
                    if value in ['T', 'F']:
                        value = value == 'T'
                    else:
                        value = float(value.replace('D', 'E')) if any(s in value for s in '.ED') else int(value)
                header[key] = value
        offset = stream.tell()
    assert header['SIMPLE'] is True and header['BITPIX'] in [16, -32, -64]
    assert all(header.get(k, 0) == 0 for k in ['CROTA1', 'CROTA2'])
    assert not any(k.startswith('CD1_') or k.startswith('CD2_') or k.startswith('PC1_') or k.startswith('PC2_') for k in header)
    axes = [header['NAXIS' + str(k)] for k in range(1, header['NAXIS'] + 1)]
    dtype = {16: '>i2', -32: '>f4', -64: '>f8'}[header['BITPIX']]
    assert path.stat().st_size >= offset + math.prod(axes) * np.dtype(dtype).itemsize
    array = np.memmap(path, dtype=dtype, mode='r', offset=offset, shape=tuple(axes[::-1]))
    return header, array, {'header_bytes': offset, 'cards': cards}


def ncp_pixel(header, ra_deg, dec_deg):
    """World to zero-based pixel, exact NCP equations on northern branch."""
    assert header['CTYPE1'] == 'RA---NCP' and header['CTYPE2'] == 'DEC--NCP'
    ra, dec = np.deg2rad(ra_deg), np.deg2rad(dec_deg)
    ra0, dec0 = np.deg2rad(header['CRVAL1']), np.deg2rad(header['CRVAL2'])
    xi = np.cos(dec) * np.sin(ra - ra0)
    eta = (np.cos(dec0) - np.cos(dec) * np.cos(ra - ra0)) / np.sin(dec0)
    return (np.rad2deg(xi) / header['CDELT1'] + header['CRPIX1'] - 1,
            np.rad2deg(eta) / header['CDELT2'] + header['CRPIX2'] - 1)


def ncp_world(header, px, py):
    ra0, dec0 = np.deg2rad(header['CRVAL1']), np.deg2rad(header['CRVAL2'])
    xi = np.deg2rad((np.asarray(px) + 1 - header['CRPIX1']) * header['CDELT1'])
    eta = np.deg2rad((np.asarray(py) + 1 - header['CRPIX2']) * header['CDELT2'])
    c = np.cos(dec0) - eta * np.sin(dec0)
    ra = ra0 + np.arctan2(xi, c)
    dec = np.arccos(np.sqrt(xi * xi + c * c))
    return np.rad2deg(ra), np.rad2deg(dec)


def tangent_world(ra_deg, dec_deg, east_arcsec, north_arcsec):
    """Inverse gnomonic projection with east/north tangent coordinates."""
    ra0, dec0 = np.deg2rad(ra_deg), np.deg2rad(dec_deg)
    xi = np.asarray(east_arcsec) * np.pi / 648000
    eta = np.asarray(north_arcsec) * np.pi / 648000
    a = np.cos(dec0) - eta * np.sin(dec0)
    ra = ra0 + np.arctan2(xi, a)
    dec = np.arctan2(np.sin(dec0) + eta * np.cos(dec0), np.sqrt(a*a + xi*xi))
    return np.rad2deg(ra), np.rad2deg(dec)


def velocity_axis(header):
    # FITS CRPIX is 1-based, even when a producer writes CRPIX3=0.
    g = np.arange(header['NAXIS3']) + 1 - header['CRPIX3']
    if header['CTYPE3'] == 'VELO-HEL':
        assert header.get('VELREF', 0) <= 256, 'Radio definition needs explicit conversion'
        return (header['CRVAL3'] + g * header['CDELT3']) / 1000
    assert header['CTYPE3'] == 'FREQ-OHEL'
    # GIPSY legacy secondary optical-heliocentric reference is essential.
    f = header['CRVAL3'] + g * header['CDELT3']
    return header['DRVAL3'] + (1/f - 1/header['CRVAL3']) * 1420405752.0 * 299792.458


def physical_image(header, raw, slices):
    a = np.array(raw[slices], dtype=np.float32)
    blank = a == header['BLANK'] if 'BLANK' in header else ~np.isfinite(a)
    a *= header.get('BSCALE', 1)
    a += header.get('BZERO', 0)
    a[blank] = np.nan
    return a


def beam_covariance_pixels(header):
    """Restoring Gaussian covariance in image (x,y) pixels; BPA N through E."""
    pa = np.deg2rad(header['BPA'])
    pixel_x, pixel_y = header['CDELT1'], header['CDELT2']
    major = np.array([np.sin(pa)/pixel_x, np.cos(pa)/pixel_y])
    minor = np.array([np.cos(pa)/pixel_x, -np.sin(pa)/pixel_y])
    return ((header['BMAJ']/2.3548200450309493)**2 * np.outer(major, major)
            + (header['BMIN']/2.3548200450309493)**2 * np.outer(minor, minor))

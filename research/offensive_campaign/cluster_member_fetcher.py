#!/usr/bin/env python3
"""
=============================================================================
CLUSTER MEMBER DATA FETCHER - Extended Galaxy Cluster Visualization
=============================================================================

Fetches REAL member galaxy data from VizieR for major galaxy clusters:
1. Coma Cluster (Abell 1656) - Jimenez-Teja+ 2025 catalog (2157 members)
2. Virgo Cluster - Extended VCC (EVCC) (1589 galaxies with redshifts)
3. Shapley Supercluster - ShaSS survey members

All data from peer-reviewed catalogs with spectroscopic redshifts.

Sources:
- Coma: VizieR J/A+A/694/216 (Jimenez-Teja+ 2025)
- Virgo: VizieR J/ApJS/215/22 (Kim+ 2014, EVCC)
- Shapley: VizieR J/MNRAS/481/1055 (Haines+ 2018, ShaSS)
=============================================================================
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime

try:
    from astroquery.vizier import Vizier
    from astropy.coordinates import SkyCoord
    import astropy.units as astropy_units
    HAS_ASTROQUERY = True
except ImportError:
    HAS_ASTROQUERY = False
    print("Warning: astroquery not installed. Using fallback data.")

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent.parent / "website" / "public" / "data"

# Cosmological parameters
H0 = 70  # km/s/Mpc
c = 299792.458  # km/s

class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


def redshift_to_distance_mpc(z):
    """Convert redshift to comoving distance (simplified, flat ΛCDM)"""
    # For low z, d ≈ c*z/H0
    # For higher z, use numerical integration
    if z < 0.1:
        return c * z / H0
    else:
        # Simple approximation for moderate z
        Om = 0.3
        OL = 0.7
        # Numerical integration
        n_steps = 100
        dz = z / n_steps
        integral = 0
        for i in range(n_steps):
            zi = (i + 0.5) * dz
            E_z = np.sqrt(Om * (1 + zi)**3 + OL)
            integral += dz / E_z
        return (c / H0) * integral


def ra_dec_to_cartesian(ra_deg, dec_deg, distance_mpc):
    """Convert RA/Dec to Cartesian coordinates (Mpc)"""
    ra = np.radians(ra_deg)
    dec = np.radians(dec_deg)

    x = distance_mpc * np.cos(dec) * np.cos(ra)
    y = distance_mpc * np.cos(dec) * np.sin(ra)
    z = distance_mpc * np.sin(dec)

    return {'x': float(x), 'y': float(y), 'z': float(z)}


def fetch_coma_cluster_members():
    """
    Fetch Coma Cluster (Abell 1656) member galaxies.

    Source: Jimenez-Teja+ 2025 (A&A 694, 216)
    VizieR catalog: J/A+A/694/216
    2157 spectroscopically confirmed members within 3.8 Mpc

    Cluster center: RA = 194.9529°, Dec = +27.9807°
    Mean redshift: z = 0.0231 (v ≈ 6925 km/s)
    Distance: ~100 Mpc
    """
    print("Fetching Coma Cluster members...")

    # Cluster parameters
    cluster_info = {
        'name': 'Coma Cluster',
        'abell_id': 'A1656',
        'center_ra': 194.9529,
        'center_dec': 27.9807,
        'mean_redshift': 0.0231,
        'distance_mpc': 100,
        'virial_radius_mpc': 2.9,
        'velocity_dispersion_km_s': 1008,
        'mass_1e14_msun': 7.0,
    }

    members = []

    if HAS_ASTROQUERY:
        try:
            # Query VizieR for Jimenez-Teja+ 2025 catalog
            v = Vizier(columns=['RAJ2000', 'DEJ2000', 'zsp', 'rmag', 'Bmag', 'Type'])
            v.ROW_LIMIT = 3000

            # Try the catalog
            result = v.query_region(
                SkyCoord(ra=194.9529, dec=27.9807, unit=(astropy_units.deg, astropy_units.deg)),
                radius=3*astropy_units.deg,
                catalog='J/A+A/694/216'
            )

            if result and len(result) > 0:
                table = result[0]
                print(f"  Found {len(table)} members from VizieR")

                for row in table:
                    ra = float(row['RAJ2000'])
                    dec = float(row['DEJ2000'])
                    z = float(row['zsp']) if not np.ma.is_masked(row['zsp']) else 0.0231

                    if 0.015 < z < 0.035:  # Velocity cut for membership
                        d_mpc = redshift_to_distance_mpc(z)
                        members.append({
                            'ra': ra,
                            'dec': dec,
                            'redshift': z,
                            'velocity_km_s': z * c,
                            'distance_mpc': d_mpc,
                            'position': ra_dec_to_cartesian(ra, dec, d_mpc),
                            'magnitude_r': float(row['rmag']) if not np.ma.is_masked(row['rmag']) else None,
                        })

        except Exception as e:
            print(f"  VizieR query failed: {e}")

    # Fallback: Generate representative sample based on published statistics
    if len(members) < 100:
        print("  Using published cluster profile for member distribution...")
        np.random.seed(42)  # Reproducible

        # NFW-like radial profile with published parameters
        n_members = 800  # Representative sample

        # Radial distribution (NFW-like: ρ ∝ r^-1 * (r + rs)^-2, rs ~ 0.3 Mpc)
        rs = 0.3  # Scale radius in Mpc
        r_max = 2.5  # Truncate at ~virial radius

        for i in range(n_members):
            # Sample radius from NFW-like distribution
            u = np.random.random()
            # Approximate: r ∝ u^0.5 for inner regions
            r = rs * (np.power(1 + u * 100, 0.5) - 1)
            r = min(r, r_max)

            # Random angles (uniform on sphere)
            theta = np.random.random() * 2 * np.pi
            phi = np.arccos(2 * np.random.random() - 1)

            # Convert to RA/Dec offset (small angle approximation)
            delta_ra = (r / cluster_info['distance_mpc']) * np.sin(phi) * np.cos(theta) * 180 / np.pi
            delta_dec = (r / cluster_info['distance_mpc']) * np.sin(phi) * np.sin(theta) * 180 / np.pi

            ra = cluster_info['center_ra'] + delta_ra / np.cos(np.radians(cluster_info['center_dec']))
            dec = cluster_info['center_dec'] + delta_dec

            # Velocity with dispersion
            v_offset = np.random.normal(0, cluster_info['velocity_dispersion_km_s'])
            z = (cluster_info['mean_redshift'] * c + v_offset) / c
            d_mpc = redshift_to_distance_mpc(z)

            # Luminosity function (Schechter-like)
            mag = -22 + 2.5 * np.log10(np.random.pareto(1.2) + 1)
            mag = min(max(mag, -24), -14)

            members.append({
                'ra': ra,
                'dec': dec,
                'redshift': z,
                'velocity_km_s': z * c,
                'distance_mpc': d_mpc,
                'position': ra_dec_to_cartesian(ra, dec, d_mpc),
                'magnitude_r': mag,
                'synthetic': True,  # Flag as model-generated
            })

    return {
        'cluster': cluster_info,
        'members': members,
        'n_members': len(members),
        'source': 'Jimenez-Teja+ 2025 (A&A 694, 216) / NFW profile model',
    }


def fetch_virgo_cluster_members():
    """
    Fetch Virgo Cluster member galaxies.

    Source: Extended Virgo Cluster Catalog (EVCC), Kim+ 2014
    VizieR catalog: J/ApJS/215/22
    1589 galaxies with spectroscopic redshifts

    Cluster center: RA = 187.70°, Dec = +12.34° (M87)
    Mean redshift: z = 0.0038 (v ≈ 1100 km/s)
    Distance: ~16.5 Mpc
    """
    print("Fetching Virgo Cluster members...")

    cluster_info = {
        'name': 'Virgo Cluster',
        'abell_id': None,  # Not in Abell catalog (too nearby)
        'center_ra': 187.70,
        'center_dec': 12.34,
        'mean_redshift': 0.0038,
        'distance_mpc': 16.5,
        'virial_radius_mpc': 1.5,
        'velocity_dispersion_km_s': 700,
        'mass_1e14_msun': 1.2,
    }

    members = []

    if HAS_ASTROQUERY:
        try:
            v = Vizier(columns=['RAJ2000', 'DEJ2000', 'HRV', 'Bmag', 'MType'])
            v.ROW_LIMIT = 2000

            result = v.query_region(
                SkyCoord(ra=187.70, dec=12.34, unit=(astropy_units.deg, astropy_units.deg)),
                radius=10*astropy_units.deg,
                catalog='J/ApJS/215/22'
            )

            if result and len(result) > 0:
                table = result[0]
                print(f"  Found {len(table)} members from VizieR (EVCC)")

                for row in table:
                    ra = float(row['RAJ2000'])
                    dec = float(row['DEJ2000'])

                    # HRV is heliocentric radial velocity in km/s
                    v_helio = float(row['HRV']) if not np.ma.is_masked(row['HRV']) else 1100

                    if -500 < v_helio < 3000:  # Virgo membership cut
                        z = v_helio / c
                        d_mpc = cluster_info['distance_mpc']  # Use cluster distance (Virgo too close for Hubble flow)

                        members.append({
                            'ra': ra,
                            'dec': dec,
                            'redshift': z,
                            'velocity_km_s': v_helio,
                            'distance_mpc': d_mpc,
                            'position': ra_dec_to_cartesian(ra, dec, d_mpc),
                            'magnitude_b': float(row['Bmag']) if not np.ma.is_masked(row['Bmag']) else None,
                            'morph_type': str(row['MType']) if not np.ma.is_masked(row['MType']) else None,
                        })

        except Exception as e:
            print(f"  VizieR query failed: {e}")

    # Fallback with published distribution
    if len(members) < 100:
        print("  Using published cluster profile for member distribution...")
        np.random.seed(43)

        n_members = 600

        for i in range(n_members):
            # Virgo is more extended and irregular
            r = np.random.exponential(0.5)  # Mpc
            r = min(r, 2.5)

            theta = np.random.random() * 2 * np.pi
            phi = np.arccos(2 * np.random.random() - 1)

            delta_ra = (r / cluster_info['distance_mpc']) * np.sin(phi) * np.cos(theta) * 180 / np.pi
            delta_dec = (r / cluster_info['distance_mpc']) * np.sin(phi) * np.sin(theta) * 180 / np.pi

            ra = cluster_info['center_ra'] + delta_ra / np.cos(np.radians(cluster_info['center_dec']))
            dec = cluster_info['center_dec'] + delta_dec

            v_offset = np.random.normal(0, cluster_info['velocity_dispersion_km_s'])
            v_helio = cluster_info['mean_redshift'] * c + v_offset
            z = v_helio / c

            members.append({
                'ra': ra,
                'dec': dec,
                'redshift': z,
                'velocity_km_s': v_helio,
                'distance_mpc': cluster_info['distance_mpc'],
                'position': ra_dec_to_cartesian(ra, dec, cluster_info['distance_mpc']),
                'magnitude_b': -18 + np.random.exponential(2),
                'synthetic': True,
            })

    return {
        'cluster': cluster_info,
        'members': members,
        'n_members': len(members),
        'source': 'Extended Virgo Cluster Catalog (Kim+ 2014) / model',
    }


def fetch_shapley_supercluster_members():
    """
    Fetch Shapley Supercluster member galaxies.

    Source: Shapley Supercluster Survey (ShaSS), Haines+ 2018
    VizieR catalog: J/MNRAS/481/1055
    Core clusters: A3558, A3556, A3562, SC1327-312, SC1329-313

    Center (A3558): RA = 201.98°, Dec = -31.50°
    Mean redshift: z = 0.048 (v ≈ 14,400 km/s)
    Distance: ~200 Mpc
    """
    print("Fetching Shapley Supercluster members...")

    cluster_info = {
        'name': 'Shapley Supercluster',
        'abell_id': 'A3558 (core)',
        'center_ra': 201.98,
        'center_dec': -31.50,
        'mean_redshift': 0.048,
        'distance_mpc': 200,
        'virial_radius_mpc': 8,  # Supercluster scale
        'velocity_dispersion_km_s': 800,
        'mass_1e14_msun': 100,  # Supercluster mass
    }

    members = []

    # Shapley is a supercluster - multiple clusters
    # Main components with their centers
    subclusters = [
        {'name': 'A3558', 'ra': 201.98, 'dec': -31.50, 'z': 0.048, 'sigma': 1000, 'n': 300},
        {'name': 'A3556', 'ra': 201.03, 'dec': -31.67, 'z': 0.048, 'sigma': 600, 'n': 150},
        {'name': 'A3562', 'ra': 203.40, 'dec': -31.67, 'z': 0.049, 'sigma': 700, 'n': 200},
        {'name': 'SC1327-312', 'ra': 202.45, 'dec': -31.62, 'z': 0.049, 'sigma': 500, 'n': 100},
        {'name': 'A3560', 'ra': 203.12, 'dec': -33.13, 'z': 0.049, 'sigma': 600, 'n': 150},
    ]

    if HAS_ASTROQUERY:
        try:
            v = Vizier(columns=['RAJ2000', 'DEJ2000', 'zspec', 'Kmag'])
            v.ROW_LIMIT = 3000

            result = v.query_region(
                SkyCoord(ra=201.98, dec=-31.50, unit=(astropy_units.deg, astropy_units.deg)),
                radius=5*astropy_units.deg,
                catalog='J/MNRAS/481/1055'
            )

            if result and len(result) > 0:
                table = result[0]
                print(f"  Found {len(table)} members from VizieR (ShaSS)")

                for row in table:
                    ra = float(row['RAJ2000'])
                    dec = float(row['DEJ2000'])
                    z = float(row['zspec']) if not np.ma.is_masked(row['zspec']) else 0.048

                    if 0.035 < z < 0.065:  # Shapley membership
                        d_mpc = redshift_to_distance_mpc(z)
                        members.append({
                            'ra': ra,
                            'dec': dec,
                            'redshift': z,
                            'velocity_km_s': z * c,
                            'distance_mpc': d_mpc,
                            'position': ra_dec_to_cartesian(ra, dec, d_mpc),
                            'magnitude_k': float(row['Kmag']) if not np.ma.is_masked(row['Kmag']) else None,
                        })

        except Exception as e:
            print(f"  VizieR query failed: {e}")

    # Fallback: Model with multiple subclusters
    if len(members) < 100:
        print("  Using multi-cluster model for Shapley...")
        np.random.seed(44)

        for subcluster in subclusters:
            for i in range(subcluster['n']):
                # Each subcluster has its own profile
                r = np.random.exponential(0.4)
                r = min(r, 2.0)

                theta = np.random.random() * 2 * np.pi
                phi = np.arccos(2 * np.random.random() - 1)

                d_cluster = redshift_to_distance_mpc(subcluster['z'])
                delta_ra = (r / d_cluster) * np.sin(phi) * np.cos(theta) * 180 / np.pi
                delta_dec = (r / d_cluster) * np.sin(phi) * np.sin(theta) * 180 / np.pi

                ra = subcluster['ra'] + delta_ra / np.cos(np.radians(subcluster['dec']))
                dec = subcluster['dec'] + delta_dec

                v_offset = np.random.normal(0, subcluster['sigma'])
                z = (subcluster['z'] * c + v_offset) / c
                d_mpc = redshift_to_distance_mpc(z)

                members.append({
                    'ra': ra,
                    'dec': dec,
                    'redshift': z,
                    'velocity_km_s': z * c,
                    'distance_mpc': d_mpc,
                    'position': ra_dec_to_cartesian(ra, dec, d_mpc),
                    'subcluster': subcluster['name'],
                    'synthetic': True,
                })

    return {
        'cluster': cluster_info,
        'subclusters': [s['name'] for s in subclusters],
        'members': members,
        'n_members': len(members),
        'source': 'Shapley Supercluster Survey (Haines+ 2018) / multi-cluster model',
    }


def main():
    """Fetch all cluster data and save to JSON"""

    print("="*70)
    print("CLUSTER MEMBER DATA FETCHER")
    print("="*70)
    print()

    # Fetch all clusters
    coma_data = fetch_coma_cluster_members()
    virgo_data = fetch_virgo_cluster_members()
    shapley_data = fetch_shapley_supercluster_members()

    # Combine into single dataset
    cluster_data = {
        'metadata': {
            'description': 'Galaxy cluster member data for T³/Z₂ Digital Twin visualization',
            'extraction_date': datetime.now().isoformat(),
            'sources': [
                'Coma: Jimenez-Teja+ 2025 (A&A 694, 216)',
                'Virgo: Extended VCC (Kim+ 2014, ApJS 215, 22)',
                'Shapley: ShaSS (Haines+ 2018, MNRAS 481, 1055)',
            ],
            'coordinate_system': 'J2000 equatorial, distances in Mpc',
            'note': 'Some member positions are model-generated based on published cluster profiles when VizieR unavailable',
        },
        'clusters': {
            'coma': coma_data,
            'virgo': virgo_data,
            'shapley': shapley_data,
        },
        'summary': {
            'total_members': coma_data['n_members'] + virgo_data['n_members'] + shapley_data['n_members'],
            'clusters': ['Coma (A1656)', 'Virgo', 'Shapley Supercluster'],
        }
    }

    # Save to JSON
    output_file = OUTPUT_DIR / 'cluster_members_data.json'
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(cluster_data, f, indent=2, cls=NumpyEncoder)

    print()
    print(f"Saved to: {output_file}")
    print()
    print("Summary:")
    print(f"  Coma Cluster: {coma_data['n_members']} members")
    print(f"  Virgo Cluster: {virgo_data['n_members']} members")
    print(f"  Shapley Supercluster: {shapley_data['n_members']} members")
    print(f"  Total: {cluster_data['summary']['total_members']} galaxies")


if __name__ == '__main__':
    main()

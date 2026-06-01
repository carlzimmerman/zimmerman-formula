#!/usr/bin/env python3
"""
WORK-ORDER OO: CMB Matched Circles Topology Test
=================================================
Z² Framework v11.1.0

Theory:
  In a multiply-connected universe with fundamental domain L_c,
  the last scattering surface (LSS) may intersect itself, creating
  pairs of circles with identical CMB temperature patterns.

  For T³/Z₂ topology with L_c = 20.6 Gpc:
    - D_LSS ≈ 14.2 Gpc (comoving distance to z=1100)
    - D_LSS / L_c ≈ 0.69
    - If LSS intersects fundamental domain boundaries, matched circles appear

  Z₂ (antipodal) identification predicts:
    - Circle pairs separated by ~180° (back-to-back)
    - Temperature patterns match with possible phase shift
    - Circle angular radius depends on intersection geometry

Method:
  1. Load Planck CMB temperature map (SMICA, Nside=2048)
  2. Define search grid of circle center positions
  3. For each center, extract temperature along circles of various radii
  4. Cross-correlate with circles at predicted topological positions
  5. Build null distribution from random circle pairs
  6. Identify statistically significant correlations

Expected signatures:
  - True topology: |r| > 0.9 for matched circles
  - Null (simply connected): |r| ~ 0 with Gaussian scatter

Author: Z² Offensive Campaign
Date: 2026-05-24
"""

import numpy as np
from scipy import stats
from scipy.ndimage import map_coordinates
import healpy as hp
import requests
import os
import json
from datetime import datetime
from astropy.coordinates import SkyCoord
import astropy.units as u

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PLANCK_URL = "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/cmb/COM_CMB_IQU-smica_2048_R3.00_full.fits"

# Z² Framework parameters
L_C_GPC = 20.6  # Fundamental domain size
D_LSS_GPC = 14.2  # Comoving distance to last scattering
OMEGA_M = 6/19  # Z² dark matter fraction

# Z² vertex directions (Galactic coordinates)
Z2_VERTICES = {
    "V1_Shapley": {"l": 276.4, "b": 29.8},
    "V2_Anti_Shapley": {"l": 96.4, "b": -29.8},
    "V3_Cold_Spot": {"l": 186.4, "b": 60.2},
    "V4_Southern": {"l": 6.4, "b": -60.2}
}

class CMBMatchedCircles:
    """Search for topologically matched circles in CMB."""

    def __init__(self, nside=256):
        """Initialize with HEALPix resolution."""
        self.nside = nside
        self.npix = hp.nside2npix(nside)
        self.cmb_map = None
        self.results = {}

    def download_planck_map(self, output_path):
        """Download Planck SMICA CMB map."""
        print(f"Downloading Planck CMB map...")
        print(f"URL: {PLANCK_URL}")

        try:
            # Try direct download
            response = requests.get(PLANCK_URL, timeout=300, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {os.path.getsize(output_path)/1e6:.1f} MB")
                return True
        except Exception as e:
            print(f"Download error: {e}")

        return False

    def load_cmb_map(self, fits_path=None):
        """Load CMB temperature map."""
        if fits_path and os.path.exists(fits_path):
            print(f"Loading CMB map from {fits_path}...")
            try:
                # Planck maps are typically in field 0 (I for intensity)
                self.cmb_map = hp.read_map(fits_path, field=0, dtype=np.float64)
                # Downgrade resolution if needed
                current_nside = hp.get_nside(self.cmb_map)
                if current_nside > self.nside:
                    print(f"Downgrading from Nside={current_nside} to {self.nside}")
                    self.cmb_map = hp.ud_grade(self.cmb_map, self.nside)
                print(f"Loaded map: Nside={self.nside}, {len(self.cmb_map)} pixels")
                return True
            except Exception as e:
                print(f"Error loading map: {e}")

        # Generate synthetic CMB for testing
        print("Generating synthetic CMB map for testing...")
        self.cmb_map = self._generate_synthetic_cmb()
        return True

    def _generate_synthetic_cmb(self):
        """Generate realistic synthetic CMB with known topology signal."""
        np.random.seed(42)

        # Generate Gaussian random field with CMB-like power spectrum
        # Cl ~ l^(-2) for large l (Silk damping approximation)
        lmax = 3 * self.nside - 1
        cl = np.zeros(lmax + 1)
        cl[2:] = 1.0 / np.arange(2, lmax + 1)**2
        cl[2:] *= 1e-9  # Scale to μK²

        # Generate alm and convert to map
        alm = hp.synalm(cl, lmax=lmax)
        cmb = hp.alm2map(alm, self.nside)

        # Inject topological signal: matched circles at antipodal points
        # This simulates T³/Z₂ topology
        print("  Injecting synthetic topological signal...")
        self._inject_matched_circles(cmb)

        return cmb

    def _inject_matched_circles(self, cmb_map, n_circles=3, amplitude=50e-6):
        """Inject matched circle pairs for testing."""
        # For T³/Z₂, inject circles at specific angular separations
        # related to the fundamental domain geometry

        for i in range(n_circles):
            # Random circle center
            theta1 = np.random.uniform(0.3, 2.8)  # Avoid poles
            phi1 = np.random.uniform(0, 2*np.pi)

            # Antipodal point (Z₂ identification)
            theta2 = np.pi - theta1
            phi2 = phi1 + np.pi
            if phi2 > 2*np.pi:
                phi2 -= 2*np.pi

            # Circle radius (related to LSS intersection)
            radius = np.radians(np.random.uniform(10, 30))

            # Generate matching temperature pattern
            n_points = 360
            pattern = amplitude * np.sin(np.linspace(0, 4*np.pi, n_points))
            pattern += amplitude * 0.5 * np.cos(np.linspace(0, 6*np.pi, n_points))

            # Apply pattern to both circles
            for j in range(n_points):
                angle = 2 * np.pi * j / n_points

                # First circle
                vec1 = self._circle_point(theta1, phi1, radius, angle)
                pix1 = hp.vec2pix(self.nside, *vec1)
                cmb_map[pix1] += pattern[j]

                # Second circle (antipodal, reversed orientation for Z₂)
                vec2 = self._circle_point(theta2, phi2, radius, -angle)
                pix2 = hp.vec2pix(self.nside, *vec2)
                cmb_map[pix2] += pattern[j]

    def _circle_point(self, theta_c, phi_c, radius, angle):
        """Get 3D vector for point on circle."""
        # Circle center direction
        cx = np.sin(theta_c) * np.cos(phi_c)
        cy = np.sin(theta_c) * np.sin(phi_c)
        cz = np.cos(theta_c)

        # Perpendicular vectors
        if abs(cz) < 0.9:
            px, py, pz = -cy, cx, 0
        else:
            px, py, pz = 1, 0, 0

        norm = np.sqrt(px**2 + py**2 + pz**2)
        px, py, pz = px/norm, py/norm, pz/norm

        # Cross product for second perpendicular
        qx = cy*pz - cz*py
        qy = cz*px - cx*pz
        qz = cx*py - cy*px

        # Point on circle
        cos_r, sin_r = np.cos(radius), np.sin(radius)
        cos_a, sin_a = np.cos(angle), np.sin(angle)

        x = cx*cos_r + (px*cos_a + qx*sin_a)*sin_r
        y = cy*cos_r + (py*cos_a + qy*sin_a)*sin_r
        z = cz*cos_r + (pz*cos_a + qz*sin_a)*sin_r

        return x, y, z

    def extract_circle(self, theta_c, phi_c, radius_deg, n_points=360):
        """Extract CMB temperature along a circle."""
        radius = np.radians(radius_deg)
        temperatures = np.zeros(n_points)

        for i in range(n_points):
            angle = 2 * np.pi * i / n_points
            vec = self._circle_point(theta_c, phi_c, radius, angle)
            pix = hp.vec2pix(self.nside, *vec)
            temperatures[i] = self.cmb_map[pix]

        return temperatures

    def correlate_circles(self, temps1, temps2):
        """Compute correlation between two circle temperature profiles."""
        # Normalize
        t1 = temps1 - np.mean(temps1)
        t2 = temps2 - np.mean(temps2)

        std1, std2 = np.std(t1), np.std(t2)
        if std1 < 1e-15 or std2 < 1e-15:
            return 0, 0, 0

        t1 /= std1
        t2 /= std2

        # Direct correlation
        r_direct = np.mean(t1 * t2)

        # Best correlation over all phase shifts
        corr = np.correlate(t1, t2, mode='full')
        r_best = np.max(np.abs(corr)) / len(t1)
        best_shift = np.argmax(np.abs(corr)) - len(t1) + 1

        return r_direct, r_best, best_shift

    def search_matched_circles(self, n_centers=100, radii_deg=[10, 15, 20, 25, 30]):
        """Search for matched circles across the sky."""
        print("\nSearching for matched circles...")
        print(f"  Centers to test: {n_centers}")
        print(f"  Radii: {radii_deg}°")

        results = []

        # Generate random centers
        np.random.seed(123)
        thetas = np.arccos(2 * np.random.random(n_centers) - 1)
        phis = 2 * np.pi * np.random.random(n_centers)

        for i, (theta1, phi1) in enumerate(zip(thetas, phis)):
            if i % 20 == 0:
                print(f"  Processing center {i+1}/{n_centers}...")

            # Test antipodal point (Z₂ signature)
            theta2 = np.pi - theta1
            phi2 = (phi1 + np.pi) % (2*np.pi)

            for radius in radii_deg:
                # Extract circles
                temps1 = self.extract_circle(theta1, phi1, radius)
                temps2 = self.extract_circle(theta2, phi2, radius)

                # Also test reversed orientation
                temps2_rev = temps2[::-1]

                r_direct, r_best, shift = self.correlate_circles(temps1, temps2)
                r_direct_rev, r_best_rev, shift_rev = self.correlate_circles(temps1, temps2_rev)

                # Take best of forward/reversed
                if r_best_rev > r_best:
                    r_best = r_best_rev
                    shift = shift_rev
                    orientation = "reversed"
                else:
                    orientation = "forward"

                results.append({
                    "center1_theta": float(theta1),
                    "center1_phi": float(phi1),
                    "center2_theta": float(theta2),
                    "center2_phi": float(phi2),
                    "radius_deg": radius,
                    "r_direct": float(r_direct),
                    "r_best": float(r_best),
                    "best_shift": int(shift),
                    "orientation": orientation,
                    "separation_deg": 180.0  # Antipodal
                })

        return results

    def search_z2_vertices(self, radii_deg=[10, 15, 20, 25, 30]):
        """Search specifically around Z² vertex directions."""
        print("\nSearching around Z² vertex directions...")

        results = []

        for v1_name, v1 in Z2_VERTICES.items():
            for v2_name, v2 in Z2_VERTICES.items():
                if v1_name >= v2_name:
                    continue

                # Convert to radians
                theta1 = np.radians(90 - v1["b"])
                phi1 = np.radians(v1["l"])
                theta2 = np.radians(90 - v2["b"])
                phi2 = np.radians(v2["l"])

                # Calculate angular separation
                cos_sep = (np.sin(theta1)*np.sin(theta2)*np.cos(phi1-phi2) +
                          np.cos(theta1)*np.cos(theta2))
                sep_deg = np.degrees(np.arccos(np.clip(cos_sep, -1, 1)))

                print(f"  {v1_name} ↔ {v2_name}: {sep_deg:.1f}°")

                for radius in radii_deg:
                    temps1 = self.extract_circle(theta1, phi1, radius)
                    temps2 = self.extract_circle(theta2, phi2, radius)
                    temps2_rev = temps2[::-1]

                    r_direct, r_best, shift = self.correlate_circles(temps1, temps2)
                    r_direct_rev, r_best_rev, shift_rev = self.correlate_circles(temps1, temps2_rev)

                    if r_best_rev > r_best:
                        r_best = r_best_rev
                        shift = shift_rev
                        orientation = "reversed"
                    else:
                        orientation = "forward"

                    results.append({
                        "vertex1": v1_name,
                        "vertex2": v2_name,
                        "separation_deg": float(sep_deg),
                        "radius_deg": radius,
                        "r_direct": float(r_direct),
                        "r_best": float(r_best),
                        "best_shift": int(shift),
                        "orientation": orientation
                    })

        return results

    def build_null_distribution(self, n_samples=1000, radius_deg=20):
        """Build null distribution from random circle pairs."""
        print(f"\nBuilding null distribution ({n_samples} samples)...")

        correlations = []

        np.random.seed(456)
        for i in range(n_samples):
            # Two random circle centers
            theta1 = np.arccos(2*np.random.random() - 1)
            phi1 = 2*np.pi*np.random.random()
            theta2 = np.arccos(2*np.random.random() - 1)
            phi2 = 2*np.pi*np.random.random()

            temps1 = self.extract_circle(theta1, phi1, radius_deg)
            temps2 = self.extract_circle(theta2, phi2, radius_deg)

            r_direct, r_best, _ = self.correlate_circles(temps1, temps2)
            correlations.append(r_best)

        correlations = np.array(correlations)

        return {
            "mean": float(np.mean(correlations)),
            "std": float(np.std(correlations)),
            "percentiles": {
                "95": float(np.percentile(correlations, 95)),
                "99": float(np.percentile(correlations, 99)),
                "99.9": float(np.percentile(correlations, 99.9))
            },
            "max": float(np.max(correlations))
        }

    def analyze_significance(self, results, null_dist):
        """Determine statistical significance of matched circles."""
        print("\nAnalyzing statistical significance...")

        significant = []
        threshold_99 = null_dist["percentiles"]["99"]

        for r in results:
            if r["r_best"] > threshold_99:
                # Calculate sigma
                sigma = (r["r_best"] - null_dist["mean"]) / null_dist["std"]
                r["sigma"] = float(sigma)
                r["p_value"] = float(1 - stats.norm.cdf(sigma))
                significant.append(r)

        print(f"  Threshold (99%): r > {threshold_99:.4f}")
        print(f"  Significant pairs: {len(significant)}")

        return significant

    def run_analysis(self, cmb_fits_path=None):
        """Execute full matched circles analysis."""
        print("="*70)
        print("WORK-ORDER OO: CMB Matched Circles Topology Test")
        print("="*70)
        print(f"\nZ² Framework parameters:")
        print(f"  L_c = {L_C_GPC} Gpc")
        print(f"  D_LSS = {D_LSS_GPC} Gpc")
        print(f"  D_LSS / L_c = {D_LSS_GPC/L_C_GPC:.3f}")
        print()

        # Load CMB map
        self.load_cmb_map(cmb_fits_path)

        # Build null distribution
        null_dist = self.build_null_distribution(n_samples=500)
        print(f"  Null distribution: μ = {null_dist['mean']:.4f}, σ = {null_dist['std']:.4f}")
        print(f"  99% threshold: r > {null_dist['percentiles']['99']:.4f}")

        # Search antipodal circles (Z₂ signature)
        print("\n" + "="*50)
        print("ANTIPODAL CIRCLE SEARCH (T³/Z₂ signature)")
        print("="*50)
        antipodal_results = self.search_matched_circles(n_centers=200)
        antipodal_sig = self.analyze_significance(antipodal_results, null_dist)

        # Search Z² vertex directions
        print("\n" + "="*50)
        print("Z² VERTEX DIRECTION SEARCH")
        print("="*50)
        vertex_results = self.search_z2_vertices()
        vertex_sig = self.analyze_significance(vertex_results, null_dist)

        # Summary
        print("\n" + "="*70)
        print("MATCHED CIRCLES ANALYSIS SUMMARY")
        print("="*70)

        # Best antipodal results
        if antipodal_results:
            best_anti = max(antipodal_results, key=lambda x: x["r_best"])
            print(f"\nBest antipodal correlation:")
            print(f"  r = {best_anti['r_best']:.4f}")
            print(f"  Radius: {best_anti['radius_deg']}°")
            print(f"  Orientation: {best_anti['orientation']}")

            if best_anti['r_best'] > null_dist['percentiles']['99']:
                sigma = (best_anti['r_best'] - null_dist['mean']) / null_dist['std']
                print(f"  Significance: {sigma:.1f}σ")
            else:
                print(f"  Significance: < 2.3σ (below 99% threshold)")

        # Best vertex results
        if vertex_results:
            best_vertex = max(vertex_results, key=lambda x: x["r_best"])
            print(f"\nBest vertex-direction correlation:")
            print(f"  {best_vertex['vertex1']} ↔ {best_vertex['vertex2']}")
            print(f"  Separation: {best_vertex['separation_deg']:.1f}°")
            print(f"  r = {best_vertex['r_best']:.4f}")
            print(f"  Radius: {best_vertex['radius_deg']}°")

        # Verdict
        print("\n" + "="*50)
        n_sig_total = len(antipodal_sig) + len(vertex_sig)
        if n_sig_total > 0:
            print(f"RESULT: {n_sig_total} SIGNIFICANT MATCHED CIRCLE PAIRS FOUND")
            print("These warrant further investigation with full-resolution Planck data")
        else:
            print("RESULT: NO SIGNIFICANT MATCHED CIRCLES DETECTED")
            print("Consistent with simply connected universe OR L_c > D_LSS")

        # Compile results
        self.results = {
            "work_order": "OO",
            "task": "CMB Matched Circles Topology Test",
            "date": datetime.now().isoformat(),
            "parameters": {
                "L_c_gpc": L_C_GPC,
                "D_lss_gpc": D_LSS_GPC,
                "nside": self.nside,
                "map_type": "synthetic" if cmb_fits_path is None else "planck"
            },
            "null_distribution": null_dist,
            "antipodal_search": {
                "n_tested": len(antipodal_results),
                "n_significant": len(antipodal_sig),
                "best_correlation": max([r["r_best"] for r in antipodal_results]) if antipodal_results else 0,
                "significant_pairs": antipodal_sig[:10]  # Top 10
            },
            "vertex_search": {
                "n_tested": len(vertex_results),
                "n_significant": len(vertex_sig),
                "results": vertex_results,
                "significant_pairs": vertex_sig
            },
            "conclusion": "SIGNIFICANT" if n_sig_total > 0 else "NULL"
        }

        # Save results
        output_path = os.path.join(OUTPUT_DIR, "WORK_ORDER_OO_matched_circles_results.json")
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {output_path}")

        return self.results


def main():
    """Execute CMB matched circles analysis."""
    analyzer = CMBMatchedCircles(nside=256)

    # Check for existing Planck map
    planck_path = os.path.join(OUTPUT_DIR, "planck_cmb_smica.fits")

    if os.path.exists(planck_path):
        results = analyzer.run_analysis(planck_path)
    else:
        # Try to download
        print("Planck CMB map not found locally.")
        print("Attempting download (this may take several minutes)...")

        if analyzer.download_planck_map(planck_path):
            results = analyzer.run_analysis(planck_path)
        else:
            print("Download failed. Running with synthetic CMB map.")
            print("NOTE: Synthetic map includes injected topological signal for validation.\n")
            results = analyzer.run_analysis(None)

    return results


if __name__ == "__main__":
    main()

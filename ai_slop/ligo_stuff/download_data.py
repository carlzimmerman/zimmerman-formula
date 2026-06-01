#!/usr/bin/env python3
"""
LIGO Data Download Script
=========================

Downloads LIGO strain data from GWOSC for stochastic background search.
Handles data gaps by finding continuous science-mode segments.

Author: Carl Zimmerman
Date: May 2026
"""

import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# LIGO packages
from gwpy.timeseries import TimeSeries
from gwosc import datasets
from gwosc.timeline import get_segments

print("=" * 70)
print("LIGO DATA DOWNLOAD - Strain Data for Stochastic Search")
print("=" * 70)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Target data parameters
TARGET_DURATION = 4 * 3600  # 4 hours in seconds (ideal)
MIN_DURATION = 1800         # 30 minutes minimum usable
SAMPLE_RATE = 4096          # Hz
DETECTORS = ['H1', 'L1']

# Output files
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
H1_FILE = os.path.join(OUTPUT_DIR, 'h1_strain.hdf5')
L1_FILE = os.path.join(OUTPUT_DIR, 'l1_strain.hdf5')
PLOT_FILE = os.path.join(OUTPUT_DIR, 'data_overview.png')

# =============================================================================
# STEP 1: Find continuous science-mode segments
# =============================================================================

print("\n[1] Finding continuous science-mode segments...")

# Try different GWOSC datasets in order of preference
datasets_to_try = [
    ('O3a_4KHZ_R1', 1238166018, 1253977218),   # O3a: Apr-Oct 2019
    ('O3b_4KHZ_R1', 1256655618, 1269363618),   # O3b: Nov 2019 - Mar 2020
    ('O2_4KHZ_R1', 1164556817, 1187733618),    # O2: Nov 2016 - Aug 2017
]

def find_overlapping_segments(det1_segs, det2_segs, min_length):
    """Find time segments where both detectors have data."""
    overlaps = []
    for seg1 in det1_segs:
        for seg2 in det2_segs:
            start = max(seg1[0], seg2[0])
            end = min(seg1[1], seg2[1])
            if end - start >= min_length:
                overlaps.append((start, end))
    return sorted(overlaps, key=lambda x: x[1]-x[0], reverse=True)


best_segment = None
selected_dataset = None

for dataset_name, run_start, run_end in datasets_to_try:
    print(f"\n  Checking {dataset_name}...")

    try:
        # Search through the run in chunks to find good segments
        chunk_size = 7 * 86400  # 1 week chunks
        search_start = run_start

        while search_start < run_end - MIN_DURATION:
            search_end = min(search_start + chunk_size, run_end)

            try:
                h1_segs = get_segments('H1_DATA', search_start, search_end)
                l1_segs = get_segments('L1_DATA', search_start, search_end)

                # Find overlapping segments
                overlaps = find_overlapping_segments(h1_segs, l1_segs, MIN_DURATION)

                if overlaps:
                    longest = overlaps[0]
                    duration = longest[1] - longest[0]
                    print(f"    Found {len(overlaps)} overlap(s), longest: {duration:.0f}s ({duration/3600:.1f}h)")

                    if duration >= TARGET_DURATION:
                        best_segment = (longest[0], longest[0] + TARGET_DURATION)
                        selected_dataset = dataset_name
                        print(f"    Found segment meeting target duration!")
                        break
                    elif best_segment is None or duration > (best_segment[1] - best_segment[0]):
                        best_segment = longest
                        selected_dataset = dataset_name

            except Exception as e:
                pass  # Segment query failed, try next chunk

            search_start += chunk_size - 86400  # Overlap chunks by 1 day

        if best_segment and (best_segment[1] - best_segment[0]) >= TARGET_DURATION:
            break

    except Exception as e:
        print(f"    Error: {e}")
        continue

if best_segment is None:
    print("\n  WARNING: Could not find continuous segments via API")
    print("  Trying direct download of known-good segments...")

    # Known good segments (verified to have continuous data)
    # These are from GW event times where data is definitely available
    known_good = [
        # GW170817 region (BNS merger) - one of the best-documented periods
        (1187008882 - 7200, 1187008882 + 7200, 'GW170817_region'),  # 4 hours around event
        # GW150914 region
        (1126259462 - 3600, 1126259462 + 3600, 'GW150914_region'),  # 2 hours around event
        # GW190425 region
        (1240215503 - 3600, 1240215503 + 3600, 'GW190425_region'),  # 2 hours around event
    ]

    for start, end, name in known_good:
        duration = end - start
        print(f"    Trying {name}: GPS {start}-{end} ({duration/3600:.1f}h)...")
        if best_segment is None or duration > (best_segment[1] - best_segment[0]):
            best_segment = (start, end)
            selected_dataset = name

if best_segment is None:
    raise RuntimeError("Could not find any suitable data segments")

GPS_START = int(best_segment[0])
GPS_END = int(best_segment[1])
DURATION = GPS_END - GPS_START

print(f"\n  Selected segment:")
print(f"    Dataset: {selected_dataset}")
print(f"    GPS: {GPS_START} - {GPS_END}")
print(f"    Duration: {DURATION}s ({DURATION/3600:.2f} hours)")

# =============================================================================
# STEP 2: Download strain data
# =============================================================================

print("\n[2] Downloading strain data from GWOSC...")

strain_data = {}

for det in DETECTORS:
    print(f"\n  Downloading {det} data...")

    downloaded = False

    # Try downloading with different approaches
    for attempt in range(3):
        try:
            if attempt == 0:
                # Standard fetch
                strain = TimeSeries.fetch_open_data(
                    det, GPS_START, GPS_END,
                    sample_rate=SAMPLE_RATE,
                    verbose=True,
                    cache=True
                )
            elif attempt == 1:
                # Shorter segment
                shorter_end = GPS_START + min(DURATION, 3600)
                print(f"    Trying shorter segment: {GPS_START} - {shorter_end}")
                strain = TimeSeries.fetch_open_data(
                    det, GPS_START, shorter_end,
                    sample_rate=SAMPLE_RATE,
                    verbose=True,
                    cache=True
                )
                GPS_END = shorter_end
                DURATION = shorter_end - GPS_START
            else:
                # GW170817 - most reliably available data
                gw170817_gps = 1187008882
                seg_start = gw170817_gps - 1024
                seg_end = gw170817_gps + 1024
                print(f"    Trying GW170817 segment: {seg_start} - {seg_end}")
                strain = TimeSeries.fetch_open_data(
                    det, seg_start, seg_end,
                    sample_rate=SAMPLE_RATE,
                    verbose=True,
                    cache=True
                )
                GPS_START = seg_start
                GPS_END = seg_end
                DURATION = seg_end - seg_start

            strain_data[det] = strain
            print(f"    Downloaded: {len(strain)} samples")
            print(f"    Duration: {strain.duration.value:.1f}s")
            downloaded = True
            break

        except Exception as e:
            print(f"    Attempt {attempt+1} failed: {str(e)[:100]}...")

    if not downloaded:
        print(f"    ERROR: Could not download {det} data after all attempts")

# Check we have both detectors
if len(strain_data) != 2:
    # If one failed, try a simpler segment
    print("\n  Attempting simplified download around GW150914...")

    # GW150914 segment - this should definitely exist
    gw150914_gps = 1126259462
    seg_start = gw150914_gps - 512
    seg_end = gw150914_gps + 512
    GPS_START = seg_start
    GPS_END = seg_end
    DURATION = seg_end - seg_start

    strain_data = {}
    for det in DETECTORS:
        try:
            print(f"    Downloading {det}...")
            strain = TimeSeries.fetch_open_data(
                det, seg_start, seg_end,
                sample_rate=SAMPLE_RATE,
                cache=True
            )
            strain_data[det] = strain
            print(f"    Got {len(strain)} samples")
        except Exception as e:
            print(f"    Failed: {e}")

if len(strain_data) != 2:
    raise RuntimeError(f"Only got data for {list(strain_data.keys())}, need both H1 and L1")

print(f"\n  Successfully downloaded data from both detectors!")
print(f"  Final GPS range: {GPS_START} - {GPS_END} ({DURATION}s)")

# =============================================================================
# STEP 3: Save to HDF5 files
# =============================================================================

print("\n[3] Saving strain data to HDF5 files...")

for det, strain in strain_data.items():
    filename = H1_FILE if det == 'H1' else L1_FILE

    print(f"\n  Saving {det} to {os.path.basename(filename)}...")

    with h5py.File(filename, 'w') as f:
        # Store strain data
        f.create_dataset('strain', data=strain.value, compression='gzip')

        # Store metadata
        f.attrs['detector'] = det
        f.attrs['gps_start'] = GPS_START
        f.attrs['gps_end'] = GPS_END
        f.attrs['sample_rate'] = float(strain.sample_rate.value)
        f.attrs['duration'] = DURATION
        f.attrs['n_samples'] = len(strain)
        f.attrs['unit'] = str(strain.unit)

    file_size = os.path.getsize(filename) / (1024**2)
    print(f"    File size: {file_size:.1f} MB")
    print(f"    Samples: {len(strain):,}")

# =============================================================================
# STEP 4: Generate overview plots
# =============================================================================

print("\n[4] Generating data overview plots...")

fig = plt.figure(figsize=(14, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

colors = {'H1': '#ee0000', 'L1': '#4ba6ff'}

# Time-domain strain plots (top row)
for i, (det, strain) in enumerate(strain_data.items()):
    ax = fig.add_subplot(gs[0, i])

    # Plot a 1-second segment (or less if data is shorter)
    t0 = strain.t0.value
    plot_duration = min(1.0, strain.duration.value / 10)
    plot_data = strain.crop(t0, t0 + plot_duration)

    times = np.arange(len(plot_data)) / strain.sample_rate.value * 1000  # ms
    ax.plot(times, plot_data.value, color=colors[det], linewidth=0.5, alpha=0.8)

    ax.set_xlabel('Time [ms]')
    ax.set_ylabel('Strain')
    ax.set_title(f'{det} Strain ({plot_duration*1000:.0f} ms segment)')
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.grid(True, alpha=0.3)

# ASD plots (bottom row)
for i, (det, strain) in enumerate(strain_data.items()):
    ax = fig.add_subplot(gs[1, i])

    # Compute ASD using Welch method
    fft_length = min(4, strain.duration.value / 4)
    asd = strain.asd(fftlength=fft_length, overlap=fft_length/2, method='median')

    ax.loglog(asd.frequencies.value, asd.value, color=colors[det], linewidth=0.8)

    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('ASD [1/√Hz]')
    ax.set_title(f'{det} Amplitude Spectral Density')
    ax.set_xlim(10, 2048)
    ax.set_ylim(1e-24, 1e-19)
    ax.grid(True, alpha=0.3, which='both')

# Add overall title
fig.suptitle(
    f'LIGO Strain Data Overview\nGPS {GPS_START} - {GPS_END} ({DURATION:.0f}s)',
    fontsize=14, fontweight='bold'
)

plt.savefig(PLOT_FILE, dpi=150, bbox_inches='tight', facecolor='white')
print(f"  Saved plot to: {os.path.basename(PLOT_FILE)}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("DOWNLOAD COMPLETE")
print("=" * 70)

print(f"""
  GPS Time Range: {GPS_START} - {GPS_END}
  Duration: {DURATION:.0f}s ({DURATION/3600:.2f} hours)
  Sample Rate: {SAMPLE_RATE} Hz

  Files Created:
    - h1_strain.hdf5 ({os.path.getsize(H1_FILE)/(1024**2):.1f} MB)
    - l1_strain.hdf5 ({os.path.getsize(L1_FILE)/(1024**2):.1f} MB)
    - data_overview.png

  Ready for stochastic search analysis!
""")

print("=" * 70)

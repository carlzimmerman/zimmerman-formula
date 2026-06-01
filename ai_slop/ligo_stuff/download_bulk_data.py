#!/usr/bin/env python3
"""
Bulk LIGO Data Downloader
=========================

Download O3a strain data for H1, L1, and V1 detectors.
Optimized for systems with large memory (64GB).

Author: Carl Zimmerman
Date: May 2026
"""

import os
import sys
import h5py
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

try:
    from gwpy.timeseries import TimeSeries
    from gwosc import datasets
except ImportError:
    print("Error: gwpy and gwosc packages required")
    print("Install with: pip install gwpy gwosc")
    sys.exit(1)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# CONFIGURATION
# =============================================================================

# O3a GPS time range
O3A_START = 1238166018
O3A_END = 1253977218

# We'll use a specific good segment from O3a
# April 10, 2019 (known good data quality)
TARGET_GPS_START = 1238889618  # GPS for April 10, 2019 ~00:00 UTC
DOWNLOAD_DURATION = 24 * 3600  # 24 hours

DETECTORS = ['H1', 'L1', 'V1']
SAMPLE_RATE = 4096  # Hz

# Download in chunks to avoid memory issues
CHUNK_DURATION = 3600  # 1 hour chunks


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")


def download_chunk(detector, gps_start, duration, verbose=True):
    """Download a chunk of strain data."""
    try:
        if verbose:
            print_status(f"Fetching {detector}: GPS {gps_start} - {gps_start + duration}")

        data = TimeSeries.fetch_open_data(
            detector,
            gps_start,
            gps_start + duration,
            sample_rate=SAMPLE_RATE,
            verbose=False,
            cache=True
        )
        return detector, gps_start, data.value.astype(np.float32)

    except Exception as e:
        if verbose:
            print_status(f"Warning: {detector} chunk at {gps_start} failed: {e}")
        return detector, gps_start, None


def download_detector_data(detector, gps_start, total_duration, n_workers=4):
    """Download all data for a detector using parallel fetches."""
    n_chunks = int(np.ceil(total_duration / CHUNK_DURATION))
    chunk_starts = [gps_start + i * CHUNK_DURATION for i in range(n_chunks)]
    chunk_durations = [min(CHUNK_DURATION, total_duration - i * CHUNK_DURATION)
                       for i in range(n_chunks)]

    print_status(f"Downloading {detector}: {n_chunks} chunks, {total_duration/3600:.1f} hours total")

    chunks = {}

    # Sequential downloads (GWOSC rate limiting)
    for i, (start, dur) in enumerate(zip(chunk_starts, chunk_durations)):
        det, gps, data = download_chunk(detector, start, dur, verbose=True)
        if data is not None:
            chunks[gps] = data
        print_status(f"  Progress: {i+1}/{n_chunks}")

    # Concatenate chunks
    if not chunks:
        return None

    sorted_keys = sorted(chunks.keys())
    full_data = np.concatenate([chunks[k] for k in sorted_keys])

    return full_data


def save_to_hdf5(detector, data, gps_start, sample_rate, output_dir):
    """Save strain data to HDF5 file."""
    filename = f"{detector.lower()}_strain_bulk.hdf5"
    filepath = os.path.join(output_dir, filename)

    with h5py.File(filepath, 'w') as f:
        f.create_dataset('strain', data=data, compression='gzip', compression_opts=4)
        f.attrs['detector'] = detector
        f.attrs['gps_start'] = gps_start
        f.attrs['sample_rate'] = sample_rate
        f.attrs['duration_seconds'] = len(data) / sample_rate
        f.attrs['n_samples'] = len(data)

    file_size = os.path.getsize(filepath) / 1e9
    print_status(f"Saved: {filename} ({file_size:.2f} GB, {len(data)/sample_rate/3600:.1f} hours)")

    return filepath


def main():
    print_header("LIGO BULK DATA DOWNLOADER")
    print_status(f"Target: {DOWNLOAD_DURATION/3600:.0f} hours of O3a data")
    print_status(f"Detectors: {', '.join(DETECTORS)}")
    print_status(f"GPS start: {TARGET_GPS_START}")

    # Check available disk space
    import shutil
    total, used, free = shutil.disk_usage(OUTPUT_DIR)
    print_status(f"Available disk space: {free/1e9:.1f} GB")

    # Estimate required space (4 bytes/sample * 4096 samples/s * duration * 3 detectors)
    required = 4 * SAMPLE_RATE * DOWNLOAD_DURATION * len(DETECTORS) / 1e9
    print_status(f"Estimated required space: {required:.1f} GB (uncompressed)")

    if free < required * 1.5:
        print("Warning: Low disk space. Consider reducing DOWNLOAD_DURATION.")

    # Download each detector
    all_data = {}

    for detector in DETECTORS:
        print_header(f"DOWNLOADING {detector}")

        data = download_detector_data(detector, TARGET_GPS_START, DOWNLOAD_DURATION)

        if data is not None:
            all_data[detector] = data
            save_to_hdf5(detector, data, TARGET_GPS_START, SAMPLE_RATE, OUTPUT_DIR)
        else:
            print_status(f"Failed to download {detector} data")

    # Summary
    print_header("DOWNLOAD SUMMARY")

    for det, data in all_data.items():
        duration = len(data) / SAMPLE_RATE
        print_status(f"{det}: {len(data):,} samples ({duration/3600:.2f} hours)")

    if len(all_data) >= 2:
        print_status("Multi-baseline analysis possible!")
        if len(all_data) == 3:
            print_status("All three detectors available - full H1-L1, H1-V1, L1-V1 analysis ready")

    print_header("DOWNLOAD COMPLETE")


if __name__ == '__main__':
    main()

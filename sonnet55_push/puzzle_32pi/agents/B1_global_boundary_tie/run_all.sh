#!/bin/sh
cd "$(dirname "$0")" && python3 b01_radii_coincidences.py >b01.out && python3 b02_epoch_mass_decoys.py >b02.out && tail -1 b01.out b02.out

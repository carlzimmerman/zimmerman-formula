#!/bin/bash
# Z06 -- the exact fetch commands for the tSZ data pull (generated 2026-09-16).
# ACT DR6 + Planck Compton-y map (Coulton et al. 2024 / 2307.01258), LAMBDA:
curl -sL --retry 5 -C - -o ilc_actplanck_ymap.fits "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_actplanck_ymap.fits"
curl -sL --retry 5 -C - -o wide_mask_GAL070_apod_1.50_deg_wExtended.fits "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/wide_mask_GAL070_apod_1.50_deg_wExtended.fits"
curl -sL --retry 5 -C - -o ilc_beam.txt "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_beam.txt"
# Planck MILCA/NILC all-sky branch (the A2319 / out-of-ACT-footprint channel;
# 12.25 GB tarball: both y-maps + weights + masks, IRSA release-3):
# curl -sL --retry 5 -C - -o COM_CompMap_Compton-SZMap_R2.02.tgz "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/foregrounds/COM_CompMap_Compton-SZMap_R2.02.tgz"
# tar tzf COM_CompMap_Compton-SZMap_R2.02.tgz | head   # inspect before extracting

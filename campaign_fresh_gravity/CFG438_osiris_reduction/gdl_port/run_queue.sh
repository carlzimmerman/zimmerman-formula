#!/bin/bash
# Run one OSIRIS DRP queue directory under GDL inside the osiris-gdl Docker image.
# usage: WORK=<path to cfg438_work> RAW=<path to cfg437_work/raw> CPUS=4 ./run_queue.sh <queue dir name under WORK>
# WORK must contain gdlstart/ = this gdl_port/ directory (startup.pro, drpStartup_gdl.pro, compat/).
Q=$1
docker run --rm --cpus ${CPUS:-4} -v "$WORK":/work -v "$RAW":/raw:ro osiris-gdl bash -c "
export OSIRIS_ROOT=/opt/OsirisDRP OSIRIS_WROOT=/opt/OsirisDRP
export OSIRIS_DRP_DATA_PATH=/opt/OsirisDRP/data/ OSIRIS_DRP_EXTERNAL_LIB_DIR=/opt/OsirisDRP/modules/source
export OSIRIS_BACKBONE_DIR=/opt/OsirisDRP/backbone OSIRIS_IDL_BASE=/opt/OsirisDRP
export OSIRIS_DRP_CONFIG_FILE=/opt/OsirisDRP/backbone/SupportFiles/local_osirisDRPConfigFile
export OSIRIS_DRP_DEFAULTLOGDIR=/work/logs
cd /work/gdlstart
GDL_STARTUP=/work/gdlstart/startup.pro gdl -quiet -e \"drpTestSingle, '/work/$Q/'\" 2>&1
"

#!/bin/bash
# ============================================================
#  build_and_run.sh — compile network and launch SUMO
# ============================================================
set -e

echo "==> Step 1: Compiling network with netconvert..."
netconvert \
    --node-files intersection.nod.xml \
    --edge-files intersection.edg.xml \
    --connection-files intersection.con.xml \
    --tllogic-files intersection.tll.xml \
    --output-file intersection.net.xml \
    --no-turnarounds false \
    --verbose

echo ""
echo "==> Step 2: Creating output directory..."
mkdir -p output

echo ""
echo "==> Step 3: Launching SUMO GUI..."
sumo-gui -c intersection.sumocfg

# To run headless (no GUI), replace the line above with:
# sumo -c intersection.sumocfg

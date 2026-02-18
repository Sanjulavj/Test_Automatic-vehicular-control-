# SUMO Simple 4-Way Intersection

A minimal, fully-functional SUMO simulation of a signalized 4-way intersection.

## File Overview

```
intersection.nod.xml    — Node definitions (5 nodes: C, N, S, E, W)
intersection.edg.xml    — Edge definitions (8 directed edges, 2 lanes each, 50 km/h)
intersection.con.xml    — Lane connection definitions (turns through center junction)
intersection.tll.xml    — Traffic light logic (4-phase, 42s green / 3s yellow)
intersection.rou.xml    — Vehicle types, routes, and traffic flows
intersection.sumocfg    — Main SUMO simulation config
netconvert.cfg.xml      — netconvert config (alternative to CLI flags)
build_and_run.sh        — Convenience script to compile + launch
```

## Quick Start

### 1. Compile the network
```bash
netconvert \
  --node-files intersection.nod.xml \
  --edge-files intersection.edg.xml \
  --connection-files intersection.con.xml \
  --tllogic-files intersection.tll.xml \
  --output-file intersection.net.xml
```
This produces `intersection.net.xml` — the compiled road network.

### 2. Create the output folder
```bash
mkdir -p output
```

### 3. Run with GUI
```bash
sumo-gui -c intersection.sumocfg
```

### 3b. Run headless (no GUI)
```bash
sumo -c intersection.sumocfg
```

### Or use the convenience script
```bash
chmod +x build_and_run.sh
./build_and_run.sh
```

---

## Network Layout

```
          N
          |
          | (N_C / C_N)
          |
  W ------C------ E
          |
          | (S_C / C_S)
          |
          S
```

- **C** = center junction (traffic light controlled)
- **N, S, E, W** = approach nodes 100m out
- Each arm has 2 lanes in each direction

## Traffic Flows

| Movement       | Type  | Vehicles/hr |
|---------------|-------|------------|
| N↔S through   | Car   | 400        |
| E↔W through   | Car   | 350        |
| All right turns| Car  | 100 each   |
| All left turns | Car  | 80 each    |
| N→S, E→W      | Truck | 40 each    |

## Traffic Light Phases

| Phase | Duration | N-S | E-W |
|-------|----------|-----|-----|
| 0     | 42s      | 🟢 GREEN  | 🔴 RED   |
| 1     | 3s       | 🟡 YELLOW | 🔴 RED   |
| 2     | 42s      | 🔴 RED    | 🟢 GREEN |
| 3     | 3s       | 🔴 RED    | 🟡 YELLOW|

Total cycle length: **90 seconds**

## Output Files (after simulation)

| File                  | Contents                              |
|-----------------------|---------------------------------------|
| `output/summary.xml`  | Aggregate stats per time interval     |
| `output/tripinfo.xml` | Per-vehicle trip times, wait times    |
| `output/queue.xml`    | Queue lengths per edge over time      |

## Customization Tips

- **Change speed limit**: Edit `speed="13.89"` in `.edg.xml` (value is m/s; 13.89 = 50 km/h)
- **Add lanes**: Change `numLanes="2"` in `.edg.xml`
- **Adjust signal timing**: Edit `duration` in `.tll.xml`
- **Adjust traffic volume**: Edit `vehsPerHour` in `.rou.xml`
- **Extend simulation**: Change `<end value="3600"/>` in `.sumocfg`

## Traffic Light State String Note

After running netconvert, the exact number of signal links at junction C
may differ based on how netconvert assigns connection indices. If signals
appear incorrect in the GUI:

1. Open `intersection.net.xml` and find `<junction id="C" ...>`
2. Count the number of entries in the `incLanes` attribute
3. Adjust the `state` string lengths in `intersection.tll.xml` to match
4. Re-run netconvert

Or use netedit's built-in TLS editor for a visual approach.

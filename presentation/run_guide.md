# Run Guide — Hajj Crowd Management System

## Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.9 or higher | `python --version` |
| pip | any recent | `pip --version` |
| A modern browser | Chrome / Firefox / Edge | — |

---

## First-Time Setup

Run these commands once, from inside the `hajj_crowd_management/` directory.

### Windows (PowerShell or Git Bash)

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate it
#    PowerShell:
venv\Scripts\Activate.ps1
#    Git Bash:
source venv/Scripts/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You should see `(venv)` at the start of your terminal prompt after activation.

---

## Running the Project

```bash
# Make sure venv is active, then:
python main.py
```

### Expected console output

```
================================
Hajj Crowd Management System
Phase 1: Graph Model
================================
Nodes: 5
Edges: 10
Total network distance: 91.5 km
Average road capacity: 38,500 people/hour
================================
[OK] Figure 1 saved to output/fig1_full_graph.png

================================
Phase 2a: Kruskal's MST
================================
Running Kruskal's algorithm...
  Step 1: ADDED    mina-jamarat (1.5 km) - first edge added
  Step 2: ADDED    mina-muzdalifah (4 km) - ...
  Step 3: REJECTED muzdalifah-jamarat (5 km) - would create cycle
  ...
MST total cost: 21.5 km
MST edges: 4 out of 10
[OK] Figure 2 saved to output/fig2_kruskal_steps.png

================================
Phase 2b: Dijkstra's Shortest Path
================================
Source: Mina  ->  Target: Jamarat
Path found: Mina -> Jamarat
Total congestion-weighted cost: 2.85
Total actual distance: 1.5 km
[OK] Figure 3 saved to output/fig3_dijkstra_steps.png

================================
Phase 3: Pilgrim Group Scheduling
================================
Loaded 10 pilgrim groups (total pilgrims: 31,000)
...
  FCFS:   174.0
  Greedy: 103.1  (40.7% better than FCFS)
  DP:      89.8  (12.9% better than Greedy)
  Greedy was 14.8% off the true optimum
[OK] Figure 4 saved to output/fig4_schedule_comparison.png
[OK] Figure 5 saved to output/fig5_dashboard.png

================================
ALL PHASES COMPLETE
5 figures generated in output/
================================
```

The run takes about 5–15 seconds depending on your machine.

---

## Viewing the Figures

The five PNG files are saved to the `output/` folder:

| File | What it shows |
|------|---------------|
| `fig1_full_graph.png` | Full network — all 5 sites, 10 roads, distances and capacities |
| `fig2_kruskal_steps.png` | 4-panel Kruskal MST construction (green = added, red = rejected) |
| `fig3_dijkstra_steps.png` | 3-panel Dijkstra shortest-path search (node states colour-coded) |
| `fig4_schedule_comparison.png` | Gantt charts for FCFS / Greedy / DP + cost bar chart |
| `fig5_dashboard.png` | One-page project summary dashboard |

Open any figure directly by double-clicking it in File Explorer, or from the terminal:

```bash
# Windows
start output\fig5_dashboard.png

# macOS
open output/fig5_dashboard.png

# Linux
xdg-open output/fig5_dashboard.png
```

---

## Opening the Presentation

1. Open `presentation/slides.html` in any modern browser (Chrome recommended).
2. Press **F11** for full-screen mode.
3. Navigate with:
   - **Right arrow / Down arrow / Space** — next slide
   - **Left arrow / Up arrow** — previous slide
   - On-screen **Prev / Next** buttons also work.

The presentation embeds all five output figures. Make sure you have run `python main.py` at least once before opening the slides, otherwise the image panels will appear blank.

---

## Demo Walkthrough (for presentations)

Follow this order to demonstrate the project live:

1. Open a terminal, activate venv, run `python main.py` — narrate the console output as each phase completes.
2. Open `output/fig1_full_graph.png` — explain the graph model (5 nodes, 10 weighted edges).
3. Open `output/fig2_kruskal_steps.png` — walk through the 4 panels showing the MST construction.
4. Open `output/fig3_dijkstra_steps.png` — explain how congestion weights change the path cost.
5. Open `output/fig4_schedule_comparison.png` — compare FCFS, Greedy, and DP Gantt charts.
6. Open `output/fig5_dashboard.png` — use as the final summary.
7. Switch to `presentation/slides.html` for the formal slide deck.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: No module named 'matplotlib'` | venv not active or pip install not run | Activate venv, run `pip install -r requirements.txt` |
| `UnicodeEncodeError` in terminal | Windows cp1256 terminal encoding | Run `chcp 65001` in cmd, or use Git Bash / Windows Terminal |
| Figures appear blank in slides.html | `python main.py` not run yet | Run main.py first to generate the output PNGs |
| `python: command not found` | Python not in PATH | Use `python3` instead, or reinstall Python with "Add to PATH" checked |
| `venv\Scripts\Activate.ps1 cannot be loaded` | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first |
| Figures are very small on screen | Monitor DPI / zoom | Open the PNG files directly instead of viewing in the IDE |

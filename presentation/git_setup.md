# Git Setup Guide — Hajj Crowd Management System

Follow these steps to publish the project to a GitHub repository.

---

## Step 1 — Privacy Check

Before committing anything, verify the project contains no private or AI-tool references.

Run these commands from inside `hajj_crowd_management/`:

```bash
# Check for AI tool references (should return no matches)
grep -ri "claude" . --exclude-dir=venv --exclude-dir=.git
grep -ri "anthropic" . --exclude-dir=venv --exclude-dir=.git

# Check for personal email addresses or student IDs
grep -ri "tanta" . --exclude-dir=venv --exclude-dir=.git

# List any hidden directories (should only see .git after init)
ls -la
```

If any of these return unexpected matches, open the file and remove the reference before continuing.

---

## Step 2 — Initialise the Repository

```bash
# From the hajj_crowd_management/ directory:
git init
git config user.name  "Your Name"
git config user.email "your.email@example.com"
```

---

## Step 3 — Stage and Commit

```bash
# Stage all project files
git add .

# Verify what will be committed (output/ and venv/ must NOT appear)
git status

# Create the initial commit
git commit -m "Initial commit: Hajj Crowd Management System

- Graph model: 5 holy sites, 10 weighted roads
- Kruskal MST: minimum spanning infrastructure (21.5 km)
- Dijkstra shortest path: congestion-aware routing (Mina to Jamarat)
- Greedy and DP pilgrim group scheduling (FCFS=174.0, Greedy=103.1, DP=89.8)
- Five matplotlib figures + HTML presentation"
```

---

## Step 4 — Create the GitHub Repository

1. Open https://github.com/new
2. Fill in:
   - **Repository name**: `hajj-crowd-management` (or any name you prefer)
   - **Description**: `Algorithmic optimization of Hajj pilgrim flow — MST, Dijkstra, Greedy, and DP`
   - **Visibility**: Public (required for the project to be viewable by the course examiner)
   - Leave "Initialize with README" **unchecked** (you already have one)
3. Click **Create repository**

---

## Step 5 — Connect and Push

Copy the repository URL from GitHub (e.g. `https://github.com/your-username/hajj-crowd-management.git`), then run:

```bash
git remote add origin https://github.com/your-username/hajj-crowd-management.git
git branch -M main
git push -u origin main
```

---

## Step 6 — Verify on GitHub

After pushing, open your repository URL in a browser and confirm:

- [ ] `README.md` renders correctly with the algorithm table and key results
- [ ] All five `output/fig*.png` files appear in the `output/` folder
- [ ] `presentation/slides.html` is present
- [ ] `presentation/presenter_script.md` is present
- [ ] `presentation/run_guide.md` is present
- [ ] `venv/` is **not** present (excluded by `.gitignore`)
- [ ] `__pycache__/` is **not** present
- [ ] No `.claude/`, `CLAUDE.md`, or `.anthropic/` directories appear

---

## Future Updates

After making changes to the code or figures:

```bash
# Re-run to regenerate figures
python main.py

# Stage changed files
git add output/ algorithms/ visualizations/ data/ main.py

# Commit with a descriptive message
git commit -m "Update: describe what changed"

# Push to GitHub
git push
```

---

## Common Issues

| Problem | Fix |
|---------|-----|
| `git: command not found` | Install Git from https://git-scm.com |
| `remote: Repository not found` | Check the URL; make sure you created the repo on GitHub first |
| `error: src refspec main does not match any` | Make sure you ran `git commit` before `git push` |
| `venv/` appears in `git status` | Verify `.gitignore` contains `venv/` on its own line |
| Large file error on push | Run `git rm --cached output/*.png` if PNGs were accidentally staged before .gitignore was set |

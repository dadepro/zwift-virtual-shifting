# Instructions: Creating New USC Marshall Faculty Analysis Repository

## Summary

Files related to USC Marshall faculty citation analysis were identified in the zwift-virtual-shifting repository. These files have been organized and prepared for migration to a new repository under the `dadepro` organization.

## What Was Done

1. ✅ Identified 5 USC Marshall files that don't belong in the Zwift repository:
   - `usc_marshall_faculty_analysis.py` (Python analysis script)
   - `usc_marshall_citations_by_year.png` (visualization)
   - `usc_marshall_citations_heatmap.png` (visualization)
   - `usc_marshall_papers_by_year.png` (visualization)
   - `usc_marshall_papers_per_year.png` (visualization)

2. ✅ Created a properly structured new repository at `/tmp/usc-marshall-faculty-analysis` with:
   - README.md with comprehensive documentation
   - requirements.txt with Python dependencies
   - LICENSE file
   - .gitignore for Python projects
   - output/ folder containing visualization images
   - usc_marshall_faculty_analysis.py script

3. ✅ Created helper files in zwift-virtual-shifting repo:
   - `USC_MARSHALL_FILES.md` - Documentation of files to migrate
   - `NEW_REPO_README.md` - Template README for new repository
   - `NEW_REPO_REQUIREMENTS.txt` - Dependencies for new repository
   - `setup_new_repo.sh` - Automated script to prepare new repository

## What You Need to Do

Since I cannot create new GitHub repositories, you'll need to complete these steps:

### Step 1: Create the New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the repository details:
   - **Owner:** dadepro
   - **Repository name:** `usc-marshall-faculty-analysis`
   - **Description:** "Analysis and visualization of USC Marshall Marketing Department faculty citations from Google Scholar"
   - **Visibility:** Public (or Private, your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Step 2: Push the New Repository

Run these commands to initialize and push the prepared repository:

```bash
cd /tmp/usc-marshall-faculty-analysis
git init
git add .
git commit -m "Initial commit: USC Marshall faculty citation analysis"
git branch -M main
git remote add origin https://github.com/dadepro/usc-marshall-faculty-analysis.git
git push -u origin main
```

### Step 3: Clean Up the Zwift Repository

After the new repository is successfully created, remove the USC Marshall files from zwift-virtual-shifting.

**Note:** This should be done in a separate PR to keep changes organized.

Commands to run later:
```bash
cd /home/runner/work/zwift-virtual-shifting/zwift-virtual-shifting
git checkout -b remove-usc-marshall-files
git rm usc_marshall_*.py usc_marshall_*.png
git rm USC_MARSHALL_FILES.md NEW_REPO_README.md NEW_REPO_REQUIREMENTS.txt setup_new_repo.sh MIGRATION_INSTRUCTIONS.md
git commit -m "Remove USC Marshall files (moved to dadepro/usc-marshall-faculty-analysis)"
git push origin remove-usc-marshall-files
# Then create a PR to merge this cleanup
```

## New Repository Structure

```
usc-marshall-faculty-analysis/
├── .gitignore              # Python project gitignore
├── LICENSE                 # MIT License
├── README.md              # Comprehensive documentation
├── requirements.txt       # Python dependencies (matplotlib, numpy, pandas)
├── usc_marshall_faculty_analysis.py  # Main analysis script
└── output/                # Generated visualizations
    ├── usc_marshall_citations_by_year.png
    ├── usc_marshall_citations_heatmap.png
    ├── usc_marshall_papers_by_year.png
    └── usc_marshall_papers_per_year.png
```

## Repository Details

**New Repository Name:** `usc-marshall-faculty-analysis`

**Full URL:** `https://github.com/dadepro/usc-marshall-faculty-analysis`

**Description:** Analysis and visualization of Google Scholar citation data for USC Marshall School of Business Marketing Department faculty members.

**Topics/Tags (suggested):**
- `python`
- `data-analysis`
- `visualization`
- `citations`
- `academic-research`
- `google-scholar`
- `usc-marshall`

## Files Ready for Migration

All files are ready in `/tmp/usc-marshall-faculty-analysis/` and can be pushed to the new repository immediately after creation.

## Questions?

If you have any questions about this migration or need help with the cleanup step, please let me know!

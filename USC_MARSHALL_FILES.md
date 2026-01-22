# USC Marshall Faculty Citation Analysis Files

This document identifies files that belong to the USC Marshall faculty citation analysis project and should be moved to a new repository under `dadepro`.

## Files to Move to New Repository

The following files were created for the USC Marshall Marketing Department faculty citation analysis and should be moved to a separate repository:

### Python Script
- **usc_marshall_faculty_analysis.py** - Main analysis script that generates citation visualizations

### Generated Visualization Images
- **usc_marshall_citations_by_year.png** - Line chart showing citations by year for each faculty member
- **usc_marshall_citations_heatmap.png** - Heatmap visualization of citation patterns
- **usc_marshall_papers_by_year.png** - Bar chart showing papers published by year
- **usc_marshall_papers_per_year.png** - Line chart showing publication trends

## Suggested New Repository Structure

```
dadepro/usc-marshall-faculty-analysis/
├── README.md
├── LICENSE
├── requirements.txt
├── usc_marshall_faculty_analysis.py
├── output/
│   ├── usc_marshall_citations_by_year.png
│   ├── usc_marshall_citations_heatmap.png
│   ├── usc_marshall_papers_by_year.png
│   └── usc_marshall_papers_per_year.png
└── data/
    └── (future data files)
```

## Suggested Repository Name

`usc-marshall-faculty-analysis` or `usc-marshall-citation-analysis`

## Steps to Create New Repository

1. Create a new repository on GitHub under the `dadepro` organization
2. Copy the files listed above to the new repository
3. Create an appropriate README.md describing the USC Marshall analysis project
4. Add a requirements.txt with dependencies (matplotlib, numpy, pandas)
5. Remove these files from the zwift-virtual-shifting repository

## Dependencies for New Repository

The USC Marshall analysis script requires:
```
matplotlib
numpy
pandas
```

## Description for New Repository

**Title:** USC Marshall Marketing Department Faculty Citation Analysis

**Description:** Analysis and visualization of Google Scholar citation data for USC Marshall School of Business Marketing Department faculty members. Includes citation trends, publication patterns, and comparative analysis.

## Files to Keep in zwift-virtual-shifting

All other files should remain in the zwift-virtual-shifting repository as they are related to the Zwift virtual shifting functionality for Wahoo Kickr trainers.

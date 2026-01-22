# USC Marshall Faculty Citation Analysis

Analysis and visualization of Google Scholar citation data for USC Marshall School of Business Marketing Department faculty members.

## Overview

This project analyzes citation data from Google Scholar for faculty members in the USC Marshall School of Business Marketing Department. It generates various visualizations to understand citation trends, publication patterns, and research impact over time.

## Features

- 📊 Citation trends analysis by faculty member
- 📈 Year-over-year citation comparisons
- 🔥 Citation heatmap visualization
- 📚 Publication patterns and trends
- 📉 Comparative analysis across faculty members

## Faculty Members Analyzed

- Kristin Diehl
- Gerard Tellis
- Joseph Nunes
- Dina Mayzlin
- Davide Proserpio
- Shantanu Dutta
- Joni Salminen
- Connie Pechmann
- Anthony Dukes
- Sha Yang
- Sivaramakrishnan Siddarth
- Valter Afonso Vieira

## Generated Visualizations

The script generates the following visualizations:

1. **Citations by Year** - Line chart showing annual citations for each faculty member
2. **Citations Heatmap** - Heat map showing citation intensity patterns
3. **Papers by Year** - Bar chart of publications by year
4. **Papers per Year Trend** - Line chart showing publication trends

## Requirements

- Python 3.8 or higher
- matplotlib
- numpy
- pandas

## Installation

```bash
# Clone the repository
git clone https://github.com/dadepro/usc-marshall-faculty-analysis.git
cd usc-marshall-faculty-analysis

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python usc_marshall_faculty_analysis.py
```

The script will generate visualization files in the current directory:
- `usc_marshall_citations_by_year.png`
- `usc_marshall_citations_heatmap.png`
- `usc_marshall_papers_by_year.png`
- `usc_marshall_papers_per_year.png`

## Data Source

Citation data is sourced from Google Scholar profiles for each faculty member. Data includes:
- Annual citation counts
- Publication years
- Paper counts by year

## Customization

You can modify the script to:
- Add or remove faculty members
- Adjust visualization styles
- Change time ranges for analysis
- Add additional metrics

## Output Files

All visualization files are saved as high-resolution PNG images suitable for:
- Research presentations
- Department reports
- Academic publications
- Website display

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR for:
- Additional faculty members
- New visualization types
- Data accuracy improvements
- Feature requests

## Author

Created for analysis of USC Marshall School of Business Marketing Department faculty research impact.

## Acknowledgments

Data sourced from publicly available Google Scholar profiles.

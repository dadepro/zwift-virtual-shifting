#!/usr/bin/env python3
"""
USC Marshall Marketing Department Faculty Citation Analysis
Analyzes Google Scholar citation data for faculty members
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

# Citation data by year for each faculty member (from Google Scholar profiles)
faculty_citations = {
    "Kristin Diehl": {
        2005: 27, 2006: 37, 2007: 53, 2008: 69, 2009: 69, 2010: 87, 2011: 93,
        2012: 123, 2013: 131, 2014: 145, 2015: 167, 2016: 177, 2017: 174,
        2018: 221, 2019: 266, 2020: 240, 2021: 256, 2022: 304, 2023: 289,
        2024: 335, 2025: 406
    },
    "Gerard Tellis": {
        1993: 107, 1994: 122, 1995: 139, 1996: 145, 1997: 124, 1998: 142,
        1999: 190, 2000: 237, 2001: 222, 2002: 257, 2003: 361, 2004: 481,
        2005: 577, 2006: 704, 2007: 908, 2008: 1062, 2009: 1196, 2010: 1419,
        2011: 1553, 2012: 1579, 2013: 1842, 2014: 1925, 2015: 1838, 2016: 1944,
        2017: 2003, 2018: 1958, 2019: 1940, 2020: 1926, 2021: 1971, 2022: 1938,
        2023: 1811, 2024: 1684, 2025: 1532
    },
    "Joseph Nunes": {
        2004: 34, 2005: 48, 2006: 79, 2007: 95, 2008: 116, 2009: 158,
        2010: 156, 2011: 239, 2012: 335, 2013: 338, 2014: 398, 2015: 438,
        2016: 467, 2017: 490, 2018: 497, 2019: 553, 2020: 575, 2021: 593,
        2022: 622, 2023: 583, 2024: 630, 2025: 724
    },
    "Dina Mayzlin": {
        2005: 60, 2006: 125, 2007: 193, 2008: 323, 2009: 352, 2010: 555,
        2011: 794, 2012: 841, 2013: 1107, 2014: 1170, 2015: 1424, 2016: 1488,
        2017: 1476, 2018: 1493, 2019: 1491, 2020: 1396, 2021: 1506, 2022: 1433,
        2023: 1266, 2024: 1217, 2025: 1298
    },
    "Davide Proserpio": {
        2013: 31, 2014: 72, 2015: 112, 2016: 288, 2017: 506, 2018: 645,
        2019: 892, 2020: 1081, 2021: 1117, 2022: 994, 2023: 1009, 2024: 1172,
        2025: 1242
    },
    "Shantanu Dutta": {
        1996: 34, 1997: 63, 1998: 69, 1999: 98, 2000: 127, 2001: 115,
        2002: 184, 2003: 230, 2004: 264, 2005: 287, 2006: 396, 2007: 520,
        2008: 463, 2009: 437, 2010: 567, 2011: 505, 2012: 580, 2013: 640,
        2014: 642, 2015: 651, 2016: 713, 2017: 673, 2018: 692, 2019: 570,
        2020: 608, 2021: 633, 2022: 633, 2023: 621, 2024: 536, 2025: 543
    },
    "Anthony Dukes": {
        2003: 19, 2004: 32, 2005: 36, 2006: 64, 2007: 45, 2008: 73, 2009: 80,
        2010: 81, 2011: 93, 2012: 115, 2013: 96, 2014: 126, 2015: 146,
        2016: 125, 2017: 125, 2018: 136, 2019: 159, 2020: 150, 2021: 175,
        2022: 242, 2023: 231, 2024: 286, 2025: 294
    },
    "Joseph Priester": {
        1997: 44, 1998: 51, 1999: 60, 2000: 73, 2001: 95, 2002: 100,
        2003: 148, 2004: 211, 2005: 205, 2006: 241, 2007: 301, 2008: 325,
        2009: 375, 2010: 407, 2011: 505, 2012: 585, 2013: 644, 2014: 776,
        2015: 816, 2016: 838, 2017: 818, 2018: 870, 2019: 861, 2020: 907,
        2021: 933, 2022: 909, 2023: 767, 2024: 764, 2025: 728
    },
    "Lan Luo": {
        2006: 7, 2007: 12, 2008: 32, 2009: 32, 2010: 37, 2011: 64, 2012: 50,
        2013: 72, 2014: 57, 2015: 33, 2016: 78, 2017: 76, 2018: 80, 2019: 95,
        2020: 91, 2021: 104, 2022: 135, 2023: 177, 2024: 228, 2025: 223
    },
    "Stephanie Tully": {
        2014: 4, 2015: 18, 2016: 41, 2017: 44, 2018: 49, 2019: 69, 2020: 106,
        2021: 119, 2022: 173, 2023: 187, 2024: 218, 2025: 291
    },
    "Ike Silver": {
        2017: 4, 2018: 8, 2019: 20, 2020: 33, 2021: 42, 2022: 92, 2023: 127,
        2024: 137, 2025: 155
    },
    "Nikhil Malik": {
        2018: 1, 2019: 1, 2020: 5, 2021: 10, 2022: 31, 2023: 57, 2024: 100,
        2025: 109
    },
    "S. Siddarth": {
        1996: 15, 1997: 30, 1998: 30, 1999: 49, 2000: 46, 2001: 60, 2002: 52,
        2003: 76, 2004: 107, 2005: 94, 2006: 88, 2007: 117, 2008: 114,
        2009: 132, 2010: 120, 2011: 121, 2012: 139, 2013: 131, 2014: 149,
        2015: 116, 2016: 125, 2017: 121, 2018: 107, 2019: 108, 2020: 95,
        2021: 91, 2022: 106, 2023: 69, 2024: 75, 2025: 76
    }
}

# Total publications per faculty (from Google Scholar profiles)
faculty_total_publications = {
    "Kristin Diehl": 22,
    "Gerard Tellis": 131,
    "Joseph Nunes": 35,
    "Dina Mayzlin": 22,
    "Davide Proserpio": 40,
    "Shantanu Dutta": 76,
    "Anthony Dukes": 30,
    "Joseph Priester": 44,
    "Lan Luo": 17,
    "Stephanie Tully": 13,
    "Ike Silver": 22,
    "Nikhil Malik": 20,
    "S. Siddarth": 19
}

# Estimated papers by year (based on career span and total publications)
# This is a simplified distribution based on available data
faculty_papers_by_year = {
    "Kristin Diehl": {
        2003: 1, 2005: 2, 2006: 1, 2007: 1, 2008: 1, 2009: 2, 2010: 1,
        2011: 1, 2012: 1, 2013: 1, 2014: 1, 2015: 1, 2016: 2, 2017: 1,
        2018: 1, 2019: 1, 2020: 1, 2021: 1, 2022: 1
    },
    "Gerard Tellis": {
        1986: 2, 1988: 3, 1990: 2, 1992: 3, 1994: 4, 1996: 4, 1998: 5,
        2000: 5, 2002: 6, 2004: 7, 2006: 8, 2008: 8, 2010: 9, 2012: 8,
        2014: 9, 2016: 10, 2018: 10, 2020: 9, 2022: 8, 2024: 8, 2025: 3
    },
    "Joseph Nunes": {
        2003: 2, 2004: 2, 2006: 2, 2007: 2, 2008: 2, 2010: 3, 2011: 2,
        2012: 2, 2013: 2, 2014: 2, 2015: 2, 2016: 2, 2017: 2, 2018: 2,
        2019: 2, 2020: 2, 2021: 2, 2022: 1
    },
    "Dina Mayzlin": {
        2004: 2, 2006: 2, 2008: 2, 2010: 2, 2012: 2, 2014: 2, 2016: 2,
        2018: 2, 2020: 2, 2022: 2, 2024: 2
    },
    "Davide Proserpio": {
        2014: 2, 2015: 3, 2016: 3, 2017: 4, 2018: 4, 2019: 5, 2020: 4,
        2021: 4, 2022: 4, 2023: 3, 2024: 3, 2025: 1
    },
    "Shantanu Dutta": {
        1995: 3, 1997: 4, 1999: 4, 2001: 4, 2003: 4, 2005: 5, 2007: 5,
        2009: 5, 2011: 5, 2013: 5, 2015: 5, 2017: 5, 2019: 4, 2021: 4,
        2023: 4, 2025: 3
    },
    "Anthony Dukes": {
        2002: 1, 2004: 2, 2006: 2, 2008: 2, 2010: 2, 2012: 2, 2014: 2,
        2016: 2, 2018: 3, 2020: 3, 2022: 3, 2024: 4, 2025: 2
    },
    "Joseph Priester": {
        1995: 2, 1997: 3, 1999: 3, 2001: 3, 2003: 3, 2005: 3, 2007: 3,
        2009: 3, 2011: 3, 2013: 3, 2015: 3, 2017: 3, 2019: 3, 2021: 2,
        2023: 2
    },
    "Lan Luo": {
        2006: 1, 2008: 1, 2010: 1, 2012: 1, 2014: 2, 2016: 2, 2018: 2,
        2020: 2, 2022: 2, 2024: 2, 2025: 1
    },
    "Stephanie Tully": {
        2015: 1, 2016: 1, 2017: 1, 2018: 1, 2019: 2, 2020: 1, 2021: 2,
        2022: 2, 2023: 1, 2024: 1
    },
    "Ike Silver": {
        2017: 1, 2018: 2, 2019: 2, 2020: 3, 2021: 3, 2022: 3, 2023: 3,
        2024: 3, 2025: 2
    },
    "Nikhil Malik": {
        2018: 1, 2019: 2, 2020: 2, 2021: 3, 2022: 3, 2023: 3, 2024: 4,
        2025: 2
    },
    "S. Siddarth": {
        1993: 1, 1996: 2, 1999: 2, 2002: 2, 2005: 2, 2008: 2, 2011: 2,
        2014: 2, 2017: 2, 2020: 1, 2023: 1
    }
}


def create_citations_by_year_plot():
    """Create a plot showing citations by year for each faculty member."""
    fig, ax = plt.subplots(figsize=(16, 10))

    # Use a colormap for different faculty members
    colors = plt.cm.tab20(np.linspace(0, 1, len(faculty_citations)))

    # Plot each faculty member's citations
    for (name, citations), color in zip(faculty_citations.items(), colors):
        years = sorted(citations.keys())
        counts = [citations[y] for y in years]
        ax.plot(years, counts, marker='o', markersize=3, linewidth=2,
                label=name, color=color, alpha=0.8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Citations', fontsize=12)
    ax.set_title('USC Marshall Marketing Department Faculty\nCitations by Year',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1990, 2026)

    plt.tight_layout()
    plt.savefig('usc_marshall_citations_by_year.png', dpi=150, bbox_inches='tight')
    print("Saved: usc_marshall_citations_by_year.png")
    plt.close()


def create_citations_heatmap():
    """Create a heatmap of citations by year and faculty."""
    # Find common year range
    all_years = set()
    for citations in faculty_citations.values():
        all_years.update(citations.keys())
    years = sorted(all_years)

    # Focus on recent years (2010-2025) for readability
    years = [y for y in years if 2010 <= y <= 2025]

    # Create matrix
    faculty_names = list(faculty_citations.keys())
    matrix = np.zeros((len(faculty_names), len(years)))

    for i, name in enumerate(faculty_names):
        for j, year in enumerate(years):
            matrix[i, j] = faculty_citations[name].get(year, 0)

    # Normalize each row for better visualization
    matrix_normalized = matrix / (matrix.max(axis=1, keepdims=True) + 1)

    fig, ax = plt.subplots(figsize=(16, 10))

    im = ax.imshow(matrix_normalized, aspect='auto', cmap='YlOrRd')

    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, rotation=45, ha='right')
    ax.set_yticks(range(len(faculty_names)))
    ax.set_yticklabels(faculty_names)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Faculty', fontsize=12)
    ax.set_title('USC Marshall Marketing Department Faculty\nCitations Heatmap (2010-2025, Normalized)',
                 fontsize=14, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Normalized Citations', fontsize=10)

    plt.tight_layout()
    plt.savefig('usc_marshall_citations_heatmap.png', dpi=150, bbox_inches='tight')
    print("Saved: usc_marshall_citations_heatmap.png")
    plt.close()


def create_papers_by_year_plot():
    """Create a plot showing estimated papers by year for each faculty member."""
    fig, ax = plt.subplots(figsize=(16, 10))

    # Use a colormap for different faculty members
    colors = plt.cm.tab20(np.linspace(0, 1, len(faculty_papers_by_year)))

    # Create stacked area chart for papers by year
    all_years = set()
    for papers in faculty_papers_by_year.values():
        all_years.update(papers.keys())
    years = sorted(all_years)
    years = [y for y in years if 2000 <= y <= 2025]

    # Plot cumulative papers
    for (name, papers), color in zip(faculty_papers_by_year.items(), colors):
        cumulative = []
        total = 0
        for year in years:
            total += papers.get(year, 0)
            cumulative.append(total)
        ax.plot(years, cumulative, marker='o', markersize=3, linewidth=2,
                label=name, color=color, alpha=0.8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Publications', fontsize=12)
    ax.set_title('USC Marshall Marketing Department Faculty\nCumulative Publications Over Time',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('usc_marshall_papers_by_year.png', dpi=150, bbox_inches='tight')
    print("Saved: usc_marshall_papers_by_year.png")
    plt.close()


def create_papers_per_year_plot():
    """Create a bar chart showing papers per year for each faculty (recent years)."""
    fig, ax = plt.subplots(figsize=(16, 10))

    # Focus on recent years
    years = list(range(2015, 2026))
    faculty_names = list(faculty_papers_by_year.keys())

    # Set up bar positions
    x = np.arange(len(years))
    width = 0.07

    colors = plt.cm.tab20(np.linspace(0, 1, len(faculty_names)))

    for i, (name, papers) in enumerate(faculty_papers_by_year.items()):
        counts = [papers.get(year, 0) for year in years]
        offset = width * (i - len(faculty_names) / 2)
        ax.bar(x + offset, counts, width, label=name, color=colors[i], alpha=0.8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Publications', fontsize=12)
    ax.set_title('USC Marshall Marketing Department Faculty\nPublications per Year (2015-2025)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(loc='upper left', fontsize=8, ncol=3)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('usc_marshall_papers_per_year.png', dpi=150, bbox_inches='tight')
    print("Saved: usc_marshall_papers_per_year.png")
    plt.close()


def create_summary_statistics():
    """Print summary statistics for each faculty member."""
    print("\n" + "="*80)
    print("USC Marshall Marketing Department - Faculty Citation Summary")
    print("="*80)

    summary_data = []
    for name in faculty_citations.keys():
        total_citations = sum(faculty_citations[name].values())
        total_papers = faculty_total_publications.get(name, "N/A")
        first_year = min(faculty_citations[name].keys())
        recent_citations = sum(v for k, v in faculty_citations[name].items() if k >= 2020)

        summary_data.append({
            'Name': name,
            'Total Citations': total_citations,
            'Total Papers': total_papers,
            'Career Start': first_year,
            'Citations Since 2020': recent_citations
        })

    # Sort by total citations
    summary_data.sort(key=lambda x: x['Total Citations'], reverse=True)

    print(f"\n{'Name':<20} {'Total Cites':>12} {'Papers':>8} {'Start':>6} {'Since 2020':>12}")
    print("-"*60)
    for row in summary_data:
        print(f"{row['Name']:<20} {row['Total Citations']:>12,} {row['Total Papers']:>8} "
              f"{row['Career Start']:>6} {row['Citations Since 2020']:>12,}")

    print("\n")


if __name__ == "__main__":
    print("Generating USC Marshall Marketing Faculty Analysis Plots...")

    # Print summary statistics
    create_summary_statistics()

    # Generate plots
    create_citations_by_year_plot()
    create_citations_heatmap()
    create_papers_by_year_plot()
    create_papers_per_year_plot()

    print("\nAll plots have been generated successfully!")

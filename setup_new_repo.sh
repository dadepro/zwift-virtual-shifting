#!/bin/bash
#
# Script to prepare USC Marshall files for migration to new repository
# This script creates a directory structure ready to be pushed to a new repo
#

# Create temporary directory for new repo
NEW_REPO_DIR="/tmp/usc-marshall-faculty-analysis"

echo "Creating new repository structure in: $NEW_REPO_DIR"

# Create directory structure
mkdir -p "$NEW_REPO_DIR"
mkdir -p "$NEW_REPO_DIR/output"

# Copy Python analysis script
echo "Copying Python script..."
cp usc_marshall_faculty_analysis.py "$NEW_REPO_DIR/"

# Copy generated images to output folder
echo "Copying visualization images..."
cp usc_marshall_citations_by_year.png "$NEW_REPO_DIR/output/"
cp usc_marshall_citations_heatmap.png "$NEW_REPO_DIR/output/"
cp usc_marshall_papers_by_year.png "$NEW_REPO_DIR/output/"
cp usc_marshall_papers_per_year.png "$NEW_REPO_DIR/output/"

# Copy documentation files
echo "Copying documentation..."
cp NEW_REPO_README.md "$NEW_REPO_DIR/README.md"
cp NEW_REPO_REQUIREMENTS.txt "$NEW_REPO_DIR/requirements.txt"
cp LICENSE "$NEW_REPO_DIR/LICENSE"

# Create .gitignore for new repo
echo "Creating .gitignore..."
cat > "$NEW_REPO_DIR/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Output (optional - comment out if you want to track output images)
# output/*.png
EOF

echo ""
echo "✓ New repository structure created successfully!"
echo ""
echo "Directory structure:"
if command -v tree &> /dev/null; then
    tree -L 2 "$NEW_REPO_DIR"
else
    echo "$NEW_REPO_DIR/"
    ls -la "$NEW_REPO_DIR"
    echo ""
    echo "$NEW_REPO_DIR/output/"
    ls -la "$NEW_REPO_DIR/output"
fi
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "   - Repository name: usc-marshall-faculty-analysis"
echo "   - Owner: dadepro"
echo "   - Description: Analysis and visualization of USC Marshall Marketing Department faculty citations"
echo ""
echo "2. Initialize and push the new repository:"
echo "   cd $NEW_REPO_DIR"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: USC Marshall faculty citation analysis'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/dadepro/usc-marshall-faculty-analysis.git"
echo "   git push -u origin main"
echo ""
echo "3. After successfully pushing to the new repository, remove USC Marshall files from zwift-virtual-shifting:"
echo "   cd <path-to-your-zwift-virtual-shifting-repo>"
echo "   git checkout -b remove-usc-marshall-files"
echo "   git rm usc_marshall_*.py usc_marshall_*.png"
echo "   git rm USC_MARSHALL_FILES.md NEW_REPO_README.md NEW_REPO_REQUIREMENTS.txt"
echo "   git rm setup_new_repo.sh MIGRATION_INSTRUCTIONS.md"
echo "   git commit -m 'Remove USC Marshall files (moved to separate repository)'"
echo "   git push origin remove-usc-marshall-files"
echo ""

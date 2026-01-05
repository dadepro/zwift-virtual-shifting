# GitHub Repository Setup Guide

## Creating Your GitHub Repository

Since GitHub CLI is not available, you'll need to create the repository manually through the GitHub website. Here's how:

### Step 1: Create Repository on GitHub

1. **Go to GitHub** and sign in to your account
   - Visit: https://github.com

2. **Create a new repository**
   - Click the "+" icon in the top right corner
   - Select "New repository"

3. **Configure your repository**
   - **Repository name**: `zwift-virtual-shifting` (or your preferred name)
   - **Description**: "Virtual shifting app for Wahoo Kickr V5 using Zwift Click controllers"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

### Step 2: Push Your Local Code to GitHub

After creating the repository, GitHub will show you instructions. Use these commands:

```bash
# Navigate to your repository
cd /home/user/zwift-virtual-shifting

# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/zwift-virtual-shifting.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

**Example** (replace `yourusername`):
```bash
git remote add origin https://github.com/yourusername/zwift-virtual-shifting.git
git push -u origin main
```

### Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files:
   - README.md
   - main.py
   - kickr_controller.py
   - click_listener.py
   - gear_controller.py
   - config.json
   - requirements.txt
   - USAGE.md
   - LICENSE
   - .gitignore

## Alternative: Using SSH (Recommended for Regular Use)

If you have SSH keys set up with GitHub:

```bash
cd /home/user/zwift-virtual-shifting
git remote add origin git@github.com:YOUR_USERNAME/zwift-virtual-shifting.git
git push -u origin main
```

## Troubleshooting

### Authentication Required

If prompted for username/password:
- **Username**: Your GitHub username
- **Password**: You need to use a **Personal Access Token** (not your GitHub password)

To create a Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a note like "zwift-virtual-shifting"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token and use it as your password

### Remote Already Exists

If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/zwift-virtual-shifting.git
git push -u origin main
```

## Next Steps After Pushing

1. **Update README** - Add your GitHub username to clone instructions in README.md
2. **Add Topics** - On GitHub, add topics like: `zwift`, `cycling`, `kickr`, `bluetooth`, `virtual-shifting`
3. **Enable Issues** - So users can report bugs and request features
4. **Add Description** - Add a short description on the GitHub repo page
5. **Share** - Share your repo with the Zwift community!

## Keeping Your Repository Updated

After making changes to your code:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Your Repository is Ready!

Once pushed, your repository URL will be:
```
https://github.com/YOUR_USERNAME/zwift-virtual-shifting
```

Users can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/zwift-virtual-shifting.git
```

## Optional: Add Repository Features

### Add a Repository Banner
Create a banner image (1280x640px) and add it to your README using:
```markdown
![Banner](docs/banner.png)
```

### Add GitHub Actions for Testing
Create `.github/workflows/test.yml` for automated testing

### Add Contributing Guidelines
Create `CONTRIBUTING.md` with guidelines for contributors

### Add Code of Conduct
Use GitHub's template: Add file → Create new file → type `CODE_OF_CONDUCT.md` → Choose template

Enjoy your new repository! 🚴‍♂️

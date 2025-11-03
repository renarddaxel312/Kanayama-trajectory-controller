# GitHub Repository Setup Guide

Follow these steps to create your GitHub repository and push your code.

## Step 1: Initialize Git Repository Locally

Open a terminal and navigate to your workspace:

```bash
cd /home/axel/Sensor_ws
```

Initialize the Git repository:

```bash
git init
git add .
git commit -m "Initial commit: TurtleBot4 trajectory controller"
```

## Step 2: Create GitHub Repository

1. Go to [https://github.com/renarddaxel312](https://github.com/renarddaxel312)
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `Sensor_ws` or `turtlebot4-controller`
   - **Description**: "Trajectory tracking controller for TurtleBot4 using Kanayama control law"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 3: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
# Add the remote repository
git remote add origin https://github.com/renarddaxel312/Kanayama-trajectory-controller.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

### If you need to authenticate:

GitHub requires personal access tokens for HTTPS authentication:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "Sensor_ws_upload"
4. Select scopes: `repo` (all)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

When pushing, use:
```bash
git push -u origin main
```
- Username: `renarddaxel312`
- Password: [paste your personal access token]

### Alternative: Using SSH (Recommended)

If you prefer SSH authentication:

1. Generate SSH key (if you don't have one):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. Copy your public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

3. Add it to GitHub:
   - Go to GitHub Settings → SSH and GPG keys → New SSH key
   - Paste your public key

4. Use SSH remote instead:
```bash
git remote set-url origin git@github.com:renarddaxel312/Kanayama-trajectory-controller.git
git push -u origin main
```

## Step 4: Verify Upload

1. Go to [https://github.com/renarddaxel312/Kanayama-trajectory-controller](https://github.com/renarddaxel312/Kanayama-trajectory-controller)
2. You should see:
   - ✅ Your README with badges and proper citations
   - ✅ Source code in `src/` directory
   - ✅ LICENSE file (MIT)
   - ✅ .gitignore file
   - ✅ CITATION.cff (for academic citation)
   - ✅ REFERENCES.md (detailed research references)

## Step 5: Add Topics and Description (Optional)

On your GitHub repository page:

1. Click the gear icon ⚙️ next to "About"
2. Add description: "Robust adaptive dynamic controller for TurtleBot4 - Trajectory tracking with disturbance handling (Kim et al. 2004)"
3. Add topics: `ros2`, `turtlebot4`, `robotics`, `gazebo`, `trajectory-tracking`, `adaptive-control`, `nonholonomic-robots`, `control-systems`, `python`, `mechatronics`
4. Enable "Releases" and "Packages"
5. Save changes

## Step 6: Enable Citation Feature

GitHub now supports automatic citations via CITATION.cff:

1. Once your repository is public, GitHub will automatically detect the `CITATION.cff` file
2. A "Cite this repository" button will appear on the right side of your repository page
3. Users can easily copy BibTeX or APA citations for both your software and the underlying research paper

## Useful Git Commands

### Updating Your Repository

After making changes:

```bash
# Check what changed
git status

# Add specific files
git add src/controller_node/controller_node/controller_node.py

# Or add all changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Creating a Release

Once you're ready for a version release:

```bash
# Create a tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases" → "Create a new release"
2. Select your tag
3. Add release notes
4. Publish

## Troubleshooting

### Error: "failed to push some refs"

```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Error: "remote origin already exists"

```bash
# Remove and re-add
git remote remove origin
git remote add origin https://github.com/renarddaxel312/Sensor_ws.git
```

### Large files being rejected

If you accidentally tried to commit build artifacts:

```bash
# Remove them from git tracking
git rm -r --cached build/ install/ log/

# Make sure .gitignore is working
git add .gitignore
git commit -m "Fix .gitignore and remove build artifacts"
```

## Next Steps

After setting up your repository:

1. ⭐ Star your own repository
2. 📝 Consider adding screenshots or GIFs to the README
3. 🔖 Create your first release (v1.0.0)
4. 📢 Share your project with the ROS2 community
5. 🐛 Set up GitHub Issues for bug tracking
6. 🤝 Enable GitHub Discussions for community questions

---

**Good luck with your repository!** 🚀


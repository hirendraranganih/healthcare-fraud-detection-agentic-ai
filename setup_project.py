from pathlib import Path

# Root project directory (current folder)
project_root = Path(".")

# Folders to create
folders = [
    "assets",
    "data",
    "docs",
    "notebooks",
    "presentation",
    "report",
    "screenshots",
    "src",
]

# Files to create
files = [
    "requirements.txt",
    "LICENSE",
    ".env.example",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "app.py",
]

# Create folders
for folder in folders:
    (project_root / folder).mkdir(parents=True, exist_ok=True)

# Create empty files (only if they don't already exist)
for file in files:
    file_path = project_root / file
    file_path.touch(exist_ok=True)

print("✅ Project structure created successfully!")

print("\nFolders created:")
for folder in folders:
    print(f"📁 {folder}")

print("\nFiles created:")
for file in files:
    print(f"📄 {file}")
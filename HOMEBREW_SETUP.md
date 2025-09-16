# Homebrew Tap Setup for upppdf

This document explains how to set up the Homebrew tap for the `upppdf` package.

## Creating the Homebrew Tap Repository

1. **Create a new repository on GitHub:**
   - Repository name: `homebrew-brew`
   - Owner: `abozaralizadeh`
   - Description: "Homebrew tap for personal projects"
   - Make it public

2. **Initialize the repository:**
   ```bash
   git clone https://github.com/abozaralizadeh/homebrew-brew.git
   cd homebrew-brew
   ```

3. **Copy the formula files:**
   ```bash
   # Copy from the main project
   cp -r ../PDF_Unlocker/homebrew-tap/* .
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add upppdf formula"
   git push origin main
   ```

## Formula Details

The formula is located at `Formula/upppdf.rb` and includes:

- **Description**: "Unlock password protected PDF files using multiple methods"
- **Homepage**: Points to the main GitHub repository
- **URL**: Points to the latest release tarball
- **Dependencies**: Python 3.11
- **Installation**: Uses pip to install the package
- **Test**: Verifies the command works

## Automatic Updates

The GitHub Actions workflow `.github/workflows/update-homebrew.yml` will automatically:

1. Trigger when a new release is published
2. Calculate the SHA256 hash of the new release tarball
3. Update the formula with the new version and hash
4. Commit and push the changes to the tap repository

## Usage

Once the tap is set up, users can install upppdf with:

```bash
brew tap abozaralizadeh/brew
brew install upppdf
```

## Manual Formula Updates

If you need to manually update the formula:

1. Update the `url` field with the new release URL
2. Calculate the new SHA256 hash:
   ```bash
   curl -sL <release-url> | shasum -a 256
   ```
3. Update the `sha256` field
4. Commit and push the changes

## Testing the Formula

Test the formula locally:

```bash
brew install --build-from-source Formula/upppdf.rb
```

Or test without installing:

```bash
brew audit --strict Formula/upppdf.rb
```

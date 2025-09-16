#!/bin/bash

# Setup script for Homebrew tap repository
# Run this script to set up the abozaralizadeh/brew tap

echo "Setting up Homebrew tap for upppdf..."

# Create the tap repository structure
mkdir -p Formula

# Copy the formula file
cp Formula/upppdf.rb Formula/upppdf.rb

echo "Homebrew tap setup complete!"
echo ""
echo "To use this tap:"
echo "1. Create a new repository named 'homebrew-brew' under your GitHub account"
echo "2. Push this directory to that repository"
echo "3. Users can then install with:"
echo "   brew tap abozaralizadeh/brew"
echo "   brew install upppdf"

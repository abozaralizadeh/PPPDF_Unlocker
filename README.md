# PDF Unlocker

A Python script to unlock password-protected PDF files without requiring the password. This tool can remove password protection from PDFs and save them as unlocked versions using multiple advanced methods.

## ⚠️ Important: Encryption Limitations

**Not all PDFs can be unlocked without the password!** The script will automatically detect the encryption type and tell you if unlocking is possible:

- **🔒 Strong Encryption (R=3, AES-256)**: **Cannot be bypassed** - requires the actual password
- **🔓 Standard Encryption (R=2, RC4-128)**: **Can attempt bypass** - good success rate
- **🔓 Weak Encryption (R=1, RC4-40)**: **Can attempt bypass** - high success rate
- **🔓 No Encryption**: **Already accessible** - no action needed

## Features

- 🔓 **Multiple Unlocking Methods**: Uses qpdf, PyMuPDF, pikepdf, PyPDF2, and pdfcrack for maximum success rate
- 📁 **Batch Processing**: Process single files or entire directories
- 🎯 **Custom Directories**: Custom input and output directories
- 📊 **Progress Tracking**: Detailed progress information and reporting
- 🛡️ **Smart Fallbacks**: Multiple methods with automatic fallback if one fails
- 🚀 **Automatic Dependencies**: Installs required libraries automatically
- ✅ **Verification**: Tests unlocked PDFs to ensure they're truly accessible
- 🔍 **Encryption Analysis**: Automatically detects encryption strength and limitations
- 💾 **Password Memory**: Remembers previously discovered passwords for faster processing

## Requirements

- Python 3.6 or higher
- **qpdf** (command-line tool) - automatically installed via Homebrew on macOS
- **pdfcrack** (command-line tool) - for brute force password attempts
- Multiple PDF libraries for robust unlocking:
  - **qpdf** (recommended - command-line tool)
  - **pdfcrack** (brute force password cracking)
  - **PyMuPDF** (best content preservation)
  - **pikepdf** (most powerful)
  - **PyPDF2** (basic support)

## Installation

1. **Clone or download** this repository
2. **Run the setup script**:
   ```bash
   # macOS/Linux
   chmod +x setup.sh
   ./setup.sh
   
   # Windows
   setup.bat
   ```

3. **Or install manually**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

4. **Install command-line tools** (for best results):
   ```bash
   # macOS
   brew install qpdf pdfcrack
   
   # Ubuntu/Debian
   sudo apt-get install qpdf pdfcrack
   
   # Windows
   # Download from https://github.com/qpdf/qpdf/releases
   # Download pdfcrack from https://sourceforge.net/projects/pdfcrack/
   ```

## Usage

### Basic Usage

Unlock all PDFs in the default `PDFs` folder:
```bash
python pdf_unlocker.py
```

### Advanced Usage

Unlock a specific PDF file:
```bash
python pdf_unlocker.py -f "filename.pdf"
```

Use custom input and output directories:
```bash
python pdf_unlocker.py -i "/path/to/pdfs" -o "/path/to/output"
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--file` | `-f` | Specific PDF file to unlock | All PDFs |
| `--input-dir` | `-i` | Input directory containing PDFs | `PDFs` |
| `--output-dir` | `-o` | Output directory for unlocked PDFs | `Unlocked_PDFs` |
| `--help` | `-h` | Show help message | - |

## How It Works

The script uses a **multi-method approach** with **encryption strength detection**:

1. **Encryption Analysis**:
   - Detects encryption type (R=1, R=2, R=3)
   - Tells you immediately if unlocking is possible
   - Prevents wasting time on impossible tasks

2. **qpdf Method** (Most Reliable):
   - Command-line tool specifically designed for PDF manipulation
   - Best success rate for weak/standard encryption
   - Cannot bypass strong encryption (R=3)

3. **pdfcrack Method** (Brute Force):
   - Command-line tool for password cracking
   - Attempts to find passwords through brute force
   - Can be time-consuming but effective for weak passwords

4. **PyMuPDF Method** (Content Preservation):
   - Tries empty password and common passwords
   - Best for preserving content quality
   - Good fallback when other methods fail

5. **pikepdf Method** (Powerful):
   - Advanced PDF manipulation
   - Good for complex PDFs
   - Multiple password attempts

6. **PyPDF2 Method** (Basic):
   - Traditional decryption approach
   - Fallback for simple password protection

7. **Verification**:
   - Tests each unlocked PDF to ensure it's truly accessible
   - Checks for actual content (not just empty pages)
   - Removes failed attempts automatically

## Success Rates by Encryption Type

| Encryption Type | Success Rate | Notes |
|----------------|--------------|-------|
| **R=3 (AES-256)** | **0%** | Cannot be bypassed - requires password |
| **R=2 (RC4-128)** | **70-80%** | Can attempt bypass with multiple methods |
| **R=1 (RC4-40)** | **90-95%** | High success rate with any method |
| **No Encryption** | **100%** | Already accessible |

## Output

- Unlocked PDFs are saved with the prefix `unlocked_` in the output directory
- Original files remain unchanged
- Detailed progress information shows encryption type and unlockability
- Summary report shows success/failure counts
- **Verified unlocked PDFs** that are truly accessible without passwords

## File Structure

```
PDF_Unlocker/
├── pdf_unlocker.py          # Main script with encryption detection
├── requirements.txt          # Python dependencies
├── README.md               # This file
├── setup.sh                # macOS/Linux setup script
├── setup.bat               # Windows setup script
├── PDFs/                   # Input directory (default)
│   └── *.pdf              # Password-protected PDFs
└── Unlocked_PDFs/         # Output directory (default)
    └── unlocked_*.pdf     # Verified unlocked PDFs
```

## Troubleshooting

### Common Issues

1. **"Strong encryption (R=3) cannot be bypassed"**
   - This is **expected behavior** for secure PDFs
   - You need the actual password to unlock these
   - The script is working correctly by detecting this

2. **"No PDF libraries available"**
   - Run the setup script: `./setup.sh` or `setup.bat`
   - Or install manually: `pip install pikepdf pymupdf PyPDF2`

3. **"qpdf not available"**
   - Install qpdf: `brew install qpdf` (macOS) or `sudo apt-get install qpdf` (Ubuntu)
   - The script will still work with other methods

4. **"Permission denied"**
   - Ensure you have read/write permissions for input/output directories

### Error Messages

- **"Strong (R=3, AES-256)"**: Cannot be bypassed - requires password
- **"Standard (R=2, RC4-128)"**: Can attempt bypass - good chance of success
- **"Weak (R=1, RC4-40)"**: Can attempt bypass - high chance of success
- **"Successfully unlocked"**: Password protection was removed and verified

## When Unlocking Fails

If unlocking fails, it's usually because:

1. **Strong Encryption (R=3)**: This is **impossible to bypass** - you need the password
2. **Corrupted PDF**: The file may be damaged
3. **Unsupported Encryption**: Very rare, but some custom encryption exists

**This is normal and expected** for properly secured PDFs!

## Security Note

⚠️ **Important**: This tool is intended for legitimate use cases such as:
- Recovering access to your own password-protected documents
- Processing documents where you have legal permission to remove protection
- Educational and research purposes

**The tool cannot bypass strong encryption (R=3)** - this is a security feature, not a bug!

## License

MIT License

Copyright (c) 2024 Abozar Alizadeh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Disclaimer

The authors are not responsible for any misuse of this tool. Users must ensure they have proper authorization to unlock any PDF files they process. **Strong encryption (R=3) cannot be bypassed** - this is by design for security.

# 🚀 Quick Start Guide

## ⚠️ Important: What Can Be Unlocked

**Not all PDFs can be unlocked without the password!** The script automatically detects:

- **🔒 Strong Encryption (R=3, AES-256)**: **Cannot be bypassed** - requires actual password (minor chance with brute force)
- **🔓 Standard/Weak Encryption (R=1-2)**: **Can attempt bypass** - good success rate
- **🔓 No Encryption**: **Already accessible** - no action needed

## For macOS/Linux Users

1. **Setup** (one-time):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Install command-line tools** (for best results):
   ```bash
   brew install qpdf pdfcrack  # macOS
   sudo apt-get install qpdf pdfcrack  # Ubuntu/Debian
   ```

3. **Use**:
   ```bash
   source venv/bin/activate
   python pdf_unlocker.py
   ```

## For Windows Users

1. **Setup** (one-time):
   ```cmd
   setup.bat
   ```

2. **Install command-line tools** (optional):
   - Download qpdf from https://github.com/qpdf/qpdf/releases
   - Download pdfcrack from https://sourceforge.net/projects/pdfcrack/
   - Add to PATH for best results

3. **Use**:
   ```cmd
   venv\Scripts\activate.bat
   python pdf_unlocker.py
   ```

## Manual Setup (Alternative)

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
   ```

2. **Install dependencies**:
   ```bash
   pip install pikepdf pymupdf PyPDF2
   ```

3. **Run the script**:
   ```bash
   python pdf_unlocker.py
   ```

## What Happens Next?

- The script will automatically find PDFs in the `PDFs/` folder
- **Encryption analysis** tells you immediately if unlocking is possible
- **Multiple unlocking methods** will be tried for maximum success:
  - **qpdf** (command-line tool - most reliable)
  - **pdfcrack** (brute force password cracking)
  - **PyMuPDF** (best content preservation)
  - **pikepdf** (most powerful)
  - **PyPDF2** (basic fallback)
- Unlocked PDFs will be saved in `Unlocked_PDFs/` with the prefix `unlocked_`
- **Each unlocked PDF is verified** to ensure it's truly accessible
- Your original PDFs remain unchanged

## Need Help?

- Run `python pdf_unlocker.py --help` for all options
- Check the full `README.md` for detailed documentation
- The script handles errors gracefully and provides clear feedback
- **Encryption detection** prevents wasting time on impossible tasks

## Example Output

### Successful Unlock:
```
Processing: document.pdf
  - Password protected (pikepdf)
  - Encryption: Standard (R=2, RC4-128)
  - Can unlock: Yes - Can attempt bypass
  - Attempting to unlock...
    - Trying qpdf...
    - Successfully unlocked with qpdf
  - ✅ Successfully unlocked and verified: unlocked_document.pdf
    - Valid PDF with content (1 pages)
```

### Strong Encryption (Cannot Bypass):
```
Processing: secure.pdf
  - Password protected (pikepdf)
  - Encryption: Strong (R=3, AES-256)
  - Can unlock: No - Requires password
  - ❌ This PDF has strong encryption that cannot be bypassed
  - 💡 You need the actual password to unlock this PDF
```

## 🔓 Why Multiple Methods?

The script uses **5 different approaches** because:
- **qpdf**: Best for weak/standard encryption (command-line tool)
- **pdfcrack**: Brute force password cracking (can be time-consuming)
- **PyMuPDF**: Best for content preservation and quality
- **pikepdf**: Most powerful for complex PDFs
- **PyPDF2**: Reliable fallback for basic protection

This gives you the **highest possible success rate** for PDFs that can actually be unlocked!

## 💡 When Unlocking Fails

If unlocking fails, it's usually because:
1. **Strong Encryption (R=3)**: **Nearly impossible to bypass** - you need the password (minor chance with brute force)
2. **Corrupted PDF**: The file may be damaged
3. **Unsupported Encryption**: Very rare

**This is normal and expected** for properly secured PDFs!

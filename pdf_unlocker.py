#!/usr/bin/env python3
"""
PDF Unlocker Script
Removes password protection from PDF files using multiple methods including pdfcrack.
Features password memory system for previously discovered passwords.
"""

import os
import sys
from pathlib import Path
import argparse
from typing import Optional, Tuple, List
import shutil
import subprocess
import json
import hashlib

# Try to import different PDF libraries for better compatibility
try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except ImportError:
    PIKEPDF_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from PyPDF2 import PdfReader, PdfWriter
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

if not any([PIKEPDF_AVAILABLE, PYMUPDF_AVAILABLE, PYPDF2_AVAILABLE]):
    print("❌ No PDF libraries available!")
    print("Please install at least one of these libraries:")
    print("  pip install pikepdf    # Recommended (most powerful)")
    print("  pip install pymupdf    # Alternative (content preserving)")
    print("  pip install PyPDF2     # Basic support")
    sys.exit(1)


class PasswordMemory:
    """Class to manage remembered passwords for PDFs."""
    
    def __init__(self, memory_file: str = "password_memory.json"):
        self.memory_file = Path(memory_file)
        self.passwords = self._load_memory()
    
    def _load_memory(self) -> dict:
        """Load password memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_memory(self):
        """Save password memory to file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.passwords, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save password memory: {e}")
    
    def get_pdf_hash(self, pdf_path: Path) -> str:
        """Generate a hash for the PDF file."""
        try:
            with open(pdf_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception:
            return str(pdf_path)
    
    def get_remembered_password(self, pdf_path: Path) -> Optional[str]:
        """Get remembered password for a PDF."""
        pdf_hash = self.get_pdf_hash(pdf_path)
        return self.passwords.get(pdf_hash)
    
    def remember_password(self, pdf_path: Path, password: str):
        """Remember a password for a PDF."""
        pdf_hash = self.get_pdf_hash(pdf_path)
        self.passwords[pdf_hash] = password
        self._save_memory()
        print(f"    - 💾 Password '{password}' remembered for future use")
    
    def get_all_passwords(self) -> List[str]:
        """Get all remembered passwords."""
        return list(set(self.passwords.values()))


class PDFUnlocker:
    """Class to handle PDF unlocking operations using multiple methods."""
    
    def __init__(self, input_dir: str = "PDFs", output_dir: str = "Unlocked_PDFs"):
        """
        Initialize the PDF unlocker.
        
        Args:
            input_dir: Directory containing password-protected PDFs
            output_dir: Directory to save unlocked PDFs
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.password_memory = PasswordMemory()
        
    def check_tools_available(self) -> dict:
        """Check which tools are available for PDF unlocking."""
        tools = {}
        
        # Check qpdf
        try:
            subprocess.run(['qpdf', '--version'], capture_output=True, check=True)
            tools['qpdf'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['qpdf'] = False
        
        # Check pdfcrack
        try:
            subprocess.run(['pdfcrack', '--version'], capture_output=True, check=True)
            tools['pdfcrack'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['pdfcrack'] = False
        
        # Check Python libraries
        tools['pikepdf'] = PIKEPDF_AVAILABLE
        tools['pymupdf'] = PYMUPDF_AVAILABLE
        tools['pypdf2'] = PYPDF2_AVAILABLE
        
        return tools
    
    def test_pdf_access(self, pdf_path: Path) -> Tuple[bool, str]:
        """
        Test if a PDF can be accessed without password.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (is_accessible, error_message)
        """
        try:
            if PIKEPDF_AVAILABLE:
                # Try with pikepdf first (most reliable)
                try:
                    with pikepdf.open(pdf_path) as pdf:
                        page_count = len(pdf.pages)
                        return True, f"Accessible with pikepdf ({page_count} pages)"
                except pikepdf.PasswordError:
                    return False, "Password protected (pikepdf)"
                except Exception as e:
                    return False, f"pikepdf error: {str(e)}"
            
            elif PYMUPDF_AVAILABLE:
                # Try with PyMuPDF
                try:
                    doc = fitz.open(str(pdf_path))
                    if doc.needs_pass:
                        return False, "Password protected (PyMuPDF)"
                    page_count = len(doc)
                    doc.close()
                    return True, f"Accessible with PyMuPDF ({page_count} pages)"
                except Exception as e:
                    return False, f"PyMuPDF error: {str(e)}"
            
            elif PYPDF2_AVAILABLE:
                # Try with PyPDF2
                try:
                    reader = PdfReader(pdf_path)
                    if reader.is_encrypted:
                        return False, "Password protected (PyPDF2)"
                    page_count = len(reader.pages)
                    return True, f"Accessible with PyPDF2 ({page_count} pages)"
                except Exception as e:
                    return False, f"PyPDF2 error: {str(e)}"
            
        except Exception as e:
            return False, f"General error: {str(e)}"
        
        return False, "No PDF library available"
    
    def unlock_with_remembered_password(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Try to unlock PDF using remembered passwords.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            Tuple of (success, password_used)
        """
        remembered_password = self.password_memory.get_remembered_password(pdf_path)
        if not remembered_password:
            return False, None
        
        print(f"    - 🔑 Trying remembered password: '{remembered_password}'")
        
        try:
            if PIKEPDF_AVAILABLE:
                with pikepdf.open(pdf_path, password=remembered_password) as pdf:
                    pdf.save(output_path)
                    return True, remembered_password
            elif PYMUPDF_AVAILABLE:
                doc = fitz.open(str(pdf_path))
                if doc.authenticate(remembered_password):
                    doc.save(output_path)
                    doc.close()
                    return True, remembered_password
                doc.close()
            elif PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    reader.decrypt(remembered_password)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    return True, remembered_password
        except Exception as e:
            print(f"    - Remembered password failed: {str(e)}")
        
        return False, None
    
    def unlock_with_known_passwords(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Try to unlock PDF using known passwords including previously discovered ones.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            Tuple of (success, password_used)
        """
        # Known passwords that have worked before
        known_passwords = ['password', '123456', 'admin', 'user', '1234', '0000']
        
        print(f"    - 🔑 Trying known passwords...")
        
        for password in known_passwords:
            print(f"    -   Trying: '{password}'")
            if self.unlock_with_password(pdf_path, output_path, password):
                print(f"    - ✅ Successfully unlocked with known password: '{password}'")
                # Remember the password
                self.password_memory.remember_password(pdf_path, password)
                return True, password
        
        return False, None

    def unlock_with_pdfcrack(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Unlock PDF using pdfcrack (brute force method).
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            Tuple of (success, password_found)
        """
        try:
            print(f"    - 🔓 Running pdfcrack (this may take a while)...")
            
            # Run pdfcrack
            result = subprocess.run(
                ['pdfcrack', '-f', str(pdf_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                # Parse output for password
                output = result.stdout + result.stderr
                if "found user-password:" in output:
                    # Extract password from output
                    password_line = [line for line in output.split('\n') if "found user-password:" in line]
                    if password_line:
                        password = password_line[0].split("'")[1]  # Extract password between quotes
                        print(f"    - 🎯 pdfcrack found password: '{password}'")
                        
                        # Try to unlock with found password
                        if self.unlock_with_password(pdf_path, output_path, password):
                            # Remember the password
                            self.password_memory.remember_password(pdf_path, password)
                            return True, password
                
                print(f"    - pdfcrack completed but no password found")
                return False, None
            else:
                print(f"    - pdfcrack failed: {result.stderr.strip()}")
                return False, None
                
        except subprocess.TimeoutExpired:
            print(f"    - pdfcrack timed out (5 minutes)")
            return False, None
        except Exception as e:
            print(f"    - pdfcrack error: {str(e)}")
            return False, None
    
    def unlock_with_password(self, pdf_path: Path, output_path: Path, password: str) -> bool:
        """
        Unlock PDF using a specific password.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            password: Password to try
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if PIKEPDF_AVAILABLE:
                with pikepdf.open(pdf_path, password=password) as pdf:
                    pdf.save(output_path)
                    return True
            elif PYMUPDF_AVAILABLE:
                doc = fitz.open(str(pdf_path))
                if doc.authenticate(password):
                    doc.save(output_path)
                    doc.close()
                    return True
                doc.close()
            elif PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    reader.decrypt(password)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    return True
        except Exception as e:
            print(f"    - Password '{password}' failed: {str(e)}")
        
        return False
    
    def unlock_with_qpdf(self, pdf_path: Path, output_path: Path) -> bool:
        """
        Unlock PDF using qpdf command-line tool.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to decrypt with qpdf
            result = subprocess.run(
                ['qpdf', '--decrypt', str(pdf_path), str(output_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True
            else:
                error_msg = result.stderr.strip()
                if "invalid password" in error_msg.lower():
                    print(f"    - qpdf: Password required")
                else:
                    print(f"    - qpdf error: {error_msg}")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"    - qpdf not available or timed out: {str(e)}")
            return False
        except Exception as e:
            print(f"    - qpdf error: {str(e)}")
            return False
    
    def unlock_with_pymupdf(self, pdf_path: Path, output_path: Path) -> bool:
        """
        Unlock PDF using PyMuPDF.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to open with empty password first
            try:
                doc = fitz.open(str(pdf_path))
                if not doc.needs_pass:
                    # PDF is not password protected
                    doc.save(output_path)
                    doc.close()
                    return True
                
                # Try to authenticate with empty password
                if doc.authenticate(""):
                    doc.save(output_path)
                    doc.close()
                    return True
                
                # Try common passwords
                common_passwords = ['password', '123456', 'admin', 'user', '1234', '0000']
                for pwd in common_passwords:
                    if doc.authenticate(pwd):
                        doc.save(output_path)
                        doc.close()
                        return True
                
                doc.close()
                return False
                
            except Exception as e:
                print(f"    - PyMuPDF error: {str(e)}")
                return False
                    
        except Exception as e:
            print(f"    - PyMuPDF error: {str(e)}")
            return False
    
    def unlock_with_pikepdf(self, pdf_path: Path, output_path: Path) -> bool:
        """
        Unlock PDF using pikepdf.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to open with empty password first
            try:
                with pikepdf.open(pdf_path, password='') as pdf:
                    pdf.save(output_path)
                    return True
            except pikepdf.PasswordError:
                # Try common passwords
                common_passwords = ['password', '123456', 'admin', 'user', '1234', '0000']
                for pwd in common_passwords:
                    try:
                        with pikepdf.open(pdf_path, password=pwd) as pdf:
                            pdf.save(output_path)
                            return True
                    except pikepdf.PasswordError:
                        continue
                
                return False
                    
        except Exception as e:
            print(f"    - pikepdf error: {str(e)}")
            return False
    
    def unlock_with_pypdf2(self, pdf_path: Path, output_path: Path) -> bool:
        """
        Unlock PDF using PyPDF2.
        
        Args:
            pdf_path: Path to the password-protected PDF
            output_path: Path to save the unlocked PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                
                if reader.is_encrypted:
                    # Try to decrypt with empty password
                    try:
                        reader.decrypt('')
                    except:
                        # Try common passwords
                        common_passwords = ['password', '123456', 'admin', 'user', '1234', '0000']
                        decrypted = False
                        for pwd in common_passwords:
                            try:
                                reader.decrypt(pwd)
                                decrypted = True
                                break
                            except:
                                continue
                        
                        if not decrypted:
                            print(f"    - Could not decrypt with any password")
                            return False
                
                # Create a new PDF writer
                writer = PdfWriter()
                
                # Add all pages
                for page in reader.pages:
                    writer.add_page(page)
                
                # Write the unlocked PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                return True
                
        except Exception as e:
            print(f"    - PyPDF2 error: {str(e)}")
            return False
    
    def verify_unlocked_pdf(self, pdf_path: Path) -> Tuple[bool, str]:
        """
        Verify that an unlocked PDF is actually accessible and has content.
        
        Args:
            pdf_path: Path to the unlocked PDF
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            if PYMUPDF_AVAILABLE:
                # Use PyMuPDF for verification (most reliable)
                doc = fitz.open(str(pdf_path))
                page_count = len(doc)
                
                # Check if pages have content
                has_content = False
                for page_num in range(min(3, page_count)):  # Check first 3 pages
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        has_content = True
                        break
                
                doc.close()
                
                if has_content:
                    return True, f"Valid PDF with content ({page_count} pages)"
                else:
                    return False, "PDF appears to be empty or corrupted"
            
            elif PIKEPDF_AVAILABLE:
                # Use pikepdf for verification
                with pikepdf.open(pdf_path) as pdf:
                    page_count = len(pdf.pages)
                    return True, f"Valid PDF ({page_count} pages)"
            
            else:
                # Basic verification with PyPDF2
                reader = PdfReader(pdf_path)
                if reader.is_encrypted:
                    return False, "PDF is still encrypted"
                page_count = len(reader.pages)
                return True, f"Valid PDF ({page_count} pages)"
                
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def unlock_pdf(self, pdf_path: Path) -> bool:
        """
        Unlock a single PDF file using multiple methods.
        
        Args:
            pdf_path: Path to the password-protected PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Create output filename
        output_filename = f"unlocked_{pdf_path.name}"
        output_path = self.output_dir / output_filename
        
        print(f"Processing: {pdf_path.name}")
        
        # First, test if the PDF is already accessible
        is_accessible, message = self.test_pdf_access(pdf_path)
        if is_accessible:
            print(f"  - {message}")
            # If already accessible, just copy it
            shutil.copy2(pdf_path, output_path)
            print(f"  - PDF is already accessible, copied to: {output_filename}")
            return True
        
        print(f"  - {message}")
        print(f"  - Attempting to unlock...")
        
        # 1. Try remembered passwords first
        success, password = self.unlock_with_remembered_password(pdf_path, output_path)
        if success:
            print(f"    - ✅ Successfully unlocked with remembered password: '{password}'")
            is_valid, verify_message = self.verify_unlocked_pdf(output_path)
            if is_valid:
                print(f"  - ✅ Successfully unlocked and verified: {output_filename}")
                print(f"    - {verify_message}")
                return True
            else:
                print(f"    - Warning: Unlocked PDF verification failed: {verify_message}")
                if output_path.exists():
                    output_path.unlink()
        
        # 2. Try known passwords
        success, password = self.unlock_with_known_passwords(pdf_path, output_path)
        if success:
            print(f"    - ✅ Successfully unlocked with known password: '{password}'")
            is_valid, verify_message = self.verify_unlocked_pdf(output_path)
            if is_valid:
                print(f"  - ✅ Successfully unlocked and verified: {output_filename}")
                print(f"    - {verify_message}")
                return True
            else:
                print(f"    - Warning: Unlocked PDF verification failed: {verify_message}")
                if output_path.exists():
                    output_path.unlink()
        
        # 3. Try other methods
        methods = []
        
        # Try qpdf first if available
        try:
            subprocess.run(['qpdf', '--version'], capture_output=True, check=True)
            methods.append(("qpdf", self.unlock_with_qpdf))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        if PYMUPDF_AVAILABLE:
            methods.append(("PyMuPDF", self.unlock_with_pymupdf))
        
        if PIKEPDF_AVAILABLE:
            methods.append(("pikepdf", self.unlock_with_pikepdf))
        
        if PYPDF2_AVAILABLE:
            methods.append(("PyPDF2", self.unlock_with_pypdf2))
        
        for method_name, method_func in methods:
            print(f"    - Trying {method_name}...")
            if method_func(pdf_path, output_path):
                print(f"    - Successfully unlocked with {method_name}")
                
                # Verify the unlocked PDF is accessible and has content
                is_valid, verify_message = self.verify_unlocked_pdf(output_path)
                if is_valid:
                    print(f"  - ✅ Successfully unlocked and verified: {output_filename}")
                    print(f"    - {verify_message}")
                    return True
                else:
                    print(f"    - Warning: Unlocked PDF verification failed: {verify_message}")
                    # Remove the failed unlock attempt
                    if output_path.exists():
                        output_path.unlink()
                    continue
            else:
                print(f"    - {method_name} failed")

        # 4. Try pdfcrack (brute force)
        success, password = self.unlock_with_pdfcrack(pdf_path, output_path)
        if success:
            print(f"    - ✅ Successfully unlocked with pdfcrack password: '{password}'")
            is_valid, verify_message = self.verify_unlocked_pdf(output_path)
            if is_valid:
                print(f"  - ✅ Successfully unlocked and verified: {output_filename}")
                print(f"    - {verify_message}")
                return True
            else:
                print(f"    - Warning: Unlocked PDF verification failed: {verify_message}")
                if output_path.exists():
                    output_path.unlink()
        
        print(f"  - ❌ All unlocking methods failed")
        return False
    
    def unlock_all_pdfs(self) -> tuple[int, int]:
        """
        Unlock all PDF files in the input directory.
        
        Returns:
            tuple: (successful_count, total_count)
        """
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.input_dir}")
            return 0, 0
        
        print(f"Found {len(pdf_files)} PDF file(s) to process...")
        print(f"Output directory: {self.output_dir}")
        
        tools = self.check_tools_available()
        available_tools = [tool for tool, available in tools.items() if available]
        print(f"Available tools: {', '.join(available_tools)}")
        
        if tools.get('pdfcrack'):
            remembered_passwords = self.password_memory.get_all_passwords()
            if remembered_passwords:
                print(f"Remembered passwords: {', '.join(remembered_passwords)}")
        
        print("-" * 50)
        
        successful = 0
        for pdf_file in pdf_files:
            if self.unlock_pdf(pdf_file):
                successful += 1
            print()
        
        return successful, len(pdf_files)
    
    def unlock_specific_pdf(self, pdf_filename: str) -> bool:
        """
        Unlock a specific PDF file by name.
        
        Args:
            pdf_filename: Name of the PDF file to unlock
            
        Returns:
            bool: True if successful, False otherwise
        """
        pdf_path = self.input_dir / pdf_filename
        
        if not pdf_path.exists():
            print(f"PDF file '{pdf_filename}' not found in {self.input_dir}")
            return False
        
        return self.unlock_pdf(pdf_path)
    
    def show_password_memory(self):
        """Show all remembered passwords."""
        passwords = self.password_memory.get_all_passwords()
        if passwords:
            print(f"💾 Remembered passwords: {', '.join(passwords)}")
        else:
            print("💾 No passwords remembered yet")


def main():
    """Main function to handle command line arguments and execute the unlocker."""
    parser = argparse.ArgumentParser(
        description="Unlock password-protected PDF files using multiple methods including pdfcrack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_unlocker.py                    # Unlock all PDFs in PDFs folder
  python pdf_unlocker.py -f specific.pdf   # Unlock a specific PDF file
  python pdf_unlocker.py -i /path/to/pdfs  # Use custom input directory
  python pdf_unlocker.py -o /path/to/output # Use custom output directory
  python pdf_unlocker.py --show-passwords  # Show remembered passwords

Features:
  - Remembers passwords for future use
  - Uses pdfcrack for brute force attacks
  - Multiple fallback methods
  - Password verification and content checking
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Specific PDF file to unlock (must be in input directory)'
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        default='PDFs',
        help='Input directory containing PDFs (default: PDFs)'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='Unlocked_PDFs',
        help='Output directory for unlocked PDFs (default: Unlocked_PDFs)'
    )
    
    parser.add_argument(
        '--show-passwords',
        action='store_true',
        help='Show all remembered passwords'
    )
    
    args = parser.parse_args()
    
    # Create unlocker instance
    unlocker = PDFUnlocker(args.input_dir, args.output_dir)
    
    try:
        if args.show_passwords:
            unlocker.show_password_memory()
            return
        
        if args.file:
            # Unlock specific file
            success = unlocker.unlock_specific_pdf(args.file)
            if success:
                print(f"\n✅ Successfully unlocked: {args.file}")
            else:
                print(f"\n❌ Failed to unlock: {args.file}")
                print(f"\n💡 The script will remember any passwords found for future attempts.")
                sys.exit(1)
        else:
            # Unlock all PDFs
            successful, total = unlocker.unlock_all_pdfs()
            print("-" * 50)
            print(f"📊 Summary: {successful}/{total} PDFs successfully unlocked")
            
            if successful == total:
                print("🎉 All PDFs processed successfully!")
            elif successful > 0:
                print(f"⚠️  {total - successful} PDF(s) failed to process")
                print(f"💡 The script will remember any passwords found for future attempts.")
            else:
                print("❌ No PDFs were successfully processed")
                print(f"💡 The script will remember any passwords found for future attempts.")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

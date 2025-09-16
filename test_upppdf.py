#!/usr/bin/env python3
"""
Minimal tests for upppdf package
"""

import unittest
import tempfile
import os
from pathlib import Path
from upppdf.pdf_unlocker import PDFUnlocker, PasswordMemory


class TestUpppdf(unittest.TestCase):
    """Minimal tests for upppdf package"""
    
    def test_imports(self):
        """Test that all imports work"""
        import upppdf
        from upppdf import PDFUnlocker, PasswordMemory
        self.assertTrue(hasattr(upppdf, '__version__'))
    
    def test_password_memory_basic(self):
        """Test basic PasswordMemory functionality"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            memory_file = f.name
        
        try:
            memory = PasswordMemory(memory_file)
            self.assertIsInstance(memory, PasswordMemory)
            
            # Test basic functionality
            test_pdf = Path("test.pdf")
            memory.remember_password(test_pdf, "test123")
            remembered = memory.get_remembered_password(test_pdf)
            self.assertEqual(remembered, "test123")
        finally:
            if os.path.exists(memory_file):
                os.remove(memory_file)
    
    def test_pdf_unlocker_creation(self):
        """Test PDFUnlocker can be created"""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = os.path.join(temp_dir, "input")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(input_dir)
            os.makedirs(output_dir)
            
            unlocker = PDFUnlocker(input_dir, output_dir)
            self.assertIsInstance(unlocker, PDFUnlocker)
            
            # Test tools check
            tools = unlocker.check_tools_available()
            self.assertIsInstance(tools, dict)


if __name__ == '__main__':
    unittest.main()

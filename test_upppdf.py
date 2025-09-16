#!/usr/bin/env python3
"""
Basic tests for upppdf package
"""

import unittest
import tempfile
import os
from pathlib import Path
from upppdf.pdf_unlocker import PDFUnlocker, PasswordMemory


class TestPasswordMemory(unittest.TestCase):
    """Test the PasswordMemory class"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.temp_dir, "test_memory.json")
        self.memory = PasswordMemory(self.memory_file)
    
    def tearDown(self):
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        os.rmdir(self.temp_dir)
    
    def test_memory_creation(self):
        """Test that PasswordMemory can be created"""
        self.assertIsInstance(self.memory, PasswordMemory)
        self.assertEqual(self.memory.passwords, {})
    
    def test_password_remembering(self):
        """Test that passwords can be remembered"""
        test_pdf = Path("test.pdf")
        test_password = "test123"
        
        self.memory.remember_password(test_pdf, test_password)
        remembered = self.memory.get_remembered_password(test_pdf)
        
        self.assertEqual(remembered, test_password)
    
    def test_get_all_passwords(self):
        """Test getting all remembered passwords"""
        test_pdf1 = Path("test1.pdf")
        test_pdf2 = Path("test2.pdf")
        
        self.memory.remember_password(test_pdf1, "pass1")
        self.memory.remember_password(test_pdf2, "pass2")
        
        all_passwords = self.memory.get_all_passwords()
        self.assertIn("pass1", all_passwords)
        self.assertIn("pass2", all_passwords)


class TestPDFUnlocker(unittest.TestCase):
    """Test the PDFUnlocker class"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, "input")
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.input_dir)
        os.makedirs(self.output_dir)
        
        self.unlocker = PDFUnlocker(self.input_dir, self.output_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_unlocker_creation(self):
        """Test that PDFUnlocker can be created"""
        self.assertIsInstance(self.unlocker, PDFUnlocker)
        self.assertEqual(self.unlocker.input_dir, Path(self.input_dir))
        self.assertEqual(self.unlocker.output_dir, Path(self.output_dir))
    
    def test_tools_check(self):
        """Test that tools availability can be checked"""
        tools = self.unlocker.check_tools_available()
        self.assertIsInstance(tools, dict)
        self.assertIn('pikepdf', tools)
        self.assertIn('pymupdf', tools)
        self.assertIn('pypdf2', tools)


if __name__ == '__main__':
    unittest.main()

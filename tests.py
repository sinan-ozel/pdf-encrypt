import os
import pytest
from tempfile import TemporaryDirectory
from argparse import Namespace
import pdf_encrypt
from PyPDF2 import PdfFileWriter, PdfFileReader

def test_encryption():
    "Test if file is encrypted."
    with TemporaryDirectory() as temp_dir:
        pdf_encrypt.getpass = lambda: 'testpass'
        kwargs = {
            'filepaths': 'test_assets/test.pdf',
            'output_folder': temp_dir,
        }
        pdf_encrypt.main(**kwargs)
        reader = PdfFileReader(os.path.join(temp_dir, 'test.pdf'))
        assert reader.isEncrypted

def test_wildcard_use():
    "Test that wildcard work as expected."
    with TemporaryDirectory() as temp_dir:
        pdf_encrypt.getpass = lambda: 'testpass'
        kwargs = {
            'filepaths': 'test_assets/test*.pdf',
            'output_folder': temp_dir,
        }
        pdf_encrypt.main(**kwargs)
        assert os.path.exists(os.path.join(temp_dir, 'test1.pdf'))
        assert os.path.exists(os.path.join(temp_dir, 'test2.pdf'))


def test_multiple_files():
    "Test multiple file encryption."
    with TemporaryDirectory() as temp_dir:
        pdf_encrypt.getpass = lambda: 'testpass'
        kwargs = {
            'filepaths': ['test_assets/test1.pdf', 'test_assets/test2.pdf'],
            'output_folder': temp_dir,
        }
        pdf_encrypt.main(**kwargs)
        assert os.path.exists(os.path.join(temp_dir, 'test1.pdf'))
        assert os.path.exists(os.path.join(temp_dir, 'test2.pdf'))


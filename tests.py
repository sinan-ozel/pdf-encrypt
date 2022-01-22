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
        args = Namespace(
            FILES='test_assets/test.pdf',
            output_folder=temp_dir,
            log_level='ERROR'
        )
        pdf_encrypt.main(args)
        reader = PdfFileReader(os.path.join(temp_dir, 'test.pdf'))
        assert reader.isEncrypted

def test_wildcard_use():
    "Test that wildcard work as expected."
    with TemporaryDirectory() as temp_dir:
        pdf_encrypt.getpass = lambda: 'testpass'
        args = Namespace(
            FILES='test_assets/test*.pdf',
            output_folder=temp_dir,
            log_level='ERROR'
        )
        pdf_encrypt.main(args)
        assert os.path.exists(os.path.join(temp_dir, 'test1.pdf'))
        assert os.path.exists(os.path.join(temp_dir, 'test2.pdf'))



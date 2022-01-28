#!/usr/bin/env python3
"""
pdf-encrypt

Command-line tool to add password to multiple PDF files.

For security reasons, the program will prompt for password. Multiple
files can be password-protected at the same time, but the same password
will be used for all of them.
"""

__version__ = "0.2.0"
__author__ = 'Sinan Ozel'

import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from glob import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
from getpass import getpass
import logging
from SecureString import clearmem


class Password:
    """Ask for a password, then securely delete it from memory.

    Inspired by the following blog post:
    https://www.sjoerdlangkemper.nl/2016/06/09/clearing-memory-in-python/
    """
    def __enter__(self):
        self.password = getpass()  #pylint: disable=attribute-defined-outside-init
        retyped_passwd = getpass()
        if self.password != retyped_passwd:
            clearmem(self.password)
            clearmem(retyped_passwd)
            raise ValueError("""The two passwords do not match.""")
        clearmem(retyped_passwd)

        return self.password

    def __exit__(self, exc_type, exc_val, exc_tb):
        clearmem(self.password)


def main(filepaths, suffix:str=None, output_folder:str=None):
    if isinstance(filepaths, str):
        filepaths = glob(filepaths)
    if not filepaths:
        raise ValueError("No input filenames.")
    logging.debug("%d files found.", len(filepaths))

    # Check if all files exist.
    for input_filepath in filepaths:
        if os.path.isdir(input_filepath):
            raise IsADirectoryError(f"{input_filepath} is a directory, but it "
                                    f"needs to be a path.")

    if output_folder is None:
        output_folder = os.getcwd()
    # Create output folder
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for input_filepath in filepaths:
        basename = os.path.basename(input_filepath)
        if suffix is not None:
            filename, extension = os.path.splitext(basename)
            output_filename = filename + suffix + '.' + extension
        else:
            output_filename = basename
        output_filepath = os.path.join(output_folder, output_filename)
        if os.path.exists(output_filepath):
            prompt = input(f"{output_filename} already exists. Overwrite? (Y/N)")
            if prompt[0].upper() != 'Y':
                continue

        # Open input file
        logging.info("Opening %s...", input_filepath)
        input_file = PdfFileReader(input_filepath)
        logging.info("Opened %s...", input_filepath)
        output_writer = PdfFileWriter()
        page_count = input_file.numPages
        logging.debug("%d pages found in file %s.", page_count, input_filepath)
        for page_number in range(page_count):
            page = input_file.getPage(page_number)
            output_writer.addPage(page)

        with Password() as password:
            output_writer.encrypt(password)

        # Write to output file
        logging.info("Writing to %s...", output_filepath)
        with open(output_filepath, "wb") as output_file:
            output_writer.write(output_file)
        logging.info("Written to %s...", output_filepath)



if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("FILES",
                        type=str,
                        help="Path to the PDF file to encrypt. "
                             "Wildcards are allowed.")
    parser.add_argument("--suffix",
                        "-s",
                        default="-encrypted",
                        help="Suffix to add to output filename "
                             "before the file extension .pdf.")
    parser.add_argument("--output-folder",
                        "-o",
                        type=str,
                        default='.',
                        help="Output path to put all the files in. "
                             "If left blank, current path will be used. "
                             "If it does not exist, it will be created.")
    parser.add_argument("--log-level",
                        type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='ERROR',
                        help="Set logging level.")
    args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=args.log_level)
    logging.raiseExceptions = True

    main(filepaths=args.FILES, suffix=args.suffix, output_folder=args.output_folder)

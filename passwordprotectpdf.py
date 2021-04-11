#!/usr/bin/env python3
"""
passwordprotectpdf.

Command-line tool to add password to multiple PDF files.

For security reasons, the program will prompt for password. Multiple
files can be password-protected at the same time, but the same password
will be used for all of them.
"""

__version__ = "0.1.0"
__author__ = 'Sinan Ozel'

import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from textwrap import dedent
from glob import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
from getpass import getpass
import logging
import gc


def main(args):
    logging.basicConfig(level=args.verbosity)
    logging.raiseExceptions = True

    filepaths = glob(args.FILES)
    if not filepaths:
        raise FileNotFoundError("Input files not found.")
    logging.debug("{} files found.".format(len(filepaths)))

    # Check if all files exist.
    for input_filepath in filepaths:
        if os.path.isdir(input_filepath):
            del password
            raise IsADirectoryError(
                dedent(f"""{input_filepath} is a directory, but it
                        need to be a path."""))

    # Prompt and save password.
    # TODO: Change password into a class to avoid memory leaks.
    password = getpass()
    retyped_password = getpass()
    if password != retyped_password:
        del password
        del retyped_password
        raise ValueError("""The two passwords do not match.""")
    del retyped_password

    # Create output folder
    if not os.path.isdir(args.output_folder):
        os.mkdir(args.output_folder)

    for input_filepath in filepaths:
        filename = os.path.basename(input_filepath)
        output_filepath = os.path.join(args.output_folder, filename)
        if os.path.exists(output_filepath):
            prompt = input(f"{filename} already exists. Overwrite? (Y/N)")
            if prompt[0].upper() != 'Y':
                continue

        # Open input file
        logging.info(f"Opening {input_filepath}...")
        input_file = PdfFileReader(input_filepath)
        logging.info(f"Opened {input_filepath}...")
        output_writer = PdfFileWriter()
        page_count = input_file.numPages
        logging.debug(f"{page_count} pages found in file {input_filepath}.")
        for page_number in range(page_count):
            page = input_file.getPage(page_number)
            output_writer.addPage(page)

        output_writer.encrypt(password)

        # Write to output file
        logging.info(f"Writing to {output_filepath}...")
        with open(output_filepath, "wb") as output_file:
            output_writer.write(output_file)
        logging.info(f"Written to {output_filepath}...")

    # Delete password to avoid memory leaks
    ref_count = sys.getrefcount(password)
    if ref_count > 2:
        logging.warning(dedent(f"""Ref count for the password variable
                                   is {ref_count}. Any number larger than
                                   2 may indicate a memory leak."""))
    else:
        logging.debug(dedent(f"""Ref count for the password: {ref_count}.
                                 (Values greater than 2 could be a cause for
                                 memory leak concerns.)"""))
    del password
    gc.collect()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("FILES",
                        type=str,
                        help=dedent("""
                            Path to the PDF file to encrypt.
                            Wildcards are allowed.
                            """))
    parser.add_argument("--output-folder",
                        "-o",
                        type=str,
                        default='encrypted',
                        help=dedent("""
                            Output path to put all the files in.
                            If left blank, current path will be used.

                            If it does not exist, it will be created."""))
    parser.add_argument("--verbosity",
                        "-v",
                        type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='ERROR',
                        help=dedent("""Set verbosity."""))
    args = parser.parse_args(sys.argv[1:])

    main(args)

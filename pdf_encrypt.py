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
import gc

class Password:
    def __enter__(self):
        password = getpass()
        retyped_password = getpass()
        if password != retyped_password:
            del password
            del retyped_password
            raise ValueError("""The two passwords do not match.""")
        del retyped_password
        self.password = password

        return password

    def __get__(self):
        return self.password

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.password = ' ' * 32
        del self.password
        gc


def main(filepaths, suffix, output_folder):
    print(filepaths)
    print(filepaths)
    if isinstance(filepaths, str):
        filepaths = glob(filepaths)
    if not filepaths:
        raise FileNotFoundError("No input filenames.")
    logging.debug("{} files found.".format(len(filepaths)))

    # Check if all files exist.
    for input_filepath in filepaths:
        if os.path.isdir(input_filepath):
            raise IsADirectoryError(f"{input_filepath} is a directory, but it "
                                    f"needs to be a path.")

    # # Prompt and save password.
    # # TODO: Change password into a class to avoid memory leaks.
    # password = getpass()
    # retyped_password = getpass()
    # if password != retyped_password:
    #     del password
    #     del retyped_password
    #     raise ValueError("""The two passwords do not match.""")
    # del retyped_password

    with Password() as password:
        # Create output folder
        if not os.path.isdir(output_folder):
            # TODO: Add recursive folder support.
            os.mkdir(output_folder)

        for input_filepath in filepaths:
            filename = os.path.basename(input_filepath)
            # TODO: Add the suffix.
            output_filepath = os.path.join(output_folder, filename)
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


    del password
    gc.collect()


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
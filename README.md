# Introduction

Command-line tool to add password to multiple PDF files.

For security reasons, the program will prompt for password. Multiple
files can be password-protected at the same time, but the same password
will be used for all of them.

# Usage

To encrypt all PDF files in the current directory and put the
password-protected copies of these files in a folder called `output`, run:

```
pdf-encrypt *.pdf --output-folder output
```

# Download & Installation

## Installation for Windows

Download [dist/passwordprotectpdf.exe](dist/passwordprotectpdf.exe)
and save it in a directory in your "[Path](https://en.wikipedia.org/wiki/PATH_(variable))" (`%PATH%`).

# Development & Compiling

Create a virtual environment using the `requirements.txt` file found in
the repo. For example, you can run:
```
python -m venv .venv
```

while in your github repo clone, and then activate the environment using `.venv/scripts/activate`. Finally, you can install the required packages
with the command:
```
pip install -r requirements.txt
```

## Testing

Unit tests are not ready yet.

## Compilation

### Compiling on Windows Systems

While the virtual environment is activated, run:
```
python -m PyInstaller --hidden-import 'PyPDF2' --onefile .\passwordprotectpdf.py
```

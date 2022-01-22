from cx_Freeze import setup, Executable

setup(
    name='pdf-encrypt',
    description='A cross-platform tool to encrypt PDF files.',
    version='0.2.0',
    author='Sinan Ozel',
    license='MIT',
    packages=['PyPDF2'],
)

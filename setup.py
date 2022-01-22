from cx_Freeze import setup, Executable

setup(
    name='pdf-encrypt',
    description='A cross-platform tool to encrypt PDF files.',
    version='0.2.0',
    url='https://github.com/sinan-ozel/pdf-encrypt',
    author='Sinan Ozel',
    license='MIT',
    packages=['PyPDF2'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ]
)

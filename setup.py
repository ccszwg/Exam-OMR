import os

import pip
from setuptools import setup

lxml = os.path.dirname(os.path.abspath(__file__)) + '\lxml-3.7.0-cp35-cp35m-win32.whl'

dependancies = ['exceptions', 'comtypes', lxml, 'python-docx', 'qrcode', 'PyPDF2', 'pyqtgraph', 'PyQt5', 'numpy',
                'Pillow', 'opencv-python', 'wheel']


def install():
    try:
        for package in dependancies:
            pip.main(['install', package])

        setup(
            name='OMR',
            version='1.0.0',
            packages=['omr.src', 'omr.interface', 'omr.resources'],
            url='',
            license='',
            author='Theo Charalambous',
            author_email='theo.cftw@gmail.com',
            description='',
            tests_require=dependancies
        )
    except Exception as e:
        print(e)


install()

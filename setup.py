import pip
from setuptools import setup

dependancies = ['comtypes', 'docx', 'qrcode', 'PyPDF2', 'pyqtgraph', 'PyQt5', 'numpy', 'Pillow', 'opencv-python',
                'wheel']


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

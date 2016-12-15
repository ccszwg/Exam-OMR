from distutils.core import setup

# todo: test (OpenCV probably doesn't work)

setup(
    name='OMR',
    version='',
    packages=['omr.src', 'omr.interface'],
    url='',
    license='',
    author='Theo Charalambous',
    author_email='theo.cftw@gmail.com',
    description='',
    requires=['comtypes', 'docx', 'qrcode', 'PyPDF2', 'pyqtgraph', 'PyQt5', 'numpy', 'PIL', 'cv2']
)

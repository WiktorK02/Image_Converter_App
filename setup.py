from setuptools import setup, find_packages, Command
import os

here = os.path.abspath(os.path.dirname(__file__))
req_file = os.path.join(here, 'requirements.txt')
with open(req_file, 'r') as f:
    REQUIREMENTS = [line.strip() for line in f.readlines()]

LONG_DESCRIPTION = 'About Image converter GUI App to arduino oled display ssd1306 128x64'

setup(
   name='image-to-arduino',
   version='1.0.4.3',
   description='Image converter to arduino',
   license="MIT",
   author='WiktorK02',
   author_email='wiktor.kidon@hotmail.com',
   url="https://github.com/WiktorK02/Image_Converter_App.git",
   long_description_content_type="text/markdown",
   long_description=LONG_DESCRIPTION,
   packages=['image_to_arduino'],
   package_data={'image_to_arduino': ['data/*.dat']},
   install_requires=REQUIREMENTS, 
    entry_points={
        'console_scripts': [
            'image-to-arduino = image_to_arduino.__main__:main'
        ]
    },

)


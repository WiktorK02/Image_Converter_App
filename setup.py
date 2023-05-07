from setuptools import setup, find_packages, Command
import os


# Get the absolute path to the directory containing this setup.py file
here = os.path.abspath(os.path.dirname(__file__))

# Join the path to the requirements.txt file relative to the setup.py file
req_file = os.path.join(here, 'requirements.txt')

# Read the requirements.txt file and split into a list of lines
with open(req_file, 'r') as f:
    REQUIREMENTS = [line.strip() for line in f.readlines()]
LONG_DESCRIPTION = 'About Image converter GUI App to arduino oled display ssd1306 128x64'

setup(
   name='image-to-arduino',
   version='1.0.4.1',
   description='Image converter to arduino',
   license="MIT",
   author='WiktorK02',
   author_email='wiktor.kidon@hotmail.com',
   url="https://github.com/WiktorK02/Image_Converter_App.git",
   long_description_content_type="text/markdown",
   long_description=LONG_DESCRIPTION,
   packages=['src'],
   package_data={'src': ['data/*.dat']},
   install_requires=REQUIREMENTS, 
    entry_points={
        'console_scripts': [
            'image-to-arduino = src.imagetoarduino:main'
        ]
    },

)


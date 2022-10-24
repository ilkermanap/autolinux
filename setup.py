import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup ( name = 'autolinux',
                   version = '0.0.2',
                   description = 'Linux automation classes',
                   author = 'Ilker Manap',
                   author_email='ilkermanap@gmail.com',
                   long_description = long_description,
                   long_description_content_type="text/markdown",
                   url="https://github.com/ilkermanap/autolinux",
                   package_dir={'': 'src'},
                   packages=setuptools.find_packages('src'),
                   install_requires=[
                           'paramiko','scp',
                   ],
                   classifiers=[
                           "Programming Language :: Python :: 3",
                           "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                           "Operating System :: OS Independent",
                   ],           
)

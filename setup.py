from setuptools import setup, find_packages

setup(
	name = 'ovf2io',
	packages = find_packages(),
	version = '0.9.1',
	author = 'William S. Parker',
	author_email = 'will.parker0@gmail.com',
	description = 'Utility for reading and writing OOMMF Vector Field (.ovf) format.',
    url = 'https://github.com/McMorranLab/ovf2io',
    project_urls={
        "Documentation" : "https://mcmorranlab.github.io/ovf2io/",
        "Bug Tracker": "https://github.com/McMorranLab/ovf2io/issues",
    },
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
	python_requires='>=3.6',
    install_requires=['numpy']
)

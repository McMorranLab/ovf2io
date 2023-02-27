from setuptools import setup, find_packages

setup(
	name = 'ovf2io',
	packages = find_packages(),
	version = '0.9',
	author = 'William S. Parker',
	author_email = 'will.parker0@gmail.com',
	description = 'Utility for reading and writing OOMMF Vector Field (.ovf) format.',
	# url = 'https://github.com/McMorranLab/ltempy',
	# project_urls={
		# "Documentation" : "https://mcmorranlab.github.io/ltempy/",
		# "Bug Tracker": "https://github.com/McMorranLab/ltempy/issues",
	# },
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

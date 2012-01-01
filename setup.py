try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup



config = {
	'description' : 'dickslayer',
	'author' : 'David Winters',
	'url' : 'url',
	'download_url' : 'Where to download it',
	'author_email' : 'macdotdave@gmail.com',
	'version' : '1.0',
	'install_requires' : ['nose'],
	'packages' : ['dickslayer'],
	'scripts' : [],
	'name' : 'dickslayer'
}

setup(**config)
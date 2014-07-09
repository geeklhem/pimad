from setuptools import setup

setup(name='pimad',
      version=open('VERSION').read(),
      description='Pimad is modeling adaptive dynamics',
      url='http://www.eleves.ens.fr/home/doulcier/projects/celladhesion/',
      author='Guilhem Doulcier',
      long_description=open('README').read(),
      author_email='guilhem.doulcier@ens.fr',
      license='GPLv3',
      packages=['pimad'],
      #     scripts=['bin/vcontact','bin/vcontact-pcs'],
      install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
      ],
)

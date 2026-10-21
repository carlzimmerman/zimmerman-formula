pyHIARD
=====

The Python HI Artificial and Real Database (pyHIARD ) is a project to create a comprehensive database of Artificial and real galaxies that can be used for testing the various  software that is available for fitting galaxy survey. In principle it is developed for testing Tilted Ring Fitting Software but in principle it can be used for testing any Software for which the input parameters should be known.


pyHIARD Requires working versions of tirific and sofia2  for full functionality.

CASA is required for full simulations which are achieved through the casa python modules and they should be installed through the pip install. Note however that currently the modules are only available up to python 3.8.
!!!!!!!!For python versions > 3.8 the install will progress normally but the casatasks will not be installed and the casa corruption method will be unavailable!!!!!!!!

tirific is required for the Artificial branch and can be installed trough kern-suite https://kernsuite.info/ for ubuntu or it can be downloaded from https://github.com/gigjozsa/tirific. If you are struggling with tirific's pg plot dependency the branch no_pgp can be installed from the github. It wll work with pyHIARD

SoFiA2 is required for the masking and can be downloaded from https://github.com/SoFiA-Admin/SoFiA-2

Except for The Real Observed Catalogue should work without any external installations as long as no new galaxies are added. Do note that at the first instance of creating a base galaxy it requires an internet connection to download the original cubes. An origins disclaimer will be positions in each directory.

Please see the read the docs pages for additional information and set up.


Installation
----

Download the source code from the Github or simply install with pip as:

  `pip install pyHIARD`

This should also install all required python dependencies. We recommend the use of python virtual environments. If so desired a pyHIARD installation would look like:

  `python3 -m venv pyHIARD_venv`

  `source pyHIARD_venv/bin/activate.csh`

  `pip install --upgrade wheel setuptools pip`

  `pip install pyHIARD`

(In case of bash the correct middle line is 	source pyHIARD_venv/bin/activate)
You might have to restart the env:

  `deactivate`

  `source pyHIARD_venv/bin/activate.csh`

Often it is necessary to update the casa tables through:

  `python -m casatools --update-user-data`


Running pyHIARD
----

cd to the directory where you want the database to exist.
run pyHIARD by typing:

  `pyHIARD configuration_file=my_setup.yml`

or

  `pyHIARD`

answer the questions about what you want to create.

Setting can also be specified from the command line. These will take preference over the configuration file. For example if you want to recreate your data base with a slightly different beam. you could rerun pyHIARD as:

  'pyHIARD configuration_file=pyHIARD_tests.yml "agc.variables_to_vary=[beam_size]" "agc.beam_size=[[7.5,7.5,30.]]"

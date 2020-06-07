{{cookiecutter.project_name}}
==============================
add description

Tools and Libraries that are used (or encorage to use)
--------------------------------------------------------
for testing
- pytest, unittest

Packaging
- tox

Documentation
- sphinx, Read the Docs

Continuous Integration
- TravisCI

Container
- Docker

Coding Style
- flake8

start with CookieCutter
------------------------
ANYTHING inside of cookiecutter.Root is what you will be used as your bases (copy content within root and paste it to your project folder)

ANYTHING outside of cookiecutter.Root is components are must be build first by any packaging/build-in built tool (such as sphnix-quickstart which generate content for docs/ )

For further detail of folder outside of {{cookiecutter.Root}}, please read REAMDE contain within the folder

for more info of how to use cookiecutter click here: https://cookiecutter.readthedocs.io/en/1.7.2/first_steps.html
To use cookiecutter, please follow the following step

1. first modify cookiecutter.json file
2.  run the following command

.. code-block::

    cd Your/Project/Directory
    cd Root
    cookiecutter Path/to/Root


For more infomation of what each file do, there are a workshop on "Writing Reusable, Reproducible Python: Documentation, Packaging, Continuous Integration, and Beyond"

it can be found here: https://www.youtube.com/watch?v=lo_g-GbYtaA&t=8706s.

I created a duplication of github project used in the video for you to practice: https://github.com/Awannaphasch2016/Reusable-Reproducible-Python-Documentation-Packaging-Continuous-Integration-and-Beyond

Folder Usercase Explaination
------------------------------

global_parameters.py contains all global parameters. Also, you may want to consider having path to specific folder as global variable.

{{cookiecutter.Data}}
    - contains all data.
    - data has 4 child folders: External, Processed, Interim, Raw
    - External = external data extracted from online sources.
    - Processed = raw data + preprocessed
    - Interim = data that are saved while programs are running (purposed is to speed up the computing process. or use file to capture states of parameter used in exteriments)
    - Raw == raw data

{{cookiecutter.Docs}}
    - Contains Documents (similar to one create by sphinx-quickstart command)

{{cookiecutter.Examples}}
    - Note: child folder of Examples can be defined in anyway you like. (it will be ignore by .gitignore)
    - Examples are used for data explorations/trying out new methods/conduct quick example to get idea across
    - it differ from Notebook in that it does not use .ipynb it only uses .py.
    - Notice that are are scratch.py file. The use of scratch file is quite powerful when you want to try combination of new libraries while allow the snippet of code to be saved in relavant example file.

{{cookiecutter.Models}}
    - Models are used for data explorations/trying out new methods/conduct quick example to get idea across

{{cookiecutter.Notebooks_dir}}
    - contians all notebooks.
    - Notebooks contains only .ipynb file
    - Notebooks are used for data explorations/trying out new methods/conduct quick example to get idea across
    - when should you consider using Notebooks instead of Examples folder? when your experiment required interactive features/visual effects. or you need to show a quick experiment with your team and want them to be able to interact with the code.

{{cookiecutter.Outputs}}
    - Note: Output folder should not contain reports. You can think of Report as collection of data that are used to capture concept or emphasis on particular ideas
    - contains all output including img, data

{{cookiecutter.Sources_dir}}
    - Note: this file should contain function used for to deliver experimentation. It only contain components required for to conduct experiment.
    - contain all the meat including evalution/modeling/date preparation/data preprocessing/visualization function.

{{cookiecutter.Test_dir}}
    - contain unittest test.

{{cookiecutter.Utilites}}
    - contain utilities function or class that are shared across Modules/class/function.

Common question {{cookiecutter.Examples}} vs {{cookiecutter.Notebooks}}

{{cookiecutter.Examples}} is the same as notebook mostly. The only different is that {{cookiecutter.Notebooks}} uses .ipynb and {{cookiecutter.Examples}} uses .py


Installation
--------------
if you want to download and install it in develpemnt mode
do this is your favorite shell:


Installation
----------------
note: There is no need to use requirements.txt because all
of the required packages are contained in setup.cfg

.. code-block::

    git clone <this github repo>
    cd iter-together
    pip install -e .

Testing
----------------
Note: You must change directory of testing accordingly
.. code-block::

    pip install tox
    tox

Documentation
----------------
Note:
.. code-block::

    cd Documents
    sphinx-quickstart
    make build/html/index.html
    start


Usage
--------
Note: How does your project work? What does it do?


About the author
------------------
Author: {{cookiecutter.author}}

Email: {{cookiecutter.email}}

follow me on medium: account =  {{cookiecutter.medium_account}}

follow me on github: {{cookiecutter.github_repo}}

follow me on youtube: {{cookiecutter.youtube_channel}}



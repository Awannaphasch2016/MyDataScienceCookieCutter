Important Note
================
- please note that I am using window cmd shell.
- make necessary changes if you are using different shell.
- you must define cookiecutter variable by yourself in cookcutter.json file.


Intructions
===============
please take a look into each README within folder separately for more details on what there are and how to use them

you should first read REAMDME in {{cookiecutter.Root}}. This is a starting point.


TODO
================

- learn about click and add it here
    figure out why uploading to readthedocs show sphinx_click (Extension error: Could not import extension sphinx_click.ext (exception: No module named 'click')) I did put sphinx_click in docs/requirements.txt
- test that docs/sources/conf.py work as expected with this folder strucutre optimize for data science project.
- add planning folder -> introduce the way of using typing (code) and PlanUML (uml) to plan project.
- make [testenv:docs] compatible with window cmd
- make [testenv:docs] work for all requested shell
- learn about MANIFEST and add it here
- learn how to upload package to PyPI
- decide whether I should stick with pip or use conda ( from what I read using conda is alot better but Charlie Hoyt disagree and mention conda is just a wraper of pip which make things that are not supported by conda hard to setup. but how often are those cases? is it worth it? I just love conda)

Side Project
--------------
curated shared life long learning knowledge project: please send me email if anyone want to created "online shared brain"

**Goal** of curated shared life long learning knowledge is to compact knowledge to be as easy to absort as possible.

**Example** : could be identify a tutorial on "calculus" topic that are selected by a group member as easiest to understand.
There are no need to create various/new ways to explains things, just pick the best one and stick with it.

Now, imagine every single idea to be as compact as possible. How great would that be?

We will be using "Roam Research" as our main tools.

Here is the best roam research walkthrough:https://www.youtube.com/watch?v=vxOffM_tVHI&t=3s

About the author
------------------
Author: {{cookiecutter.author}}

Email: {{cookiecutter.email}}

follow me on medium: account =  {{cookiecutter.medium_account}}

follow me on github: {{cookiecutter.github_repo}}

follow me on youtube: {{cookiecutter.youtube_channel}}


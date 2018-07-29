========================================================
pydrop: Minimal Python Client for Digital Ocean Droplets
========================================================

This is a minimal tool designed to interact with the Digital Ocean API.
This does not translate all functionalities of the API but is a template
I created for some of the most common operations I could perform. New
tools will be added in the future as I familiarize myself further with
the API structure and use as a student. For now this tool allows you to
summarize all your droplets running, including and necessarily a price
summary to keep tabs on your droplets monthly and hourly rates. The tool
also allows you to seach by tags, delete a drop or perfrom actions such
as start, stop or shutdown a droplet.

Table of contents
-----------------

-  `Installation <#installation>`__
-  `Getting started <#getting-started>`__
-  `Digital Ocean Python CLI Tools <#digital-ocean-python-cli-tools>`__

   -  `Digital Ocean Key <#digital-ocean-key>`__
   -  `Droplets Info <#droplets-info>`__
   -  `Droplets Delete <#droplets-delete>`__
   -  `Droplets Action <#droplets-action>`__

Installation
------------

This assumes that you have native python & pip installed in your system,
you can test this by going to the terminal (or windows command prompt)
and trying

``python`` and then ``pip list``

If you get no errors and you have python 2.7.14 or higher you should be
good to go. Please note that I have tested this only on python 2.7.15
but can be easily modified for python 3.

To install **Python CLI for Digital Ocean** you can install using two
methods

``pip install pydrop``

or you can also try

::

   git clone https://github.com/samapriya/pydrop.git
   cd pydrop
   python setup.py install

For linux use sudo.

Installation is an optional step; the application can be also run
directly by executing pydrop.py script. The advantage of having it
installed is being able to execute ppipe as any command line tool. I
recommend installation within virtual environment. If you don’t want to
install, browse into the pydrop folder and try ``python pydrop.py`` to
get to the same result.


## Getting started

As usual, to print help:

::

   usage: pydrop [-h] {dokey,dropinfo,dropdelete,dropaction} ...

   Digital Ocean API Python CLI

   positional arguments:
     {dokey,dropinfo,dropdelete,dropaction}
       dokey               Enter your Digital Ocean API Key
       dropinfo            Prints information about all your droplets
       dropdelete          Permanently deletes the droplet
       dropaction          Performs an action on your droplets

   optional arguments:
     -h, --help            show this help message and exit

To obtain help for a specific functionality, simply call it with *help*
switch, e.g.: ``pydrop dropinfo -h``. If you didn’t install pydrop, then
you can run it just by going to *pydrop* directory and running
``python pydrop.py [arguments go here]``

Digital Ocean Python CLI Tools
------------------------------

The Digital Ocean Python CLI and tools setup contains minimal CLI in
python to perform basic actions on droplets along with query and analyze
your DO enviroment quickly.

Digital Ocean Key
~~~~~~~~~~~~~~~~~

This tool basically asks you to input your Digital Ocean API Key using a
password prompt this is then used for all subsequent tools. This tool
now includes an option for a quiet authentication using the API key
incase it is unable to invoke an interactive environment such as in
Google colaboratory.

::

   usage: pydrop dokey [-h] [--key KEY]

   optional arguments:
     -h, --help  show this help message and exit

   Optional named arguments:
     --key KEY   Your Digital Ocean API Key

If using on a private machine the Key is saved as a csv file for all
future runs of the tool.

Droplets Info
~~~~~~~~~~~~~

The droplets info tool prints summary info about all your droplets. You
can choose to narrow it down further using a droplet tag so only those
droplets with speific tags will be printed. Since I wanted the ability
of including price summaries, I have included prices summaries.

::

   usage: pydrop dropinfo [-h] [--tag TAG]

   optional arguments:
     -h, --help  show this help message and exit

   Optional named arguments:
     --tag TAG   Use a tag to refine your search

Droplets Delete
~~~~~~~~~~~~~~~

This deletes a droplet and you can specify either the droplet name or
id. Incase you don’t remember the name or id, just run the tool without
any arguments and it will list out all droplet id(s) and names.

::

   usage: pydrop dropdelete [-h] [--id ID] [--name NAME]

   optional arguments:
     -h, --help   show this help message and exit

   Optional named arguments:
     --id ID      Use an image ID to delete droplet
     --name NAME  Use an image name to delete droplet

Droplets Action
~~~~~~~~~~~~~~~

The droplet action tool was designed to achieve and have more control
over individual droplet actions and I included actions such as shutdown,
power off, power on and rename. Just like the droplet delete tool, this
tool will print the name and id of all droplets if no arguments are
passed and you can then choose the one on which to perform the action.

::

   usage: pydrop dropaction [-h] [--id ID] [--name NAME] [--action ACTION]
                          [--rename RENAME]

   optional arguments:
     -h, --help       show this help message and exit

   Optional named arguments:
     --id ID          Use an image ID to perform action
     --name NAME      Use an image name to perform action
     --action ACTION  Action type |shutdown="graceful shutdown"|power_off="hard
                      shutdown"|power_on="power on"|rename="rename
     --rename RENAME  Incase you are renaming droplet you can provide new name
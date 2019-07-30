# Light demo processing project

This is currently a pain. The demo is written in processing.py, which uses jython and hence is python 2.7 compatible. It seems difficult to load any external python code into jython except by the 'standard' processing.py way, which is to compile any code it finds in the project directory. Therefore to run the project we must copy any dependencies into the project. 

From our own directory we have `config.py` and `utils/types.py`, note that in python 2.7 an `__init.py__` file is needed for `utils` to appear as a package. I have also copied in the pure python2 implementation of pyyaml 5.1.

This leaves some manual work to do to make sure the code in the processing project is up-to-date with changes that occur in the main directory, and with the yaml library we use.

There's also an annoyance with loading files in processing: it doesn't seem to work.
You're supposed to put data files in a `data` subdirectory and use the builtin `loadStrings` function, but this fails silently for me. You can still load files with the standard python function `open`, but you must supply an absolute path because behind the scenes processing copies some files around and runs the project from a temporary location. Annoyingly it doesn't seem to also copy the data files.

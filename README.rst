jenks
=====

A Jenkins command-line tool.

* since jenkinsapi (one of the dependencies) is only python2 compatible, jenks is currently only python2 compatible.

-------
Install
-------

There's a few ways to install jenks.

Through pip:

    pip install jenks
    pip install http://github.com/toumorokoshi/jenks/tarball/master

Through `sprinter <http://sprinter.readthedocs.org/en/latest/>`_:

    sprinter install https://raw.github.com/toumorokoshi/jenks/master/sprinter.cfg

-----
Using
-----

jenks looks for a .jenksrc file, recursively going up from the current working directory your in.

Most users are probably ok with just adding a .jenksrc to their user root.

Example .jenksrc::

    localhost: 
      url: 'http://localhost:8080/'
      jobs:
        - foo
        - bar

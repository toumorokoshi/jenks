jenks
=====

A Jenkins command-line tool

* since jenkinsapi (one of the dependencies) is only python2 compatible, jenks is currently only python2 compatible.


Example .jenksrc::

    localhost: 
      url: 'http://localhost:8080/'
      jobs:
        - foo
        - bar

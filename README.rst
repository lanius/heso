====
Heso
====

Welcome to Heso
===============
Heso is web application to share snippets and pastes with others, and an open source clone of Gist.

Getting started
===============
Heso requires git. Install it anyway::

    sudo yum install git -y

Download the source code::

     git clone git://github.com/lanius/heso.git
     cd heso

Edit buildout.cfg and change value of "host" or "port" to suit your environment::

    vi buildout.cfg

Install Heso with buildout::

    python bootstrap.py -d
    bin/buildout

Now, you can run the server::

    bin/server

License
=======
Heso is licensed under the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html).


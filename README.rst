====
Heso
====

Welcome to Heso
===============
Heso is web application to share snippets and pastes with others, and an open source clone of Gist.

Live Demo
=========
You can see Heso running at http://heso.nirvake.org/.

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

Installing on Heroku
====================
Install git and heroku gem anyway::

    sudo yum install git -y
    sudo yum install rubygems -y && sudo gem install heroku

Log in to Heroku. If you're not yet setting up your SSH keys, you have to do it::

    heroku login

Download the source code and change directory::

    git clone git://github.com/lanius/heso.git
    cd heso/src/heso

Edit setting.py and change value of "RUN_ON_HEROKU" to "True"::

    vi setting.py

Track files (heso/src/heso/\*) with git::

    git init
    git add .
    git commit -m "initial commit for Heso on Heroku"

Create a new Cedar app on Heroku and push Heso::

    heroku create --stack cedar
    git push heroku master

License
=======
Heso is licensed under the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html).

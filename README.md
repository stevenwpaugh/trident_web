# trident_web

trident_web is a django based framework for bioinformatics anaylsis packages

To use trident_web, clone the repo and then

Copy ple/local_settings.py.example to ple/local_settings.py

Edit ple/local_settings.py to appropriate values

The run:

    python manage.py collectstatic

    python manage.py syncdb

    python manage.py testserver

knyhar
=======
Knyhar online library demo

PROJECT STRUCTURE
-------------

	knyhar
	├── docs						# Documentation
	│   └── uml						# UML diagrams
	├── knyhar
	│   ├── api						# Endpoints implementation
	│   ├── database			    # Database 
	│   ├── migrations			    # Alembic migrations
	│   │   └── versions
	│   └── models					# SQLAlchemy and Pydantic Models
	└── tests
	    ├── api						# API tests
	    ├── database				# Database tests
	    └── mocks				 
	        └── database		    # Database mocks object

INSTALLING
------------
As for now, knyhar can't be installed and should be ran from virtual environment as python module.
To build virtual environment use Makefile in the root of the project:
```
$ make venv
```
To run tests, just use special target:
```
$ make tests
```
USAGE
-----
After creating virtual environment, you should setup some settings. It can be down either by altering
settings.py file, or by setting up environment variables. You should definitely change database settings and
application secret key. For example:
```bash
# Database credentials
export KNYHAR_DB_USERNAME = admin
export KNYHAR_DB_PASSWORD = admin

# Application secret key
export KNYHAR_SECRET_KEY = dev
```

This is just an example configuration. Full list of settings with description can be seen in settings.py file. When using environment variables, every setting from settings.py should be prepended with **knyhar_** prefix.

After changing settings, application can be run as python package (be sure you are using virtual environment):
```
$ python3 -m knyhar.knyhar
```

License
-------
knyhar is available under [GNU General Public License v2.0](https://github.com/reallygoodnickname/knyhar/blob/dev/LICENSE).

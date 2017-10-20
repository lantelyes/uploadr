## Uploadr

This is a completed code challenge for Atrium LTS engineering

## Features
* Initial gate authentication
* File upload and download
* File search using name and contents
* File type detection
* File description save and edit
* Scan for new files on startup

## Prerequisites

* Python 2.7
* Virtualenv
* MongoDB running on system
* Textract dependencies, please see https://textract.readthedocs.io/en/stable/installation.html

## Instructions

In order to run Uploadr, follow the following steps:

Clone the repository and enter the directory
```
git clone https://github.com/lantelyes/uploadr.git
cd uploadr
```

Create a pyhton virtualenv and activate it
```
virtualenv env
source env/bin/activate
```

Install the python dependencies required
```
pip install -r requirements.txt
```

Finally, run the server!
```
python server.py
```

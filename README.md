# Uploadr

Uploadr is a simple file storage server.
it is a completed code challenge for Atrium LTS engineering.

## Usage Notes:
### Platform
This has only been tested on Mac OSX 10.12 and python 2.7

### Authentication

The default login information is:
```
Username: atrium
Password: atrium
```


### Known Bugs
* The client will sometimes send a junk request after an upload attempt
* The message for no files found is sometimes incorrect


## Features
* Initial gate authentication
* File list
* File upload and download
* File search using name and contents
* File type detection
* File description save and edit
* Scan for new files on startup


## Installation

### Prerequisites

* Python 2.7
* Virtualenv
* MongoDB running on system
* Textract dependencies, please see https://textract.readthedocs.io/en/stable/installation.html

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

Run the server
```
python server.py
```

## Production-ready Steps

In order to make Uploadr a production ready application the following steps would need to be completed:

* User data would be encrypted and stored in a database rather than the code itself
* Unit tests would be written to test application functionality
* A Continuous Integration system would need to be implemented
* The client and backend would ideally be split into their own repositories and ran independently from each other
* Deployment procedures would need to be created

## Postmortem

I had a lot of fun completing this challenge! However, there were some things I didn't get to implement due to time constraints that I wish I could have, they are:

* Login page
* Multiple users
* File list sorting based different properties on name/date etc
* File list pagination with configurable number of items per page
* Do more polish and cleanup of the UI
* More robust error handling for both the client and backend
* Full folder synchronization with server directory and database, not just new files, deleted ones also
* Server directory poller do check for new/deleted files
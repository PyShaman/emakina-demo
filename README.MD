# Emakina Demo with Accessibility and Security Testing
_User guide_


**List of contents**

**1. Python version and installation**

**2. Installing required packages and tools**

**3. Usage**

**4. Output**


_1. Python version and installation_

Tests are written in Python 3.8+ and it should be ran on this version or higher.
User can download newest version of Python at [Python download site](https://www.python.org/downloads/).

Install [PIP](https://pypi.org/project/pip/).

_2. Installing required packages and tools_

After cloning [Emakina-demo](https://github.com/PyShaman/emakina-demo.git) repository locally user should enter 
emakina-demo folder and create separate virtual environment for this project by using following command:
```
$ python -m venv venv
```
Python will create new directory called venv and install there basic packages. Next step is to activate virtual environment:
```
$ ./venv/Scripts/Activate.ps1
```
for Windows systems or
```
$ ./venv/Scripts/activate
```
for Linux.
When virtual environment will be activated the user will see additional mark at console:
```
(venv) path\emakina-demo >
```
Next step is to install required packages using following command:
```
$ pip3 install -r requirements.txt
```

This will automatically download and install all necessary packages.

_3. Usage:_

To run all tests use following command:
```
$ python runner.py
```

_4. Output:_

The tests will perform WCAG 2A, WCAG 2AA, full accessibility scan and finally vulnerability scan of the websites.
Results of accessibility will be kept in results folder. After scanning the tests will zip a11y output files and post a ticket
to JIRA instance with zip files as attachments. Vulnerability scan will create scan report in html form and will be attached 
to newly created JIRA ticket automatically.
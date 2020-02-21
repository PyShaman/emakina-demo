Usage:

- Install Python 3.8+ (add Python to path - there will be checkbox during installation)
- Clone this repository
- Create new virtual environment: 
>python -m venv venv
- Activate virtual environment: 
>./venv/Scripts/Activate.ps1 (on Windows)

or 
>./venv/Scripts/activate (on MacOS or Linux)
- In the repository directory run in command prompt: 
>pip install -r requirements.txt
- To run test_01_check_accessibility_wcag_only.py or test_02_check_accessibility_all.py type in console: 

>pytest -v test_01_check_accessibility_wcag_only.py 

or 
>pytest -v test_02_check_accessibility_all.py

- To run test_03_check_vulnerabilities.py type in console:
> python -m unittest discover

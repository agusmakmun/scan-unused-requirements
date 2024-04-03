# scan-unused-requirements

Python tool to scan all unused packages in requirements.txt file for your project.

## Background

One popular tool for checking requirements in a Python project is `pipdeptree`. However, the problem arises when we don't know which packages listed in the `requirements.txt` file are actually being used in the project or not. It's easy to check if your project is small, but as your project grows larger, it becomes a headache to check one by one.

So, this tool comes in handy for easily identifying which exact packages are actually unused in our project.


> **Note:** Don't forget to double cross-check after finding the unused packages, \
> because sometimes they are used in different cases without being imported in the code. \
> For example: `argon2-cffi` used in `settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher", ...]` for Django.


## Usage

```bash
(env-myproject) ➜  myproject git:(development) ✗ python scan.py -r requirements.txt -p .

[i] Please wait! It may take few minutes to complete...
[i] Scanning unused packages:
 1. rcssmin
 2. argon2-cffi
 3. flower
 4. django-model-utils
 5. pinax-theme-bootstrap
 6. phonenumbers
```

Cool right? 😎

```bash
(env-myproject) ➜  scan-unused-requirements git:(master) ✗ python scan.py --help
usage: scan.py [-h] [-r REQUIREMENTS] [-p PATH]

Scan for unused Python packages.

optional arguments:
  -h, --help            show this help message and exit
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path to the requirements.txt file to read packages from.
  -p PATH, --path PATH  Project path to scan for unused packages (default: current directory).
```


## ToDo List

- [x] Support sys argv (command arguments)
   - [x] Directory to scan
   - [x] Requirement file to scan
- [ ] Auto replace the package from requirements.txt file
- [ ] Support multiple python versions
- [ ] Make it as a command by adding file to /bin
- [ ] Support multiple devices (Linux, Macbook, and Windows)
- [ ] Write some tests
- [ ] Publish to PyPi

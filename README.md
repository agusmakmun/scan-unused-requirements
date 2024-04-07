# ScanReq

[![PyPI - Version](https://img.shields.io/pypi/v/scanreq.svg)](https://pypi.org/project/scanreq)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scanreq.svg)](https://pypi.org/project/scanreq)
[![Build Status](https://img.shields.io/github/actions/workflow/status/agusmakmun/scan-unused-requirements/run-tests.yml?branch=master)](https://github.com/agusmakmun/scan-unused-requirements/actions/workflows/run-tests.yml)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**ScanReq** - Python tool to scan all unused packages in requirements.txt file for your project.

## Background

One popular tool for checking requirements in a Python project is `pipdeptree`. However, the problem arises when we don't know which packages listed in the `requirements.txt` file are actually being used in the project or not. It's easy to check if your project is small, but as your project grows larger, it becomes a headache to check one by one.

So, this tool comes in handy for easily identifying which exact packages are actually unused in our project.

### Benefits

1. **Save Money**: Remove unused dependencies to lower hosting costs.
2. **Speed Up**: Faster installation and build times mean quicker development.
3. **Use Resources Wisely**: Free up disk and memory space by removing what you don't use.
4. **Easier Maintenance**: Keep your project cleaner and simpler for easier management.
5. **Focus Better**: Work with only what you need, enhancing productivity.
6. **Update Efficiently**: Ensure your dependencies are up-to-date for smoother compatibility.
7. **Stay Safe**: Reduce the chance of security vulnerabilities by trimming unnecessary dependencies.
8. **Stay Legal**: Avoid licensing issues by managing dependencies more effectively.
9. **Work Together**: Simplify collaboration with a consistent set of dependencies.
10. **Code Better**: Keep your documentation and codebase cleaner for improved quality.


## Installation


```console
pip3 install scanreq
```


## Usage

> **Note:** Ensure you're working on python environment & already installed all your project requirements.txt

```console
scanreq -r requirements.txt -p . -o unused-requirements.txt -i black,flake8
```

```
[i] Please wait! It may take few minutes to complete...
[i] Scanning unused packages:
 1.  Module: rcssmin                       -> Package: rcssmin
 2.  Module: model_utils                   -> Package: django-model-utils
 3.  Module: pinax_theme_bootstrap         -> Package: pinax-theme-bootstrap
 4.  Module: phonenumbers                  -> Package: phonenumbers
```

```console
cat unused-requirements.txt
```

```
rcssmin
django-model-utils
pinax-theme-bootstrap
phonenumbers
```

Cool right? 😎

```console
scanreq --help
```

```
usage: scanreq [-h] [-r REQUIREMENTS] [-p PATH] [-o OUTPUT] [-i IGNORED_PACKAGES]

Scan for unused Python packages.

optional arguments:
  -h, --help            show this help message and exit
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path to the requirements.txt file to read packages from.
  -p PATH, --path PATH  Project path to scan for unused packages (default: current directory).
  -o OUTPUT, --output OUTPUT
                        Path to the output file where unused packages will be saved.
  -i IGNORED_PACKAGES, --ignored-packages IGNORED_PACKAGES
                        Comma separated list of package names to be ignored.
```

> **Note:** Don't forget to cross-check the unused packages after finding them,
> because sometimes they are used in different cases without being imported in the code.
> For example: `argon2-cffi` used in `settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher", ...]` for Django.


## ToDo List

- [x] Support argument parser (command arguments)
   - [x] Directory to scan
   - [x] Requirement file to scan
   - [x] Option to write the output of unused packages
   - [x] Option to exclude or ignore some packages
   - [ ] Option to auto replace the package from requirements.txt file
- [x] Support CLI - make it as a command
- [x] Write some tests
- [x] Publish to PyPi
- [x] Support multiple python versions
- [x] Support multiple devices (Linux, Macbook, and Windows)
- [ ] Support scan the `pyproject.toml`

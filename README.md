# ScanReq

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

> **Note:** Don't forget to cross-check the unused packages after finding them,
> because sometimes they are used in different cases without being imported in the code.
> For example: `argon2-cffi` used in `settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher", ...]` for Django.


## ToDo List

- [x] Support argument parser (command arguments)
   - [x] Directory to scan
   - [x] Requirement file to scan
   - [ ] Option to auto replace the package from requirements.txt file
   - [ ] Option to exclude or ignore some packages
- [ ] Support multiple python versions
- [ ] Support CLI - make it as a command
- [ ] Support multiple devices (Linux, Macbook, and Windows)
- [ ] Write some tests
- [ ] Publish to PyPi
- [ ] Support scan the `pyproject.toml`

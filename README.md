# scan-unused-requirements

Python tool to scan all unused requirements in your project

```bash
(env-myproject) ➜  myproject git:(development) ✗ python scan.py -r requirements.txt -p .

[i] Please wait! It may take few minutes to complete...
[+] Scanning unused packages:
 1. rcssmin
 2. argon2-cffi
 3. flower
 4. django-model-utils
 5. pinax-theme-bootstrap
 6. phonenumbers
```

Cool hah? 😎



# ToDo List

- [x] Support sys argv (command arguments)
      - [x] Directory to scan
      - [x] Requirement file to scan
- [ ] Auto replace the package from requirements.txt file
- [ ] Support multiple python versions
- [ ] Make it as a command by adding file to /bin
- [ ] Support multiple devices (Linux, Macbook, and Windows)
- [ ] Write some tests
- [ ] Publish to PyPi

### 1. Installation

Modern, extensible Python project management using Hatch:
https://hatch.pypa.io/latest/install/

```console
$ pip3 install hatch
```

> Ensure were working on environment.

Just for knowledge how this project generated using `hatch new {project_name}`:

```
$ hatch new scanreq
```

### 2. Testing

```console
$ hatch run test -vv
```

Executing the script:

```console
$ hatch run python src/scanreq/__main__.py -r requirements.txt -p .
```


### 3. Versioning

https://hatch.pypa.io/latest/version/#updating

**To check the current version:**

```console
$ hatch version
0.0.1
```

**To tag new release:**

```console
$ hatch version "0.1.0"
Old: 0.0.1
New: 0.1.0
```

**Release micro version:**

```console
$ hatch version micro
Old: 0.0.1
New: 0.0.2
```


### 4. Building

https://hatch.pypa.io/latest/build/

```console
$ hatch build
[sdist]
dist/hatch_demo-1rc0.tar.gz

[wheel]
dist/hatch_demo-1rc0-py3-none-any.whl
```


### 5. Publishing

https://hatch.pypa.io/latest/publish/

Ensure we already setup the api token:
https://pypi.org/help/#apitoken

To make it easy, you can save inside `~/.pypirc` file:

```console
➜  ~ cat .pypirc
[pypi]
  username = __token__
  password = pypi-XXXXX
```


For the first time, `hatch` will require user to fill above PyPi token,
but it will be caching for the next publishments:

```console
$ hatch publish

Enter your username [__token__]:
Enter your credentials:
dist/scanreq-0.0.1.tar.gz ... success
dist/scanreq-0.0.1-py3-none-any.whl ... success

[scanreq]
https://pypi.org/project/scanreq/0.0.1/
```

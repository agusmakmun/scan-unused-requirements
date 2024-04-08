import multiprocessing
import os
import re
from typing import Any, List, Optional, Tuple

import importlib_metadata

"""
Logic:
1. Search the installed packages distributions
   {"module_name": ["folder-name"], ...}
   - Process only the "valid main packages"
2. Iterate the "packages name" in requirements.txt file
   - Check if any of the "packages name" is in the "valid main packages"
   - If yes, scan to check if their "module_name" if it used in the project or not.
     - If not, then print the "packages name".
"""

# allowed extensions to scan
DEFAULT_ALLOWED_EXTENSIONS: Tuple[str, ...] = (
    ".py",
    ".conf",
    ".cfg",
    ".yml",
    ".yaml",
    "Dockerfile",
)

# default ignored packages to scan
DEFAULT_IGNORED_PACKAGES: List[str] = [
    "scanreq",
    "ipdb",
    "mypy",
    "isort",
    "black",
    "flake8",
    "twine",
    "codespell",
    "django-coverage-plugin",
    "pytest-sugar",
    "pytest-cov",
    "pytest-asyncio",
    "pytest-mock",
    "pytest-subtests",
    "pytest-xdist",
    "pylint-django",
    "pylint-celery",
    "pytest-django",
    "pre-commit",
]


def get_main_packages() -> dict:
    """
    Get the main packages available in the distribution.

    Returns:
        dict: A dictionary where keys are module names
              and values are corresponding package names.
        {"module_name": ["folder-name"], ...}
    """
    packages = importlib_metadata.packages_distributions()
    excluded_packages: List[str] = [
        "-",  # exclude invalid package
        "/",  # exclude subfolders
        "__mypyc",  # exclude pyc files
    ]
    main_packages: dict = {}
    for module_name, package_names in packages.items():
        if (
            not any(exclude in module_name for exclude in excluded_packages)
            and not module_name.startswith("_")
            and package_names
            and isinstance(package_names, list)
        ):
            main_packages[module_name] = package_names
    return main_packages


def search_string_in_file(file_path: str, search_string: str) -> Optional[str]:
    """
    A function that searches for a specific string in a file.

    Parameters:
    - file_path: a string representing the path to the file to be searched
    - search_string: a string to search for within the file

    Returns:
    - str: the file_path if the search_string is found in the file, otherwise None
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            if search_string in file.read():
                return file_path
    except UnicodeDecodeError:
        # Handle cases where the file can't be decoded with utf-8
        pass
    except Exception as e:
        print(f"Error occurred while reading {file_path}: {e}")
    return None


def search_string_in_files(directory: str, search_string: str) -> List[str]:
    """
    Search for a specific string within files in a given directory using multiprocessing.

    Args:
        directory (str): The directory path to search for files.
        search_string (str): The string to search for within the files.

    Returns:
        List[str]: A list of file paths where the search_string was found.
    """
    found_files: List[Any] = []
    pool = multiprocessing.Pool()
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(DEFAULT_ALLOWED_EXTENSIONS):
                file_path = os.path.join(root, file_name)
                found_file = pool.apply_async(
                    search_string_in_file, (file_path, search_string)
                )
                found_files.append(found_file)
    pool.close()
    pool.join()
    return [result.get() for result in found_files if result.get()]


def clean_package_name(package_name: str) -> str:
    """
    Clean the package name by removing any version number and extra spaces, and converting to lowercase.
    For example:
    - "django==3.2" -> "django", "Django==3.2" -> "django"
    - "Flask>=1.0" -> "flask", "Flask<=1.0" -> "flask"
    - "django-cookie-cutter<2.0" -> "django-cookie-cutter"
    - "django-cookie-cutter>2.0" -> "django-cookie-cutter"
    - "NumPy" -> "numpy"

    Args:
        package_name (str): The name of the package.

    Returns:
        str: The cleaned package name.
    """
    # Remove the version number and any relational operators
    cleaned_name = re.sub(r"[<=>!]=?\d+(\.\d+)*", "", package_name)
    # Replace any hyphens followed by non-alphanumeric characters (like hyphen version separator)
    cleaned_name = re.sub(r"-[^a-zA-Z0-9]", "", cleaned_name)
    # Remove any remaining non-alphanumeric characters except hyphens and underscores
    cleaned_name = re.sub(r"[^a-zA-Z0-9-_]", "", cleaned_name)
    # Convert to lowercase and strip extra spaces
    return cleaned_name.strip().lower()


def read_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements from the specified file and returns a list of package names.
    For example: ["django", "django-cors-headers"]

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        List[str]: A list of package names extracted from the requirements file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    package_names: List[str] = []
    with open(file_path) as file:
        for line in file:
            # Remove comments and leading/trailing whitespaces
            line = re.sub(r"#.*", "", line).strip()
            if line:
                # Split the line to get the package name
                package_name: str = clean_package_name(line)
                package_names.append(package_name)
    return package_names


def scan(
    requirement_file: str,
    project_path: str,
    output_path: Optional[str] = None,
    ignored_packages: List[str] = [],
) -> None:
    """
    A function that scans for unused packages in a project based on a given requirements file.

    Parameters:
        - requirement_file (str): the path to the requirements file to be scanned.
        - project_path (str): the path to the project to be scanned.
        - output_path (str, optional): the path to the output file where unused packages will be saved. Defaults to None.
        - ignored_packages (List[str], optional): a list of package names to be ignored. Defaults to [].

    Returns:
        - None
    """
    print("\n[i] Please wait! It may take few minutes to complete...")

    package_names: List[str] = read_requirements(requirement_file)
    main_packages: dict = get_main_packages()

    # ignored packages to scan
    ignored_packages = (
        DEFAULT_IGNORED_PACKAGES + [clean_package_name(pkg) for pkg in ignored_packages]
        if ignored_packages
        else DEFAULT_IGNORED_PACKAGES
    )

    print("[i] Scanning unused packages:")
    unused_packages: List[str] = []
    number: int = 1
    for package_name in package_names:
        for module_name, main_package_names in main_packages.items():
            if (
                package_name in main_package_names
                and package_name not in ignored_packages
            ):
                results: list = search_string_in_files(project_path, module_name)
                if not results and (module_name not in unused_packages):
                    unused_packages.append(package_name)
                    number_str: str = f"{number}."
                    print(
                        f" {number_str: <4}Module: {module_name: <30}-> Package: {package_name}"
                    )
                    number += 1

    unused_packages = list(set(unused_packages))
    if len(unused_packages) < 1:
        print("[i] Great! No unused packages found.")

    elif unused_packages and output_path:
        with open(output_path, "w") as _file:
            _file.writelines("\n".join(unused_packages) + "\n")

import argparse
from typing import List

from scanreq.scanner import (
    get_main_packages,
    read_requirements,
    search_string_in_python_files,
)


def main():
    parser = argparse.ArgumentParser(description="Scan for unused Python packages.")
    parser.add_argument(
        "-r",
        "--requirements",
        type=str,
        default="requirements.txt",
        help="Path to the requirements.txt file to read packages from.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=".",
        help="Project path to scan for unused packages (default: current directory).",
    )
    args = parser.parse_args()
    project_path: str = args.path
    requirement_file: str = args.requirements

    print("\n[i] Please wait! It may take few minutes to complete...")

    main_packages: dict = get_main_packages()
    package_names: List[str] = read_requirements(requirement_file)

    print("[i] Scanning unused packages:")
    unused_packages: List[str] = []
    number: int = 1
    for package_name in package_names:
        for module_name, package_names in main_packages.items():
            if package_name in package_names:
                results: list = search_string_in_python_files(project_path, module_name)
                if not results and (module_name not in unused_packages):
                    unused_packages.append(package_name)
                    print(
                        f" {number}. Module: {module_name} ---> Package: {package_name}"
                    )
                    number += 1

    if len(unused_packages) < 1:
        print("[i] Great! No unused packages found.")
    return unused_packages


if __name__ == "__main__":
    main()

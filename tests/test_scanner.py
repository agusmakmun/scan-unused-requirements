import os
from unittest import mock

import pytest

from src.scanreq.scanner import (
    clean_package_name,
    get_main_packages,
    read_requirements,
    search_string_in_file,
    search_string_in_python_files,
)


def test_get_main_packages():
    # Mock the importlib_metadata.packages_distributions to return known values
    expected_packages: dict = {
        "valid_package": ["folder-name"],
        "valid2": ["folder-name2"],
        "_private_package": ["should-not-include"],
        "package-with-dash": ["should-not-include"],
        "package/with-slash": ["should-not-include"],
        "package__mypyc": ["should-not-include"],
    }

    with mock.patch(
        "importlib_metadata.packages_distributions", return_value=expected_packages
    ):
        result = get_main_packages()
        assert result == {"valid_package": ["folder-name"], "valid2": ["folder-name2"]}


# Assuming the existence of a fixture that provides a temporary directory
@pytest.fixture
def temp_file(tmpdir):
    file = tmpdir.join("test_file.py")
    file.write("# This is a test file for search_string_in_file function\n")
    return str(file)


def test_search_string_in_file_found(temp_file):
    search_string = "search_string_in_file"
    result = search_string_in_file(temp_file, search_string)
    assert result == temp_file, "The search string should be found in the file"


def test_search_string_in_file_not_found(temp_file):
    search_string = "non_existent_string"
    result = search_string_in_file(temp_file, search_string)
    assert result is None, "The search string should not be found in the file"


def test_search_string_in_file_unicode_error(temp_file):
    # Write non-utf-8 content to the file to trigger UnicodeDecodeError
    with open(temp_file, "wb") as file:
        file.write(b"\x80abc")
    result = search_string_in_file(temp_file, "abc")
    assert result is None, "UnicodeDecodeError should be handled gracefully"


def test_search_string_in_file_general_exception(temp_file, capsys):
    # Simulate an exception by providing an invalid file path
    invalid_file_path = temp_file + "_invalid"
    result = search_string_in_file(invalid_file_path, "test")
    captured = capsys.readouterr()
    assert (
        "Error occurred while reading" in captured.out
    ), "General exceptions should be handled and logged"
    assert result is None, "General exceptions should result in None"


@pytest.fixture
def create_test_files(tmp_path):
    sub_dir = tmp_path / "test_dir"
    sub_dir.mkdir()
    (sub_dir / "test1.py").write_text("print('Hello, world!')")
    (sub_dir / "test2.py").write_text("def foo():\n    return 'bar'")
    (sub_dir / "non_python.txt").write_text("This is not a Python file.")
    return sub_dir


def test_search_string_in_python_files(create_test_files):
    directory = str(create_test_files)
    search_string = "foo"
    expected_file = os.path.join(directory, "test2.py")

    found_files = search_string_in_python_files(directory, search_string)
    assert expected_file in found_files
    assert len(found_files) == 1


@pytest.mark.parametrize(
    "package_name, expected",
    [
        ("django==3.2", "django"),
        (" Django==3.2 ", "django"),
        ("Flask>=1.0", "flask"),
        ("requests", "requests"),
        (" NumPy ", "numpy"),
        ("django-cookie-cutter>2.0", "django-cookie-cutter"),
        ("django-cookie-cutter<2.0", "django-cookie-cutter"),
    ],
)
def test_clean_package_name(package_name, expected):
    assert clean_package_name(package_name) == expected


def test_read_requirements_valid_file(tmp_path):
    # Create a temporary requirements file
    requirements_content = """
    Django==3.0.5
    requests==2.23.0 # A comment
    numpy
    """
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(requirements_content)

    # Call the function with the path to the created temporary file
    result = read_requirements(str(requirements_file))

    # Assert the function's output
    expected_packages = ["django", "requests", "numpy"]
    assert (
        result == expected_packages
    ), "The read_requirements function did not return expected package names."


def test_read_requirements_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_requirements("non_existent_file.txt")

from pathlib import Path

import pytest

from renamer.entry import rename_variable


@pytest.mark.parametrize(["path_to_source", "path_to_expected", "old_name", "new_name"], [
    ("tests/fixtures/rename_arg_source.py", "tests/fixtures/rename_arg_expected.py", "arg1", "new_name"),
    ("tests/fixtures/rename_arg_source.py", "tests/fixtures/rename_arg_expected.py", "arg1", "new_name"),
    ("tests/fixtures/rename_arg_source.py", "tests/fixtures/rename_arg_expected.py", "arg1", "new_name"),
    ("tests/fixtures/rename_func_source.py", "tests/fixtures/rename_func_expected.py", "my_function", "new_function"),
    ("tests/fixtures/rename_class_source.py", "tests/fixtures/rename_class_expected.py", "MyClass", "NewClass"),
])
def test_rename(path_to_source: str, path_to_expected: str, old_name: str, new_name: str) -> None:
    got = rename_variable(
        Path(path_to_source).read_text(),
        old_name,
        new_name,
    )

    assert got == Path(path_to_expected).read_text()

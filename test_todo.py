from todo import seperate_flags, flag_check, collect_args, blank_check
import pytest
import sys

def test_seperate_flags():
    assert seperate_flags(["Nn"]) == ["N", "n"]
    assert seperate_flags(["new-task", "new-list"]) == ["new-task", "new-list"]
    assert seperate_flags(["NSr"]) == ["N", "S", "r"]

def test_flag_check():
    assert flag_check(["N", "n"]) == ["N", "n"]
    assert flag_check(["new-task", "new-list"]) == ["new-task", "new-list"]
    with pytest.raises(SystemExit):
        flag_check(["N", "S", "r"])
        flag_check(["delete-task", "update-list"])

def test_collect_args():
    if len(sys.argv) < 2:
        pytest.raises(SystemExit)
    else:
        collect_args() == sys.argv[1:]

def test_blank_check():
    with pytest.raises(IndexError):
        blank_check([])

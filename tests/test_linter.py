from past.past import Linter
from past.rules import (
    UnusedVariableChecker,
    SetDuplicateItemChecker,
    DictionaryDuplicateItemChecker,
)
import textwrap


def test_unused_global(capsys):
    code = textwrap.dedent(
        """\
        s = {1, 2}  # Unused global
        l = [1, 2, 3]
        print(l)
        """
    )
    linter = Linter()
    linter.checkers.append(UnusedVariableChecker())
    linter.validate(code, "global.py")
    out = capsys.readouterr().out
    assert out == "global.py:1:0: F841: Variable 's' is assigned to but never used\n"


def test_unused_local(capsys):
    code = textwrap.dedent(
        """\
        s = 2
        def main():
            unused = 5  # Unused local
            print(s)
        """
    )
    linter = Linter()
    linter.checkers.append(UnusedVariableChecker())
    linter.validate(code, "local.py")
    out = capsys.readouterr().out
    assert (
        out == "local.py:3:4: F841: Variable 'unused' is assigned to but never used\n"
    )


def test_duplicate_set_global(capsys):
    code = textwrap.dedent(
        """\
        s = {1, 2, 2}
        """
    )
    linter = Linter()
    linter.checkers.append(SetDuplicateItemChecker())
    linter.validate(code, "dupe_global.py")
    out = capsys.readouterr().out
    assert out == "dupe_global.py:1:11: D001: Set contains duplicate item 2\n"


def test_duplicate_dict_global(capsys):
    code = textwrap.dedent(
        """\
        s = { 1: 2, 1: 3}
        """
    )
    linter = Linter()
    linter.checkers.append(DictionaryDuplicateItemChecker())
    linter.validate(code, "dupe_global.py")
    out = capsys.readouterr().out
    assert out == "dupe_global.py:1:12: D002: Dictionary contains duplicate key 1\n"


def test_unused_duplicate_set(capsys):
    code = textwrap.dedent(
        """\
        g = {1, 2, 3, 1}  # Unused, and has a duplicate
        """
    )
    linter = Linter()
    linter.checkers.append(SetDuplicateItemChecker())
    linter.checkers.append(UnusedVariableChecker())
    linter.validate(code, "unused_dupe.py")
    out = capsys.readouterr().out
    assert (
        out
        == "unused_dupe.py:1:14: D001: Set contains duplicate item 1\nunused_dupe.py:1:0: F841: Variable 'g' is assigned to but never used\n"
    )


def test_unused_duplicate_dict(capsys):
    code = textwrap.dedent(
        """\
        g = {1 : 2, 3: 4, 1 : 5}  # Unused, and has a duplicate
        """
    )
    linter = Linter()
    linter.checkers.append(DictionaryDuplicateItemChecker())
    linter.checkers.append(UnusedVariableChecker())
    linter.validate(code, "unused_dupe.py")
    out = capsys.readouterr().out
    assert (
        out
        == "unused_dupe.py:1:18: D002: Dictionary contains duplicate key 1\nunused_dupe.py:1:0: F841: Variable 'g' is assigned to but never used\n"
    )

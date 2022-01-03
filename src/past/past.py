import ast
from pathlib import Path
from typing import List, NamedTuple
import collections


class UniqueList(collections.abc.MutableSequence):
    """A list implementation that only contains unique items."""

    def __init__(self, *args):
        self.list = list()
        self.extend(list(args))

    def exists(self, v):
        if v in self.list:
            return True
        return False

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i]

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        if not self.exists(v):
            self.list[i] = v

    def insert(self, i, v):
        if not self.exists(v):
            self.list.insert(i, v)

    def __str__(self):
        return str(self.list)


class Violation(NamedTuple):
    """
    Every rule violation contains a node that breaks the rule
    and a message that will be shown to the user.
    """

    node: ast.AST
    message: str


class Checker(ast.NodeVisitor):
    """
    A Checker is a Visitor that defines a lint rule, and stores all the
    nodes that violate that lint rule.
    """

    def __init__(self, issue_code: str):
        self.issue_code: str = issue_code
        self.violations: List[Violation] = UniqueList()


class Linter:
    """Holds all linting rules and runs them against a python program."""

    def __init__(self):
        self.checkers: List[Checker] = UniqueList()

    def print_violations(self, checker: Checker, file_name: str):
        for node, message in checker.violations:
            print(
                f"{file_name}:{node.lineno}:{node.col_offset}: "
                f"{checker.issue_code}: {message}"
            )

    def validate(self, source_code: str, file_name: str):
        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, file_name)

    def run(self, source_path: str):
        """Runs all lint rules on a source file."""
        source_file = Path(source_path)

        with source_file.open() as f:
            source_code = f.read()

        self.validate(source_code, source_file.name)

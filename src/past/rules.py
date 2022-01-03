import ast
from past.past import Checker, Violation


class SetDuplicateItemChecker(Checker):
    """Checks if a set has duplicate constants."""

    def __init__(self, issue_code: str = "D001"):
        super().__init__(issue_code)

    def visit_Set(self, node: ast.Set):
        """Stores all the constants this set holds, and finds duplicates."""
        seen_constants = set()
        for element in node.elts:
            # We're only concerned about constant values
            if isinstance(element, ast.Constant):
                if element.value not in seen_constants:
                    seen_constants.add(element.value)

                else:
                    violation = Violation(
                        node=element,
                        message=f"Set contains duplicate item {element.value!r}",
                    )
                    self.violations.append(violation)


class DictionaryDuplicateItemChecker(Checker):
    """Checks if a Dictionary has duplicate keys."""

    def __init__(self, issue_code: str = "D002"):
        super().__init__(issue_code)

    def visit_Dict(self, node: ast.Dict):
        """Stores all the keys this dictionary holds, and finds duplicates."""
        seen_constants = set()
        for element in node.keys:
            if isinstance(element, ast.Constant):
                if element.value not in seen_constants:
                    seen_constants.add(element.value)

                else:
                    violation = Violation(
                        node=element,
                        message=f"Dictionary contains duplicate key {element.value!r}",
                    )
                    self.violations.append(violation)


class UnusedVariableInScopeChecker(Checker):
    """Checks if any variables are unused inside of this node's scope."""

    def __init__(self, issue_code):
        super().__init__(issue_code)
        self.unused_names = {}
        self.name_nodes = {}

    def visit_Name(self, node: ast.Name):
        """Find all nodes that only exist in `Store` context"""
        var_name = node.id

        if isinstance(node.ctx, ast.Store):
            # If it's a new name, save the node for later
            if var_name not in self.name_nodes:
                self.name_nodes[var_name] = node

            # If we've never seen it before, it is unused.
            if var_name not in self.unused_names:
                self.unused_names[var_name] = True

        else:
            # Name is used somewhere because the node type is not Store.
            self.unused_names[var_name] = False


class UnusedVariableChecker(Checker):
    """Checks if any variables are unused."""

    def __init__(self, issue_code: str = "F841"):
        super().__init__(issue_code)

    def check_for_unused_variables(self, node):
        """Find unused variables in the local scope of this node."""
        visitor = UnusedVariableInScopeChecker(self.issue_code)
        visitor.visit(node)

        for name, unused in visitor.unused_names.items():
            if unused:
                node = visitor.name_nodes[name]
                violation = Violation(
                    node, f"Variable {name!r} is assigned to but never used"
                )
                self.violations.append(violation)

    def visit_Module(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_ClassDef(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)

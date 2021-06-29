# -*- coding: utf-8 -*-
# Copyright 2021 Damien Nguyen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main file for the flake8_secure_coding_standard plugin"""

import ast
import sys

from typing import Any, Dict, Generator, List, Tuple, Type

if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata  # pylint: disable=E0401

    ast_Constant = ast.NameConstant
else:  # pragma: no cover (PY38+)
    ast_Constant = ast.Constant
    import importlib.metadata as importlib_metadata

# ==============================================================================

SCS100 = (
    'SCS100 use of os.path.abspath() and os.path.relpath() should be avoided in favor of ' + 'os.path.realpath()'
)  # noqa: E501
SCS101 = 'SCS101 `eval()` and `exec()` represent a security risk and should be avoided'  # noqa: E501
SCS102 = 'SCS102 use of `os.system()` should be avoided'  # noqa: E501
SCS103 = 'SCS103 use of `shell=True` in subprocess functions should be avoided'  # noqa: E501
SCS104 = 'SCS104 use of `tempfile.mktemp()` should be avoided, prefer `tempfile.mkstemp()`'  # noqa: E501
SCS105 = (
    'SCS105 use of `yaml.load()` should be avoided, prefer `yaml.safe_load()` or '
    + '`yaml.load(xxx, Loader=SafeLoader)`'
)  # noqa: E501
SCS106 = 'SCS106 use of `jsonpickle.decode()` should be avoided'  # noqa: E501
SCS107 = 'SCS107 debugging code shoud not be present in production code (e.g. `import pdb`)'  # noqa: E501
SCS108 = 'SCS108 `assert` statements should not be present in production code'  # noqa: E501
SCS109 = (
    'SCS109 Use of builtin `open` for writing is discouraged in favor of `os.open` '
    + 'to allow for setting file permissions'
)  # noqa: E501


def _is_os_system_call(node: ast.Call) -> bool:
    return (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == 'os'
        and node.func.attr == 'system'
    )


def _is_os_path_call(node: ast.Call) -> bool:
    return (
        isinstance(node.func, ast.Attribute)  # pylint: disable=R0916
        and (
            (isinstance(node.func.value, ast.Name) and node.func.value.id == 'op')
            or (
                isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == 'path'
                and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == 'os'
            )
        )
        and node.func.attr in ('abspath', 'relpath')
    )


def _is_builtin_open_for_writing(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Name) and node.func.id == 'open':
        mode = ''
        if len(node.args) > 1:
            if isinstance(node.args[1], ast.Name):
                return True  # variable -> to be on the safe side, flag as inappropriate
            if isinstance(node.args[1], ast_Constant):
                mode = node.args[1].value
            if isinstance(node.args[1], ast.Str):
                mode = node.args[1].s
        else:
            for keyword in node.keywords:
                if keyword.arg == 'mode':
                    if not isinstance(keyword.value, ast_Constant):
                        return True  # variable -> to be on the safe side, flag as inappropriate
                    mode = keyword.value.value
                    break
        if any(m in mode for m in 'awx'):
            # open(..., "w")
            # open(..., "wb")
            # open(..., "a")
            # open(..., "x")
            return True
    return False


def _is_subprocess_shell_true_call(node: ast.Call) -> bool:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in ('subprocess', 'sp')
    ):
        for keyword in node.keywords:
            if keyword.arg == 'shell' and isinstance(keyword.value, ast_Constant) and bool(keyword.value.value):
                return True

        if len(node.args) > 8 and isinstance(node.args[8], ast_Constant) and bool(node.args[8].value):
            return True
    return False


def _is_pdb_call(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Attribute):
        if isinstance(node.func.value, ast.Name) and node.func.value.id == 'pdb':
            # pdb.func()
            return True
    if isinstance(node.func, ast.Name):
        if node.func.id == 'Pdb':
            # Pdb()
            return True
    return False


def _is_mktemp_call(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Attribute):
        if node.func.attr == 'mktemp':
            # tempfile.mktemp()
            # xxxx.mktemp()
            return True
    if isinstance(node.func, ast.Name):
        if node.func.id == 'mktemp':
            # mktemp()
            return True
    return False


def _is_yaml_unsafe_call(node: ast.Call) -> bool:
    _safe_loaders = ('BaseLoader', 'SafeLoader')
    _unsafe_loaders = ('Loader', 'UnsafeLoader', 'FullLoader')
    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'yaml':
        if node.func.attr in ('unsafe_load', 'full_load'):
            # yaml.full_load()
            # yaml.unsafe_load()
            return True
        if node.func.attr == 'load':
            for keyword in node.keywords:
                if keyword.arg == 'Loader' and isinstance(keyword.value, ast.Name):
                    if keyword.value.id in _unsafe_loaders:
                        # yaml.load(x, Loader=Loader), yaml.load(x, Loader=UnsafeLoader),
                        # yaml.load(x, Loader=FullLoader)
                        return True
                    if keyword.value.id in _safe_loaders:
                        # yaml.load(x, Loader=BaseLoader), yaml.load(x, Loader=SafeLoader),
                        return False

            if len(node.args) < 2 or (node.args[1].id in _unsafe_loaders):
                # yaml.load(x)
                # yaml.load(x, Loader), yaml.load(x, UnsafeLoader), yaml.load(x, FullLoader)
                return True

    if isinstance(node.func, ast.Name):
        if node.func.id in ('unsafe_load', 'full_load'):
            # unsafe_load()
            # full_load()
            return True
    return False


def _is_jsonpickle_encode_call(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Attribute):
        if isinstance(node.func.value, ast.Name) and node.func.value.id == 'jsonpickle' and node.func.attr == 'decode':
            return True
    return False


class Visitor(ast.NodeVisitor):
    """AST visitor class for the plugin"""

    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []
        self._from_imports: Dict[str, str] = {}

    def visit_Call(self, node: ast.Call) -> None:
        """
        Visitor method called for ast.Call nodes
        """
        if _is_pdb_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS107))
        elif _is_mktemp_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS104))
        elif _is_yaml_unsafe_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS105))
        elif _is_jsonpickle_encode_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS106))
        elif _is_os_system_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS102))
        elif _is_os_path_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS100))
        elif _is_subprocess_shell_true_call(node):
            self.errors.append((node.lineno, node.col_offset, SCS103))
        elif _is_builtin_open_for_writing(node):
            self.errors.append((node.lineno, node.col_offset, SCS109))
        elif isinstance(node.func, ast.Name) and (node.func.id in ('eval', 'exec')):
            self.errors.append((node.lineno, node.col_offset, SCS101))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """
        Visitor method called for ast.Import nodes
        """
        for alias in node.names:
            if alias.name == 'pdb':
                # import pdb
                # import pdb as xxx
                self.errors.append((node.lineno, node.col_offset, SCS107))

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Visitor method called for ast.ImportFrom nodes
        """
        for alias in node.names:
            if (node.module is None and alias.name == 'pdb') or node.module == 'pdb':
                # from pdb import xxx
                self.errors.append((node.lineno, node.col_offset, SCS107))
            elif node.module == 'tempfile' and alias.name == 'mktemp':
                # from tempfile import mktemp
                self.errors.append((node.lineno, node.col_offset, SCS104))
            elif node.module in ('os.path', 'op') and alias.name in ('relpath', 'abspath'):
                # from os.path import relpath, abspath
                # import os.path as op; from op import relpath, abspath
                self.errors.append((node.lineno, node.col_offset, SCS100))
            elif node.module == 'os' and alias.name == 'system':
                # from os import system
                self.errors.append((node.lineno, node.col_offset, SCS102))

        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        """
        Visitor method called for ast.With nodes
        """
        for item in node.items:
            if isinstance(item.context_expr, ast.Call) and _is_builtin_open_for_writing(item.context_expr):
                self.errors.append((node.lineno, node.col_offset, SCS109))

    def visit_Assert(self, node: ast.Assert) -> None:
        """
        Visitor method called for ast.Assert nodes
        """
        self.errors.append((node.lineno, node.col_offset, SCS108))
        self.generic_visit(node)


class Plugin:  # pylint: disable=R0903
    """Plugin class"""

    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """
        Function entry point from flake8
        """
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)

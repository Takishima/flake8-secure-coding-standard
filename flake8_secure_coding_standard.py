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

import ast
import sys

from typing import Any, Dict, Generator, List, Tuple, Type

if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    import importlib.metadata as importlib_metadata

# ==============================================================================

SCS100 = (
    'SCS100 use of os.path.abspath() and os.path.relpath() should be avoided in favor of os.path.realpath()',
)  # noqa: E501
SCS101 = 'SCS101 eval() and exec() can represent a security risk and should be avoided'  # noqa: E501
SCS102 = 'SCS102 use of os.system() should be avoided'  # noqa: E501
SCS103 = 'SCS103 use of shell=True in subprocess functions should be avoided'  # noqa: E501
SCS104 = 'SCS104 use of tempfile.mktemp() should be avoided'  # noqa: E501
SCS105 = 'SCS105 use of yaml.load() should be avoided'  # noqa: E501
SCS106 = 'SCS106 use of jsonpickle.decode() should be avoided'  # noqa: E501
SCS107 = 'SCS107 debugging code shoud not be present in production code'  # noqa: E501
SCS108 = 'SCS108 assert statement should not be present in production code'  # noqa: E501


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []
        self._from_imports: Dict[str, str] = {}

    def visit_Call(self, node: ast.Call) -> None:
        # if node.id == 'PY3' and self._from_imports.get(node.id) == 'six':
        #     self.errors.append((node.lineno, node.col_offset, SCS100))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)

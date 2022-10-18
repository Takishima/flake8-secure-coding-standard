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

import pytest

import flake8_secure_coding_standard as flake8_scs


def results(s):
    return {'{}:{}: {}'.format(*r) for r in flake8_scs.Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    's',
    (
        '',
        'int(0)',
        'foo()',
    ),
)
def test_pdb_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    's',
    (
        'import pdb',
        'import pdb, six',
        'from pdb import set_trace',
        'pdb.set_trace()',
        'pdb.post_mortem(traceback=None)',
        'pdb.Pdb(skip=["django.*"])',
        'Pdb(skip=["django.*"])',
    ),
)
def test_pdb_not_ok(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS107}

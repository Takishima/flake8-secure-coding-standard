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
        'pickle.dump(data, "file.txt")',
        'pickle.dumps(data)',
    ),
)
def test_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    's',
    (
        'pickle.load("file.txt")',
        r'pickle.loads(b"\x80\x04K\x01.")',
        'pickle.loads(data)',
        'from pickle import load',
        'from pickle import loads',
        'from pickle import dump, load',
    ),
)
def test_not_ok(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS113}

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
    ('',),
)
def test_ok(s):
    assert results(s) == set()


_not_ok = (
    'shelve.open("file.txt")',
    'shelve.open(filename)',
)


@pytest.mark.parametrize('s', _not_ok)
def test_shelve_open_call(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS115}


@pytest.mark.parametrize('s', _not_ok)
def test_shelve_open_with(s):
    assert results(f'with {s} as fd: fd.read()') == {'1:0: ' + flake8_scs.SCS115}


@pytest.mark.parametrize('s', ('from shelve import open',))
def test_shelve_open_importfrom(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS115}

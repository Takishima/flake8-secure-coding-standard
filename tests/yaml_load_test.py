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
        'yaml.safe_load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader=BaseLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader=SafeLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", BaseLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", SafeLoader)',
    ),
)
def test_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    's',
    (
        'full_load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'unsafe_load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'yaml.full_load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'yaml.unsafe_load("!!python/object/new:os.system [echo EXPLOIT!]")',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader=Loader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader=UnsafeLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader=FullLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", Loader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", UnsafeLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", FullLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", yaml.Loader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", yaml.UnsafeLoader)',
        'yaml.load("!!python/object/new:os.system [echo EXPLOIT!]", yaml.FullLoader)',
    ),
)
def test_abspath(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS105}

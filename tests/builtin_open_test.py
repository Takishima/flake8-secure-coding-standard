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
        'open("file.txt")',
        'bla.open("file.txt")',
        'bla.open("file.txt", "w")',
        'with open("file.txt") as fd: fd.read()',
        'with bla.open("file.txt") as fd: fd.read()',
        'with bla.open("file.txt", "w") as fd: fd.read()',
    ),
)
def test_builtin_open_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    's',
    (
        'open("file.txt", "w")',
        'open("file.txt", "wb")',
        'open("file.txt", "bw")',
        'open("file.txt", "a")',
        'open("file.txt", "ab")',
        'open("file.txt", "ba")',
        'open("file.txt", "x")',
        'open("file.txt", "xb")',
        'open("file.txt", "bx")',
        'open("file.txt", mode)',
        'open("file.txt", mode="w")',
        'open("file.txt", mode="wb")',
        'open("file.txt", mode="bw")',
        'open("file.txt", mode="a")',
        'open("file.txt", mode="ab")',
        'open("file.txt", mode="ba")',
        'open("file.txt", mode="x")',
        'open("file.txt", mode="xb")',
        'open("file.txt", mode="bx")',
        'open("file.txt", mode=mode)',
        'with open("file.txt", "w") as fd: fd.read()',
        'with open("file.txt", "wb") as fd: fd.read()',
        'with open("file.txt", "bw") as fd: fd.read()',
        'with open("file.txt", "a") as fd: fd.read()',
        'with open("file.txt", "ab") as fd: fd.read()',
        'with open("file.txt", "ba") as fd: fd.read()',
        'with open("file.txt", "x") as fd: fd.read()',
        'with open("file.txt", "xb") as fd: fd.read()',
        'with open("file.txt", "bx") as fd: fd.read()',
        'with open("file.txt", mode) as fd: fd.read()',
        'with open("file.txt", mode="w") as fd: fd.read()',
        'with open("file.txt", mode="wb") as fd: fd.read()',
        'with open("file.txt", mode="bw") as fd: fd.read()',
        'with open("file.txt", mode="a") as fd: fd.read()',
        'with open("file.txt", mode="ab") as fd: fd.read()',
        'with open("file.txt", mode="ba") as fd: fd.read()',
        'with open("file.txt", mode="x") as fd: fd.read()',
        'with open("file.txt", mode="xb") as fd: fd.read()',
        'with open("file.txt", mode="bx") as fd: fd.read()',
        'with open("file.txt", mode=mode) as fd: fd.read()',
    ),
)
def test_builtin_open_not_ok(s):
    assert results(s) == {'1:0: ' + flake8_scs.SCS109}

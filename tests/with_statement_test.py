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
from itertools import starmap

import flake8_secure_coding_standard as flake8_scs

import pytest


def results(s):
    return set(starmap('{}:{}: {}'.format, flake8_scs.Plugin(ast.parse(s)).run()))


@pytest.mark.parametrize('prefix', ['', 'async '], ids=['with', 'async_with'])
@pytest.mark.parametrize(
    ('s', 'expected'),
    [
        ('with ctx():\n    pass', set()),
        ('with open("file.txt") as fd:\n    fd.read()', set()),
        # Statements inside of the body
        ('with ctx():\n    os.system("ls -l")', {'2:4: ' + flake8_scs.SCS102}),
        ('with ctx():\n    assert value', {'2:4: ' + flake8_scs.SCS108}),
        ('with ctx():\n    import pdb', {'2:4: ' + flake8_scs.SCS107}),
        ('with ctx():\n    with other():\n        eval(code)', {'3:8: ' + flake8_scs.SCS101}),
        ('with open("file.txt") as fd:\n    pickle.load(fd)', {'2:4: ' + flake8_scs.SCS113}),
        # Context expressions
        ('with ctx(os.system("ls -l")):\n    pass', {'1:9: ' + flake8_scs.SCS102}),
        ('with os.popen("ls -l") as fd:\n    pass', {'1:5: ' + flake8_scs.SCS110}),
        # Context expressions reported at the location of the `with` statement are only reported once
        ('with open("file.txt", "w") as fd:\n    pass', {'1:0: ' + flake8_scs.SCS109}),
        ('with shelve.open("file.db") as db:\n    pass', {'1:0: ' + flake8_scs.SCS115}),
        (
            'with open("file.txt", "w") as fd:\n    os.system("ls -l")',
            {'1:0: ' + flake8_scs.SCS109, '2:4: ' + flake8_scs.SCS102},
        ),
        (
            'with open(os.path.abspath("file.txt"), "w") as fd:\n    pass',
            {'1:0: ' + flake8_scs.SCS109, '1:10: ' + flake8_scs.SCS100},
        ),
    ],
)
def test_with_statement(prefix, s, expected):
    if prefix:
        s = 'async def func():\n' + '\n'.join(
            f'    {prefix if not idx else ""}{line}' for idx, line in enumerate(s.split('\n'))
        )
    assert {r.split(': ', 1)[1] for r in results(s)} == {e.split(': ', 1)[1] for e in expected}
    if not prefix:
        assert results(s) == expected

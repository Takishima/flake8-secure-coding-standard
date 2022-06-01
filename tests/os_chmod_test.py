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
import stat

import pytest

import flake8_secure_coding_standard as flake8_scs


def results(s):
    return {'{}:{}: {}'.format(*r) for r in flake8_scs.Plugin(ast.parse(s)).run()}


# ==============================================================================


@pytest.mark.parametrize(
    's, expected',
    (
        ('S_IREAD', stat.S_IREAD),
        ('stat.S_IREAD', stat.S_IREAD),
        ('S_IREAD | S_IWRITE', stat.S_IREAD | stat.S_IWRITE),
        ('stat.S_IREAD | stat.S_IWRITE', stat.S_IREAD | stat.S_IWRITE),
        ('stat.S_IREAD | stat.S_IWRITE | S_IXUSR', stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR),
    ),
)
def test_chmod_get_mode(s, expected):
    node = ast.parse(s).body[0].value
    assert flake8_scs._chmod_get_mode(node) == expected


@pytest.mark.parametrize(
    's',
    (
        'stat.ST_MODE',
        'bla.S_IREAD',
    ),
)
def test_chmod_get_mode_invalid(s):
    node = ast.parse(s).body[0].value
    with pytest.raises(ValueError):
        flake8_scs._chmod_get_mode(node)


@pytest.mark.parametrize(
    's, expected',
    (
        ('-stat.S_IREAD', -stat.S_IREAD),
        ('~stat.S_IREAD', ~stat.S_IREAD),
        ('not stat.S_IREAD', not stat.S_IREAD),
    ),
)
def test_chmod_get_mode_unop(s, expected):
    node = ast.parse(s).body[0].value
    assert flake8_scs._chmod_get_mode(node) == expected


@pytest.mark.parametrize(
    's, expected',
    (
        ('stat.S_IREAD + stat.S_IWRITE', stat.S_IREAD + stat.S_IWRITE),
        ('stat.S_IREAD - stat.S_IWRITE', stat.S_IREAD - stat.S_IWRITE),
        ('stat.S_IREAD * stat.S_IWRITE', stat.S_IREAD * stat.S_IWRITE),
        ('stat.S_IREAD / stat.S_IWRITE', stat.S_IREAD / stat.S_IWRITE),
        ('stat.S_IREAD // stat.S_IWRITE', stat.S_IREAD // stat.S_IWRITE),
        ('stat.S_IREAD % stat.S_IWRITE', stat.S_IREAD % stat.S_IWRITE),
        ('stat.S_IREAD ^ stat.S_IWRITE', stat.S_IREAD ^ stat.S_IWRITE),
        ('stat.S_IREAD | stat.S_IWRITE', stat.S_IREAD | stat.S_IWRITE),
        ('stat.S_IREAD & stat.S_IWRITE', stat.S_IREAD & stat.S_IWRITE),
    ),
)
def test_chmod_get_mode_binop(s, expected):
    node = ast.parse(s).body[0].value
    assert flake8_scs._chmod_get_mode(node) == expected


@pytest.mark.parametrize(
    'platform, enabled_platform',
    (
        ('Linux', True),
        ('Darwin', True),
        ('Java', True),
        ('Windows', False),
    ),
)
@pytest.mark.parametrize('fname', ('"file.txt"', 'fname'))
@pytest.mark.parametrize('arg_type', ('', 'mode='), ids=('arg', 'keyword'))
@pytest.mark.parametrize(
    'forbidden',
    (
        'S_IRGRP',  # NB: not actually a forbidden value, only for testing...
        'S_IRWXG',
        'S_IWGRP',
        'S_IXGRP',
        'S_IRWXO',
        'S_IWOTH',
        'S_IXOTH',
    ),
)
@pytest.mark.parametrize(
    's',
    (
        '',
        'S_IREAD',
        'S_IREAD | S_IWRITE',
        'S_IRUSR | S_IWUSR | S_IXUSR',
    ),
    ids=lambda s: s if s else '<empty>',
)
def test_chmod(mocker, platform, enabled_platform, fname, arg_type, forbidden, s):
    mocker.patch('platform.system', lambda: platform)

    if s:
        code = f'os.chmod({fname}, {arg_type}{s} | {forbidden}) #@'
    else:
        code = f'os.chmod({fname}, {arg_type} {forbidden}) #@'

    print(code)
    flake8_warnings = results(code)
    if enabled_platform and forbidden != 'S_IRGRP':
        assert flake8_warnings == {'1:0: ' + flake8_scs.SCS119}
    else:
        assert flake8_warnings == set()


@pytest.mark.parametrize('platform', ('Linux', 'Darwin', 'Java', 'Windows'))
@pytest.mark.parametrize(
    's',
    (
        'os.chmod("file.txt", stat.ST_MODE)',
        'os.chmod("file.txt", other.S_IRWXO)',
        'os.chmod("file.txt", mode)',
        'os.chmod("file.txt", mode=mode)',
    ),
)
def test_chmod_no_warning(mocker, platform, s):
    mocker.patch('platform.system', lambda: platform)

    assert results(s) == set()


@pytest.mark.parametrize(
    'platform, enabled_platform',
    (
        ('Linux', True),
        ('Darwin', True),
        ('Java', True),
        ('Windows', False),
    ),
)
@pytest.mark.parametrize('s', ('os.chmod("file")',))
def test_chmod_invalid_raise(mocker, platform, enabled_platform, s):
    mocker.patch('platform.system', lambda: platform)

    if enabled_platform:
        with pytest.raises(RuntimeError):
            results(s)
    else:
        assert results(s) == set()

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
from collections import namedtuple

import pytest

import flake8_secure_coding_standard as flake8_scs

# ==============================================================================

_os_function_strings = {
    'mkdir': (
        'os.mkdir("/tmp/test", 0o777)',
        'os.mkdir(dir_name, 0o777)',
        'os.mkdir("/tmp/test", mode=0o777)',
        'os.mkdir(dir_name, mode=0o777)',
        'os.makedirs("/tmp/test/utils", 0o777)',
        'os.makedirs(dir_name, 0o777)',
        'os.makedirs("/tmp/test/utils", mode=0o777)',
        'os.makedirs(dir_name, mode=0o777)',
    ),
    'mkfifo': (
        'os.mkfifo("/tmp/test.log", 0o777)',
        'os.mkfifo(dir_name, 0o777)',
        'os.mkfifo("/tmp/test.log", mode=0o777)',
        'os.mkfifo(dir_name, mode=0o777)',
    ),
    'mknod': (
        'os.mknod("/tmp/test", 0o777)',
        'os.mknod(dir_name, 0o777)',
        'os.mknod("/tmp/test", mode=0o777)',
        'os.mknod(dir_name, mode=0o777)',
    ),
}


# ------------------------------------------------------------------------------


def results(s):
    return {'{}:{}: {}'.format(*r) for r in flake8_scs.Plugin(ast.parse(s)).run()}


# ==============================================================================


def configure_plugin(function, arg):
    mode = flake8_scs._read_octal_mode_option(f'os_{function}_mode', arg, flake8_scs._DEFAULT_MAX_MODE)
    OptionValue = namedtuple(
        'options_values',
        field_names=('os_mkdir_mode', 'os_mkfifo_mode', 'os_mknod_mode', 'os_open_mode'),
    )

    option = OptionValue(
        **{
            **{'os_mkdir_mode': False, 'os_mkfifo_mode': False, 'os_mknod_mode': False, 'os_open_mode': False},
            **{f'os_{function}_mode': mode},
        }
    )
    flake8_scs.Plugin.parse_options(option)
    assert getattr(flake8_scs.Visitor, f'os_{function}_modes_allowed') == [] if mode is None else mode


# ==============================================================================


@pytest.mark.parametrize(
    'platform',
    ('Linux', 'Darwin', 'Java', 'Windows'),
)
@pytest.mark.parametrize('function', ('mkdir', 'mkfifo', 'mknod'))
@pytest.mark.parametrize(
    'option',
    ('False', 'True'),
)
@pytest.mark.parametrize(
    's',
    (
        # mkdir
        'os.mkdir("/tmp/test")',
        'os.mkdir(dir_name)',
        'os.mkdir("/tmp/test", 0o644)',
        'os.mkdir(dir_name, 0o644)',
        'os.mkdir("/tmp/test", mode=mode)',
        'os.mkdir(dir_name, mode=mode)',
        # makedirs
        'os.makedirs("/tmp/test/utils")',
        'os.makedirs(dir_name)',
        'os.makedirs("/tmp/test/utils", 0o644)',
        'os.makedirs(dir_name, 0o644)',
        'os.makedirs("/tmp/test/utils", mode=mode)',
        'os.makedirs(dir_name, mode=mode)',
        # mkfifo
        'os.mkfifo("/tmp/test/utils")',
        'os.mkfifo("/tmp/test/utils", 0o644)',
        'os.mkfifo("/tmp/test/utils", mode=mode)',
        # mknod
        'os.mknod(dir_name)',
        'os.mknod(dir_name, 0o644)',
        'os.mknod(dir_name, mode=mode)',
    ),
)
def test_os_function_ok(mocker, platform, function, option, s):
    configure_plugin(function, option)
    mocker.patch('platform.system', lambda: platform)

    assert results(s) == set()


@pytest.mark.parametrize(
    'platform, enabled_platform',
    (
        ('Linux', True),
        ('Darwin', True),
        ('Java', False),
        ('Windows', False),
    ),
)
@pytest.mark.parametrize(
    'option',
    ('False', 'True'),
)
@pytest.mark.parametrize(
    'function, s', ((function, s) for function, tests in _os_function_strings.items() for s in tests)
)
def test_os_function_call(mocker, platform, enabled_platform, function, option, s):
    _msg_map = {'mkdir': flake8_scs.SCS116, 'mkfifo': flake8_scs.SCS117, 'mknod': flake8_scs.SCS118}

    configure_plugin(function, option)
    mocker.patch('platform.system', lambda: platform)

    flake8_warnings = results(s)
    if enabled_platform and option == 'True':
        assert flake8_warnings == {'1:0: ' + flake8_scs.Visitor.format_mode_msg(_msg_map[function])}
    else:
        assert flake8_warnings == set()

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


def results(s):
    return {'{}:{}: {}'.format(*r) for r in flake8_scs.Plugin(ast.parse(s)).run()}


# ==============================================================================


def configure_plugin(arg):
    mode = flake8_scs._read_octal_mode_option('os_open_mode', arg, flake8_scs._DEFAULT_MAX_MODE)
    OptionValue = namedtuple(
        'options_values',
        field_names=('os_mkdir_mode', 'os_mkfifo_mode', 'os_mknod_mode', 'os_open_mode'),
    )
    flake8_scs.Plugin.parse_options(
        OptionValue(
            False,
            False,
            False,
            mode,
        )
    )
    assert flake8_scs.Visitor.os_open_modes_allowed == [] if mode is None else mode


# ==============================================================================


@pytest.mark.parametrize(
    'arg',
    ('No', 'True', '0o644', '0o644,'),
)
@pytest.mark.parametrize(
    's',
    (
        'os.open("file.txt")',
        'os.open("file.txt", flags, mode)',
        'os.open("file.txt", os.O_RDONLY)',
        'os.open("file.txt", os.O_RDONLY, mode)',
        'os.open("file.txt", os.O_RDONLY, 0o644)',
        'os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW)',
        'os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode)',
        'os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o644)',
        'os.open("file.txt", os.O_RDONLY, mode=mode)',
        'os.open("file.txt", os.O_RDONLY, mode=0o644)',
        'os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode=mode)',
        'os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode=0o644)',
        'bla.open("file.txt")',
        'bla.open("file.txt", os.O_RDONLY)',
        'bla.open("file.txt", flags=os.O_RDONLY)',
        'bla.open("file.txt", os.O_RDONLY, mode)',
        'bla.open("file.txt", os.O_RDONLY, 0o644)',
        'bla.open("file.txt", os.O_RDONLY, 0o777)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o644)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o777)',
        'bla.open("file.txt", os.O_RDONLY, mode=mode)',
        'bla.open("file.txt", os.O_RDONLY, mode=0o644)',
        'bla.open("file.txt", os.O_RDONLY, mode=0o777)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode=mode)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode=0o644)',
        'bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode=0o777)',
        'with os.open("file.txt") as fd: fd.read()',
        'with os.open("file.txt", flags, mode) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY, mode) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY, 0o644) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode) as fd: fd.read()',
        'with os.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o644) as fd: fd.read()',
        'with os.open("file.txt", flags=flags, mode=mode) as fd: fd.read()',
        'with os.open("file.txt", flags=os.O_RDONLY, mode=mode) as fd: fd.read()',
        'with os.open("file.txt", flags=os.O_RDONLY, mode=0o644) as fd: fd.read()',
        'with os.open("file.txt", flags=os.O_RDONLY | os.O_NOFOLLOW, mode=mode) as fd: fd.read()',
        'with os.open("file.txt", flags=os.O_RDONLY | os.O_NOFOLLOW, mode=0o644) as fd: fd.read()',
        'with bla.open("file.txt") as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY, mode) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY, 0o644) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY, 0o777) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, mode) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o644) as fd: fd.read()',
        'with bla.open("file.txt", os.O_RDONLY | os.O_NOFOLLOW, 0o777) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY, mode=mode) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY, mode=0o644) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY, mode=0o777) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY | os.O_NOFOLLOW, mode=mode) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY | os.O_NOFOLLOW, mode=0o644) as fd: fd.read()',
        'with bla.open("file.txt", flags=os.O_RDONLY | os.O_NOFOLLOW, mode=0o777) as fd: fd.read()',
    ),
)
def test_ok(s, arg):
    configure_plugin(arg)
    assert results(s) == set()


# ==============================================================================


@pytest.mark.parametrize('mode', range(0o756, 0o777 + 1), ids=lambda arg: oct(arg))
@pytest.mark.parametrize(
    'arg, expected_warning',
    (
        ('False', False),
        ('True', True),
    ),
)
def test_os_open_call_default_modes(mode, arg, expected_warning):
    configure_plugin(arg)
    flake8_warnings = results(f'os.open("file.txt", os.O_WRONLY, 0o{mode:o})')
    if expected_warning:
        assert flake8_warnings == {'1:0: ' + flake8_scs.Visitor.format_mode_msg(flake8_scs.SCS112)}
    else:
        assert flake8_warnings == set()


# ------------------------------------------------------------------------------


@pytest.mark.parametrize('mode', range(0o750, 0o761), ids=lambda arg: oct(arg))
@pytest.mark.parametrize(
    'call_mode',
    (
        'os.open("file.txt", os.O_WRONLY, 0o{:o})',
        'os.open("file.txt", flags=os.O_WRONLY, mode=0o{:o})',
    ),
    ids=('args', 'keyword'),
)
@pytest.mark.parametrize(
    'arg, expected_warning',
    (
        ('False', False),
        ('0o755,', True),
    ),
    ids=('False-False', '[0o755]-True'),
)
def test_os_open_call(mode, call_mode, arg, expected_warning):
    configure_plugin(arg)
    flake8_warnings = results(call_mode.format(mode))

    if expected_warning and mode != 0o755:
        assert flake8_warnings == {'1:0: ' + flake8_scs.Visitor.format_mode_msg(flake8_scs.SCS112)}
    else:
        assert flake8_warnings == set()


# ==========================================================================


@pytest.mark.parametrize('mode', range(0o756, 0o777 + 1), ids=lambda arg: oct(arg))
@pytest.mark.parametrize(
    'call_mode',
    (
        'with os.open("file.txt", os.O_WRONLY, 0o{:o}) as fd: fd.read()',
        'with os.open("file.txt", flags=os.O_WRONLY, mode=0o{:o}) as fd: fd.read()',
    ),
    ids=('args', 'keyword'),
)
@pytest.mark.parametrize(
    'arg, expected_warning',
    (
        ('False', False),
        ('True', True),
    ),
)
def test_os_open_with_default_modes(mode, call_mode, arg, expected_warning):
    configure_plugin(arg)
    flake8_warnings = results(call_mode.format(mode))

    if expected_warning:
        assert flake8_warnings == {'1:0: ' + flake8_scs.Visitor.format_mode_msg(flake8_scs.SCS112)}
    else:
        assert flake8_warnings == set()


# --------------------------------------------------------------------------


@pytest.mark.parametrize('mode', range(0o750, 0o761), ids=lambda arg: oct(arg))
@pytest.mark.parametrize(
    'arg, expected_warning',
    (
        ('False', False),
        ('0o755,', True),
    ),
)
def test_os_open_with(mode, arg, expected_warning):
    configure_plugin(arg)
    flake8_warnings = results(f'with os.open("file.txt", os.O_WRONLY, 0o{mode:o}) as fd: fd.read()')

    if expected_warning and mode != 0o755:
        assert flake8_warnings == {'1:0: ' + flake8_scs.Visitor.format_mode_msg(flake8_scs.SCS112)}
    else:
        assert flake8_warnings == set()

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

# Copyright 2022 Damien Nguyen
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

import flake8
import pytest

import flake8_secure_coding_standard as flake8_scs


def create_options_manager():
    ctor_args = {'version': '1.0', 'plugin_versions': '', 'parents': []}
    if int(flake8.__version__[0]) >= 6:
        ctor_args['formatter_names'] = []
    return flake8.options.manager.OptionManager(**ctor_args)


def results(s):
    return {'{}:{}: {}'.format(*r) for r in flake8_scs.Plugin(ast.parse(s)).run()}


# ==============================================================================

_default_modes = list(range(0, flake8_scs._DEFAULT_MAX_MODE + 1))


def _id_func(arg):
    _max_len = 4
    if arg == _default_modes:
        return 'default_modes'
    if isinstance(arg, list) and len(arg) > _max_len:
        return '[{}...{}]'.format(
            ','.join(str(val) for val in arg[:_max_len]),
            ','.join(str(val) for val in arg[-_max_len:]),
        )
    return str(arg)


# ==============================================================================


@pytest.mark.parametrize(
    'arg, expected',
    (
        ('0', 0),
        ('false', None),
        ('False', None),
        ('n', None),
        ('no', None),
        ('No', None),
        ('NO', None),
        ('y', _default_modes),
        ('yes', _default_modes),
        ('Yes', _default_modes),
        ('YES', _default_modes),
        ('true', _default_modes),
        ('True', _default_modes),
        ('1', 1),
        ('493', 493),
        ('0o755', 0o755),
        ('0o755,', [0o755]),
        ('0o644, 0o755,', [0o644, 0o755]),
    ),
    ids=_id_func,
)
def test_read_octal_mode_option(arg, expected):
    print(f'INFO: expected: {expected}')
    assert flake8_scs._read_octal_mode_option('test', arg, _default_modes) == expected


@pytest.mark.parametrize('arg', ('', ',', ',,', 'nope', 'asd', 'a,', '493, a'))
def test_read_octal_mode_option_invalid(arg):
    with pytest.raises(ValueError):
        flake8_scs._read_octal_mode_option('test', arg, _default_modes)


@pytest.mark.parametrize('function', ('open', 'mkdir', 'mkfifo', 'mknod'))
@pytest.mark.parametrize(
    'arg, allowed_modes',
    (
        ('n', []),
        ('y', _default_modes),
        ('0', []),
        ('0o755', _default_modes),
        ('0o644, 0o755,', [0o644, 0o755]),
    ),
    ids=_id_func,
)
def test_os_allowed_mode(function, arg, allowed_modes):
    options = create_options_manager()
    flake8_scs.Plugin.add_options(options)
    flake8_scs.Plugin.parse_options(options.parse_args([f'--os-{function}-mode={arg}']))
    assert getattr(flake8_scs.Visitor, f'os_{function}_modes_allowed') == allowed_modes

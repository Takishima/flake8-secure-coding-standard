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
        'from os import getcwd',
        'from os.path import join',
        'subprocess.Popen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c)',
        'subprocess.Popen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c, False)',
        'subprocess.Popen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c, False, cwd)',
        'subprocess.Popen(["cat", "/etc/passwd"], shell=False)',
        'sp.Popen(["cat", "/etc/passwd"], shell=False)',
        'subprocess.run(["cat", "/etc/passwd"], shell=False)',
        'sp.run(["cat", "/etc/passwd"], shell=False)',
        'subprocess.call(["cat", "/etc/passwd"], shell=False)',
        'sp.call(["cat", "/etc/passwd"], shell=False)',
        'subprocess.check_call(["cat", "/etc/passwd"], shell=False)',
        'sp.check_call(["cat", "/etc/passwd"], shell=False)',
        'subprocess.check_output(["cat", "/etc/passwd"], shell=False)',
        'sp.check_output(["cat", "/etc/passwd"], shell=False)',
    ),
)
def test_shell_exec_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    's, msg_id',
    (
        ('os.system("ls -l")', 'SCS102'),
        ('from os import system', 'SCS102'),
        ('from os import system as os_system', 'SCS102'),
        ('from os import popen', 'SCS110'),
        ('from os import popen as os_popen', 'SCS110'),
        ('from subprocess import getoutput', 'SCS103'),
        ('from subprocess import getoutput as sp_getoutput', 'SCS103'),
        ('from subprocess import getstatusoutput', 'SCS103'),
        ('from subprocess import getstatusoutput as sp_getstatusoutput', 'SCS103'),
        ('from asyncio import create_subprocess_shell', 'SCS103'),
        ('from asyncio import create_subprocess_shell as create_sp_shell', 'SCS103'),
        ('subprocess.Popen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c, True)', 'SCS103'),
        ('subprocess.Popen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c, True, cwd)', 'SCS103'),
        ('subprocess.run(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('sp.run(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('subprocess.call(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('sp.call(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('subprocess.check_call(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('sp.check_call(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('subprocess.check_output(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('sp.check_output(["cat", "/etc/passwd"], shell=True)', 'SCS103'),
        ('subprocess.getoutput("ls /bin/ls")', 'SCS103'),
        ('sp.getoutput("ls /bin/ls")', 'SCS103'),
        ('subprocess.getstatusoutput("ls /bin/ls")', 'SCS103'),
        ('sp.getstatusoutput("ls /bin/ls")', 'SCS103'),
        ('asyncio.create_subprocess_shell("ls /bin/ls")', 'SCS103'),
        ('asyncio.create_subprocess_shell(cmd)', 'SCS103'),
        ('asyncio.create_subprocess_shell("ls /bin/ls", stdin=PIPE, stdout=PIPE)', 'SCS103'),
        ('asyncio.create_subprocess_shell(cmd, stdin=PIPE, stdout=PIPE)', 'SCS103'),
        ('loop.subprocess_shell(asyncio.SubprocessProtocol, "ls /bin/ls")', 'SCS103'),
        ('loop.subprocess_shell(asyncio.SubprocessProtocol, cmd)', 'SCS103'),
        ('loop.subprocess_shell(asyncio.SubprocessProtocol, cmd, **kwds)', 'SCS103'),
        ('os.popen("cat")', 'SCS110'),
        ('os.popen("cat", "r")', 'SCS110'),
        ('os.popen("cat", "r", 1)', 'SCS110'),
        ('os.popen("cat", buffering=1)', 'SCS110'),
        ('os.popen("cat", mode="w")', 'SCS110'),
        ('os.popen("cat", mode="w", buffering=1)', 'SCS110'),
    ),
)
def test_shell_exec_not_ok(s, msg_id):
    assert results(s) == {'1:0: ' + getattr(flake8_scs, msg_id)}

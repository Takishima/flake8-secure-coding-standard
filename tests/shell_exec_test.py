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


@pytest.mark.parametrize(
    's',
    [
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
        'from subprocess import call',
        'from subprocess import call\ncall(["cat", "/etc/passwd"])',
        'from subprocess import call\ncall(["cat", "/etc/passwd"], shell=False)',
        'from subprocess import Popen\nPopen(["cat", "/etc/passwd"], b, e, i, o, e, pre, c, False)',
        'import subprocess as subp\nsubp.run(["cat", "/etc/passwd"], shell=False)',
        # Not the functions from the subprocess module
        'call("cat /etc/passwd", shell=True)',
        'from mymodule import call\ncall("cat /etc/passwd", shell=True)',
        'from .subprocess import call\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call\nfrom mymodule import call\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call\ncall = my_call\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call\ncall, other = my_call, 1\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call\ndef call(cmd, shell): pass\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call\nasync def call(cmd, shell): pass\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import Popen\nclass Popen: pass\nPopen("cat /etc/passwd", shell=True)',
        'import subprocess as subp\nsubp = other\nsubp.run("cat /etc/passwd", shell=True)',
        'import subprocess as subp\nimport other as subp\nsubp.run("cat /etc/passwd", shell=True)',
    ],
)
def test_shell_exec_ok(s):
    assert results(s) == set()


@pytest.mark.parametrize(
    ('s', 'msg_id'),
    [
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
    ],
)
def test_shell_exec_not_ok(s, msg_id):
    assert results(s) == {'1:0: ' + getattr(flake8_scs, msg_id)}


@pytest.mark.parametrize(
    's',
    [
        'from subprocess import call\ncall("cat /etc/passwd", shell=True)',
        'from subprocess import call as sp_call\nsp_call("cat /etc/passwd", shell=True)',
        'from subprocess import check_call\ncheck_call("cat /etc/passwd", shell=True)',
        'from subprocess import check_output\ncheck_output("cat /etc/passwd", shell=True)',
        'from subprocess import run\nrun("cat /etc/passwd", shell=True)',
        'from subprocess import Popen\nPopen("cat /etc/passwd", shell=True)',
        'from subprocess import Popen\nPopen("cat /etc/passwd", b, e, i, o, e, pre, c, True)',
        'from subprocess import PIPE, run\nrun("cat /etc/passwd", shell=True, stdout=PIPE)',
        'import subprocess as subp\nsubp.run("cat /etc/passwd", shell=True)',
        'import subprocess as subp\nsubp.getoutput("cat /etc/passwd")',
        'import subprocess\nsubprocess = other\nsubprocess.run("cat /etc/passwd", shell=True)',
        'call = my_call\nfrom subprocess import call\ncall("cat /etc/passwd", shell=True)',
    ],
)
def test_shell_exec_imported_names_not_ok(s):
    assert results(s) == {f'{len(s.splitlines())}:0: {flake8_scs.SCS103}'}

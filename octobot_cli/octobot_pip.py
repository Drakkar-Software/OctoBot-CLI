#  Drakkar-Software OctoBot-CLI
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import os

import venv

from octobot_cli import OCTOBOT_PACKAGE, DEFAULT_VENV_PATH
from octobot_cli.util import run_command, get_current_directory


def _is_venv_installed(venv_path):
    return os.path.exists(os.path.join(get_current_directory(), venv_path))


def _create_venv(venv_path):
    venv.create(os.path.join(get_current_directory(), venv_path), with_pip=True)
    run_command(["virtualenv", venv_path])


def _get_python_path(venv_path):
    return os.path.join(get_current_directory(), venv_path, "bin", "python")


def _get_python_pip_path(venv_path):
    return [_get_python_path(venv_path=venv_path), "-m", "pip"]


def create_venv_if_necessary(venv_path):
    if not _is_venv_installed(venv_path=venv_path):
        _create_venv(venv_path=venv_path)


def _get_update_args(package_name=OCTOBOT_PACKAGE):
    return _get_install_args(package_name=package_name) + ["-U", package_name]


def _get_install_args(package_name=OCTOBOT_PACKAGE):
    return ["install", package_name]


def update(package_name=OCTOBOT_PACKAGE,
           venv_path=DEFAULT_VENV_PATH,
           verbose=False):
    create_venv_if_necessary(venv_path=venv_path)
    return run_pip_command(_get_update_args(package_name=package_name),
                           venv_path=venv_path,
                           verbose=verbose)


def install(package_name=OCTOBOT_PACKAGE,
            venv_path=DEFAULT_VENV_PATH,
            verbose=False):
    create_venv_if_necessary(venv_path=venv_path)
    return run_pip_command(_get_install_args(package_name=package_name),
                           venv_path=venv_path,
                           verbose=verbose)


def run_pip_command(pip_command_args,
                    venv_path,
                    verbose=False):
    return run_command(_get_python_pip_path(venv_path=venv_path) + pip_command_args, verbose=verbose)

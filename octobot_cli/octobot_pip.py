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
from octobot_commons.logging.logging_util import get_logger

from octobot_cli import OCTOBOT_PACKAGE, DEFAULT_VENV_PATH
from octobot_cli.util import run_command, get_current_directory, get_tentacles_manager_args


def _is_venv_installed(venv_path):
    return os.path.exists(os.path.join(get_current_directory(), venv_path))


def _create_venv(venv_path):
    venv.create(os.path.join(get_current_directory(), venv_path), with_pip=True)
    run_command(["virtualenv", venv_path])


def get_bin(name):
    if os.name == "nt":
        return ["Scripts", f"{name}.exe"]
    return ["bin", name]


def _get_python_path(venv_path):
    return os.path.join(get_current_directory(), venv_path, *get_bin("python"))


def _get_octobot_path(venv_path):
    return os.path.join(get_current_directory(), venv_path, *get_bin("OctoBot"))


def _get_python_pip_path(venv_path):
    return [_get_python_path(venv_path=venv_path), "-m", "pip"]


def create_venv_if_necessary(venv_path):
    venv_abs_path = os.path.abspath(venv_path)
    if not _is_venv_installed(venv_path=venv_path):
        get_logger().info(f"Creating a virtual env in {venv_abs_path}")
        _create_venv(venv_path=venv_path)
    else:
        get_logger().info(f"Using virtual env in {venv_abs_path}")


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


def start_octobot(args: list,
                  venv_path=DEFAULT_VENV_PATH,
                  verbose=False):
    return run_command([_get_octobot_path(venv_path=venv_path)] + args, verbose=verbose)


def install_tentacles(venv_path=DEFAULT_VENV_PATH,
                      verbose=False):
    return run_command(
        [_get_octobot_path(venv_path=venv_path)] + get_tentacles_manager_args("--install", "--all"),
        verbose=verbose)


def run_pip_command(pip_command_args,
                    venv_path,
                    verbose=False):
    if verbose:
        get_logger().info(f"Calling pip from virtual env in '{venv_path}' with arguments: {pip_command_args}")
    return run_command(_get_python_pip_path(venv_path=venv_path) + pip_command_args, verbose=verbose)

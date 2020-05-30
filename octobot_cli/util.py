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
import subprocess
import sys

from octobot_commons.logging.logging_util import get_logger


COMMAND_LOGGER = "Command runner"


def run_command(command_args: list, verbose=False, with_call=True, with_popen=False):
    try:
        if verbose:
            get_logger().info(f"Running command with: {command_args}")
        if with_call:
            return subprocess.call(command_args, stderr=sys.stdout.buffer)
        if with_popen:
            process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            return process.communicate()
        return subprocess.check_output(command_args)
    except subprocess.CalledProcessError as e:
        if verbose:
            get_logger().exception(e)


def get_current_directory():
    return os.path.abspath(os.getcwd())


def get_tentacles_manager_args(*options):
    return ["tentacles"] + list(options)

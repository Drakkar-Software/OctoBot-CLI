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
import argparse
from logging import INFO
from logging import getLogger, StreamHandler, Formatter

import sys

MIN_PYTHON_VERSION = (3, 7)

# check python version
current_version = sys.version_info
if not current_version >= MIN_PYTHON_VERSION:
    print("OctoBot requires a Python version to be higher or equal to Python " + str(MIN_PYTHON_VERSION[0])
          + "." + str(MIN_PYTHON_VERSION[1]) + " current Python version is " + str(current_version[0])
          + "." + str(current_version[1]) + "\n"
          + "You can download Python last versions on: https://www.python.org/downloads/")
    sys.exit(-1)

from octobot_cli.manager import install_octobot, update_octobot, start_octobot
from octobot_cli.octobot_cli import manage_cli


def _prepare_logger():
    logger = getLogger("Anonymous")
    logger.setLevel(INFO)
    # create console handler and set level to info
    ch = StreamHandler()
    ch.setLevel(INFO)
    # create formatter
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def cli(args=None):
    if not args:
        args = sys.argv[1:]
    _prepare_logger()

    parser = argparse.ArgumentParser(description='OctoBot-CLI')
    parser.add_argument('-v', '--version', help='Show OctoBot-CLI current version.',
                        action='store_true')
    parser.add_argument('-u', '--update', help='Update OctoBot-CLI.',
                        action='store_true')
    parser.add_argument('-vv', '--verbose', help='Activate verbose mode.',
                        action='store_true')

    parser.set_defaults(func=manage_cli)

    # octobot management commands
    octobot_management_parser = parser.add_subparsers(title="OctoBot Management")

    # install
    install_parser = octobot_management_parser.add_parser("install", help='Install Octobot')
    install_cli(install_parser)
    install_parser.set_defaults(func=install_octobot)

    # update
    update_parser = octobot_management_parser.add_parser("update", help='Update the installed Octobot')
    update_cli(update_parser)
    update_parser.set_defaults(func=update_octobot)

    # start
    start_parser = octobot_management_parser.add_parser("start", help='Start the installed OctoBot')
    start_cli(start_parser)
    start_parser.set_defaults(func=start_octobot)

    # tentacles manager
    try:
        from octobot_tentacles_manager.api.loader import load_tentacles
        from octobot_tentacles_manager.cli import register_tentacles_manager_arguments
        from octobot.commands import call_tentacles_manager
        tentacles_parser = octobot_management_parser.add_parser("tentacles", help='Calls OctoBot tentacles manager.\n'
                                                                                  'Use "tentacles --help" to get the '
                                                                                  'tentacles manager help.')
        register_tentacles_manager_arguments(tentacles_parser)
        tentacles_parser.set_defaults(func=call_tentacles_manager)
    except ImportError:
        pass

    args, octobot_args = parser.parse_known_args(args)
    # call the appropriate command entry point
    args.func(args, octobot_args)


def install_cli(octobot_management_parser):
    octobot_management_parser.add_argument('-d', '--docker', help='Install OctoBot with docker.',
                                           action='store_true')
    octobot_management_parser.add_argument('-p', '--python', help='Install OctoBot with python.',
                                           action='store_true')
    octobot_management_parser.add_argument('-r', '--arm', help='Use arm docker image (for raspberry).',
                                           action='store_true')
    octobot_management_parser.add_argument('-vv', '--verbose', help='Activate verbose mode.',
                                           action='store_true')


def update_cli(octobot_management_parser):
    octobot_management_parser.add_argument('-d', '--docker', help='Update OctoBot docker installation.',
                                           action='store_true')
    octobot_management_parser.add_argument('-p', '--python', help='Update OctoBot python installation.',
                                           action='store_true')
    octobot_management_parser.add_argument('-r', '--arm', help='Use arm docker image (for raspberry).',
                                           action='store_true')
    octobot_management_parser.add_argument('-vv', '--verbose', help='Activate verbose mode.',
                                           action='store_true')
    octobot_management_parser.add_argument('-v', '--version', help='Show OctoBot current version.',
                                           action='store_true')


def start_cli(octobot_management_parser):
    # use only arguments full names not to interfere with OctoBot's arguments
    octobot_management_parser.add_argument('--docker', help='Start OctoBot with docker.',
                                           action='store_true')
    octobot_management_parser.add_argument('--python', help='Start OctoBot with python.',
                                           action='store_true')

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

from octobot_commons.logging.logging_util import set_global_logger_level

from octobot_cli.manager import install_octobot, update_octobot
from octobot_cli.octobot_cli import manage_cli


def cli(args):
    set_global_logger_level(INFO)

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
    install_parser = octobot_management_parser.add_parser("install", help='')
    install_cli(install_parser)
    install_parser.set_defaults(func=install_octobot)

    # update
    update_parser = octobot_management_parser.add_parser("update", help='')
    update_cli(update_parser)
    update_parser.set_defaults(func=update_octobot)

    # # start
    # start_parser = octobot_management_parser.add_parser("start", help='')
    # start_cli(start_parser)
    # start_parser.set_defaults(func=start_octobot)
    #
    # # tentacles manager
    # tentacles_parser = octobot_management_parser.add_parser("tentacles", help='Calls OctoBot tentacles manager.\n'
    #                                                                           'Use "tentacles --help" to get the '
    #                                                                           'tentacles manager help.')
    # register_tentacles_manager_arguments(tentacles_parser)
    # tentacles_parser.set_defaults(func=call_tentacles_manager)

    args = parser.parse_args(args)
    # call the appropriate command entry point
    args.func(args)


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
    pass


def tentacles_cli(octobot_management_parser):
    pass

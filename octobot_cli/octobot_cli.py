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
from octobot_cli import VERSION, PROJECT_NAME
import octobot_cli.octobot_pip as octobot_pip


def manage_cli(args):
    if args.version:
        print(VERSION)
        return

    if args.update:
        update_cli(verbose=args.verbose)
        return


def update_cli(verbose=False):
    octobot_pip.update(package_name=PROJECT_NAME, verbose=verbose)

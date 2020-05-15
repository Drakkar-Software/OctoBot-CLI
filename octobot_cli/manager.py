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

import octobot_cli.octobot_pip as octobot_pip
import octobot_cli.octobot_docker as octobot_docker


def install_octobot(args):
    if args.docker:
        octobot_docker.install(use_arm_image=args.arm)
        return
    octobot_pip.install()


def update_octobot(args):
    if args.docker:
        octobot_docker.update(use_arm_image=args.arm)
        return
    octobot_pip.update()

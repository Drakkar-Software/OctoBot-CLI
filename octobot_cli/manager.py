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


def install_octobot(args, _):
    if args.docker:
        octobot_docker.install(use_arm_image=args.arm)
        return
    octobot_pip.install(verbose=args.verbose)


def update_octobot(args, _):
    if args.docker:
        octobot_docker.update(use_arm_image=args.arm)
        if not args.no_tentacles:
            octobot_docker.install_tentacles(use_arm_image=args.arm)
        return
    octobot_pip.update(verbose=args.verbose)
    if not args.no_tentacles:
        octobot_pip.install_tentacles()


def start_octobot(args, octobot_args):
    if args.docker:
        octobot_docker.start_octobot(octobot_args)
        return
    octobot_pip.start_octobot(octobot_args, verbose=args.verbose)

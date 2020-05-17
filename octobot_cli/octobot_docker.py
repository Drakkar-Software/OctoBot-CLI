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
import docker

from octobot_commons.logging.logging_util import get_logger
from octobot_cli import OCTOBOT_IMAGE, OCTOBOT_CONTAINER_NAME, CONTAINER_DEFAULT_PUBLISH_PORT, \
    OCTOBOT_STABLE_TAG, OCTOBOT_PI_IMAGE
from octobot_cli.util import get_current_directory


def _get_client():
    return docker.from_env()


def _get_complete_image(image_name, image_tag) -> str:
    return f"{image_name}:{image_tag}"


def _is_docker_available() -> bool:
    try:
        _get_client()
        return True
    except docker.errors.NotFound:
        get_logger().error("Docker service not found")
    return False


def _get_running_container(container_name=OCTOBOT_CONTAINER_NAME):
    return _get_client().containers.get(container_id=container_name)


def _is_container_running(container_name=OCTOBOT_CONTAINER_NAME) -> bool:
    try:
        _get_running_container(container_name=container_name)
        return True
    except docker.errors.NotFound:
        pass
    return False


def _pull_octobot_image(complete_image):
    get_logger().info("Pulling OctoBot docker image...")
    _get_client().images.pull(complete_image)


def _run_octobot_container(complete_image, container_name=OCTOBOT_CONTAINER_NAME, args=None):
    get_logger().info("Creating OctoBot container...")
    _get_client().containers.run(complete_image,
                                 command=args,
                                 name=container_name,
                                 ports={f"{CONTAINER_DEFAULT_PUBLISH_PORT}/tcp": CONTAINER_DEFAULT_PUBLISH_PORT},
                                 detach=True,
                                 volumes={
                                     os.path.join(get_current_directory(), "user"):
                                         {'bind': '/bot/octobot/user', 'mode': 'rw'},
                                     os.path.join(get_current_directory(), "logs"):
                                         {'bind': '/bot/octobot/logs', 'mode': 'rw'},
                                     os.path.join(get_current_directory(), "tentacles"):
                                         {'bind': '/bot/octobot/tentacles', 'mode': 'rw'}
                                 })


def update(image_name=OCTOBOT_IMAGE,
           image_tag=OCTOBOT_STABLE_TAG,
           container_name=OCTOBOT_CONTAINER_NAME,
           use_arm_image=False):
    if _is_docker_available() and _is_container_running(container_name=container_name):
        if use_arm_image:
            image_name = OCTOBOT_PI_IMAGE
        get_logger().info("Stopping OctoBot container...")
        _get_running_container(container_name=container_name).stop()
        _get_running_container(container_name=container_name).remove()
        _pull_octobot_image(_get_complete_image(image_name, image_tag))
        _run_octobot_container(_get_complete_image(image_name, image_tag),
                               container_name=container_name)
    else:
        get_logger().error("Docker container not found")


def install(image_name=OCTOBOT_IMAGE,
            image_tag=OCTOBOT_STABLE_TAG,
            container_name=OCTOBOT_CONTAINER_NAME,
            use_arm_image=False):
    if _is_docker_available() and not _is_container_running(container_name=container_name):
        if use_arm_image:
            image_name = OCTOBOT_PI_IMAGE
        _pull_octobot_image(_get_complete_image(image_name, image_tag))
        _run_octobot_container(_get_complete_image(image_name, image_tag),
                               container_name=container_name)
    else:
        get_logger().error("Docker container already exists")


def start_octobot(args: list,
                  image_name=OCTOBOT_IMAGE,
                  image_tag=OCTOBOT_STABLE_TAG,
                  container_name=OCTOBOT_CONTAINER_NAME,
                  use_arm_image=False):
    if _is_docker_available() and not _is_container_running(container_name=container_name):
        if use_arm_image:
            image_name = OCTOBOT_PI_IMAGE
        return _run_octobot_container(_get_complete_image(image_name, image_tag),
                                      container_name=container_name,
                                      args=args)
    else:
        get_logger().error("Docker container not found")

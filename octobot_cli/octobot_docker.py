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
from octobot_commons.logging.logging_util import get_logger

from octobot_cli import OCTOBOT_IMAGE, OCTOBOT_CONTAINER_NAME, OCTOBOT_LATEST_TAG
import docker


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


def _run_octobot_container(complete_image, container_name=OCTOBOT_CONTAINER_NAME):
    get_logger().info("Creating OctoBot container...")
    _get_client().containers.run(complete_image, name=container_name, detach=True)


def update(image_name=OCTOBOT_IMAGE, image_tag=OCTOBOT_LATEST_TAG, container_name=OCTOBOT_CONTAINER_NAME):
    if _is_docker_available() and _is_container_running(container_name=container_name):
        get_logger().info("Stopping OctoBot container...")
        _get_running_container(container_name=container_name).stop()
        _get_running_container(container_name=container_name).remove()
        _pull_octobot_image(_get_complete_image(image_name, image_tag))
        _run_octobot_container(_get_complete_image(image_name, image_tag),
                               container_name=container_name)
    else:
        get_logger().error("Docker container not found")


def install(image_name=OCTOBOT_IMAGE, image_tag=OCTOBOT_LATEST_TAG, container_name=OCTOBOT_CONTAINER_NAME):
    if _is_docker_available() and not _is_container_running(container_name=container_name):
        _pull_octobot_image(_get_complete_image(image_name, image_tag))
        _run_octobot_container(_get_complete_image(image_name, image_tag),
                               container_name=container_name)
    else:
        get_logger().error("Docker container already exists")

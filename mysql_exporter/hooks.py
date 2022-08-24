# Copyright 2022 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os

from jinja2 import Environment, FileSystemLoader, Template
from snaphelpers import Snap

from mysql_exporter.log import setup_logging

DEFAULT_CONFIG = {
    # MySQL Connection information
    "mysql.user": "exporter",
    "mysql.password": "exporterpasswd",
    "mysql.port": 3306,
    "mysql.host": "localhost",
    # Collection Stats information. By default, all metrics are collected.
    # There are some that are only enabled when the mysql userstat=1.
    # Intentionally disable these metrics by default as they carry a
    # significant performance impact. Also note, that for some unforeseen
    # reason, the '_' is not being recognized in config options.
    "collect.info-schema.clientstats": False,
    "collect.info-schema.tablestats": False,
    "collect.info-schema.schemastats": False,
    "collect.info-schema.userstats": False,
}


def install(snap: Snap) -> None:
    """Runs the 'install' hook for the snap.

    The 'install' hook will create the configuration directory, located
    at $SNAP_COMMON/etc and set the default configuration options.

    :param snap: the snap instance
    :type snap: Snap
    :return: None
    """
    setup_logging(snap.paths.common / "hooks.log")
    logging.info("Running install hook")
    os.makedirs(snap.paths.common / "etc", exist_ok=True)
    snap.config.set(DEFAULT_CONFIG)


def _get_template(snap: Snap, template: str) -> Template:
    """Returns the Jinja2 template to render.

    Locates the jinja template within the snap to load and returns
    the Template to the caller. This will look for the template in
    the 'templates' directory of the snap.

    :param snap: the snap to provide context
    :type snap: Snap
    :param template: the name of the template to locate
    :type template: str
    :return: the Template to use to render.
    :rtype: Template
    """
    template_dir = snap.paths.snap / "templates"
    env = Environment(loader=FileSystemLoader(searchpath=template_dir))
    return env.get_template(template)


def configure(snap: Snap) -> None:
    """Runs the `configure` hook for the snap.

    This method is invoked when the configure hook is executed by the snapd
    daemon. The `configure` hook is invoked when the user runs a sudo snap
    set mysql-exporter.<foo> setting.

    :param snap: the snap reference
    :type snap: Snap
    :return: None
    """
    setup_logging(snap.paths.common / "hooks.log")
    logging.info("Running configure hook")
    template = _get_template(snap, "my.cnf.j2")

    try:
        context = snap.config.get_options("mysql").as_dict()
        output = template.render(context)
        config_file = snap.paths.common / "etc" / "my.cnf"
        with open(config_file, "w+") as f:
            f.write(output)
    except:  # noqa
        logging.exception(
            "An error occurred when attempting to render the mysql configuration file."
        )
        raise

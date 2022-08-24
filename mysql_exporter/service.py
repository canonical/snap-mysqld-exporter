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
import subprocess
import sys
from collections.abc import Mapping
from typing import List

from snaphelpers import Snap

from mysql_exporter.log import setup_logging


class MysqldExporterService:
    """A python service object used to run the mysqld-exporter.

    This service runs the mysqld-exporter server. It will take into
    consideration the current snap configuration and determine which
    stats to enable or disable. By default, all stats are disabled
    except for those that are associated with userstat=1.

    This service will also take into account additional metrics which
    need to be turned off. To disable these, simply run the command

    $ sudo snap set mysqld-exporter collect.<grouping>.<metric>=false

    As a note, the 'grouping' and 'metric' keys will replace all underscores
    ('_') with a hyphen ('-') in the snap configuration. For example, to
    disable collection of the collect.info_schema.innodb_metrics, one would
    run:

    $ sudo snap set mysqld-exporter collect.info-schema.innodb-metrics

    This will result in the mysqld-exporter being run as follows:

    $ mysqld-exporter --no-collect.info_schema.innodb_metrics
    """

    def _keys_to_args(self, config: Mapping, prefix: str = "--no-") -> List[str]:
        """Converts the snap configuration values into parameters for exporter.

        Converts the snap configuration values into parameters for the
        prometheus exporter code. This will convert a dictionary (including
        nested dictionary) of keys and values to a dotted notation of keys.
        Only those keys that specify a value of False will be collected and
        turned into a --no-collect.<group>.<metric> parameter.

        :param config:
        :return:
        """
        args = []
        for key, value in config.items():
            group = key.replace("-", "_")

            # If the value is Truthy, then we don't want to pass this as a
            # parameter onto the commandline.
            if value is True:
                continue

            # if prefix != "--no-":
            #     prefix = ".".join([prefix, group])
            # else:
            #     prefix = "".join([prefix, group])
            # Recursively find the set of configuration options
            if isinstance(value, Mapping):
                args.extend(self._keys_to_args(value, f"{prefix}{group}."))
            else:
                args.append(f"{prefix}{group}")

        return args

    def run(self, snap: Snap) -> int:
        """Runs the mysqld-exporter service.

        Invoked when this service is started.

        :param snap: the snap context
        :type snap: Snap
        :return: exit code of the process
        :rtype: int
        """
        setup_logging(snap.paths.common / f"service-{snap.name}.log")

        collect_opts = snap.config.get_options("collect").as_dict()
        logging.info(f"Collect options: {collect_opts}")
        args = [f'--config.my-cnf={str(snap.paths.common / "etc" / "my.cnf")}']
        args.extend(self._keys_to_args(collect_opts))
        executable = snap.paths.snap / "bin" / "mysqld_exporter"
        logging.info(
            "Starting mysqld-exporter with the following arguments: "
            f'{executable} {" ".join(args)}'
        )

        cmd = [str(executable)]
        cmd.extend(args)
        completed_process = subprocess.run(cmd)

        logging.info(f"Exiting with code {completed_process.returncode}")
        return completed_process.returncode


def main():
    """Main entry point.

    :return:
    """
    service = MysqldExporterService()
    exit_code = service.run(Snap())
    sys.exit(exit_code)

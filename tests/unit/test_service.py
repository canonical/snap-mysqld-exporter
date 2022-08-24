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
# limitations under the License

import pytest

from mysql_exporter import service


class TestService:
    """Contains tests for the service module."""

    @pytest.mark.parametrize("exit_codes", [0, 100, -255])
    def test_run_exit_code(self, exit_codes, mocker, snap):
        """Tests the run of the service method."""
        mock_cp = mocker.Mock()
        mock_cp.returncode = exit_codes
        mocker.patch.object(service.subprocess, "run", return_value=mock_cp)

        svc = service.MysqldExporterService()
        code = svc.run(snap)
        assert code == exit_codes

    @pytest.mark.parametrize(
        "extra_args",
        [
            [],
            ["--foo-bar-arg"],
        ],
    )
    def test_run_process(self, extra_args, mocker, snap):
        """Tests the right process is called, with the right arguments."""
        mock_run = mocker.patch.object(service.subprocess, "run")
        mocker.patch.object(
            service.MysqldExporterService, "_keys_to_args", return_value=extra_args
        )

        svc = service.MysqldExporterService()
        svc.run(snap)

        expected_cmd = [
            str(snap.paths.snap / "bin" / "mysqld_exporter"),
            f'--config.my-cnf={str(snap.paths.common / "etc" / "my.cnf")}',
        ]
        expected_cmd.extend(extra_args)
        mock_run.assert_called_once_with(expected_cmd)

    @pytest.mark.parametrize(
        ["config", "expected"],
        [
            ({}, []),
            ({"foo": False}, ["--no-foo"]),
            ({"foo-bar": False}, ["--no-foo_bar"]),
            ({"foo": {"bar": False, "baz": True}}, ["--no-foo.bar"]),
        ],
    )
    def test_keys_to_args(self, config, expected):
        """Tests simple keys to args."""
        svc = service.MysqldExporterService()
        args = svc._keys_to_args(config)

        assert expected == args

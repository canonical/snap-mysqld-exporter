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

from pathlib import Path

import pytest

from mysql_exporter import hooks


class TestHooks:
    """Contains tests for mysql_exporter.hooks."""

    def test_install_hook(self, snap, os_makedirs):
        """Tests the install hook."""
        hooks.install(snap)

    def test_get_template(self, mocker, snap):
        """Tests retrieving the template."""
        mock_fs_loader = mocker.patch.object(hooks, "FileSystemLoader")
        mocker.patch.object(hooks, "Environment")
        hooks._get_template(snap, "foo.bar")
        mock_fs_loader.assert_called_once_with(searchpath=snap.paths.snap / "templates")

    def test_configure_hook(self, mocker, snap):
        """Tests the configure hook."""
        mock_template = mocker.Mock()
        mocker.patch.object(hooks, "_get_template", return_value=mock_template)
        mock_file = mocker.patch("builtins.open", mocker.mock_open())

        hooks.configure(snap)

        mock_template.render.assert_called_once()
        mock_file.assert_called_once_with(Path("/var/snap/mysnap/common/etc/my.cnf"), "w+")

    def test_configure_hook_exception(self, mocker, snap):
        """Tests the configure hook raising an exception while writing file."""
        mock_template = mocker.Mock()
        mocker.patch.object(hooks, "_get_template", return_value=mock_template)
        mock_file = mocker.patch("builtins.open", mocker.mock_open())
        mock_file.side_effect = FileNotFoundError

        with pytest.raises(FileNotFoundError):
            hooks.configure(snap)

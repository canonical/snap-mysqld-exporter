# Contributing

## Overview

This documents explains the processes and practices recommended for contributing enhancements to
this snap.

- Generally, before developing enhancements to this snap, you should consider [opening an issue
  ](https://github.com/wolsen/snap-mysqld-exporter/issues) explaining your use case.
- If you would like to chat with us about your use-cases or proposed implementation, you can reach
  us at [Canonical Mattermost public channel](https://chat.charmhub.io/charmhub/channels/charm-dev)
  or [Discourse](https://discourse.charmhub.io/).
- Familiarising yourself with [Snaps and Snapcraft](https://snapcraft.io/docs) documentation
  will help you a lot when working on new features or bug fixes.
- All enhancements require review before being merged. Code review typically examines
  - code quality
  - test coverage
  - user experience for MySQL operators
- Please help us out in ensuring easy to review branches by rebasing your pull request branch onto
  the `main` branch. This also avoids merge commits and creates a linear Git commit history.

## Developing

You can use the environments created by `tox` for development:

```shell
tox --notest -e unit
source .tox/unit/bin/activate
```

### Testing

```shell
tox -e fmt           # update your code according to linting rules
tox -e lint          # code style
tox -e unit          # unit tests
tox                  # runs 'lint' and 'unit' environments
```

## Build Snap

Build the snap in this git repository using:

```shell
snapcraft --use-lxd
```

### Deploy

```bash
# Install the development snap
sudo snap install --devmode mysqld-exporter_v0.14.0_amd64.snap
# Configure MySQL information
sudo snap set mysqld-exporter mysql.host=localhost mysql.user=testuser mysql.password=secret123
# Restart the service for the changes to take effect
sudo snap restart mysqld-exporter.mysqld-exporter
```

## Canonical Contributor Agreement

Canonical welcomes contributions to the MySQL Operator. Please check out our
[contributor agreement](https://ubuntu.com/legal/contributors)if you're
interested in contributing to the solution.
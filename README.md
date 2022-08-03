# Mysqld Exporter Snap

This repository contains the source for an unofficial snap for the
[mysqld exporter](https://github.com/prometheus/mysqld_exporter) for
[Prometheus](https://prometheus.io).

## Getting Started

To get started with the Mysqld Exporter, install the snap using snapd:

```commandline
sudo snap install mysqld-exporter
```

You will need to create a local user in your mysql database that allows
access for the mysql exporter. The following configuration should work:

```sql
CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'XXXXXXXX' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';
```

The mysqld-exporter is configured to run as a systemd service and
can be managed either through the `snap` command or the normal
systemd `systemctl` command.

For example, to view the services provided by the snap you can use
the `snap services mysqld-exporter` command. To restart the mysqld-exporter
service, you can use the `sudo snap restart mysqld-exporter.mysqld-exporter`
command.

## Configuration

The mysqld-exporter snap provides the following configuration variables that
can be set via the `snap set` command:

* __mysql.host__ - the host to connect to mysql on, defaults to localhost
* __mysql.port__ - the port to connect to mysql on, defaults to 3306
* __mysql.user__ - the username to use when connecting to mysql, defaults to exporter
* __mysql.password__ - the password to use when connecting to mysql

# Build

```bash
$ sudo snap install snapcraft
$ snapcraft --use-lxd
```

# Try

To try the snap that was built, you can install it locally:

```
$ sudo snap install --devmode ./mysqld-prometheus-exporter_x86_64.snap
```


# TODO Items

[x] Provide a sample my.cnf file in the $SNAP_COMMON directory

[ ] Config flags for the daemon

[x] Script wrapper to turn snap config settings into flags for the daemon

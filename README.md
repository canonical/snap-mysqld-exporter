# snap-mysqld-prometheus-exporter

A snap containing the mysqld prometheus exporter from the prometheus
community.

This is currently a work in progress


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

# my.cnf

```
[client]
user=exporter
password=XXXXXXXX
port=3306
socket=/tmp/mysql.sock
```

# TODO Items

[ ] Provide a sample my.cnf file in the $SNAP_COMMON directory

[ ] Config flags for the daemon

[ ] Script wrapper to turn snap config settings into flags for the daemon

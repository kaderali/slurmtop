# slurmtop

`slurmtop` is a lightweight interactive terminal monitor for Slurm clusters.

It provides a `top`-like overview of the cluster directly from the command line. The upper part of the screen shows the state and CPU allocation of all compute nodes, while the lower part displays currently running Slurm jobs and their resource usage.

## Features

* Interactive terminal interface using Python `curses`
* Automatic refresh of cluster and job information
* Overview of all Slurm compute nodes
* Compact visualization of CPU allocation per node
* Display of node states such as `idle`, `mixed`, `allocated`, `drain`, and `down`
* Running job overview including:

  * Job ID
  * User
  * Partition
  * Job name
  * Runtime
  * Number of nodes
  * Allocated CPUs
  * CPU utilization
  * Average and maximum resident memory
  * Allocated nodes
* Interactive filtering by user
* Interactive filtering by Slurm partition
* Scrollable job list
* Configurable refresh interval
* No external Python packages required

## Node Display

Each node is represented by its name, Slurm state, and a compact CPU allocation display.

Example:

```text
NODES
11 nodes    336 CPUs    76 allocated    260 idle
node001        idle        ........................................  0/40/0/40
node002        mixed       ############............................ 12/28/0/40
node009        allocated   ######################################## 40/0/0/40
node010        mixed       ####################.................... 20/20/0/40
node011        idle        ........................................  0/40/0/40
```

CPU symbols:

| Symbol | Meaning               |
| ------ | --------------------- |
| `.`    | Idle CPU              |
| `#`    | Allocated CPU         |
| `!`    | Other/unavailable CPU |
| `D`    | Drained node          |
| `X`    | Down/failed node      |
| `M`    | Maintenance           |

The CPU slots represent the number of CPUs in each state. They do not necessarily correspond to the physical CPU/core IDs on the node.

## Job Display

Running jobs are shown in a `top`-like table:

```text
RUNNING JOBS
     JOBID USER       PARTITION    NAME                     TIME   N  CPU   CPU%   RSSavg   RSSmax NODELIST
     83421 meier     cpu          STAR                    1:23:41   1   16   98.7     3.4G     4.1G node009
     83425 schmidt   gpu          keras                     32:18   1    8   87.4    12.8G    14.2G node030
```

Resource information is obtained from Slurm using `sstat`.

`CPU%` is calculated from Slurm's `AveCPU` relative to the elapsed wall-clock time. It therefore represents approximate average CPU utilization per task rather than the aggregate CPU percentage reported by tools such as Linux `top`.

`RSSavg` and `RSSmax` are derived from Slurm accounting information and depend on the accounting data available for the respective job steps.

## Requirements

* Linux
* Python 3
* Python `curses` support
* Slurm client tools:

  * `sinfo`
  * `squeue`
  * `sstat`

The program is intended to run on a Slurm login or head node with access to the Slurm controller and accounting information.

No additional Python packages are required.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd slurmtop
```

Make the script executable:

```bash
chmod +x slurmtop
```

You can run it directly from the repository:

```bash
./slurmtop
```

For system-wide installation, copy it to `/usr/local/bin`:

```bash
sudo cp slurmtop /usr/local/bin/slurmtop
sudo chmod 755 /usr/local/bin/slurmtop
```

It can then be started from any shell with:

```bash
slurmtop
```

## Usage

Start with the default refresh interval:

```bash
slurmtop
```

Specify a different refresh interval, for example one second:

```bash
slurmtop -i 1
```

Show command-line options:

```bash
slurmtop --help
```

## Interactive Controls

| Key             | Function                      |
| --------------- | ----------------------------- |
| `u`             | Set or clear user filter      |
| `p`             | Set or clear partition filter |
| `↑` / `↓`       | Scroll through jobs           |
| `PgUp` / `PgDn` | Scroll by larger increments   |
| `r`             | Refresh immediately           |
| `q`             | Quit                          |

### User filtering

Press `u` and enter one or more comma-separated usernames:

```text
meier,schmidt
```

Submit an empty value to remove the filter.

### Partition filtering

Press `p` and enter one or more comma-separated Slurm partitions:

```text
cpu,gpu
```

Submit an empty value to display all partitions again.

## Slurm Commands Used

`slurmtop` obtains its information from the standard Slurm command-line tools:

```text
sinfo    Node state and CPU allocation
squeue   Running jobs and their allocations
sstat    Runtime CPU and memory statistics
```

It does not require a daemon or agent to be installed on the compute nodes and does not modify the Slurm configuration.

## Permissions

The amount of information visible in `slurmtop` depends on the Slurm configuration and the permissions of the user running it.

In particular, job accounting and `sstat` information may be restricted or unavailable depending on the cluster's Slurm accounting configuration.

## Performance

The default refresh interval is 2 seconds.

For larger clusters, a longer interval can reduce the number of queries sent to the Slurm controller and accounting infrastructure:

```bash
slurmtop -i 5
```

Very short polling intervals are generally not recommended on production clusters.

## License

No license has been specified yet.


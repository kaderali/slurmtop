# slurmtop

`slurmtop` is a lightweight interactive terminal monitor for Slurm clusters.

It provides a `top`-like overview of a Slurm cluster directly from the command line. Depending on the selected mode, it can display compute-node utilization, running jobs, or queued jobs.

The interface automatically refreshes and adapts to the current terminal size.

## Features

* Interactive terminal interface using Python `curses`
* Automatic refresh of cluster and job information
* Several display modes:

  * Combined node and running-job overview
  * Running jobs only
  * Queued/pending jobs only
  * Nodes only
* Compact visualization of CPU allocation per node
* Adaptive multi-column node layout for wide terminals
* Scrollable node and job views
* Display of node states such as `idle`, `mixed`, `allocated`, `drain`, and `down`
* Running-job resource information including:

  * Job ID
  * User
  * Partition
  * Job name
  * Runtime
  * Number of nodes
  * Allocated CPUs
  * CPU utilization
  * Aggregate memory usage
  * Memory usage per allocated CPU
  * Maximum per-task RSS
  * Slurm memory reservation
  * Allocated nodes
* Pending-job overview including Slurm's pending reason
* Interactive filtering by user
* Interactive filtering by Slurm partition
* Interactive sorting by CPU usage, memory usage, runtime, or Job ID
* Configurable refresh interval
* No external Python packages required

## Node Display

Each node is represented by its name, Slurm state, and a compact CPU allocation display.

Example:

```text
NODES
11 nodes    336 CPUs    76 allocated    260 idle
node001   idle    ........................................  0/40/0/40
node002   mixed   ############............................ 12/28/0/40
node009   alloc   ######################################## 40/0/0/40
node010   mixed   ####################.................... 20/20/0/40
node011   idle    ........................................  0/40/0/40
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

The CPU slots represent the number of CPUs in each state. They do not necessarily correspond to individual physical CPU/core IDs.

### Adaptive Multi-Column Layout

If sufficient terminal width is available, `slurmtop` displays several nodes per row.

For example:

```text
node001 idle  ........................ 0/24/0/24   node002 mixed ####.................... 4/20/0/24
node003 alloc ######################## 24/0/0/24   node004 idle  ........................ 0/24/0/24
```

The number of columns is automatically determined from the terminal width and the amount of space required to represent each node.

On narrow terminals, the display automatically falls back to a single column.

The node view is scrollable, so all nodes remain accessible even when the terminal is too small to display the complete cluster at once.

## Running Job Display

Running jobs are shown in a `top`-like table:

```text
RUNNING JOBS [sort: CPU DESC]

     JOBID USER       PARTITION    NAME               TIME   N  CPU   CPU%      MEM  MEM/CPU   MAXRSS   MEMRES NODELIST
     83421 meier      cpu          STAR            1:23:41   1   16   98.7    54.3G    3.39G     4.1G      64G node009
     83425 schmidt    gpu          keras             32:18   1    8   87.4    12.8G    1.60G     2.2G      32G node030
```

### CPU Usage

`CPU%` estimates job-wide CPU utilization relative to the CPUs allocated to the job.

A job that fully utilizes all of its allocated CPUs should therefore show approximately:

```text
CPU% = 100%
```

rather than, for example, `1600%` for a 16-CPU job.

Runtime CPU statistics are obtained from Slurm using `sstat`.

### Memory Usage

The running-job view provides several memory metrics:

| Column    | Meaning                                                 |
| --------- | ------------------------------------------------------- |
| `MEM`     | Estimated aggregate current resident memory of the job  |
| `MEM/CPU` | Aggregate memory divided by allocated CPUs              |
| `MAXRSS`  | Largest resident memory observed for an individual task |
| `MEMRES`  | Memory reserved/allocated by Slurm for the job          |

Slurm reports `AveRSS` for individual job steps. `slurmtop` estimates the aggregate memory usage of each active step as:

```text
AveRSS × number of tasks
```

and combines the active job-step values to estimate total current resident memory.

This makes it possible to compare actual memory consumption with the amount of memory reserved for the job.

For example:

```text
CPU   CPU%     MEM   MEM/CPU   MAXRSS   MEMRES
 40    97.8   82.4G     2.06G    2.71G     120G
```

indicates that the job has 120 GiB reserved and is currently estimated to use approximately 82.4 GiB of resident memory.

`MAXRSS` remains a per-task value and should not be interpreted as total job memory usage.

Resource statistics depend on the Slurm accounting configuration and the privileges of the user running `slurmtop`.

## Queued Job Display

Pending jobs can be displayed separately:

```text
QUEUED JOBS

     JOBID USER       PARTITION    NAME               STATE          TIME   N  CPU REASON
     93218 meier      gpu          training           PENDING        0:00   1    8 Resources
     93219 schmidt    cpu          alignment          PENDING        0:00   1   40 Priority
     93221 mueller    gpu          pytorch            PENDING        0:00   1    4 Dependency
```

The `REASON` column shows the reason reported by Slurm for why the job is currently pending.

Common examples include:

* `Resources`
* `Priority`
* `Dependency`
* `QOSMaxCpuPerUserLimit`
* `ReqNodeNotAvail`

## Requirements

* Linux
* Python 3
* Python `curses` support
* Slurm client tools:

  * `sinfo`
  * `squeue`
  * `sstat`
  * `scontrol`

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

Run it directly:

```bash
./slurmtop
```

For system-wide installation:

```bash
sudo cp slurmtop /usr/local/bin/slurmtop
sudo chmod 755 /usr/local/bin/slurmtop
```

It can then be started from any shell:

```bash
slurmtop
```

## Usage

### Combined Dashboard

The default view shows the node overview and running jobs:

```bash
slurmtop
```

### Running Jobs Only

```bash
slurmtop --running
```

or:

```bash
slurmtop -r
```

### Queued Jobs Only

```bash
slurmtop --queued
```

or:

```bash
slurmtop -q
```

### Nodes Only

```bash
slurmtop --nodes
```

or:

```bash
slurmtop -n
```

### Refresh Interval

The default refresh interval is 2 seconds.

Specify another interval with:

```bash
slurmtop -i 5
```

Display command-line options with:

```bash
slurmtop --help
```

## Interactive Controls

### General Controls

| Key             | Function                    |
| --------------- | --------------------------- |
| `q`             | Quit                        |
| `r`             | Refresh immediately         |
| `↑` / `↓`       | Scroll                      |
| `PgUp` / `PgDn` | Scroll by larger increments |
| `Home`          | Jump to beginning           |
| `End`           | Jump to end                 |

In the combined dashboard:

| Key   | Function                                |
| ----- | --------------------------------------- |
| `Tab` | Switch focus between node and job views |

The currently focused section is highlighted. Scrolling affects the focused section.

### Filtering

| Key | Function                      |
| --- | ----------------------------- |
| `u` | Set or clear user filter      |
| `p` | Set or clear partition filter |

Press `u` and enter one or more comma-separated usernames:

```text
meier,schmidt
```

Submit an empty value to remove the user filter.

Press `p` and enter one or more comma-separated partitions:

```text
cpu,gpu
```

Submit an empty value to remove the partition filter.

### Job Sorting

Running jobs can be sorted interactively:

| Key | Sort by                      |
| --- | ---------------------------- |
| `c` | CPU utilization              |
| `m` | Aggregate memory usage       |
| `t` | Runtime                      |
| `j` | Job ID                       |
| `s` | Restore original Slurm order |

Pressing the currently active sort key again reverses the sort direction.

For example, pressing `c` initially selects:

```text
sort: CPU DESC
```

Pressing `c` again changes it to:

```text
sort: CPU ASC
```

CPU usage, memory usage, and runtime initially sort in descending order so that the jobs consuming the most resources appear at the top.

The active sort mode is displayed in the job-view title.

## Slurm Commands Used

`slurmtop` obtains its information from standard Slurm command-line tools:

```text
sinfo       Node state and CPU allocation
squeue      Running and pending jobs
sstat       Runtime CPU and memory statistics
scontrol    Detailed job allocation information
```

It does not require a daemon or agent to be installed on the compute nodes and does not modify the Slurm configuration.

## Permissions and Accounting

The amount of runtime information available depends on the Slurm configuration and the permissions of the account running `slurmtop`.

In particular, CPU and RSS statistics for jobs belonging to other users may not be available to an ordinary user.

In that case, jobs can still be displayed, but some runtime columns may contain:

```text
-
```

Cluster administrators should ensure that the desired Slurm job-accounting information is available if `slurmtop` is intended to provide cluster-wide resource monitoring.

## Performance

The default refresh interval is 2 seconds.

For larger clusters, a longer interval reduces the number of queries sent to the Slurm controller and accounting infrastructure:

```bash
slurmtop -i 5
```

Very short polling intervals are generally not recommended on production clusters.

## License

This project is distributed under the terms of the license contained in the `LICENSE` file.

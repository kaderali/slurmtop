import importlib.machinery
import importlib.util
import pathlib
import unittest
from unittest import mock


SCRIPT = pathlib.Path(__file__).parents[1] / "slurmtop"
loader = importlib.machinery.SourceFileLoader("slurmtop", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
slurmtop = importlib.util.module_from_spec(spec)
loader.exec_module(slurmtop)


def job(jobid="123", cpus=4):
    return slurmtop.Job(
        jobid, "user", "cpu", "name", "RUNNING", "00:10", 1, cpus, "node1"
    )


class MemoryStatisticsTests(unittest.TestCase):
    def test_tres_total_is_preferred_over_averss_estimate(self):
        current = job()
        output = (
            "123.batch|00:00:08|10M|12M|2|cpu=00:00:16,mem=25M,pages=0|\n"
        )

        with mock.patch.object(slurmtop, "run_command", return_value=output):
            slurmtop.read_job_statistics([current])

        self.assertEqual(current.mem_total_kib, 25 * 1024)
        self.assertEqual(current.mem_per_cpu_kib, 25 * 1024 / 4)

    def test_totals_are_summed_across_active_steps(self):
        current = job()
        output = (
            "123.batch|00:00:01|1M|2M|1|mem=3M|\n"
            "123.0|00:00:02|4M|5M|2|mem=9M|\n"
        )

        with mock.patch.object(slurmtop, "run_command", return_value=output):
            slurmtop.read_job_statistics([current])

        self.assertEqual(current.mem_total_kib, 12 * 1024)
        self.assertEqual(current.max_rss_kib, 5 * 1024)

    def test_averss_times_tasks_remains_a_fallback(self):
        current = job()
        output = "123.batch|00:00:08|10M|12M|3||\n"

        with mock.patch.object(slurmtop, "run_command", return_value=output):
            slurmtop.read_job_statistics([current])

        self.assertEqual(current.mem_total_kib, 30 * 1024)

    def test_tres_parser_accepts_long_memory_name(self):
        self.assertEqual(
            slurmtop.parse_tres_memory("cpu=00:01:00,memory=1.5G"),
            1.5 * 1024 * 1024,
        )


if __name__ == "__main__":
    unittest.main()

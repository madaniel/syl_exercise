
import sys
import random
import subprocess
from argparse import ArgumentParser
from multiprocessing import Pool, Manager

# Defines
PERCENTILE = 0.95
PROCESS_MIN_SECONDS = 1
PROCESS_MAX_SECONDS = 60
THROUGHPUT_INDEX = 1
LATENCY_INDEX = 4
DEBUG = False


class Runner(object):
    """
    This will a launch processes based on user argument
    """

    def __init__(self):
        self.process_amount = None

    def get_process_amount(self):
        """
        Get the amount of stress process that should run
        """
        parser = ArgumentParser(description="Amount of Stress processes")
        parser.add_argument("ProcessAmount", metavar="process_amount", type=int, help="Total number of processes that should run")
        args = parser.parse_args()
        process_amount = args.ProcessAmount

        if process_amount < 1:
            print("1 is the minimum value for process_amount")
            sys.exit(1)

        self.process_amount = process_amount

    @staticmethod
    def start_process(args):
        """
        Starts a single process
        """
        pid, data_dict, lock = args[:]
        seconds = random.randint(PROCESS_MIN_SECONDS, PROCESS_MAX_SECONDS)
        command = ["python", "stress.py", str(seconds)]

        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as stress_process:

            while True:
                realtime_output = stress_process.stdout.readline()

                # No more prints from stress process
                if realtime_output == b'' and stress_process.poll() is not None:
                    break

                if realtime_output:
                    # Remove 'b prefix
                    realtime_output = realtime_output.decode('ascii')
                    # Print stress process output to console
                    sys.stdout.write(f"pid={pid} {realtime_output}") if DEBUG else None
                    # Purge buffer to enable prints
                    sys.stdout.flush()
                    # Break the output into list
                    realtime_output_list = realtime_output.split()
                    throughput = int(realtime_output_list[THROUGHPUT_INDEX])
                    latency = int(realtime_output_list[LATENCY_INDEX])

                    # Prevent race between processes
                    with lock:
                        latency_list = data_dict["latency_list"]
                        throughput_list = data_dict["throughput_list"]
                        latency_list.append(latency)
                        throughput_list.append(throughput)

                        # update stats per process per latency and throughput
                        latency_stats = data_dict["latency_stats"]
                        latency_stats.update_stats(new_value=latency, data_list=latency_list)
                        throughput_stats = data_dict["throughput_stats"]
                        throughput_stats.update_stats(new_value=throughput, data_list=throughput_list)
                        data_dict["latency_stats"] = latency_stats
                        data_dict["throughput_stats"] = throughput_stats

                        data_dict["latency_list"] = latency_list
                        data_dict["throughput_list"] = throughput_list
                        data_dict["update_counter"] = data_dict.get("update_counter", 0) + 1

                        print(f"\nThroughput: {throughput_stats}")
                        print(f"Latency: {latency_stats}")

    def run_stress_process(self):
        """
        Start all the stress process
        """
        manager = Manager()
        shared_dict = manager.dict()
        shared_dict["latency_list"] = []
        shared_dict["throughput_list"] = []
        shared_dict["update_counter"] = 0
        shared_dict["latency_stats"] = Stats()
        shared_dict["throughput_stats"] = Stats()
        shared_lock = manager.Lock()

        with Pool(self.process_amount) as process:
            process.map(self.start_process, [(pid, shared_dict, shared_lock) for pid in range(self.process_amount)])


class Stats(object):

    """
    Class for statistics calculations
    """

    def __init__(self):
        self.min = None
        self.max = None
        self.sum = 0
        self.count = 0
        self.percentile = None

    @property
    def average(self) -> float:
        """
        Calculates average of values
        """
        return round(self.sum / self.count) if self.count > 0 else None

    def _update_percentile(self, data_list: list, percentile: float):
        """
        Calculates percentile of values in list based on float value
        """
        assert 0 <= percentile <= 1, "percentile should be float between 0 and 1"
        size = len(data_list)
        sorted(data_list)
        index_of_percentile = int(round(size * percentile)) - 1
        assert 0 <= index_of_percentile < len(data_list), f"index {index_of_percentile} is out of range of data_list {data_list}"

        self.percentile = data_list[index_of_percentile]

    def update_stats(self, new_value: int, data_list: list):
        """
        Update all statistics values per new value
        """
        if self.min is None or new_value < self.min:
            self.min = new_value

        if self.max is None or new_value > self.max:
            self.max = new_value

        self.sum += new_value
        self.count += 1
        self._update_percentile(data_list=data_list, percentile=PERCENTILE)

    def __repr__(self):
        return f"Average={self.average}, Min={self.min}, Max={self.max}, 95th Percentile={self.percentile}"


if __name__ == "__main__":
    runner = Runner()
    runner.get_process_amount()
    runner.run_stress_process()

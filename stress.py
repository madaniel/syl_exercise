
import sys
import random
import time
from argparse import ArgumentParser


class StressProcess(object):
    """
    This will simulate stress on db by printing the following format:

    Throughput - values in range of [0, 100,000], measured in operations/s
    Latency - values in a range of [0, 20000], measured in milliseconds
    """
    def __init__(self):
        self.stress_time = None

    def get_stress_time(self):
        """
        Get the stress_time from the user argument
        """
        parser = ArgumentParser(description="Stress time for process")
        parser.add_argument("StressTime", metavar="stress_time", type=int, help="Stress time in seconds")
        args = parser.parse_args()
        stress_time = args.StressTime

        if stress_time < 1:
            print("1 is the minimum value for stress_time")
            sys.exit(1)

        self.stress_time = stress_time

    def start_process(self):
        """
        Start the Stress process
        """
        stress_time = self.stress_time

        while stress_time > 0:
            throughput = random.randint(0, 100000)
            latency = random.randint(0, 20000)
            print(f"Throughput: {throughput} ops Latency: {latency} ms")
            time.sleep(1)
            stress_time -= 1


if __name__ == "__main__":
    stress_process = StressProcess()
    stress_process.get_stress_time()
    stress_process.start_process()

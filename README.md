# stressSimulator
Simulate stress using process and analyzer
This will demonstrate multiprocessing behavior

## process.py
Print random values of throughput and latency, during the time given in user argument.

For example:
```
python stress.py 3

Throughput: 90230 ops Latency: 12985 ms
Throughput: 94 ops Latency: 12375 ms
Throughput: 8733 ops Latency: 8136 ms
```


## analyzer.py
Launch number of processes in multiprocess, based on user argument.
Each process will be given random time to run.

All process prints will be analyzed in realtime.
Statistics aggregated data will be print for the current running processes.

For example:

```
python analyze 3

Throughput: Average=20125, Min=20125, Max=20125, 95th Percentile=20125
Latency: Average=5824, Min=5824, Max=5824, 95th Percentile=5824

Throughput: Average=29697, Min=20125, Max=39269, 95th Percentile=39269
Latency: Average=5492, Min=5159, Max=5824, 95th Percentile=5159

Throughput: Average=47958, Min=20125, Max=84480, 95th Percentile=84480
Latency: Average=4364, Min=2109, Max=5824, 95th Percentile=2109

Throughput: Average=60372, Min=20125, Max=97614, 95th Percentile=97614
Latency: Average=6432, Min=2109, Max=12638, 95th Percentile=12638

Throughput: Average=59361, Min=20125, Max=97614, 95th Percentile=55319
Latency: Average=8750, Min=2109, Max=18021, 95th Percentile=18021

Throughput: Average=56979, Min=20125, Max=97614, 95th Percentile=45068
Latency: Average=9043, Min=2109, Max=18021, 95th Percentile=10507

Throughput: Average=55339, Min=20125, Max=97614, 95th Percentile=45499
Latency: Average=9250, Min=2109, Max=18021, 95th Percentile=10491
```

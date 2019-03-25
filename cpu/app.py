#!/usr/bin/env python
"""
Produces load on all available CPU cores
"""

from multiprocessing import Pool
from multiprocessing import cpu_count
import func

if __name__ == '__main__':
    processes = 8
    print('Generating cpu load...')
    pool = Pool(processes)
    pool.map(func.f, range(processes))
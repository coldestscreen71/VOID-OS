import time
import os
import random
import sys
import platform
import json

def down_ani():
    total_blocks = 10

    for percent in range(0, 101):
        filled = percent * total_blocks // 100
        empty = total_blocks - filled
        bar = "#" * filled + "." * empty

        sys.stdout.write(f"\r{percent}%[{bar}]")
        sys.stdout.flush()
        time.sleep(0.05)

    print("\nUnpacking complete ✔")
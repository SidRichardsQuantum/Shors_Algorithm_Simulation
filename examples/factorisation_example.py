import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import shors_simulation


if __name__ == "__main__":
    """Default example N = 15 with a = 7"""
    shors_simulation(N=15, a=7, show_plots=True, sparse=True)

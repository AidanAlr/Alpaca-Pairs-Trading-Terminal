import time
from functools import wraps
import logging

# Configure the logging; you can adjust the level and format as needed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        # Use logging instead of print
        logging.info(f'{func.__name__} took {total_time:.4f} seconds')

        return result

    return timeit_wrapper

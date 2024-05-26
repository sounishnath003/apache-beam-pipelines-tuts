import time
import logging


def time_elapsed(func):
    def __wrapper__(*args, **kwargs):
        started = time.time()
        fn_out = func(*args, **kwargs)
        ended = time.time()
        time_elp = ended - started
        logging.info(f"{func}:total.time.elapsed:{time_elp} seconds")
        return fn_out

    return __wrapper__

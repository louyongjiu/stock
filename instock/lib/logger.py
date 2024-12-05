import time
import logging
import inspect
from datetime import datetime
from functools import wraps
from contextlib import ContextDecorator

class Timer(ContextDecorator):
    def __init__(self):
        self.start_time = None
        self.end_time = None
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.perf_counter()

    @property
    def elapsed(self):
        return self.end_time - self.start_time if self.end_time is not None else 0.0


def log_execution_details(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ', '.join(repr(a) for a in args) + ', ' + ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
        
        # 获取调用者信息
        caller_frame = inspect.currentframe().f_back
        caller_filename = caller_frame.f_code.co_filename
        caller_lineno = caller_frame.f_lineno

        with Timer() as timer:
            start_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            logging.info(f"开始执行 {func.__name__}({arg_str}) at {caller_filename}:{caller_lineno} 时间: {start_time_str}")
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                logging.error(f"执行 {func.__name__}({arg_str}) 失败 at {caller_filename}:{caller_lineno} 时间: {end_time_str}, 耗时: {timer.elapsed:.4f} 秒", exc_info=True)
                raise e
            
            end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            logging.info(f"完成执行 {func.__name__}({arg_str}) at {caller_filename}:{caller_lineno} 时间: {end_time_str}, 耗时: {timer.elapsed:.4f} 秒")
            
            return result

    return wrapper
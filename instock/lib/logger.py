import time
from datetime import datetime
import logging
from functools import wraps
import inspect

def log_execution_details(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取调用者的信息
        caller_frame = inspect.stack()[1]
        caller_filename = caller_frame.filename
        caller_lineno = caller_frame.lineno
        start_time = time.time()
        # print(f"Starting {func.__name__} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        arg_str = ', '.join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        logging.info(f"{func.__name__}({arg_str}) from {caller_filename}:{caller_lineno} 开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
   
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        # print(f"Finished {func.__name__} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (took {execution_time:.4f} seconds)")
        logging.info(f"{func.__name__}({arg_str}) from {caller_filename}:{caller_lineno} 完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} , 耗时: {execution_time:.4f} 秒")
        return result
    return wrapper
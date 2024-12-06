import logging
import os.path
from datetime import datetime
from functools import wraps

def log_execution(include_args=False, prefix=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取当前函数的文件名、函数名和行号
            filename = func.__code__.co_filename
            lineno = func.__code__.co_firstlineno
            base_func_name = f"{os.path.basename(filename)}:{lineno}::{func.__name__}"
            if include_args:
                arg_str = ', '.join(repr(a) for a in args + 
                                    tuple(f"{k}={v!r}" for k, v in kwargs.items()))
                base_func_name += f"({arg_str})"
            
            # 构造带有前缀的函数名字符串
            func_name = f"{prefix} {base_func_name}" if prefix else base_func_name
            
            timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
            start_time = datetime.now()
            logging.info(f"{func_name} 开始: {start_time.strftime(timestamp_format)}")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                elapsed_time = (end_time - start_time).total_seconds()
                logging.info(f"{func_name} 完成: {end_time.strftime(timestamp_format)}, 耗时: {elapsed_time:.4f} 秒")
                return result
            except Exception as e:
                logging.error(f"{func_name} 处理异常：{e}", exc_info=True)
                raise
        return wrapper
    return decorator
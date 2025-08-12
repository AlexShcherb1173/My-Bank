import functools
import sys

def log(filename=None):
    """Декоратор log, который будет автоматически логировать начало и конец выполнения функции,
       а также ее результаты или возникшие ошибки."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_output = []
            try:
                log_output.append(f"{func.__name__} start")
                result = func(*args, **kwargs)
                log_output.append(f"{func.__name__} ok")
                _write_log(log_output, filename)
                return result
            except Exception as e:
                error_msg = (f"{func.__name__} error: {type(e).__name__}. "
                             f"Inputs: {args}, {kwargs}")
                log_output.append(error_msg)
                _write_log(log_output, filename)
                raise

        return wrapper

    return decorator


def _write_log(messages, filename):
    """ Функция вывода сообщения(логов) в файл или консоль"""
    output = "\n".join(messages) + "\n"
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output, file=sys.stderr)



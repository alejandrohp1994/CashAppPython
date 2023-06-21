import signal

def timeout(seconds):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("Function execution timed out")

        def wrapper(*args, **kwargs):
            # Set the signal handler
            signal.signal(signal.SIGALRM, handler)
            # Start the timer
            signal.alarm(seconds)

            try:
                # Call the decorated function
                result = func(*args, **kwargs)
                return result
            finally:
                # Cancel the alarm
                signal.alarm(0)

        return wrapper

    return decorator


from functools import wraps
import time

def printClassAndFunction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            class_name = args[0].__class__.__name__  # Get the class name
        else:
            class_name = func.__module__  # Use module name as class name (for standalone functions)

        function_name = func.__name__  # Get the function name

        print(f"\n[{class_name} | {function_name}] started")

        start_time = time.time()  # Record the start time

        result = func(*args, **kwargs)  # Call the original function

        duration = time.time() - start_time  # Calculate the duration

        print(f"[{class_name} | {function_name}] ended with duration of {duration} seconds\n")

        return result

    return wrapper

def ClassFun(var1, var2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"\n[{var1}|{var2}] started")

            start_time = time.time()

            result = func(*args, **kwargs)

            duration = time.time() - start_time

            print(f"[{var1}|{var2}] ended. Duration: {round(duration,4)} seconds\n")

            return result

        return wrapper

    return decorator
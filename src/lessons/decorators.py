import time
from functools import wraps


def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def say(name):
    print(name)
    return "Результат"


# print(say("Xaash"))

# print(say.__code__.co_freevars)  # ('func', 'n') — обе переменные замыкания


def retry(times=3, delay=0.5):
    if times < 1:
        raise ValueError("times must be >= 1")

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except ValueError:
                    if i == times - 1:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


@retry(times=3, delay=1)
def unstable(probability):
    import random

    r = random.random()
    print(f"{r:.2f} <= {probability} ?")
    if r > probability:
        raise ValueError("Не повезло")
    return "Ok"


# try:
#     print(unstable(0.2))
# except ValueError as e:
#     print(e)


def memoize(func):
    cache = {}  # args(tuple): result(int)

    @wraps(func)
    def wrapper(*args, **kwargs):
        params = (args, tuple(sorted(kwargs.items())))
        if params in cache:
            return cache[params]

        result = func(*args, **kwargs)
        cache[params] = result
        return result

    return wrapper


@memoize
def slow_square(n, k=1, d=1):
    print(f"считаю {n} * {k} / {d}...")
    time.sleep(0.5)
    return n * k / d


print(slow_square(4, d=2, k=10))
print(slow_square(4))
print(slow_square(5))
print(slow_square(4, k=10, d=2))
print(slow_square(4, 10, d=2))

print(slow_square.__closure__)
print(slow_square.__wrapped__(4))


def stats(func):
    total_calls = 0
    by_args = {}
    total_time = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal total_calls, total_time
        total_calls += 1

        params = (args, tuple(sorted(kwargs.items())))
        by_args[params] = by_args.get(params, 0) + 1

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time += end - start

        return result

    def show_stats():
        print(f"Всего вызовов: {total_calls}")
        print(f"Уникальных аргументов: {len(by_args)}")
        print(f"Среднее время выполнения: {round(total_time * 1000 / total_calls, 6)}ms")

    wrapper.stats = show_stats

    return wrapper


@stats
def add(a, b):
    return a + b


add(1, 2)
add(1, 2)
add(3, 4)

add.stats()

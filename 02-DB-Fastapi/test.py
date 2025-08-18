def my_generator():
    n = 1
    print("first yield")
    yield n
    n += 6
    print("Second yield")
    yield n
    n *= 89
    print("third yield")
    yield n


generator = my_generator()

print(next(generator))
print(next(generator))

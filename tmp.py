def gen01():
    yield 1

print(gen01())
g = gen01()
print(next(g))

for g in gen01():
    print(g)
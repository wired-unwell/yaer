#!/usr/bin/env python
import time

## 1) range
start = time.time()
result = sum(range(10000000))
end = time.time()
print(f"\x1b[36mPython (range): {end - start} seconds.\x1b[0m")

## 2) for
start = time.time()
result = 0
for i in range(10000000):
    result = result + i
end = time.time()
print(f"\x1b[36mPython (for): {end - start} seconds.\x1b[0m")

import sys
import time

print('argv', sys.argv)
time.sleep(3)

file = open(sys.argv[1], 'r')
print(file.read())
file.close()

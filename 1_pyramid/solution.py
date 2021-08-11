import sys

max = int(sys.argv[1])
i = 1
spc = ' '
resh = '#'
while i <= max:
	print(f"{spc * (max - i)}{resh * i}")
	i += 1

import sys
import math
 
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
 
discr = b ** 2 - 4 * a * c
x1 = (-b + math.sqrt(discr)) / (2 * a)
x2 = (-b - math.sqrt(discr)) / (2 * a)
print(f"{int(x1)}\n{int(x2)}")

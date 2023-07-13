from vec2D import vec2D
from vec2D import dis
import math

# v1 = vec2D(300, 300)
# v2 = vec2D(320, 320)
# print((v1 + v2).get_tuple())

# print(math.atan2(-52, 12))

# v3 = vec2D(0, 0)
# v3.set_angle(90, 10)
# print(v3.get_tuple())

# v4 = vec2D(1, 0)
# v4.change_mod(100)
# print(v4.get_tuple())

# v5 = vec2D(100, 0)
# v6 = v5.copy()
# v6 - vec2D(-100, 100)
# print(v5.get_tuple())

# def f(a = 0) :
#     a += 100
# n = 0
# f(n)
# print(n)

# v7 = vec2D(0, 0)
# def f2(vec = vec2D(0, 0)) :
#     vec += vec2D(10, 10)
# f2(v7)
# print(v7.get_tuple())

a = 0 
for i in range(10, 1000, 10) :
    a = 1/i
    print(a)
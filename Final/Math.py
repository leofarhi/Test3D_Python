from math import cos, sin, pi

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def lerp(a, b, t):
    return a + (b - a) * t

MAX_VALUE = 360
cos_lst = []
sin_lst = []

# Generate list of cos and sin values
for i in range(MAX_VALUE):
    angle = lerp(-pi, pi, i / MAX_VALUE)
    cos_lst.append(cos(angle))
    sin_lst.append(sin(angle))

def cos(x):
    x = int(x % pi * MAX_VALUE / pi)
    return cos_lst[x%MAX_VALUE]

def sin(x):
    x = int(x % pi * MAX_VALUE / pi)
    return sin_lst[x%MAX_VALUE]
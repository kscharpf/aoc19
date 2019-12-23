import sys
min_x = 0
max_x = 0
x_pos = 0
line = sys.stdin.readline()
for s in line.split(','):
    if s[0] == 'R':
        x_pos += int(s[1:])
    elif s[0] == 'L':
        x_pos -= int(s[1:])
    if x_pos < min_x:
        min_x = x_pos
    if x_pos > max_x:
        max_x = x_pos
print(f"{min_x},{max_x}")




import string

s = "vhsg hr vzw cdbhltr anmc."
for i in range(26):
    out = ""
    for j in range(len(s)):
        idx = string.ascii_lowercase.find(s[j])
        if idx >= 0:
            idx = (idx + i) % 26
            out += string.ascii_lowercase[idx]
        else:
            out += s[j]
    print(out)
    

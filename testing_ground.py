f = open('what_is_menu', mode='r', encoding='utf-8')
s = list(map(str.strip, f.readlines()))
print(s[0])
f.close()
a = input("Enter a word you want to encrypt: ")
d = int(input("Enter a dhift number: "))
b = a.lower
for i in a:
    if i.isalpha():
        n = ord(i) + d
        if n > ord('z'):
            n -= 26
        print(chr(n), end='')
    else:
        print(i, end='')

print("hello world")




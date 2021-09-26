num = [ i for i in range(1,1001)]
sentence = "Practice Problems to Drill List Comprehension in Your Head."


a = [ i for i in range(1,1001) if i % 8 == 0 ] 

b = [ i for i in range(1,1001) if '6' in str(i) ] 

c = len ( [letter for letter in sentence if letter == ' '] )

vogals = ['a', 'e', 'i', 'o', 'u']
d = ''.join([letter for letter in sentence if not (letter in vogals)  ])

e = [ name for name in sentence.split(sep=" ") if len(name) > 5 ]

print(a)
print(b)
print(c)
print(d)
print(e)
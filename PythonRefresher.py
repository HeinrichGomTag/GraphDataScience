##% Graph Data Science Expectation vs Reality
'''
Information not in head, but resources on Internet
'''

#%
# Int - Integer
# Comment
x = 2
print(type(x))

# Float = floating point number
x = 2.1
print(type(x))

# String - list of chars
x = 'bar'
print(type(x))

# Bool = boolean => True / False
x = True
print(type(x))

x = 2 > 3

### Containeres
# List
x = [1, True, 'bar']
print(x)
print(type(x))

# List of lists
a = [1, True, 'bar', [2.3, 6]]
a = [1, [2,2], 3]
a[2]
a[-1]

# Slice a list
a[1:]
a[:2]

a = [2,1]
b = [4,3]
c = a + b

# Add value at the end
c.append(1)

x = {'one': 1, 'two': 2.0}
print(x)
print(type(x))

### Case sensivity
# FU != fu
Fu = 'bar'
Fu

fu

# Identation matters
FU = 'bar'
    FU

## Conditionals
x = 5
if x > 1:
    print('Variable x is positive.')
elif x < 0 and x/2 == -2:
    print('Variable x is 4.')
else:
    print(f'Variable x is {x}')

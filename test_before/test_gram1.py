class A():
    ...

class B(A):
    ...



a=A()
b=B()

j=isinstance(a,A)
j=isinstance(b,A)

j=issubclass(B,B)
j=issubclass(B,A)
j=issubclass(A,B)
print()

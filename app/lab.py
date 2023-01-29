class A:
	def __init__(self):
		a_var = 1

class B:
	def __init__(self):
		self.b_var = 2

class C(A, B, object):
	def ddd(self):
		print(vars(self))

o = B()

print(C.__dict__)
print(C.__bases__)
print(dir(C))
print(vars(o))

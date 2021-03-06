import sys
import os

# import pudb; pu.db

here = os.path.abspath(os.path.dirname(__file__))

module_root = os.path.join(here, "..")
sys.path.append(module_root)

from mesh2d import Matrix, Vector2, add_rotation_to_mtx

# check equality and inequality operations

mtx1 = Matrix((5, 4),[
	 1,  2,  3,  -4,
	 -5,  6,  -7,  8,
	 9, 10, 11, 12,
	13, -14, 15, 16,
	-43, 654, 99, -7
	])

print("---- ----")
print(mtx1)
print("---- ----")

print("col(0) = {}".format(mtx1.column(0)))
print("col(1) = {}".format(mtx1.column(1)))
print("col(2) = {}".format(mtx1.column(2)))
print("col(3) = {}".format(mtx1.column(3)))

print("")

print("row(0) = {}".format(mtx1.row(0)))
print("row(1) = {}".format(mtx1.row(1)))
print("row(2) = {}".format(mtx1.row(2)))
print("row(3) = {}".format(mtx1.row(3)))
print("row(4) = {}".format(mtx1.row(4)))

print("")

try:
	mtx1.column(4)
except ValueError as ve:
	print(ve)


try:
	mtx1.row(5)
except ValueError as ve:
	print(ve)


print("\ntesting column and row methods for Vector2")
vct = Vector2(16, -12)


print("Vector2 row(0) = {}".format(vct.row(0)))
print("Vector2 row(1) = {}".format(vct.row(1)))
print("Vector2 row(2) = {}".format(vct.row(2)))
print("")
print("Vector2 col(0) = {}".format(vct.column(0)))

try:
	vct.row(3)
except ValueError as ve:
	print(ve)

try:
	vct.column(1)
except ValueError as ve:
	print(ve)

print("")

print("\nidentity:")
imtx= Matrix.identity(4)
print(imtx)

print("\nafter multiplication:")
print(mtx1.multiply(imtx))


print("\nzeros:")
print(Matrix.zeros(4))


print("\nones:")
print(Matrix.ones(4))


print("\nsquare mtx:")

sqmtx = Matrix((4,4),
	[
	 -2,  2.5,  3.2,  -4.9,
	 -5.03,  6.2,  -77.05,  1.8,
	 4.32, 10.2, -6.8, 20.6565,
	13.85, -140.1, 0.5, 16.02,
	])

print(sqmtx)


print("\nits inverse mtx:")
invmtx = Matrix((4,4),
	[
	 -9325040787300/6933989939081.,
	 -217545340200/6933989939081.,
	 -1946637968000/6933989939081.,
	 -317752250900/6933989939081.,
	 -637510590150/6933989939081.,
	 -18419924000/6933989939081.,
	 -96342353200/6933989939081.,
	 -68698514960/6933989939081.,
	 615105170580/6933989939081.,
	 -76587367500/6933989939081.,
	 138860528000/6933989939081.,
	 17696635500/6933989939081.,
	 2467479940000/6933989939081.,
	 29379856000/6933989939081.,
	 836076274000/6933989939081.,
	 106201520000/6933989939081.
	])
print(invmtx)


print("\ntheir multiplication:")
print(sqmtx.multiply(invmtx))


import math

print("\n2d scaling x5:")
print(Matrix.scale2d((0., 0.), (5., 5.)))


print("\n2d scaling x5 from center (15, 15):")
print(Matrix.scale2d((15., 15.), (5., 5.)))


print("\ncheck that matrix-vector multiplication works")
scale_mtx = Matrix.scale2d((10., 20.), (3., -8.))

print("Matrix*Matrix:")
print(scale_mtx.multiply(Matrix((3,1), [5., 5., 1.])))

print("Matrix*Vector2:")
print(scale_mtx.multiply(Vector2(5., 5.)))

print("Matrix*Vector2 and cut off 3rd component:")
print(scale_mtx.multiply(Vector2(5., 5.)).values[:-1])


print("\ntest matrix indexing (getting)")
mtx = Matrix((3,3),
	[
		100, 101, 102,
		110, 111, 112,
		120, 121, 122
	])

print(mtx)
print("[0, 0]:")
print mtx.loc[(0,0)]
print("[0, 1]:")
print mtx.loc[(0,1)]
print("[0, 2]:")
print mtx.loc[(0,2)]
print("[1, 0]:")

print mtx.loc[(1,0)]
print("[1, 1]:")
print mtx.loc[(1,1)]
print("[1, 2]:")
print mtx.loc[(1,2)]

print("[2, 0]:")
print mtx.loc[(2,0)]
print("[2, 1]:")
print mtx.loc[(2,1)]
print("[2, 2]:")
print mtx.loc[(2,2)]

try:
	print("[3, 2]:")
	print mtx.loc[(3,2)]
except IndexError as er:
	print (er)

try:
	print("[0, 5]:")
	print mtx.loc[(0,5)]
except IndexError as er:
	print (er)




print("\ntest matrix indexing (setting)")


mtx.loc[(0,0)] = 900
mtx.loc[(0,1)] = 901
mtx.loc[(0,2)] = 902

mtx.loc[(1,0)] = 910
mtx.loc[(1,1)] = 911
mtx.loc[(1,2)] = 912

mtx.loc[(2,0)] = 920
mtx.loc[(2,1)] = 921
mtx.loc[(2,2)] = 922

print(mtx)

try:
	mtx.loc[(2,3)] = 922
except IndexError as er:
	print (er)


try:
	mtx.loc[(3,1)] = 922
except IndexError as er:
	print (er)


print("\ntest adding angle to rotation mtx:")
rotmtx = Matrix.rotate2d((0, 0), 0.5*math.pi)
print("before:")
print(rotmtx)

add_rotation_to_mtx(rotmtx, 0.25*math.pi)
print("after:")
print(rotmtx)
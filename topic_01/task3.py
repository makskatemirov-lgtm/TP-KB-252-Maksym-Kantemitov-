def discriminant(a, b, c):
    return b ** 2 - 4 * a * c


a = 1
b = -5
c = 6

D = discriminant(a, b, c)

print("Дискримінант:", D)

if D > 0:
    print("Рівняння має два дійсних корені.")
elif D == 0:
    print("Рівняння має один дійсний корінь.")
else:
    print("Рівняння не має дійсних коренів.")
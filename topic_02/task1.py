def discriminant(a, b, c):
    return b ** 2 - 4 * a * c


def find_roots(a, b, c):
    if a == 0:
        print("Це не квадратне рівняння (a не може дорівнювати 0)")
        return

    d = discriminant(a, b, c)

    if d > 0:
        x1 = (-b + d ** 0.5) / (2 * a)
        x2 = (-b - d ** 0.5) / (2 * a)
        print(f"Два корені: x1 = {x1}, x2 = {x2}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"Один корінь: x = {x}")
    else:
        print("Дійсних коренів немає (дискримінант від'ємний)")


find_roots(1, -3, 2)
find_roots(1, 2, 1)
find_roots(1, 0, 1)
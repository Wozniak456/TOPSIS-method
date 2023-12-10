import math

from prettytable import PrettyTable


def print_matrix(matrix):
    formatted_matrix = [["{:.4f}".format(element) for element in row] for row in matrix]
    table = PrettyTable()
    table.field_names = [f'{i + 1}K' for i in range(len(formatted_matrix[0]))]
    for row in formatted_matrix:
        table.add_row(row)
    print(table)


def normalize_matrix(matrix):
    n, m = len(matrix), len(matrix[0])
    r_matrix = [[0] * m for _ in range(n)]

    for k in range(m):
        column_square_root = math.sqrt(sum(matrix[j][k] ** 2 for j in range(n)))

        for j in range(n):
            r_matrix[j][k] = matrix[j][k] / column_square_root

    return r_matrix


def weighted_matrix(normalized_matrix, weight_array):
    n, m = len(normalized_matrix), len(normalized_matrix[0])
    for k in range(m):
        for j in range(n):
            normalized_matrix[j][k] *= weight_array[k]
    return normalized_matrix


def get_pis_nis(weighted_matrix):
    n, m = len(weighted_matrix), len(weighted_matrix[0])
    nis = []
    pis = []
    for k in range(m):
        column_values = [row[k] for row in weighted_matrix]
        pis.append(max(column_values))
        nis.append(min(column_values))
    return pis, nis


def get_distance(weighted_matrix, pis, nis):
    n, m = len(weighted_matrix), len(weighted_matrix[0])
    distance_to_pis = []
    distance_to_nis = []
    for k in range(n):
        sum1, sum2 = 0, 0
        for j in range(m):
            sum1 += (weighted_matrix[k][j] - pis[j])**2
            sum2 += (weighted_matrix[k][j] - nis[j])**2
        distance_to_pis.append(math.sqrt(sum1))
        distance_to_nis.append(math.sqrt(sum2))
    return distance_to_pis, distance_to_nis


def get_c(distance_to_pis, distance_to_nis):
    c_array = []
    for i in range(len(distance_to_pis)):
        c_array.append(distance_to_nis[i] / (distance_to_pis[i] + distance_to_nis[i]))
    return c_array


if __name__ == '__main__':
    a_count = 15  # кількість альтернатив
    k_count = 9
    mx_str = """ 
 2  5  4  8  4  4  4  8  9 
 10  9  4  4  6  6  5  9  8 
 7  7  4  3  10  2  10  4  4 
 7  3  7  8  2  7  2  7  2 
 8  8  9  4  7  4  8  8  2 
 2  2  10  2  9  3  8  3  6 
 6  8  5  4  6  8  2  9  8 
 3  9  6  6  1  4  7  10  7 
 5  7  10  3  7  10  4  5  7 
 7  1  8  4  1  6  2  1  7 
 7  2  10  7  4  6  9  9  7 
 6  5  7  1  8  5  8  4  10 
 3  3  4  9  4  1  5  5  3 
 9  9  9  4  8  7  1  6  6 
 4  8  1  9  6  2  2  3  2 
"""
    weight_array = [0.16, 0.17, 0.07, 0.02, 0.14, 0.07, 0.12, 0.09, 0.16]
    # weight_array = [0.3, 0.4, 0.3]
    matrix = [([int(number) for number in line.split()]) for line in mx_str.split('\n') if line.strip()]

    print_matrix(matrix)
    print()

    print('weight array is normalized' if sum(weight_array) == 1 else 'weight array is not normalized')
    matrix = normalize_matrix(matrix)
    print('Нормалізовані оцінки')
    print_matrix(matrix)
    matrix = weighted_matrix(matrix, weight_array)
    print('Зважені Нормалізовані оцінки')
    print_matrix(matrix)
    pis, nis = get_pis_nis(matrix)
    print("PIS")
    for el in pis:
        print(round(el, 4), end=' ')
    print("\nNIS")
    for el in nis:
        print(round(el, 4), end=' ')

    dist_pis, dist_nis = get_distance(matrix, pis, nis)
    print("\n\nDistance To PIS:")
    for el in dist_pis:
        print(round(el, 4), end=' ')

    print("\nDistance To NIS:")
    for el in dist_nis:
        print(round(el, 4), end=' ')

    c = get_c(dist_pis, dist_nis)
    print('\n\nC array:')
    for el in c:
        print(round(el, 4), end=' ')
    c_sorted = sorted(c, reverse=True)

    print(f"\n\nSorted C: ")
    for el in c_sorted:
        print(round(el, 4), end=' ')
    for i in range(len(c)):
        if c[i] == c_sorted[0]:
            print(f"\n\nЗгідно із впорядкуванням альтернатива {i+1} – найкращий вибір. (Ітерація з 1)")
    print()
    c_sorted_indices = sorted(range(len(c)), key=lambda k: c[k], reverse=True)
    for el in range(len(c_sorted)):
        original_index = c_sorted_indices[el]
        value = c_sorted[el]
        print(f"A{original_index+1}: {round(value,4)}")



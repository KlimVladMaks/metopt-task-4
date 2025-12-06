# Состояние портфеля в начале первого этапа
S1 = (100, 800, 400, 600)

# Размеры пакетов для операций с активами
L = (25, 200, 100)

# Размеры комиссий для операций с активами
c = (0.04, 0.07, 0.05)

# Минимально допустимые стоимости активов
S_min = (30, 150, 100, 0)

# Коэффициенты изменения стоимости активов на трёх этапах
w_k = {
    1: (1.115, 1.061, 1.051),
    2: (0.93, 0.995, 1.003),
    3: (1.02, 1.04, 1.024)
}


def Cost(x):
    cost = 0
    for i in range(3):
        if x[i] > 0:
            cost += x[i] * L[i] * (1 + c[i])
        elif x[i] < 0:
            cost += x[i] * L[i] * (1 - c[i])
    return cost


def T_x(S, x):
    S_after_x = S.copy()
    for i in range(3):
        S_after_x[i] += x[i] * L[i]
    S_after_x[3] -= Cost(x)
    return S_after_x


def T_w(S, k):
    S_after_w = S.copy()
    for i in range(3):
        S_after_w[i] *= w_k[k][i]


def T(S, x, k):
    S_after_x = T_x(S.copy(), x)
    S_after_w = T_w(S_after_x, k)
    return S_after_w


def is_S_valid(S):
    return all(S[i] >= S_min[i] for i in range(4))


def is_x_valid(S, x, k):
    S_after_x = T_x(S.copy(), x)
    if not is_S_valid(S_after_x):
        return False
    S_after_w = T_w(S_after_x, k)
    if not is_S_valid(S_after_w):
        return False
    return True


def discretize_S(S, DCs):
    discretized = S.copy()
    for i in range(4):
        discretized[i] = round(S[i] / DCs[i]) * DCs[i]
    return discretized


def max_exp(S, k):
    pass


def solve():
    V = {}

    S3s = []
    for cb1 in range(30, 1900, 25):
        for cb2 in range(150, 1900, 200):
            for dep in range(100, 1900, 100):
                for sds in range(0, 1900, 100):
                    S3 = (cb1, cb2, dep, sds)
                    if is_S_valid(S3):
                        S3s.append(S3)
    
    x3s = []
    for _x1 in range(-5, 5):
        for _x2 in range(-5, 5):
            for _x3 in range(-5, 5):
                x3 = (_x1, _x2, _x3)
                x3s.append(x3)
    
    optimal_x = None
    max_value = -float('inf')

    V[3] = {}

    for S3 in S3s:
        for x3 in x3s:
            if is_x_valid(S3, x3, 3):
                S4_exp = T(S3, x3, 3)
                if S4_exp > max_value:
                    optimal_x = x3
                    max_value = S4_exp
        V[3][S3] = (optimal_x, max_value)
        optimal_x = None
        max_value = -float('inf')
    
    # ==============================================

    S2s = []
    for cb1 in range(30, 1900, 25):
        for cb2 in range(150, 1900, 200):
            for dep in range(100, 1900, 100):
                for sds in range(0, 1900, 100):
                    S2 = (cb1, cb2, dep, sds)
                    if is_S_valid(S2):
                        S2s.append(S2)
    
    x2s = []
    for _x1 in range(-5, 5):
        for _x2 in range(-5, 5):
            for _x3 in range(-5, 5):
                x2 = (_x1, _x2, _x3)
                x2s.append(x2)
    
    optimal_x = None
    max_value = -float('inf')

    V[2] = {}

    for S2 in S2s:
        for x2 in x2s:
            if is_x_valid(S2, x2, 2):
                S3_exp = T(S2, x2, 2)
                value = V[3][S3_exp]
                if value > max_value:
                    optimal_x = x2
                    max_value = value
        V[2][S2] = (optimal_x, max_value)
        optimal_x = None
        max_value = -float('inf')
    
    # =============================================

    x1s = []
    for _x1 in range(-5, 5):
        for _x2 in range(-5, 5):
            for _x3 in range(-5, 5):
                x1 = (_x1, _x2, _x3)
                x1s.append(x1)
    
    optimal_x = None
    max_value = -float('inf')

    for x1 in x1s:
        if is_x_valid(S1, x1, 1):
            S2_exp = T(S1, x1, 1)
            value = V[2][S2_exp]
            if value > max_value:
                optimal_x = x2
                max_value = value
    
    print(optimal_x, max_value)


def main():
    pass


if __name__ == "__main__":
    solve()

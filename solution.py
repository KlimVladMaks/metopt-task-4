# Состояние портфеля в начале первого этапа
S_1 = (100, 800, 400, 600)

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


def discretize_S(S):
    DC = (10, 10, 10, 10)
    discretized = S.copy()
    for i in range(4):
        discretized[i] = round(S[i] / DC[i]) * DC[i]
    return discretized


def solve():
    DS = 100
    LOWER_VALUE_LIMITS_3 = (30, 150, 100, 0)
    UPPER_VALUE_LIMITS_3 = (1000, 1000, 1000, 1000)

    S3s = []

    for cb1 in range(LOWER_VALUE_LIMITS_3[0], UPPER_VALUE_LIMITS_3[0], DS):
        for cb2 in range(LOWER_VALUE_LIMITS_3[1], UPPER_VALUE_LIMITS_3[1], DS):
            for dep in range(LOWER_VALUE_LIMITS_3[2], UPPER_VALUE_LIMITS_3[2], DS):
                for sds in range(LOWER_VALUE_LIMITS_3[3], UPPER_VALUE_LIMITS_3[3], DS):
                    S3s.append((cb1, cb2, dep, sds))
    
    for S3 in S3s:
        for x1 in range(0, 10):
            for x2 in range(0, 10):
                for x3 in range(0, 10):
                    print(x1)


def main():
    pass


if __name__ == "__main__":
    solve()

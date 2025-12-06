S1 = (100, 800, 400, 600)

L = (25, 200, 100)

c = (0.04, 0.07, 0.05)

S_min = (30, 150, 100, 0)

w = {
    1: {
        1: (1.20, 1.10, 1.07),
        2: (1.05, 1.02, 1.03),
        3: (0.80, 0.95, 1.00),
    },
    2: {
        1: (1.4, 1.15, 1.01),
        2: (1.05, 1.00, 1.00),
        3: (0.60, 0.90, 1.00),
    },
    3: {
        1: (1.15, 1.12, 1.05),
        2: (1.05, 1.01, 1.01),
        3: (0.70, 0.94, 1.00),
    },
}

p = {
    1: {
        1: 0.60,
        2: 0.30,
        3: 0.10,
    },
    2: {
        1: 0.30,
        2: 0.20,
        3: 0.50,
    },
    3: {
        1: 0.40,
        2: 0.40,
        3: 0.20,
    },
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
    S_after_x = list(S)
    for i in range(3):
        S_after_x[i] += x[i] * L[i]
    S_after_x[3] -= Cost(x)
    return tuple(S_after_x)


def T_w(S, k):
    S_positive = list(S)
    w_positive = w[k][1]
    for i in range(3):
        S_positive[i] *= w_positive[i]
    
    S_neutral = list(S)
    w_neutral = w[k][2]
    for i in range(3):
        S_neutral[i] *= w_neutral[i]
    
    S_negative = list(S)
    w_negative = w[k][3]
    for i in range(3):
        S_negative[i] *= w_negative[i]
    
    Sps = (
        (S_positive, p[k][1]),
        (S_neutral, p[k][2]),
        (S_negative, p[k][3]),
    )
    
    return Sps


def T(S, x, k):
    S_after_x = T_x(S, x)
    Sps_after_w = T_w(S_after_x, k)
    return Sps_after_w


def calc_math_exp(Sps, k, V=None):
    math_exp = None

    if V is not None:
        try:
            S_positive = Sps[0][0]
            p_positive = Sps[0][1]
            positive_value = V[k][S_positive][1]

            S_neutral = Sps[1][0]
            p_neutral = Sps[1][1]
            neutral_value = V[k][S_neutral][1]

            S_negative = Sps[2][0]
            p_negative = Sps[2][1]
            negative_value = V[k][S_negative][1]
        
            math_exp = (
                (positive_value * p_positive)
                + (neutral_value * p_neutral)
                + (negative_value * p_negative)
            )
        
        except:
            return -float('inf')
    
    else:
        S_positive = Sps[0][0]
        p_positive = Sps[0][1]

        S_neutral = Sps[1][0]
        p_neutral = Sps[1][1]

        S_negative = Sps[2][0]
        p_negative = Sps[2][1]

        math_exp = (
            (sum(S_positive) * p_positive)
            + (sum(S_neutral) * p_neutral)
            + (sum(S_negative) * p_negative)
        )
    
    return math_exp


def is_S_valid(S):
    return all(S[i] >= S_min[i] for i in range(4))


def is_Sps_valid(Sps):
    for Sp in Sps:
        if not is_S_valid(Sp[0]):
            return False
    return True


def is_x_valid(S, x, k):
    S_after_x = T_x(S, x)
    if not is_S_valid(S_after_x):
        return False
    S_after_w = T_w(S_after_x, k)
    for S in S_after_w:
        if not is_S_valid(S[0]):
            return False
    return True


def discretize_S(S, DCs):
    discretized = list(S)
    for i in range(4):
        discretized[i] = round(S[i] / DCs[i]) * DCs[i]
    return tuple(discretized)


def discretize_Sps(Sps, DCs):
    discretized = []
    for Sp in Sps:
        discretized.append([
            discretize_S(Sp[0], DCs),
            Sp[1]
        ])
    return tuple(discretized)


def solve():
    V = {}

    K3_CB1 = (30, 1000, 100)
    K3_CB2 = (150, 1000, 100)
    K3_DEP = (100, 1000, 100)
    K3_SDS = (0, 1000, 100)

    K3_X1 = (-5, 5)
    K3_X2 = (-5, 5)
    K3_X3 = (-5, 5)

    K2_CB1 = (30, 1000, 100)
    K2_CB2 = (150, 1000, 100)
    K2_DEP = (100, 1000, 100)
    K2_SDS = (0, 1000, 100)

    K2_X1 = (-5, 5)
    K2_X2 = (-5, 5)
    K2_X3 = (-5, 5)

    K1_X1 = (-5, 5)
    K1_X2 = (-5, 5)
    K1_X3 = (-5, 5)

    DCS = [100, 100, 100, 100]


    # ==========

    S3s = []

    for cb1 in range(K3_CB1[0], K3_CB1[1], K3_CB1[2]):
        for cb2 in range(K3_CB2[0], K3_CB2[1], K3_CB2[2]):
            for dep in range(K3_DEP[0], K3_DEP[1], K3_DEP[2]):
                for sds in range(K3_SDS[0], K3_SDS[1], K3_SDS[2]):
                    S3 = (cb1, cb2, dep, sds)
                    if is_S_valid(S3):
                        S3s.append(S3)
    
    x3s = []
    for _x1 in range(K3_X1[0], K3_X1[1]):
        for _x2 in range(K3_X2[0], K3_X2[1]):
            for _x3 in range(K3_X3[0], K3_X3[1]):
                x3 = (_x1, _x2, _x3)
                x3s.append(x3)
    
    V[3] = {}
    
    optimal_x = None
    max_value = -float('inf')

    for S3 in S3s:
        for x3 in x3s:
            if is_x_valid(S3, x3, 3):
                S4ps = T(S3, x3, 3)
                math_exp = calc_math_exp(S4ps, 4)
                if math_exp > max_value:
                    optimal_x = x3
                    max_value = math_exp
        V[3][S3] = (optimal_x, max_value)
        optimal_x = None
        max_value = -float('inf')

    # ==========

    S2s = []

    for cb1 in range(K2_CB1[0], K2_CB1[1], K2_CB1[2]):
        for cb2 in range(K2_CB2[0], K2_CB2[1], K2_CB2[2]):
            for dep in range(K2_DEP[0], K2_DEP[1], K2_DEP[2]):
                for sds in range(K2_SDS[0], K2_SDS[1], K2_SDS[2]):
                    S2 = (cb1, cb2, dep, sds)
                    if is_S_valid(S2):
                        S2s.append(S2)
    
    x2s = []
    for _x1 in range(K2_X1[0], K2_X1[1]):
        for _x2 in range(K2_X2[0], K2_X2[1]):
            for _x3 in range(K2_X3[0], K2_X3[1]):
                x2 = (_x1, _x2, _x3)
                x2s.append(x2)

    V[2] = {}
    
    optimal_x = None
    max_value = -float('inf')
    best_S3ps = None

    for S2 in S2s:
        for x2 in x2s:
            if is_x_valid(S2, x2, 2):
                S3ps = T(S2, x2, 2)
                S3ps = discretize_Sps(S3ps, DCS)
                math_exp = calc_math_exp(S3ps, 3, V)
                if math_exp > max_value:
                    optimal_x = x2
                    max_value = math_exp
                    best_S3ps = S3ps
        V[2][S2] = (optimal_x, max_value, best_S3ps)
        optimal_x = None
        max_value = -float('inf')
        best_S3ps = None
    
    # ==========

    x1s = []
    for _x1 in range(K1_X1[0], K1_X1[1]):
        for _x2 in range(K1_X2[0], K1_X2[1]):
            for _x3 in range(K1_X3[0], K1_X3[1]):
                x1 = (_x1, _x2, _x3)
                x1s.append(x1)
    
    V[1] = {}
    
    optimal_x = None
    max_value = -float('inf')
    best_S2ps = None

    for x1 in x1s:
        if is_x_valid(S1, x1, 1):
            S2ps = T(S1, x1, 1)
            S2ps = discretize_Sps(S2ps, DCS)
            math_exp = calc_math_exp(S2ps, 2, V)
            if math_exp > max_value:
                optimal_x = x1
                max_value = math_exp
                best_S2ps = S2ps
    V[1][S1] = (optimal_x, max_value, best_S2ps)

    print(max_value)


if __name__ == "__main__":
    solve()

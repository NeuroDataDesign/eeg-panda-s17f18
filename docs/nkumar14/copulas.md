- Want wide class (beyond normal) of multivariate dists
- Separate marginal and joint behavior
    - F(x\_1, ... x\_k)
    - Look at each marginal: F\_x\_i(x\_i) = intgrate across all other marginals
    - F(x\_1, ... x\_k) = C {F\_1(x\_1), ... , F\_k(x\_k)}
    - X ~ F, F(X) ~ U
    - Remove tails and such by focusing on F\_i(x\_i)
    - C then looks how they jointly behave

### Copulas:

- d-dimensional copula is fxn C from [0, 1]^d -> [0, 1]
- C(u\_1, ... , u\_d) is nondecreasing fxn of each u
- C(1, ... , u\_i, ... , 1) = u\_i

### Drawbacks

1. Non-parametric estimations of density suffer from CoD
2. EMD is costly to compute

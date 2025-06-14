
def post_checks(N, a, r):
    """Classically checks that r is even, then returns the factors."""

    if r % 2:
        factors = (a ** (r // 2) + 1) % N, (a ** (r // 2) - 1) % N
        message = (f'The period r = {r} is even.'
                   f'\nTherefore, N = ({a}^({r}/2) + 1) * ({a}^({r}/2) - 1) mod N = {factors[0]} * {factors[1]}'
                   f'\nThe factors of N = {15} are {factors[0]} and {factors[1]}.')
        return True, factors, message

    else:
        factors = 0  # Won't be used
        message = f'r = {r} is odd. Run again with different {a}.'
        return False, factors, message

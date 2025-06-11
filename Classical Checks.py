import numpy as np
from random import randint


N = 15  # Coprime N

if N % 2 == 0:  # Check if N is even
    print('N is even.'
          'The factors are 2 and '+str(N // 2)+'')

a = randint(2, N)  # Random integer between 2 and N

if np.gcd(a, N) != 1:  # Check if a divides N
    print('Lucky! The random integer is a factor.'
          'The factors of N are: '+str(a)+' and '+str(N // a)+'')
else:
    print('a is not a factor of N.'
          'Continue to the quantum part.')

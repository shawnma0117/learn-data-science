import sys
import pprint
pprint.pprint(sys.path)  # print list in an elegant way

from decimal import getcontext,Decimal
getcontext().prec = 1
Decimal(0.1)+Decimal(0.2)
Decimal('0.3')


import numpy as np

filename = 'budget.csv          '
filename = filename.strip()
filename.upper()

dogs = []
dogs.append('a')
dogs.append('b')
dogs.append('c')
dogs.append('d')
dogs.remove('b')

animal_counts={}
animal_counts['horse'] = 1
animal_counts['cats'] = 2
animal_counts['dogs'] = 5
animal_counts['snakes'] = 0
animal_counts.keys()
animal_counts.values()

dir(animal_counts)  # return attributes and functions
pprint.pprint(dir(animal_counts))
help(animal_counts.copy)


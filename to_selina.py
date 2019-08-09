# author: Doggy Huang
import random


total_num = 100
percent_1 = 0.2
percent_3 = 0.3
percent_coupled_2 = percent_1
percent_single_2 = 1 - percent_1 - percent_coupled_2 - percent_3
percent_2 = percent_coupled_2 + percent_single_2

sum_freq = percent_1 + percent_2 + percent_3
assert abs(sum_freq - 1) < 1e-3, print("Sum of frequent ({}) not equal to 1".format(sum_freq))

num_1 = int(total_num * percent_1)
num_3 = int(total_num * percent_3)
num_single_2 = int(total_num * percent_single_2)

_data = [1]*num_1 + [3]*num_3 + [2] * num_single_2
random.shuffle(_data)

data = []
for val in _data:
	data = data + [1, 2] if val == 1 else data + [val]

# check of love
for i, val in enumerate(data):
	if val == 1:
		assert data[i+1] == 2, print("1 not followed by 2!")

print(data)

#!/usr/bin/python3

import os
import sys

bst = sys.argv[1]
if not os.path.isfile(bst):
    print("BST executable not found--please pass it as an argument")
    sys.exit(1)

num_iter = os.getenv('NUM_ITER', 10)
print(f'num_iter is {num_iter}')

def test_f(fname):
    num_passes = 0
    for j in range(0, num_iter):
        os.system('rm hash_out hash_out2 > /dev/null 2> /dev/null')
        os.system(f'{bst} -hash-workers={i} -input={fname}.txt | grep -v hashGroupTime | sort > hash_out')
        with open('hash_out', 'r') as f:
            with open('hash_out2', 'w') as f2:
                for line in f:
                    line = line.split()
                    tree_ids = sorted(line[1:])
                    print_to_f2 = line[0]
                    for tree_id in tree_ids:
                        print_to_f2 += " "
                        print_to_f2 += tree_id
                    print_to_f2 += "\n"
                    f2.write(print_to_f2)
            
        are_they_different = os.system(f'cmp hash_out2 {fname}.ref > /dev/null 2> /dev/null')
        if are_they_different == 0:
            num_passes = num_passes + 1
    return num_passes
            
for i in range(0, 13): # test simple.txt hashing
    num_passes = test_f('simple')
    print(f'simple.txt -hash-workers={i} passes {num_passes} of {num_iter}')

for i in [1, 2, 4, 8, 16, 32, 64, 128]: # test coarse.txt hashing
    num_passes = test_f('coarse')
    print(f'coarse.txt -hash-workers={i} passes {num_passes} of {num_iter}')
    
for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 65536, 131072]: # test fine.txt hashing
    num_passes = test_f('fine')
    print(f'fine.txt -hash-workers={i} passes {num_passes} of {num_iter}')

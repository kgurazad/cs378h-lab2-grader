#!/usr/bin/python3

import os
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('bst', help='path to BST executable')
ap.add_argument('-s', '--hash', action='store_true', help='pass this flag to test hash')
ap.add_argument('-c', '--comp', action='store_true', help='pass this flag to test comp')
ap.add_argument('-n', '--num_iter', help='number of times each test runs')
args = ap.parse_args()

bst = args.bst
num_iter = args.num_iter
if num_iter is None:
    num_iter = 10
else:
    num_iter = int(num_iter)
    
if not os.path.isfile(bst):
    print("BST executable not found--please pass it as an argument")
    sys.exit(1)

def hash_f(fname, i):
    os.system(f'sort -o {fname}.hash {fname}.hash')
    num_passes = 0
    for j in range(0, num_iter):
        os.system('rm hash_out hash_out2 > /dev/null 2> /dev/null')
        os.system(f'{bst} -hash-workers={i} -data-workers=1 -comp-workers=1 -input={fname}.txt | grep ":" | grep -v group | grep -v Time | sort > hash_out')
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
            
        are_they_different = os.system(f'cmp hash_out2 {fname}.hash > /dev/null 2> /dev/null')
        if are_they_different == 0:
            num_passes = num_passes + 1
    return num_passes

if args.hash:
    print(f'testing hash...')
    
    for i in range(1, 13): # test simple.txt hashing
        num_passes = hash_f('simple', i)
        print(f'simple.txt -hash-workers={i} passes {num_passes} of {num_iter}')
        
    for i in [1, 2, 4, 8, 16, 32, 64, 128]: # test coarse.txt hashing
        num_passes = hash_f('coarse', i)
        print(f'coarse.txt -hash-workers={i} passes {num_passes} of {num_iter}')
            
    for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 65536, 131072]: # test fine.txt hashing
        num_passes = hash_f('fine', i)
        print(f'fine.txt -hash-workers={i} passes {num_passes} of {num_iter}')

def comp_f(fname, i):
    num_passes = 0
    os.system(f'sort -o {fname}.comp {fname}.comp')
    for j in range(0, num_iter):
        os.system('rm comp_out comp_out2 > /dev/null 2> /dev/null')
        os.system(f'{bst} -hash-workers=1 -data-workers=1 -comp-workers={i} -input={fname}.txt | grep "^group " | sort > comp_out')
        with open('comp_out', 'r') as f:
            with open('comp_out2', 'w') as f2:
                for line in f:
                    line = line.split()
                    tree_ids = sorted(line[2:])
                    print_to_f2 = ""
                    for tree_id in tree_ids:
                        print_to_f2 += " "
                        print_to_f2 += tree_id
                    print_to_f2 += "\n"
                    f2.write(print_to_f2)
        os.system(f'sort -o comp_out2 comp_out2')
        are_they_different = os.system(f'cmp comp_out2 {fname}.comp > /dev/null 2> /dev/null')
        if are_they_different == 0:
            num_passes = num_passes + 1
    return num_passes


if args.comp:
    print(f'testing comp...')
    for i in range(1, 13):
        num_passes = comp_f('simple', i)
        print(f'simple.txt -comp-workers={i} passes {num_passes} of {num_iter}')

    for i in [1, 2, 4, 8, 16, 32, 64, 128]:
        num_passes = comp_f('coarse', i)
        print(f'coarse.txt -comp-workers={i} passes {num_passes} of {num_iter}')

    for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 65536, 131072]: # test fine.txt hashing
        num_passes = comp_f('fine', i)
        print(f'fine.txt -comp-workers={i} passes {num_passes} of {num_iter}')

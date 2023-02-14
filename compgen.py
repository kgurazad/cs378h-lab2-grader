#!/usr/bin/python3

import os

for t in ['simple', 'coarse', 'fine']:
    with open(f'{t}.comp', 'r') as f:
        with open(f'{t}.comp2', 'w') as f2:
            for line in f:
                line = line.split()
                tree_ids = sorted(line[2:])
                print_to_f2 = ""
                for tree_id in tree_ids:
                    print_to_f2 += " "
                    print_to_f2 += tree_id
                print(print_to_f2)
                print_to_f2 += "\n"
                f2.write(print_to_f2)
    os.system(f'sort -o {t}.comp2 {t}.comp2')

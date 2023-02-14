#!/usr/bin/python3

for t in ['simple', 'coarse', 'fine']:
    with open(f'{t}.hash', 'r') as f:
        with open(f'{t}.hash2', 'w') as f2:
            for line in f:
                line = line.split()
                tree_ids = sorted(line[1:])
                print_to_f2 = line[0]
                for tree_id in tree_ids:
                    print_to_f2 += " "
                    print_to_f2 += tree_id
                print(print_to_f2)
                print_to_f2 += "\n"
                f2.write(print_to_f2)
                

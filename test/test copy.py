import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import *

print("=== Generating 3-variable input data (A, B, C) ===")

# Generate inputs for 3 variables (A, B, C)
input_data = generate_inputs(3, ['A', 'B', 'C'])

print(f"Generated inputs for variables: {list(input_data.keys())}")
print(f"Total rows: {len(input_data['A'])}")

# Export input data to CSV
with open('test/input.csv', 'w') as f:
    f.write('A,B,C\n')
    for i in range(len(input_data['A'])):
        f.write(f"{input_data['A'][i]},{input_data['B'][i]},{input_data['C'][i]}\n")

print("Exported input data to test/input.csv")

# Compute output for expression: AB + A C' + B C' + A'B'C
output_data = []
for i in range(len(input_data['A'])):
    A = input_data['A'][i]
    B = input_data['B'][i]
    C = input_data['C'][i]

    term1 = A & B
    term2 = A & (1 - C)   # A and not C
    term3 = B & (1 - C)   # B and not C
    term4 = (1 - A) & (1 - B) & C  # not A and not B and C

    out = term1 | term2 | term3 | term4
    output_data.append(out)

print(f"\nGenerated output for expression AB + AC' + BC' + A'B'C: {output_data}")

# Export output data to CSV
with open('test/output.csv', 'w') as f:
    f.write('Output\n')
    for val in output_data:
        f.write(f"{val}\n")

print("Exported output data to test/output.csv")
print("\n=== Test data generation completed ===")

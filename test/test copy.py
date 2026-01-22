import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import *

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

print("=== Generating 4-variable input data ===")

# Generate inputs for 4 variables (A, B, C, D)
input_data = generate_inputs(4, ['A', 'B', 'C', 'D'])

print(f"Generated inputs for 4 variables: {list(input_data.keys())}")
print(f"Total rows: {len(input_data['A'])}")

# Export input data to CSV
with open('test/input.csv', 'w') as f:
    f.write('A,B,C,D\n')
    for i in range(len(input_data['A'])):
        f.write(f"{input_data['A'][i]},{input_data['B'][i]},{input_data['C'][i]},{input_data['D'][i]}\n")

print("Exported input data to test/input.csv")

# Generate output: 1 if the decimal value is prime, 0 otherwise
output_data = []
for i in range(len(input_data['A'])):
    # Convert binary to decimal
    decimal_value = (input_data['A'][i] * 8 + input_data['B'][i] * 4 + 
                     input_data['C'][i] * 2 + input_data['D'][i])
    output_data.append(1 if is_prime(decimal_value) else 0)

print(f"\nGenerated prime detector output: {output_data}")
print(f"Prime numbers in range 0-15: {[i for i in range(16) if is_prime(i)]}")

# Export output data to CSV
with open('test/output.csv', 'w') as f:
    f.write('IsPrime\n')
    for val in output_data:
        f.write(f"{val}\n")

print("Exported output data to test/output.csv")
print("\n=== Test data generation completed ===")

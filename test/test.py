import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import *

print("=== Testing Circuit Implementation ===\n")

# Load input data from CSV
print("Loading input.csv...")
input_data = import_csv_to_inputs_dict('test/input.csv')
print(f"Loaded inputs: {list(input_data.keys())}")
print(f"Total rows: {len(input_data[list(input_data.keys())[0]])}\n")

# Load expected output from CSV
print("Loading output.csv (expected output)...")
expected_output = import_csv_to_inputs_dict('test/output.csv')
print(f"Expected outputs: {list(expected_output.keys())}\n")

# Get input variables
A = input_data['A']
B = input_data['B']
C = input_data['C']
D = input_data['D']

num_rows = len(A)

print("="*70)
print("APPLYING CIRCUIT TRANSFORMATIONS")
print("="*70)
print("Bit3: D [complexity=0]")
print("Bit0: NAND2(NAND2(B, NAND2(B, C)), NAND2(B, NAND2(B, C))) [complexity=3]")
print("Bit2: NAND2(NAND2(A, A), NAND2(C, NAND2(B, B))) [complexity=4]")
print("Bit1: NAND2(NAND2(NAND2(A, A), NAND2(B, B)), NAND2(NAND2(A, A), NAND2(B, B))) [complexity=4]")
print("Combined Complexity: 9")
print("="*70)

# Calculate outputs using the given transformations
computed_output = {
    'Bit0': [],
    'Bit1': [],
    'Bit2': [],
    'Bit3': []
}

# Store intermediate values for detailed truth table
truth_table = []

for i in range(num_rows):
    a, b, c, d = A[i], B[i], C[i], D[i]
    
    row_data = {
        'Row': i,
        'A': a, 'B': b, 'C': c, 'D': d
    }
    
    # Bit3: D
    bit3 = d
    row_data['Bit3 = D'] = bit3
    
    # Bit0: NAND2(NAND2(B, NAND2(B, C)), NAND2(B, NAND2(B, C)))
    bit0_step1 = NAND2(b, c)
    bit0_step2 = NAND2(b, bit0_step1)
    bit0 = NAND2(bit0_step2, bit0_step2)
    row_data['Bit0: NAND2(B; C)'] = bit0_step1
    row_data['Bit0: NAND2(B; prev)'] = bit0_step2
    row_data['Bit0: NAND2(prev; prev)'] = bit0_step2
    row_data['Bit0 = NAND2(NAND2(B; NAND2(B; C)); NAND2(B; NAND2(B; C)))'] = bit0
    
    # Bit2: NAND2(NAND2(A, A), NAND2(C, NAND2(B, B)))
    bit2_step1 = NAND2(a, a)
    bit2_step2 = NAND2(b, b)
    bit2_step3 = NAND2(c, bit2_step2)
    bit2 = NAND2(bit2_step1, bit2_step3)
    row_data['Bit2: NAND2(A; A)'] = bit2_step1
    row_data['Bit2: NAND2(B; B)'] = bit2_step2
    row_data['Bit2: NAND2(C; NAND2(B; B))'] = bit2_step3
    row_data['Bit2 = NAND2(NAND2(A; A); NAND2(C; NAND2(B; B)))'] = bit2
    
    # Bit1: NAND2(NAND2(NAND2(A, A), NAND2(B, B)), NAND2(NAND2(A, A), NAND2(B, B)))
    bit1_step1 = NAND2(a, a)
    bit1_step2 = NAND2(b, b)
    bit1_step3 = NAND2(bit1_step1, bit1_step2)
    bit1 = NAND2(bit1_step3, bit1_step3)
    row_data['Bit1: NAND2(A; A)'] = bit1_step1
    row_data['Bit1: NAND2(B; B)'] = bit1_step2
    row_data['Bit1: NAND2(NAND2(A; A); NAND2(B; B))'] = bit1_step3
    row_data['Bit1 = NAND2(NAND2(NAND2(A; A); NAND2(B; B)); NAND2(NAND2(A; A); NAND2(B; B)))'] = bit1
    
    truth_table.append(row_data)
    
    computed_output['Bit0'].append(bit0)
    computed_output['Bit1'].append(bit1)
    computed_output['Bit2'].append(bit2)
    computed_output['Bit3'].append(bit3)

# Export detailed truth table to CSV
import csv
import os
output_file = 'test/truth_table_detailed.csv'
print(f"\nExporting detailed truth table to '{output_file}'...")

# Remove old file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

with open(output_file, 'w', newline='') as f:
    if truth_table:
        headers = list(truth_table[0].keys())
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(truth_table)

print("✓ Exported detailed truth table with all intermediate gate outputs\n")

# Compare results
print("\n" + "="*70)
print("COMPARISON")
print("="*70)
print(f"{'Row':<5} {'Input':<10} {'Computed':<15} {'Expected':<15} {'Match':<7}")
print("-" * 70)

all_match = True
matches = 0

for i in range(num_rows):
    input_str = f"{A[i]}{B[i]}{C[i]}{D[i]}"
    computed_str = f"{computed_output['Bit0'][i]}{computed_output['Bit1'][i]}{computed_output['Bit2'][i]}{computed_output['Bit3'][i]}"
    expected_str = f"{expected_output['Bit0'][i]}{expected_output['Bit1'][i]}{expected_output['Bit2'][i]}{expected_output['Bit3'][i]}"
    
    row_match = (computed_str == expected_str)
    if row_match:
        matches += 1
    else:
        all_match = False
    
    match_symbol = "✓" if row_match else "✗"
    print(f"{i:<5} {input_str:<10} {computed_str:<15} {expected_str:<15} {match_symbol:<7}")

print("="*70)
print(f"\nRESULT: {matches}/{num_rows} rows match")

if all_match:
    print("✓ TEST PASSED: Circuit implementation is CORRECT!")
    print("  All computed outputs match the expected outputs.")
else:
    print("✗ TEST FAILED: Circuit implementation does NOT match expected output.")
    print(f"  {num_rows - matches} row(s) have mismatches.")

print("="*70)

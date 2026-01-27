"""
Circuit Generator - Generates input and output CSV files from circuit expression
"""
import csv
import re
import itertools
from pathlib import Path
from utils import *
# Gate implementations

def extract_variables(circuit_expr):
    """Extract unique input variables from circuit expression"""
    # Find all variable patterns: single letters (A-Z) or letter+digit (A1, A2, etc.)
    variables = set(re.findall(r'\b([A-Z]\d*)\b', circuit_expr))
    return sorted(list(variables))


def evaluate_circuit(circuit_expr, variable_values):
    """Evaluate circuit expression with given variable values"""
    # Replace variables with their values
    expr = circuit_expr
    for var, val in variable_values.items():
        expr = re.sub(r'\b' + var + r'\b', str(val), expr)
    
    # Normalize gate names (handle both NAND and NAND2 formats)
    expr = re.sub(r'\bNAND\(', 'NAND2(', expr)
    expr = re.sub(r'\bAND\(', 'AND2(', expr)
    expr = re.sub(r'\bOR\(', 'OR2(', expr)
    expr = re.sub(r'\bNOR\(', 'NOR2(', expr)
    expr = re.sub(r'\bXOR\(', 'XOR2(', expr)
    expr = re.sub(r'\bXNOR\(', 'XNOR2(', expr)
    
    # Evaluate the expression
    result = eval(expr)
    return result


def generate_io_files(circuit_file, output_dir='I-O'):
    """Generate input.csv and output.csv from circuit expression file"""
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read circuit expressions (multiple lines)
    with open(circuit_file, 'r') as f:
        circuit_lines = [line.strip() for line in f if line.strip()]
    
    # Check for "No Outputs" format (inputs only)
    if len(circuit_lines) > 0 and circuit_lines[0].upper() == 'NO OUTPUTS':
        print("Mode: Input Generation Only (No Outputs)\n")
        
        # Second line should contain space-separated input variables
        if len(circuit_lines) < 2:
            print("Error: 'No Outputs' mode requires a second line with input variable names")
            return
        
        # Parse input variables from second line
        variables = circuit_lines[1].split()
        variables = sorted(variables)
        
        print(f"Input variables: {variables}")
        
        # Generate all possible input combinations
        num_vars = len(variables)
        num_rows = 2 ** num_vars
        
        print(f"Generating {num_rows} input combinations...")
        
        # Create input combinations
        input_data = []
        
        for values in itertools.product([0, 1], repeat=num_vars):
            var_map = dict(zip(variables, values))
            input_data.append(var_map)
        
        # Write input.csv
        input_file = Path(output_dir) / 'input.csv'
        with open(input_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=variables)
            writer.writeheader()
            writer.writerows(input_data)
        
        print(f"\nGenerated {input_file}")
        print(f"No output.csv created (input generation only)")
        
        # Display input table preview
        print("\nInput Table Preview (first 8 rows):")
        print(" | ".join(variables))
        print("-" * (len(variables) * 4))
        for i, input_row in enumerate(input_data[:8]):
            input_str = " | ".join(str(input_row[v]) for v in variables)
            print(input_str)
        if len(input_data) > 8:
            print(f"... ({len(input_data) - 8} more rows)")
        
        return
    
    # Normal mode: process circuit expressions
    print(f"Found {len(circuit_lines)} circuit expression(s)\n")
    
    # Process each circuit expression
    all_circuits = []
    output_names = []
    all_variables = set()
    
    for i, circuit_line in enumerate(circuit_lines):
        # Extract circuit expression (remove complexity annotation if present)
        circuit_expr = re.sub(r'\s*\[complexity=\d+\]', '', circuit_line)
        
        # Check if line has format "OutputName : Expression"
        if ':' in circuit_expr:
            parts = circuit_expr.split(':', 1)
            output_name = parts[0].strip()
            circuit_expr = parts[1].strip()
            output_names.append(output_name)
        else:
            output_name = f'Output{i+1}' if len(circuit_lines) > 1 else 'Output'
            output_names.append(output_name)
        
        print(f"{output_name}: {circuit_expr}")
        
        # Extract variables from this circuit
        variables = extract_variables(circuit_expr)
        all_variables.update(variables)
        
        all_circuits.append(circuit_expr)
    
    # Get sorted list of all unique variables
    variables = sorted(list(all_variables))
    print(f"\nInput variables: {variables}")
    
    # Generate all possible input combinations
    num_vars = len(variables)
    num_rows = 2 ** num_vars
    
    print(f"Generating {num_rows} input combinations...")
    
    # Create input combinaoutput_names[i]
    input_data = []
    output_data = []
    
    for values in itertools.product([0, 1], repeat=num_vars):
        # Create variable mapping
        var_map = dict(zip(variables, values))
        input_data.append(var_map)
        
        # Evaluate all circuits for this input combination
        output_row = {}
        for i, circuit_expr in enumerate(all_circuits):
            output_name = output_names[i]
            output_val = evaluate_circuit(circuit_expr, var_map)
            output_row[output_name] = output_val
        
        output_data.append(output_row)
    
    # Write input.csv
    input_file = Path(output_dir) / 'input.csv'
    with open(input_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=variables)
        writer.writeheader()
        writer.writerows(input_data)
    
    print(f"\nGenerated {input_file}")
    
    # Write output.csv
    output_file = Path(output_dir) / 'output.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_names)
        writer.writeheader()
        writer.writerows(output_data)
    
    print(f"Generated {output_file}")
    
    # Display truth table
    print("\nTruth Table:")
    header = " | ".join(variables) + " | " + " | ".join(output_names)
    print(header)
    print("-" * len(header))
    for i, input_row in enumerate(input_data):
        input_str = " | ".join(str(input_row[v]) for v in variables)
        output_str = " | ".join(str(output_data[i][out]) for out in output_names)
        print(f"{input_str} | {output_str}")


if __name__ == '__main__':
    circuit_file = 'circuit.txt'
    output_directory = 'I-O'
    
    print("=== Circuit Generator ===\n")
    generate_io_files(circuit_file, output_directory)
    print("\nDone! Input and output files generated successfully.")

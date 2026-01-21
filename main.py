from utils import *

if __name__ == '__main__':
    with open('log_output.log', 'w') as f:
        # Configuration
        input_filename = 'test/input.csv'
        output_filename = 'test/output.csv'
        gates_filename = 'test/gates_list.csv'
        
        f.write("=== Circuit Maker - BFS Search ===\n\n")
        
        # Load input data
        f.write(f"Loading input data from {input_filename}...\n")
        input_data = import_csv_to_inputs_dict(input_filename)
        f.write(f"Inputs: {list(input_data.keys())}\n")
        f.write(f"Input values:\n")
        for key, val in input_data.items():
            f.write(f"  {key}: {val}\n")
        
        # Load output data (target)
        f.write(f"\nLoading target output from {output_filename}...\n")
        output_data = import_csv_to_inputs_dict(output_filename)
        # Correctly identify target output column - use first column
        target_key = list(output_data.keys())[0]
        target_output = output_data[target_key]
        f.write(f"Target output column: '{target_key}'\n")
        f.write(f"Target output values: {target_output}\n")
        
        # Load available gates
        f.write(f"\nLoading gates from {gates_filename}...\n")
        gates_list = import_gates_from_file(gates_filename)
        f.write(f"Loaded {len(gates_list)} gates: {[g['name'] for g in gates_list]}\n")
        
        # Perform tree-based circuit search
        f.write("\n" + "="*50 + "\n")
        f.write("Starting Tree-Based Circuit Search\n")
        f.write("="*50 + "\n")
        
        solution = tree_circuit_search(input_data, target_output, gates_list, max_complexity=10, log_file=f)
        
        f.write("\n" + "="*50 + "\n")
        if solution:
            f.write("=== SOLUTION FOUND ===\n")
            f.write(f"Circuit Expression: {solution}\n")
            print(f"Solution found: {solution}")
        else:
            f.write("=== NO SOLUTION FOUND ===\n")
            f.write("Try increasing max_complexity or adding more gates.\n")
            print("No solution found. Check log_output.txt for details.")
        f.write("="*50 + "\n")

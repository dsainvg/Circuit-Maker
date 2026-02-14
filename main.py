from utils import *

if __name__ == '__main__':
    with open('log_output.log', 'w') as f:
        # Configuration
        input_filename = 'I-O/input.csv'
        output_filename = 'I-O/output.csv'
        gates_filename = 'I-O/gates_list.csv'
        use_parallel_complexity = True  # True = max depth (parallel), False = sum (serial)
        
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
        target_outputs = {key: val for key, val in output_data.items()}
        f.write(f"Target outputs: {list(target_outputs.keys())}\n")
        for key, val in target_outputs.items():
            f.write(f"  {key}: {val}\n")
        
        # Validate row sizes match
        input_row_count = len(next(iter(input_data.values())))
        output_row_count = len(next(iter(target_outputs.values())))
        if input_row_count != output_row_count:
            error_msg = f"ERROR: Row count mismatch - Input has {input_row_count} rows, Output has {output_row_count} rows\n"
            f.write(f"\n{error_msg}")
            print(error_msg)
            exit(1)
        
        # Load available gates
        f.write(f"\nLoading gates from {gates_filename}...\n")
        gates_list = import_gates_from_file(gates_filename)
        f.write(f"Loaded {len(gates_list)} gates: {[g['name'] for g in gates_list]}\n")
        
        # Perform tree-based circuit search
        f.write("\n" + "="*50 + "\n")
        f.write("Starting Tree-Based Circuit Search\n")
        f.write(f"Searching for {len(target_outputs)} output(s)\n")
        f.write("="*50 + "\n")
        
        solutions, combined_complexity = tree_circuit_search_multi(input_data, target_outputs, gates_list, max_complexity=1000, use_parallel_complexity=use_parallel_complexity, log_file=f)
        
        f.write("\n" + "="*50 + "\n")
        if solutions:
            f.write("=== SOLUTION FOUND ===\n")
            for output_name in sorted(solutions.keys()):
                solution = solutions[output_name]
                f.write(f"{output_name}: {solution}\n")
                print(f"{output_name}: {solution}")
            f.write(f"\nCombined Complexity: {combined_complexity}\n")
            print(f"\nCombined Complexity: {combined_complexity}")
            
            # Extract and print unique gates used
            gate_usage, gate_instances = extract_gate_usage_from_solutions(solutions, gates_list)
            if gate_usage:
                f.write("\n=== GATES USED (SUMMARY) ===\n")
                print("\n=== GATES USED (SUMMARY) ===")
                for gate_name in sorted(gate_usage.keys()):
                    info = gate_usage[gate_name]
                    f.write(f"{gate_name}: Count={info['count']}, Complexity={info['complexity']}, Total Contribution={info['total_contribution']}\n")
                    print(f"{gate_name}: Count={info['count']}, Complexity={info['complexity']}, Total Contribution={info['total_contribution']}")
            
            if gate_instances:
                # Deduplicate gate instances - keep unique ones only
                unique_instances = {}
                for instance in gate_instances:
                    gate_call = instance['gate_call']
                    if gate_call not in unique_instances:
                        unique_instances[gate_call] = instance
                
                f.write("\n=== GATE INSTANCES (DETAILED) ===\n")
                print("\n=== GATE INSTANCES (DETAILED) ===")
                for gate_call in sorted(unique_instances.keys()):
                    instance = unique_instances[gate_call]
                    f.write(f"{instance['gate_call']} - Complexity: {instance['complexity']}\n")
                    print(f"{instance['gate_call']} - Complexity: {instance['complexity']}")
        else:
            f.write("=== NO SOLUTION FOUND ===\n")
            f.write("Try increasing max_complexity or adding more gates.\n")
            print("No solution found. Check log_output.log for details.")
        f.write("="*50 + "\n")

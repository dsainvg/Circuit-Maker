# Logic gate implementations and truth table generation utilities
import itertools
from collections import defaultdict
import time

def NOT(a):
    return 1 ^ (a)

def AND2(a, b):
    return a & b

def OR2(a, b):
    return a | b

def NOR2(a, b):
    return 1 ^ (a | b)

def NAND2(a, b):
    return 1 ^ (a & b)

def XOR2(a, b):
    return a ^ b

def XNOR2(a, b):
    return 1 ^ (a ^ b)

# 3-input logic gates
def OR3(a, b, c):
    return a | b | c

def NAND3(a, b, c):
    return 1 ^ (a & b & c)

def AND3(a, b, c):
    return a & b & c

def NOR3(a, b, c):
    return 1 ^ (a | b | c)

# 4-input logic gates
def NOR4(a, b, c, d):
    return 1 ^ (a | b | c | d)

def NAND4(a, b, c, d):
    return 1 ^ (a & b & c & d)

def AND4(a, b, c, d):
    return a & b & c & d

def OR4(a, b, c, d):
    return a | b | c | d


# Input generator
def generate_inputs(num_vars, var_names=None):
    """
    Generate all possible binary input combinations for given number of variables.
    
    Args:
        num_vars: Number of input variables
        var_names: Optional list of variable names. If None, uses ['A', 'B', 'C', ...]
    
    Returns:
        Dictionary with variable names as keys and arrays of bits as values
        Example for 2 vars: {'A': [0, 0, 1, 1], 'B': [0, 1, 0, 1]}
    """
    num_rows = 1 << num_vars  # 2^num_vars using bit shift
    
    # Generate variable names if not provided
    if var_names is None:
        var_names = [chr(65 + i) for i in range(num_vars)]  # A, B, C, ...
    
    inputs_dict = {}
    
    # Generate each variable's bit pattern using bitwise operations
    for i in range(num_vars):
        bit_position = num_vars - 1 - i
        inputs_dict[var_names[i]] = [(row >> bit_position) & 1 for row in range(num_rows)]
    
    return inputs_dict


# Gate mapping
GATE_MAP = {
    'NOT': (NOT, 1),
    'AND2': (AND2, 2),
    'OR2': (OR2, 2),
    'NOR2': (NOR2, 2),
    'NAND2': (NAND2, 2),
    'XOR2': (XOR2, 2),
    'XNOR2': (XNOR2, 2),
    'AND3': (AND3, 3),
    'OR3': (OR3, 3),
    'NAND3': (NAND3, 3),
    'NOR3': (NOR3, 3),
    'AND4': (AND4, 4),
    'OR4': (OR4, 4),
    'NAND4': (NAND4, 4),
    'NOR4': (NOR4, 4)
}


def import_gates_from_file(filename):
    """
    Import gates from a CSV file with gate information.
    
    Args:
        filename: Path to CSV file containing gate information
                 Format: gate_name,num_inputs,complexity
                 Example:
                 gate_name,num_inputs,complexity
                 AND2,2,1
                 OR3,3,2
    
    Returns:
        List of dictionaries with gate information
        Example: [{'name': 'AND2', 'func': <function>, 'inputs': 2, 'complexity': 1}, ...]
    """
    gates_list = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return gates_list
    
    # Skip header line
    for line in lines[1:]:
        if not line.strip() or line.strip().startswith('#'):
            continue
        
        parts = line.strip().split(',')
        if len(parts) < 3:
            continue
        
        gate_name = parts[0].strip().upper()
        num_inputs = int(parts[1].strip())
        complexity = int(parts[2].strip())
        
        if gate_name in GATE_MAP:
            func, expected_inputs = GATE_MAP[gate_name]
            if num_inputs != expected_inputs:
                print(f"Warning: Gate '{gate_name}' input mismatch - expected {expected_inputs}, got {num_inputs}")
            gates_list.append({
                'name': gate_name,
                'func': func,
                'inputs': num_inputs,
                'complexity': complexity
            })
        else:
            print(f"Warning: Unknown gate '{gate_name}' - skipping")
    
    return gates_list


def analyze_and_filter_inputs(input_data, target_outputs, log_file=None):
    """
    Analyze input data and remove redundant/useless inputs before search.
    
    Returns:
        Tuple of (filtered_inputs, removed_info)
    """
    filtered = {}
    removed = {
        'constant': [],      # Inputs with all same value
        'duplicates': [],    # Inputs identical to others
        'exact_match': {}    # Inputs that exactly match outputs
    }
    
    # Check each input
    for inp_name, inp_bits in input_data.items():
        # Check if constant (all 0s or all 1s)
        unique_values = set(inp_bits)
        if len(unique_values) == 1:
            removed['constant'].append((inp_name, list(unique_values)[0]))
            if log_file:
                log_file.write(f"  Removing {inp_name}: constant value {list(unique_values)[0]}\n")
            continue
        
        # Check if duplicate of an already-kept input
        is_duplicate = False
        for kept_name, kept_bits in filtered.items():
            if inp_bits == kept_bits:
                removed['duplicates'].append((inp_name, kept_name))
                if log_file:
                    log_file.write(f"  Removing {inp_name}: duplicate of {kept_name}\n")
                is_duplicate = True
                break
        
        if is_duplicate:
            continue
        
        # Check if it exactly matches any output (still keep it, but note it)
        for out_name, out_bits in target_outputs.items():
            if inp_bits == out_bits:
                removed['exact_match'][out_name] = inp_name
                if log_file:
                    log_file.write(f"  Note: {inp_name} exactly matches output {out_name}\n")
        
        # Keep this input
        filtered[inp_name] = inp_bits
    
    if log_file and (removed['constant'] or removed['duplicates']):
        log_file.write(f"\n  Reduced inputs: {len(input_data)} -> {len(filtered)}\n")
    
    return filtered, removed


def analyze_gate_characteristics(gates_list):
    """
    Analyze available gates and categorize them by functionality.
    This helps prioritize gate selection during search.
    
    Returns:
        Dictionary with gate categories and metadata
    """
    categories = {
        'inverting': [],      # NOT, NAND, NOR, XNOR
        'and_like': [],       # AND, NAND
        'or_like': [],        # OR, NOR
        'xor_like': [],       # XOR, XNOR
        'by_input_count': defaultdict(list),  # Grouped by number of inputs
        'by_complexity': defaultdict(list),   # Grouped by complexity
        'min_complexity': {},  # Minimum complexity for each gate type
    }
    
    for gate in gates_list:
        name = gate['name']
        inputs = gate['inputs']
        complexity = gate.get('complexity', 1)
        
        # Categorize by functionality
        if 'NOT' in name or 'NAND' in name or 'NOR' in name or 'XNOR' in name:
            categories['inverting'].append(gate)
        
        if 'AND' in name:
            categories['and_like'].append(gate)
        
        if 'OR' in name:
            categories['or_like'].append(gate)
        
        if 'XOR' in name:
            categories['xor_like'].append(gate)
        
        # Group by input count
        categories['by_input_count'][inputs].append(gate)
        
        # Group by complexity
        categories['by_complexity'][complexity].append(gate)
        
        # Track minimum complexity for each type
        gate_type = name.rstrip('234')  # Remove number suffix
        if gate_type not in categories['min_complexity']:
            categories['min_complexity'][gate_type] = complexity
        else:
            categories['min_complexity'][gate_type] = min(
                categories['min_complexity'][gate_type], complexity
            )
    
    return categories


def should_try_gate_combination(gate, combo, target_bits, current_signals, gate_categories):
    """
    Intelligent filtering using HARD LOGIC RULES ONLY - no assumptions.
    Returns True if this gate+combination is worth trying.
    
    Logic-based redundancy elimination:
    1. Redundant gate usage (AND3(A,A,B) = AND2(A,B) if AND2 exists)
    2. XOR with same inputs always = 0
    3. Logically equivalent patterns
    """
    gate_name = gate['name']
    num_inputs = gate['inputs']
    
    # Count unique inputs
    input_counts = {}
    for node in combo:
        node_id = id(node)
        input_counts[node_id] = input_counts.get(node_id, 0) + 1
    
    unique_input_ids = len(input_counts)
    max_repetition = max(input_counts.values()) if input_counts else 0
    
    # HARD RULE 1: XOR with identical inputs = 0 (always)
    if 'XOR' in gate_name:
        if unique_input_ids == 1:  # XOR(A, A) = 0
            return False
    
    # HARD RULE 2: If smaller gate exists, don't use redundant larger gate
    # AND3(A, A, B) = AND2(A, B) if AND2 is available
    # AND4(A, A, A, B) = AND2(A, B) if AND2 is available
    has_and2 = any(g['name'] == 'AND2' for g in gate_categories['and_like'])
    has_or2 = any(g['name'] == 'OR2' for g in gate_categories['or_like'])
    has_and3 = any(g['name'] == 'AND3' for g in gate_categories['and_like'])
    has_or3 = any(g['name'] == 'OR3' for g in gate_categories['or_like'])
    
    if gate_name == 'AND3' and has_and2:
        # If 2 inputs are the same, AND3(A,A,B) = AND2(A,B)
        if max_repetition >= 2:
            return False
    
    if gate_name == 'AND4' and has_and2:
        # If 3+ inputs are the same, AND4(A,A,A,B) = AND2(A,B)
        if max_repetition >= 3:
            return False
        # If 2 pairs of same inputs, AND4(A,A,B,B) = AND2(AND2(A,A), AND2(B,B)) = AND2(A,B)
        if unique_input_ids == 2 and max_repetition == 2:
            return False
    
    if gate_name == 'AND4' and has_and3:
        # If 2 inputs are the same, AND4(A,A,B,C) = AND3(A,B,C)
        if max_repetition >= 2:
            return False
    
    if gate_name == 'OR3' and has_or2:
        # If 2 inputs are the same, OR3(A,A,B) = OR2(A,B)
        if max_repetition >= 2:
            return False
    
    if gate_name == 'OR4' and has_or2:
        # If 3+ inputs are the same, OR4(A,A,A,B) = OR2(A,B)
        if max_repetition >= 3:
            return False
        # If 2 pairs of same inputs, OR4(A,A,B,B) = OR2(A,B)
        if unique_input_ids == 2 and max_repetition == 2:
            return False
    
    if gate_name == 'OR4' and has_or3:
        # If 2 inputs are the same, OR4(A,A,B,C) = OR3(A,B,C)
        if max_repetition >= 2:
            return False
    
    # HARD RULE 3: NAND3 and NOR3 follow same logic
    has_nand2 = any(g['name'] == 'NAND2' for g in gate_categories['and_like'])
    has_nor2 = any(g['name'] == 'NOR2' for g in gate_categories['or_like'])
    has_nand3 = any(g['name'] == 'NAND3' for g in gate_categories['and_like'])
    has_nor3 = any(g['name'] == 'NOR3' for g in gate_categories['or_like'])
    
    if gate_name == 'NAND3' and has_nand2:
        if max_repetition >= 2:
            return False
    
    if gate_name == 'NAND4' and has_nand2:
        if max_repetition >= 3 or (unique_input_ids == 2 and max_repetition == 2):
            return False
    
    if gate_name == 'NAND4' and has_nand3:
        if max_repetition >= 2:
            return False
    
    if gate_name == 'NOR3' and has_nor2:
        if max_repetition >= 2:
            return False
    
    if gate_name == 'NOR4' and has_nor2:
        if max_repetition >= 3 or (unique_input_ids == 2 and max_repetition == 2):
            return False
    
    if gate_name == 'NOR4' and has_nor3:
        if max_repetition >= 2:
            return False
    
    # HARD RULE 4: All-identical inputs for certain gates
    if unique_input_ids == 1:
        # AND(A,A,...,A) = A
        # OR(A,A,...,A) = A  
        # These just pass through, redundant with existing signal
        if gate_name in ['AND2', 'AND3', 'AND4', 'OR2', 'OR3', 'OR4']:
            return False
        
        # NAND(A,A,...,A) = NOT(A), NOR(A,A,...,A) = NOT(A)
        # If we have NOT gate, don't use NAND/NOR with identical inputs
        has_not = any(g['name'] == 'NOT' for g in gate_categories['inverting'])
        if has_not and gate_name in ['NAND2', 'NAND3', 'NAND4', 'NOR2', 'NOR3', 'NOR4']:
            return False
    
    return True


# Truth table generator
def generate_truth_table(gate_func, inputs_dict):
    """
    Generate output bits for a logic gate.
    
    Args:
        gate_func: Function that takes input bits and returns output
        inputs_dict: Dictionary with input names as keys and arrays of bits as values
                    Example: {'A': [0, 0, 1, 1], 'B': [0, 1, 0, 1]}
    
    Returns:
        List of output bits
    """
    input_names = list(inputs_dict.keys())
    input_arrays = [inputs_dict[name] for name in input_names]
    
    # Determine number of rows
    num_rows = len(input_arrays[0])
    
    # Validate all arrays have same length
    if not all(len(arr) == num_rows for arr in input_arrays):
        raise ValueError("All input arrays must have the same length")
    
    output_bits = []
    
    # Generate output by iterating through rows
    for row in range(num_rows):
        row_inputs = [arr[row] for arr in input_arrays]
        output = gate_func(*row_inputs)
        output_bits.append(output)
    
    return output_bits

# CSV export/import functions
def export_truth_table_to_csv(truth_table, filename):
    """
    Export truth table to CSV file.
    
    Args:
        truth_table: List of dictionaries from generate_truth_table()
        filename: Path to CSV file to create
    """
    if not truth_table:
        return
    
    keys = list(truth_table[0].keys())
    
    with open(filename, 'w') as f:
        # Write header
        f.write(','.join(keys) + '\n')
        
        # Write rows
        for row in truth_table:
            f.write(','.join(str(row[key]) for key in keys) + '\n')


def import_csv_to_inputs_dict(filename):
    """
    Import CSV file and convert to inputs dictionary format.
    
    Args:
        filename: Path to CSV file
    
    Returns:
        Dictionary with variable names as keys and arrays of bits as values
        Example: {'A': [0, 0, 1, 1], 'B': [0, 1, 0, 1], 'Output': [0, 1, 0, 1]}
    """
    inputs_dict = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        if not lines:
            return inputs_dict
        
        # Parse header
        headers = lines[0].strip().split(',')
        
        # Initialize arrays for each column
        for header in headers:
            inputs_dict[header] = []
        
        # Parse data rows
        for line in lines[1:]:
            if line.strip():
                values = line.strip().split(',')
                for i, header in enumerate(headers):
                    inputs_dict[header].append(int(values[i]))
    
    return inputs_dict


class CircuitNode:
    """Tree node representing a circuit signal or gate output."""
    def __init__(self, name, bits, gate_name=None, inputs=None, complexity=0):
        self.name = name
        self.bits = bits
        self.gate_name = gate_name
        self.inputs = inputs or []
        self.complexity = complexity
    
    def __repr__(self):
        if self.gate_name:
            # Recursively build expression from inputs
            input_exprs = [str(inp) for inp in self.inputs]
            return f"{self.gate_name}({', '.join(input_exprs)})"
        return self.name


def tree_circuit_search(input_data, target_output, gates_list, max_complexity=10, log_file=None):
    """
    Search for circuit using tree structure with complexity-based depth.
    Uses intelligent pruning rules to reduce search space.
    
    Args:
        input_data: Dictionary of input signals {name: [bits]}
        target_output: Target output bit array
        gates_list: List of available gates with complexity
        max_complexity: Maximum total complexity allowed
        log_file: File handle for logging
    
    Returns:
        String expression of solution circuit or None
    """
    # Analyze and filter input data
    if log_file:
        log_file.write("\n=== INPUT DATA ANALYSIS ===\n")
    
    target_outputs = {'output': target_output}
    filtered_inputs, removed_info = analyze_and_filter_inputs(input_data, target_outputs, log_file)
    
    # Check if output already exists in removed exact matches
    if 'output' in removed_info['exact_match']:
        matched_input = removed_info['exact_match']['output']
        if log_file:
            log_file.write(f"\n*** SOLUTION FOUND (Complexity 0) ***\n")
            log_file.write(f"Expression: {matched_input}\n")
            log_file.write(f"Complexity: 0\n")
        return f"{matched_input} [complexity=0]"
    
    if log_file:
        log_file.write("================================\n")
    
    # Analyze gates for pruning rules
    gate_categories = analyze_gate_characteristics(gates_list)
    
    if log_file:
        log_file.write("\n=== INTELLIGENT PRUNING ENABLED ===\n")
        log_file.write(f"Available gates: {len(gates_list)}\n")
        log_file.write(f"Inverting gates: {[g['name'] for g in gate_categories['inverting']]}\n")
        log_file.write(f"AND-like gates: {[g['name'] for g in gate_categories['and_like']]}\n")
        log_file.write(f"OR-like gates: {[g['name'] for g in gate_categories['or_like']]}\n")
        log_file.write(f"XOR-like gates: {[g['name'] for g in gate_categories['xor_like']]}\n")
        log_file.write("================================\n")
    
    # Global signal pool - use filtered inputs
    all_signals = {name: CircuitNode(name, bits, complexity=0) for name, bits in filtered_inputs.items()}
    checked = set(tuple(bits) for bits in filtered_inputs.values())
    nodes_explored = 0
    nodes_skipped = 0
    
    # Timing tracking
    start_time = time.time()
    last_report_time = start_time
    last_report_count = 0
    
    for complexity in range(1, max_complexity + 1):
        if log_file:
            log_file.write(f"\n--- Searching complexity level {complexity} ---\n")
        
        new_signals = {}
        
        # Try each gate
        for gate in gates_list:
            gate_complexity = gate.get('complexity', 1)
            
            if gate_complexity > complexity:
                continue
            
            signal_list = list(all_signals.values())
            
            # Use combinations_with_replacement (no permutations - gates are commutative)
            for input_combo in itertools.combinations_with_replacement(signal_list, gate['inputs']):
                # Calculate total complexity: sum of unique input complexities + gate complexity
                unique_nodes = {id(node): node for node in input_combo}
                total_complexity = sum(node.complexity for node in unique_nodes.values()) + gate_complexity
                
                # Only create nodes at current complexity level
                if total_complexity != complexity:
                    continue
                
                # INTELLIGENT PRUNING: Skip unpromising combinations
                if not should_try_gate_combination(gate, input_combo, target_output, all_signals, gate_categories):
                    nodes_skipped += 1
                    continue
                
                nodes_explored += 1
                
                # Progress reporting every 1000 nodes
                if nodes_explored % 1000 == 0:
                    current_time = time.time()
                    interval_time = current_time - last_report_time
                    total_time = current_time - start_time
                    nodes_in_interval = nodes_explored - last_report_count
                    
                    print(f"\r[Progress] Explored: {nodes_explored:,} | Interval: {interval_time:.2f}s ({nodes_in_interval} nodes) | Total: {total_time:.2f}s | Complexity: {complexity}", end='', flush=True)
                    
                    last_report_time = current_time
                    last_report_count = nodes_explored
                
                # Compute output
                input_bits = [node.bits for node in input_combo]
                output_bits = [gate['func'](*bits) for bits in zip(*input_bits)]
                
                # Build expression for logging
                input_exprs = [str(node) for node in input_combo]
                expression = f"{gate['name']}({', '.join(input_exprs)})"
                
                if log_file:
                    log_file.write(f"  Trying: {expression} [complexity={total_complexity}] -> {output_bits}\n")
                
                # Check if solution
                if output_bits == target_output:
                    solution_node = CircuitNode(
                        f"OUT_{nodes_explored}",
                        output_bits,
                        gate['name'],
                        list(input_combo),
                        total_complexity
                    )
                    if log_file:
                        log_file.write(f"\n*** SOLUTION FOUND ***\n")
                        log_file.write(f"Expression: {solution_node}\n")
                        log_file.write(f"Complexity: {total_complexity}\n")
                        log_file.write(f"Nodes explored: {nodes_explored}\n")
                    return f"{solution_node} [complexity={total_complexity}]"
                
                # Add to new signals if not seen
                bits_tuple = tuple(output_bits)
                if bits_tuple not in checked:
                    checked.add(bits_tuple)
                    new_node = CircuitNode(
                        f"N{nodes_explored}",
                        output_bits,
                        gate['name'],
                        list(input_combo),
                        total_complexity
                    )
                    new_signals[new_node.name] = new_node
        
        # INTELLIGENT SIGNAL POOL MANAGEMENT
        # At higher complexity, limit pool size to most promising signals
        if complexity >= 2 and len(new_signals) > 100:
            # Score signals by their potential usefulness
            scored_signals = []
            for sig_name, sig_node in new_signals.items():
                score = 0
                # Prefer signals with similar bit count to target
                target_ones = sum(target_output)
                signal_ones = sum(sig_node.bits)
                bit_diff = abs(target_ones - signal_ones)
                score += 50 - bit_diff * 2
                
                # Prefer signals with similar transition complexity
                target_trans = sum(1 for i in range(len(target_output)-1) if target_output[i] != target_output[i+1])
                signal_trans = sum(1 for i in range(len(sig_node.bits)-1) if sig_node.bits[i] != sig_node.bits[i+1])
                trans_diff = abs(target_trans - signal_trans)
                score += 30 - trans_diff * 3
                
                # Prefer lower complexity
                score += (20 - sig_node.complexity)
                
                scored_signals.append((score, sig_name, sig_node))
            
            # Keep only top signals
            scored_signals.sort(reverse=True, key=lambda x: x[0])
            new_signals = {name: node for _, name, node in scored_signals[:100]}
            
            if log_file:
                log_file.write(f"  Signal pool filtered: kept top 100 most promising signals\\n")
        
        # Add all new signals to global pool for next iteration
        all_signals.update(new_signals)
        
        if log_file:
            log_file.write(f"\nComplexity {complexity} complete: {nodes_explored} nodes explored, {nodes_skipped} skipped, {len(all_signals)} total signals\n")
    
    # Print newline after progress reporting
    if nodes_explored >= 1000:
        print()  # Move to new line after progress output
    
    return None



def tree_circuit_search_multi(input_data, target_outputs, gates_list, max_complexity=50, log_file=None):
    """
    Channel-based multi-output search optimizing total circuit complexity.
    Uses intelligent pruning rules to reduce search space.
    
    Args:
        input_data: Dictionary of input signals {name: [bits]}
        target_outputs: Dictionary of target outputs {name: [bits]}
        gates_list: List of available gates with complexity
        max_complexity: Maximum total complexity allowed
        log_file: File handle for logging
    
    Returns:
        Tuple of (solutions_dict, combined_complexity) or (None, 0)
    """
    # Analyze and filter input data
    if log_file:
        log_file.write("\n=== INPUT DATA ANALYSIS ===\n")
    
    filtered_inputs, removed_info = analyze_and_filter_inputs(input_data, target_outputs, log_file)
    
    # Check for complexity 0 solutions in exact matches
    solutions = {}
    for out_name, inp_name in removed_info['exact_match'].items():
        solutions[out_name] = f"{inp_name} [complexity=0]"
        if log_file:
            log_file.write(f"\nFound {out_name}: {inp_name} [complexity=0]\n")
    
    if len(solutions) == len(target_outputs):
        if log_file:
            log_file.write("\nAll outputs found in inputs!\n")
        return solutions, 0
    
    if log_file:
        log_file.write("================================\n")
    
    # Analyze gates for pruning rules
    gate_categories = analyze_gate_characteristics(gates_list)
    
    if log_file:
        log_file.write("\n=== INTELLIGENT PRUNING ENABLED ===\n")
        log_file.write(f"Available gates: {len(gates_list)}\n")
        log_file.write(f"Inverting gates: {[g['name'] for g in gate_categories['inverting']]}\n")
        log_file.write(f"AND-like gates: {[g['name'] for g in gate_categories['and_like']]}\n")
        log_file.write(f"OR-like gates: {[g['name'] for g in gate_categories['or_like']]}\n")
        log_file.write(f"XOR-like gates: {[g['name'] for g in gate_categories['xor_like']]}\n")
        log_file.write("================================\n")
    
    # Shared channel pool for all outputs - use filtered inputs
    channels = {name: CircuitNode(name, bits, complexity=0) for name, bits in filtered_inputs.items()}
    checked = set(tuple(bits) for bits in filtered_inputs.values())
    nodes_explored = 0
    nodes_skipped = 0
    solution_nodes = {}  # Track actual CircuitNode objects for solutions
    
    # Timing tracking
    start_time = time.time()
    last_report_time = start_time
    last_report_count = 0
    
    # Channel-based search: build shared signal pool, check all targets each level
    for complexity in range(1, max_complexity + 1):
        if log_file:
            log_file.write(f"\n=== Complexity {complexity} ===\n")
        
        new_channels = {}
        
        for gate in gates_list:
            if gate.get('complexity', 1) > complexity:
                continue
            
            for combo in itertools.combinations_with_replacement(list(channels.values()), gate['inputs']):
                unique_nodes = {id(n): n for n in combo}
                total_comp = sum(n.complexity for n in unique_nodes.values()) + gate.get('complexity', 1)
                if total_comp != complexity:
                    continue
                
                # INTELLIGENT PRUNING: Check against all remaining targets
                remaining_targets = {name: bits for name, bits in target_outputs.items() if name not in solutions}
                if remaining_targets:
                    # Use first remaining target for pruning decisions
                    first_target_bits = next(iter(remaining_targets.values()))
                    if not should_try_gate_combination(gate, combo, first_target_bits, channels, gate_categories):
                        nodes_skipped += 1
                        continue
                
                nodes_explored += 1
                
                # Progress reporting every 1000 nodes
                if nodes_explored % 1000 == 0:
                    current_time = time.time()
                    interval_time = current_time - last_report_time
                    total_time = current_time - start_time
                    nodes_in_interval = nodes_explored - last_report_count
                    remaining = len(target_outputs) - len(solutions)
                    
                    print(f"\r[Progress] Explored: {nodes_explored:,} | Interval: {interval_time:.2f}s ({nodes_in_interval} nodes) | Total: {total_time:.2f}s | Complexity: {complexity} | Remaining: {remaining}", end='', flush=True)
                    
                    last_report_time = current_time
                    last_report_count = nodes_explored
                
                output_bits = [gate['func'](*bits) for bits in zip(*[n.bits for n in combo])]
                bits_tuple = tuple(output_bits)
                
                # Build expression for logging
                input_exprs = [str(node) for node in combo]
                expression = f"{gate['name']}({', '.join(input_exprs)})"
                
                if log_file:
                    log_file.write(f"  Trying: {expression} [complexity={total_comp}] -> {output_bits}\n")
                
                # Check all targets (even if already found - might find better solution)
                for tgt_name, tgt_bits in target_outputs.items():
                    if output_bits == tgt_bits and tgt_name not in solutions:
                        node = CircuitNode(tgt_name, output_bits, gate['name'], list(combo), total_comp)
                        solutions[tgt_name] = f"{node} [complexity={total_comp}]"
                        solution_nodes[tgt_name] = node  # Store the actual node
                        if log_file:
                            log_file.write(f"\n*** SOLUTION FOUND for {tgt_name} ***\n")
                            log_file.write(f"Expression: {node}\n")
                            log_file.write(f"Complexity: {total_comp}\n")
                
                # Always add to channel pool (don't stop even if all found)
                if bits_tuple not in checked:
                    checked.add(bits_tuple)
                    new_node = CircuitNode(
                        f"C{nodes_explored}",
                        output_bits,
                        gate['name'],
                        list(combo),
                        total_comp
                    )
                    new_channels[new_node.name] = new_node
        
        channels.update(new_channels)
        if log_file:
            log_file.write(f"\nComplexity {complexity} complete: {nodes_explored} nodes explored, {nodes_skipped} skipped, {len(channels)} total signals\n")
            if nodes_explored + nodes_skipped > 0:
                skip_rate = (nodes_skipped / (nodes_explored + nodes_skipped)) * 100
                log_file.write(f"Pruning efficiency: {skip_rate:.1f}% of combinations skipped\n")
            remaining = [name for name in target_outputs.keys() if name not in solutions]
            if remaining:
                log_file.write(f"Remaining targets: {remaining}\n")
        
        # Only stop if all found AND we've explored this level completely
        if len(solutions) == len(target_outputs):
            # Calculate combined complexity considering shared subcircuits
            all_nodes = set()
            for node in solution_nodes.values():
                _collect_unique_nodes(node, all_nodes)
            # Count gate complexity for each unique gate node
            gate_map = {g['name']: g.get('complexity', 1) for g in gates_list}
            total_complexity = sum(gate_map.get(n.gate_name, 0) for n in all_nodes if n.gate_name)
            if log_file:
                log_file.write(f"\nAll outputs found! Nodes explored: {nodes_explored}\n")
                log_file.write(f"Combined complexity (with shared subcircuits): {total_complexity}\n")
            # Print newline after progress reporting
            if nodes_explored >= 1000:
                print()  # Move to new line after progress output
            return solutions, total_complexity
    
    if solutions:
        all_nodes = set()
        for node in solution_nodes.values():
            _collect_unique_nodes(node, all_nodes)
        # Count gate complexity for each unique gate node
        gate_map = {g['name']: g.get('complexity', 1) for g in gates_list}
        total_complexity = sum(gate_map.get(n.gate_name, 0) for n in all_nodes if n.gate_name)
        if log_file:
            log_file.write(f"\nCombined complexity (with shared subcircuits): {total_complexity}\n")
        # Print newline after progress reporting
        if nodes_explored >= 1000:
            print()  # Move to new line after progress output
        return solutions, total_complexity
    
    # Print newline after progress reporting
    if nodes_explored >= 1000:
        print()  # Move to new line after progress output
    return None, 0


def _collect_unique_nodes(node, visited):
    """Recursively collect all unique nodes in a circuit tree."""
    if id(node) in {id(n) for n in visited}:
        return
    visited.add(node)
    for inp in (node.inputs or []):
        _collect_unique_nodes(inp, visited)


def extract_gate_usage_from_solutions(solutions_str_dict, gates_list):
    """
    Extract all unique gates used in solutions and calculate their complexity contributions.
    
    Args:
        solutions_str_dict: Dictionary of {output_name: solution_string}
        gates_list: List of available gates with complexity information
        
    Returns:
        Tuple of (gate_usage_dict, gate_instances_list)
        - gate_usage_dict: {gate_name: {'count': int, 'complexity': int, 'total_contribution': int}}
        - gate_instances_list: List of {'gate_call': str, 'complexity': int} for each gate instance
    """
    gate_map = {g['name']: g.get('complexity', 1) for g in gates_list}
    gate_instances = []
    unique_gate_calls = set()
    
    # Parse solution strings to extract gate names and instances
    for output_name, solution_str in solutions_str_dict.items():
        # Extract the expression part (before [complexity=...])
        expr = solution_str.split('[complexity=')[0].strip()
        
        # Extract all gate instances from the expression
        instances = _extract_gate_instances(expr, gate_map)
        gate_instances.extend(instances)
    
    # Deduplicate gate instances
    for instance in gate_instances:
        unique_gate_calls.add(instance['gate_call'])
    
    # Count unique gates by gate type
    gate_usage = {}
    for gate_call in unique_gate_calls:
        # Determine which gate type this is
        for gate_name in gate_map.keys():
            if gate_call.startswith(gate_name + '('):
                if gate_name not in gate_usage:
                    gate_usage[gate_name] = {
                        'count': 0,
                        'complexity': gate_map[gate_name],
                        'total_contribution': 0
                    }
                gate_usage[gate_name]['count'] += 1
                break
    
    # Calculate total contribution for each gate
    for gate_name, info in gate_usage.items():
        info['total_contribution'] = info['count'] * info['complexity']
    
    return gate_usage, gate_instances


def _extract_gate_instances(expr, gate_map):
    """
    Recursively extract all gate instances from an expression string.
    
    Args:
        expr: Expression string like "NAND2(OR2(A2, A3), NOT(A1))"
        gate_map: Dictionary of {gate_name: complexity}
        
    Returns:
        List of {'gate_call': str, 'complexity': int} for each gate instance
    """
    instances = []
    i = 0
    
    while i < len(expr):
        # Try to find a gate name
        found_gate = None
        for gate_name in gate_map.keys():
            if expr[i:i+len(gate_name)] == gate_name and i+len(gate_name) < len(expr) and expr[i+len(gate_name)] == '(':
                found_gate = gate_name
                break
        
        if found_gate:
            # Find the matching closing parenthesis
            start = i + len(found_gate)
            paren_count = 0
            end = start
            
            for j in range(start, len(expr)):
                if expr[j] == '(':
                    paren_count += 1
                elif expr[j] == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        end = j + 1
                        break
            
            # Extract the complete gate call
            gate_call = expr[i:end]
            instances.append({
                'gate_call': gate_call,
                'complexity': gate_map[found_gate]
            })
            
            # Recursively extract gates from the arguments inside this gate
            inner_expr = expr[start+1:end-1]  # Get content between parentheses
            inner_instances = _extract_gate_instances(inner_expr, gate_map)
            instances.extend(inner_instances)
            
            # Continue searching from the end of this gate
            i = end
        else:
            i += 1
    
    return instances

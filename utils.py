# Logic gate implementations and truth table generation utilities

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
    
    Args:
        input_data: Dictionary of input signals {name: [bits]}
        target_output: Target output bit array
        gates_list: List of available gates with complexity
        max_complexity: Maximum total complexity allowed
        log_file: File handle for logging
    
    Returns:
        String expression of solution circuit or None
    """
    import itertools
    
    # Global signal pool - ALL signals available
    all_signals = {name: CircuitNode(name, bits, complexity=0) for name, bits in input_data.items()}
    checked = set(tuple(bits) for bits in input_data.values())
    nodes_explored = 0
    
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
                # Calculate total complexity: sum of input complexities + gate complexity
                total_complexity = sum(node.complexity for node in input_combo) + gate_complexity
                
                # Only create nodes at current complexity level
                if total_complexity != complexity:
                    continue
                
                nodes_explored += 1
                
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
        
        # Add all new signals to global pool for next iteration
        all_signals.update(new_signals)
        
        if log_file:
            log_file.write(f"\nComplexity {complexity} complete: {nodes_explored} nodes explored, {len(all_signals)} total signals\n")
    
    return None


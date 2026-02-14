# Development Guidelines

## Code Quality Standards

### File Headers and Documentation
- Use triple-quoted docstrings at the top of modules to describe purpose
- Example: `"""Circuit Generator - Generates input and output CSV files from circuit expression"""`
- Keep module-level documentation concise and focused on primary purpose

### Function Documentation
- Use docstrings with Args/Returns sections for all non-trivial functions
- Format:
```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    
    Returns:
        Description of return value
    """
```
- Include type information in docstrings when helpful
- Document edge cases and special behaviors

### Naming Conventions
- **Functions**: lowercase_with_underscores (snake_case)
  - Examples: `generate_inputs`, `extract_variables`, `tree_circuit_search`
- **Variables**: lowercase_with_underscores (snake_case)
  - Examples: `input_data`, `gate_name`, `num_inputs`, `circuit_expr`
- **Constants**: UPPERCASE_WITH_UNDERSCORES
  - Example: `GATE_MAP`
- **Classes**: PascalCase
  - Example: `CircuitNode`
- **Private/Internal Functions**: Prefix with underscore
  - Examples: `_collect_unique_nodes`, `_extract_gate_instances`

### Code Formatting
- Use 4 spaces for indentation (no tabs)
- Maximum line length: ~100-120 characters (flexible, prioritize readability)
- Blank lines:
  - Two blank lines between top-level functions
  - One blank line between methods in a class
  - One blank line to separate logical sections within functions
- Whitespace around operators: `a = b + c` not `a=b+c`
- No whitespace inside parentheses: `func(a, b)` not `func( a, b )`

### Import Organization
- Standard library imports first
- Third-party imports second (if any)
- Local module imports last
- Use `from module import *` sparingly, only for utility modules
- Example:
```python
import csv
import re
import itertools
from pathlib import Path
from utils import *
```

## Structural Conventions

### Function Organization
- Place helper functions before main functions that use them
- Group related functions together
- Order functions by complexity: simple utilities first, complex algorithms last
- Keep functions focused on single responsibility

### Error Handling
- Validate input data early (row count matching, file existence)
- Print clear error messages to both console and log files
- Use `exit(1)` for fatal errors that prevent execution
- Example:
```python
if input_row_count != output_row_count:
    error_msg = f"ERROR: Row count mismatch - Input has {input_row_count} rows"
    f.write(f"\n{error_msg}")
    print(error_msg)
    exit(1)
```

### File I/O Patterns
- Use context managers (`with` statements) for all file operations
- Create output directories if they don't exist: `Path(output_dir).mkdir(parents=True, exist_ok=True)`
- Use `pathlib.Path` for cross-platform path handling
- Write to both log files and console for important messages

### CSV Handling
- Use `csv.DictWriter` for writing CSV files with headers
- Use custom parsing for reading (manual line processing)
- Always include headers in CSV files
- Use `newline=''` parameter when opening CSV files for writing

## Semantic Patterns

### Logic Gate Implementation Pattern
- Implement gates as simple functions returning 0 or 1
- Use bitwise operators for efficiency:
  - AND: `a & b`
  - OR: `a | b`
  - XOR: `a ^ b`
  - NOT: `1 ^ a`
  - NAND: `1 ^ (a & b)`
  - NOR: `1 ^ (a | b)`
- Example:
```python
def AND2(a, b):
    return a & b

def NAND2(a, b):
    return 1 ^ (a & b)
```

### Gate Mapping Pattern
- Store gate functions in a dictionary with metadata
- Format: `{gate_name: (function, num_inputs)}`
- Example:
```python
GATE_MAP = {
    'NOT': (NOT, 1),
    'AND2': (AND2, 2),
    'OR2': (OR2, 2),
    # ...
}
```

### Binary Input Generation Pattern
- Use bit shifting for efficient power-of-2 calculations: `1 << num_vars` instead of `2 ** num_vars`
- Generate bit patterns using bitwise operations:
```python
for i in range(num_vars):
    bit_position = num_vars - 1 - i
    inputs_dict[var_names[i]] = [(row >> bit_position) & 1 for row in range(num_rows)]
```
- Use `itertools.product([0, 1], repeat=num_vars)` for simple enumeration

### Regular Expression Patterns
- Extract variables: `r'\b([A-Z]\d*)\b'` (matches A, B, A1, A2, etc.)
- Remove complexity annotations: `r'\s*\[complexity=\d+\]'`
- Word boundary replacements: `re.sub(r'\b' + var + r'\b', str(val), expr)`
- Normalize gate names: `re.sub(r'\bNAND\(', 'NAND2(', expr)`

### Tree/Graph Node Pattern
- Use classes to represent circuit nodes with recursive structure
- Store: name, bits, gate_name, inputs (list of nodes), complexity
- Implement `__repr__` for automatic expression generation
- Example:
```python
class CircuitNode:
    def __init__(self, name, bits, gate_name=None, inputs=None, complexity=0):
        self.name = name
        self.bits = bits
        self.gate_name = gate_name
        self.inputs = inputs or []
        self.complexity = complexity
    
    def __repr__(self):
        if self.gate_name:
            input_exprs = [str(inp) for inp in self.inputs]
            return f"{self.gate_name}({', '.join(input_exprs)})"
        return self.name
```

### BFS Search Pattern
- Use complexity-based level iteration instead of queue
- Track visited states using tuples: `checked = set(tuple(bits) for bits in ...)`
- Deduplicate using bit patterns, not expressions
- Build signal pool incrementally at each complexity level
- Example structure:
```python
for complexity in range(1, max_complexity + 1):
    new_signals = {}
    for gate in gates_list:
        for combo in itertools.combinations_with_replacement(signals, gate['inputs']):
            # Calculate complexity, evaluate gate, check solution
            pass
    all_signals.update(new_signals)
```

### Intelligent Pruning Pattern
- Implement hard logic rules to skip redundant combinations
- Check for identical inputs: `unique_input_ids = len(set(id(node) for node in combo))`
- Skip logically equivalent patterns (e.g., `AND3(A,A,B)` when `AND2` exists)
- Track pruning statistics: `nodes_explored` vs `nodes_skipped`
- Example:
```python
if gate_name == 'XOR' and unique_input_ids == 1:  # XOR(A,A) = 0
    return False
```

### Progress Reporting Pattern
- Report progress every N iterations (e.g., 1000 nodes)
- Use `\r` for in-place console updates: `print(f"\r[Progress] ...", end='', flush=True)`
- Track timing: `time.time()` for intervals and total time
- Print newline after completion: `print()` to move to next line
- Example:
```python
if nodes_explored % 1000 == 0:
    current_time = time.time()
    interval_time = current_time - last_report_time
    print(f"\r[Progress] Explored: {nodes_explored:,} | Time: {interval_time:.2f}s", end='', flush=True)
```

### Multi-Output Optimization Pattern
- Use shared signal pool for all outputs (channel-based approach)
- Check all target outputs at each complexity level
- Calculate combined complexity by counting unique gate nodes
- Recursively collect unique nodes to avoid double-counting shared subcircuits
- Example:
```python
all_nodes = set()
for node in solution_nodes.values():
    _collect_unique_nodes(node, all_nodes)
total_complexity = sum(gate_map.get(n.gate_name, 0) for n in all_nodes if n.gate_name)
```

### Logging Pattern
- Write to log file handle passed as parameter
- Log major phases with separator lines: `"=" * 50`
- Log both high-level progress and detailed attempts
- Include statistics: nodes explored, skipped, pruning efficiency
- Example:
```python
if log_file:
    log_file.write(f"\n=== PHASE NAME ===\n")
    log_file.write(f"Details: {info}\n")
    log_file.write("=" * 50 + "\n")
```

## Frequently Used Code Idioms

### Dictionary Comprehension for Filtering
```python
filtered = {key: val for key, val in data.items() if condition}
```

### Tuple Conversion for Hashing
```python
bits_tuple = tuple(output_bits)
if bits_tuple not in checked:
    checked.add(bits_tuple)
```

### List Comprehension with Zip
```python
output_bits = [gate_func(*bits) for bits in zip(*input_arrays)]
```

### Defaultdict for Grouping
```python
from collections import defaultdict
categories = defaultdict(list)
categories['by_input_count'][inputs].append(gate)
```

### Pathlib for File Operations
```python
from pathlib import Path
Path(output_dir).mkdir(parents=True, exist_ok=True)
output_file = Path(output_dir) / 'output.csv'
```

### Enumerate with Conditional Indexing
```python
for i, item in enumerate(items):
    name = f'Output{i+1}' if len(items) > 1 else 'Output'
```

### Set Operations for Uniqueness
```python
unique_values = set(input_bits)
all_variables = set()
all_variables.update(variables)
```

### Sorting with Custom Keys
```python
sorted_indices = sorted(range(len(names)), key=lambda i: names[i], reverse=True)
sorted_names = [names[i] for i in sorted_indices]
```

## Best Practices

### Performance Optimization
- Use `itertools.combinations_with_replacement` instead of permutations for commutative gates
- Implement state deduplication using sets of tuples
- Limit signal pool size at high complexity levels (keep top N most promising)
- Skip redundant gate combinations using hard logic rules
- Use bitwise operations instead of boolean operators

### Memory Management
- Store only unique bit patterns, not duplicate expressions
- Prune signal pool when it grows too large
- Use generators where possible instead of building large lists
- Clear intermediate data structures when no longer needed

### Maintainability
- Keep functions under 100 lines when possible
- Extract complex logic into helper functions
- Use meaningful variable names that describe content
- Comment complex algorithms and non-obvious optimizations
- Maintain separation between generation and search logic

### Testing and Debugging
- Validate input/output row counts match
- Log detailed information to files for post-analysis
- Print progress to console for user feedback
- Include timing information for performance analysis
- Test with small examples before scaling up

### Configuration Management
- Use CSV files for gate library configuration
- Support multiple circuit expression formats
- Make complexity limits configurable
- Allow customization of output directories
- Keep configuration at top of main execution block

## Common Patterns to Avoid

### Anti-Patterns
- Don't use `eval()` without sanitizing input (only use with controlled gate expressions)
- Don't generate permutations when combinations suffice (gates are commutative)
- Don't store duplicate bit patterns in signal pool
- Don't continue searching after finding all solutions (unless looking for better ones)
- Don't use string concatenation in loops (use list comprehension + join)

### Code Smells
- Long parameter lists (use dictionaries or objects)
- Deeply nested conditionals (extract to functions)
- Magic numbers (define as named constants)
- Duplicate code (extract to shared functions)
- Overly complex expressions (break into intermediate variables)

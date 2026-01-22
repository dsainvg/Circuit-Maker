# Circuit Maker - Development Guidelines

## Code Quality Standards

### Import Organization
- **Wildcard imports**: Use `from utils import *` for internal modules (3/3 files)
- **Standard library imports**: Import specific modules (`itertools`, `collections.deque`)
- **Path manipulation**: Use `sys.path.insert()` for relative imports in test files

### Naming Conventions
- **Functions**: snake_case with descriptive names (`generate_truth_table`, `import_csv_to_inputs_dict`)
- **Variables**: snake_case with clear purpose (`input_filename`, `target_output`, `gates_list`)
- **Constants**: UPPER_CASE for mappings and globals (`GATE_MAP`)
- **Gate functions**: UPPER_CASE matching hardware conventions (`AND2`, `OR3`, `NAND4`)
- **Classes**: PascalCase for tree node structures (`CircuitNode`)

### Documentation Standards
- **Docstrings**: Triple-quoted strings with Args/Returns sections for all public functions
- **Inline comments**: Descriptive comments for complex logic and configuration sections
- **File headers**: Brief module purpose description at top of utility files

## Structural Conventions

### Function Design Patterns
- **Single responsibility**: Each function handles one specific operation
- **Parameter validation**: Check input array lengths and data consistency
- **Error handling**: Graceful handling with informative warning messages
- **Return consistency**: Standardized return types (lists, dictionaries, objects)

### Data Structure Patterns
- **Dictionary-based data**: Use `{variable_name: [bit_array]}` format consistently
- **Gate representation**: Standardized `{'name': str, 'func': callable, 'inputs': int}` structure
- **Tree node structure**: Use classes for complex hierarchical data (`CircuitNode`)
- **Truth table format**: List of dictionaries for tabular data representation

### File I/O Conventions
- **Context managers**: Always use `with open()` for file operations (100% compliance)
- **CSV handling**: Manual parsing with comma separation and header processing
- **Logging patterns**: Structured output with section separators (`===`, `---`)

## Implementation Patterns

### Boolean Logic Operations
- **Bitwise operators**: Use `&`, `|`, `^` for AND, OR, XOR operations
- **Negation pattern**: Use `1 ^ value` for NOT operations consistently
- **Multi-input gates**: Direct operator chaining (`a & b & c` for AND3)

### Algorithm Design
- **Tree-based search**: Use class-based nodes for hierarchical circuit representation
- **Bit manipulation**: Use bit shifts (`1 << num_vars`) for power-of-2 calculations
- **Combinatorial generation**: Leverage `itertools.combinations_with_replacement` for gate inputs
- **Complexity tracking**: Track circuit complexity through node hierarchy
- **Channel-based multi-output**: Optimize for entire circuit by building shared signal pool
- **Signal pool management**: Maintain global pool of all generated signals across complexity levels
- **Complete level exploration**: Continue building channels even after finding solutions to enable signal reuse

### Configuration Management
- **File-based config**: Use separate files for gates, inputs, and outputs
- **Hardcoded paths**: Relative paths in test directory structure
- **Parameter passing**: Use keyword arguments for optional parameters (`max_complexity=5`)

## Internal API Usage Patterns

### Gate Function Integration
```python
# Standard gate definition pattern
def GATE_NAME(a, b, c):
    return boolean_expression

# Gate mapping registration
GATE_MAP = {
    'GATE_NAME': (GATE_NAME, num_inputs)
}
```

### Tree Node Management
```python
# Circuit node creation pattern
node = CircuitNode(name, bits, gate_name, inputs, complexity)

# Expression building through recursion
def __repr__(self):
    if self.gate_name:
        input_exprs = [str(inp) for inp in self.inputs]
        return f"{self.gate_name}({', '.join(input_exprs)})"
    return self.name
```

### Data Processing Pipeline
```python
# Standard data import pattern
input_data = import_csv_to_inputs_dict(filename)
gates_list = import_gates_from_file(gates_filename)

# Single output search
solution = tree_circuit_search(input_data, target_output, gates_list, max_complexity=5)

# Multi-output channel-based search (optimizes for entire circuit)
solutions = tree_circuit_search_multi(input_data, target_outputs_dict, gates_list, max_complexity=10, log_file=f)
```

### Logging and Output
```python
# Structured logging pattern
f.write("=== Section Header ===\n")
f.write(f"Descriptive message: {variable}\n")
f.write("="*50 + "\n")
```

## Code Quality Practices

### Error Prevention
- **Input validation**: Check array lengths and data types before processing
- **Graceful degradation**: Skip unknown gates with warnings rather than crashing
- **Path handling**: Use `os.path.join()` for cross-platform compatibility

### Performance Considerations
- **Early termination**: Stop search when solution found
- **Memory efficiency**: Use generators and iterators where possible
- **Bit operations**: Prefer bitwise operations over arithmetic for boolean logic
- **Complexity bounds**: Use complexity limits to prevent exponential explosion

### Testing Patterns
- **Integration testing**: Test complete workflows from file input to output
- **Function isolation**: Test individual utility functions with known inputs
- **Output verification**: Compare generated results against expected values
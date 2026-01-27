# Circuit Maker - Circuit Generator

A Python-based tool for generating input/output CSV files from circuit expressions and finding circuit implementations using logic gates.

## Overview

This project consists of two main components:
1. **Circuit Generator** (`circuit_generator.py`) - Generates input and output CSV files from circuit expressions
2. **Circuit Finder** (`main.py`) - Finds circuit implementations using available logic gates

## Circuit Generator Usage

The circuit generator reads circuit expressions from `circuit.txt` and automatically generates:
- `I-O/input.csv` - All possible input combinations
- `I-O/output.csv` - Corresponding outputs for each circuit
- Console output with a truth table

### Running the Generator

```bash
python circuit_generator.py
```

## Circuit Expression Formats

The generator supports multiple formats in `circuit.txt`:

### Format 1: Single Circuit Expression

```
NAND2(NAND2(A, NAND2(C, NAND2(A, B))), NAND2(NAND2(B, C), NAND2(NAND2(B, B), NAND2(C, NAND2(A, A))))) [complexity=10]
```

- Single line with one circuit
- Optional `[complexity=N]` annotation (will be ignored)
- Output column named: `Output`
- Input variables: Any uppercase letters (A, B, C, etc.)

**Generated Files:**
- `input.csv`: Columns A, B, C (all combinations)
- `output.csv`: Column Output

### Format 2: Multiple Circuits (No Names)

```
XOR2(A,B)
XOR2(A,NAND(B,C))
OR(C,D)
```

- One circuit per line
- Output columns automatically named: `Output1`, `Output2`, `Output3`, etc.
- Input variables: Any uppercase letters (A, B, C, D, etc.)
- All unique variables from all circuits are combined

**Generated Files:**
- `input.csv`: Columns A, B, C, D (all combinations)
- `output.csv`: Columns Output1, Output2, Output3

### Format 3: Named Circuits

```
B1 : XOR2(A1,A2)
B2 : XOR2(A5,NAND(A3,A4))
B3 : OR(A3,A5)
```

- One circuit per line
- Format: `OutputName : CircuitExpression`
- Output columns use specified names: `B1`, `B2`, `B3`
- Input variables: Letters with optional numbers (A1, A2, A3, etc.)
- Supports any alphanumeric variable names

**Generated Files:**
- `input.csv`: Columns A1, A2, A3, A4, A5 (all combinations)
- `output.csv`: Columns B1, B2, B3

## Supported Logic Gates

The generator supports both 2-input and generic gate names:

### Basic Gates (2-input)
- `NOT(a)` - Inverter
- `AND(a, b)` / `AND2(a, b)` - AND gate
- `OR(a, b)` / `OR2(a, b)` - OR gate
- `NAND(a, b)` / `NAND2(a, b)` - NAND gate
- `NOR(a, b)` / `NOR2(a, b)` - NOR gate
- `XOR(a, b)` / `XOR2(a, b)` - XOR gate
- `XNOR(a, b)` / `XNOR2(a, b)` - XNOR gate

### Multi-input Gates (3-input)
- `OR3(a, b, c)`
- `NAND3(a, b, c)`
- `AND3(a, b, c)`
- `NOR3(a, b, c)`

### Multi-input Gates (4-input)
- `NOR4(a, b, c, d)`
- `NAND4(a, b, c, d)`
- `AND4(a, b, c, d)`
- `OR4(a, b, c, d)`

**Note:** The generator automatically normalizes gate names, so `NAND(A,B)` and `NAND2(A,B)` are equivalent.

## Input Variables

### Variable Naming
- **Simple format**: Single uppercase letters: `A`, `B`, `C`, `Z`
- **Numbered format**: Letter + digit: `A1`, `A2`, `B5`, `X10`
- Variables are automatically detected from circuit expressions
- All unique variables become input columns

### Input Generation
- Generates all possible binary combinations (0 and 1)
- For N variables: 2^N rows
- Examples:
  - 3 variables (A, B, C): 8 rows (000 to 111)
  - 5 variables (A1-A5): 32 rows
  - 10 variables: 1024 rows

## Example Workflows

### Example 1: Simple XOR Circuit

**circuit.txt:**
```
XOR2(A,B)
```

**Run:**
```bash
python circuit_generator.py
```

**Output:**
```
=== Circuit Generator ===

Found 1 circuit expression(s)

Output: XOR2(A,B)

Input variables: ['A', 'B']
Generating 4 input combinations...

Generated I-O\input.csv
Generated I-O\output.csv

Truth Table:
A | B | Output
--------------
0 | 0 | 0
0 | 1 | 1
1 | 0 | 1
1 | 1 | 0
```

### Example 2: Half Adder

**circuit.txt:**
```
Sum : XOR2(A,B)
Carry : AND2(A,B)
```

**Output:**
- `input.csv`: A, B columns (4 rows)
- `output.csv`: Sum, Carry columns (4 rows)

### Example 3: Complex Multi-Circuit

**circuit.txt:**
```
Output1 : NAND2(A1, NAND2(A2, A3))
Output2 : OR3(A1, A2, A4)
Output3 : XOR2(NAND2(A3, A4), A1)
```

**Output:**
- `input.csv`: A1, A2, A3, A4 columns (16 rows)
- `output.csv`: Output1, Output2, Output3 columns (16 rows)

## File Structure

```
Circuit Maker/
├── circuit.txt              # Input: Circuit expressions
├── circuit_generator.py     # Generator script
├── main.py                  # Circuit finder (uses generated files)
├── utils.py                 # Utility functions
├── README.md               # This file
└── I-O/                    # Generated files directory
    ├── input.csv           # Generated inputs
    ├── output.csv          # Generated outputs
    └── gates_list.csv      # Available gates for circuit finder
```

## Tips and Best Practices

1. **Keep circuits readable**: Use whitespace in complex expressions
2. **Name your outputs**: Use Format 3 for clarity in multi-circuit files
3. **Check truth tables**: Verify generated outputs match expectations
4. **Limit variables**: More than 8-10 variables creates very large truth tables
5. **Use both gate names**: `NAND(A,B)` and `NAND2(A,B)` work identically
6. **Nested expressions**: Gates can be nested to any depth

## Integration with Circuit Finder

After generating input/output files, use `main.py` to find circuit implementations:

```bash
python main.py
```

This will:
1. Load `I-O/input.csv` (inputs)
2. Load `I-O/output.csv` (target outputs)
3. Load `I-O/gates_list.csv` (available gates)
4. Search for circuit implementations using BFS
5. Output found solutions with complexity ratings

## Troubleshooting

### Error: "name 'X' is not defined"
- Check that the gate name is supported (see Supported Logic Gates)
- Ensure gate names are spelled correctly

### Error: "dict contains fields not in fieldnames"
- Internal error - restart Python and try again
- Ensure circuit.txt is properly formatted

### Empty output or wrong results
- Verify circuit expressions are syntactically correct
- Check parentheses are balanced
- Ensure variables are uppercase letters

### Too many rows
- Reduce the number of unique input variables
- Consider splitting into smaller circuits

## Advanced Usage

### Custom Output Directory

Edit `circuit_generator.py`:
```python
if __name__ == '__main__':
    circuit_file = 'circuit.txt'
    output_directory = 'custom-output'  # Change this
```

### Adding New Gate Functions

Add to the gate implementations section in `circuit_generator.py`:
```python
def CUSTOM_GATE(a, b, c):
    return your_logic_here
```

## License

This project is provided as-is for educational and circuit design purposes.

# Circuit Maker - Technology Stack

## Programming Language
- **Python 3.x**: Primary development language
- Standard library dependencies only (no external packages required)

## Core Dependencies

### Standard Library Modules
- **itertools**: Combinatorial operations and permutations for gate combinations
- **collections.deque**: Efficient queue operations for tree-based search
- **csv**: CSV file parsing for input/output data
- **os/sys**: File system operations and path management

### File Formats
- **CSV**: Input/output data specification format
- **LOG**: Runtime execution and debugging output

### Development Commands

### Running the Application
```bash
python main.py
```

### Running Tests
```bash
python test/test.py
```

### Project Setup
No additional installation required - uses Python standard library only.

## Build System
- No formal build system required
- Direct Python script execution
- File-based configuration management

## Development Environment
- **IDE**: Any Python-compatible editor
- **Python Version**: 3.6+ (uses f-strings and modern syntax)
- **Operating System**: Cross-platform (Windows, Linux, macOS)

## Data Processing Pipeline
1. **CSV Import**: Custom parsing functions for input/output data
2. **Gate Loading**: Text file parsing for logic gate definitions
3. **Circuit Evaluation**: Pure Python boolean logic operations
4. **Result Export**: File-based logging and output generation

## Performance Characteristics
- **Search Algorithm**: Tree-based search with configurable complexity limits
- **Memory Usage**: Scales with search complexity and gate count
- **Execution Time**: Exponential with circuit complexity
- **Optimization**: Early termination on solution discovery
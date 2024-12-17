# Disk-Based Direct Address Table Toolkit

## Overview
A Python-based tool for creating and querying a key-value mapping backed by **disk-based direct address tables**. This system uses disk seeking to manage key-value data efficiently, making it possible to query large datasets without loading everything into memory.

### Features
- Create `keys.bin` and `values.bin` files for efficient key-value storage.
- Leverages disk seeking for fast data retrieval without the need for full in-memory loading.
- Supports arbitrary-length values stored in `values.bin`.

---

## How It Works

### Data Assembly
Use the `dat_writer.py` script to process a tab-separated file  (e.g. ```python dat_writer.py example_data.psv```)

This creates 2 files that use direct-addressing to create a key-value mapping:
- **`keys.bin`**: Maps integer keys to corresponding a byte position in `values.bin`.
- **`values.bin`**: Stores associated values with length-prefixed encoding for variable-length data.


### Querying
Use the `key_lookup.py` client to retrieve values by key. For example:
```
	$ python key_lookup.py 313
	Train like a warrior, think like a sage	
```

For a given key _k_, the client will:
1. Seek to the _k<sup>th</sup>_ byte in `keys.bin`.
2. Retrieve the position of the corresponding value in `values.bin`.
3. Seek to the value position in `values.bin` and read the value.

---

## Setup

### Prerequisites
- Python 3.x
- Basic knowledge of Python file operations

## Tradeoffs, Limitations, and Future Work

### Tradeoffs
1. **Disk I/O vs Memory Usage**: 
   - This tool trades memory efficiency for disk I/O overhead. While it can handle datasets larger than available memory, disk seeks are inherently slower than in-memory operations. This makes it ideal for scenarios where memory is constrained but not for workloads requiring extremely high throughput.
2. **Sparse Keys**:
   - If the key space is sparse (e.g., keys `1, 1000, 1000000`), the size of `keys.bin` can grow significantly due to wasted space in unused positions. This tradeoff simplifies direct address computation but can lead to inefficient storage for certain datasets.
3. **Lack of Indexing Flexibility**:
   - The current approach uses direct addressing. While this provides fast lookup, it lacks more advanced indexing features, such as range queries or ordered traversal, which are available in database systems or tree-based structures.

### Limitations and Considerations for Future Work
1. **Sequential Access**:
   - The tool is optimized for random access. If the workload primarily involves sequential access, other data structures (e.g., B-trees, hash maps) or databases (e.g., SQLite) may perform better.
2. **Key Space Constraints**:
   - The tool assumes that the key space is bounded and uses direct mapping to byte positions. For unbounded or unpredictable key spaces, a hash-based or more dynamic approach may be necessary.
3. **Performance on Slow Disks**:
   - Performance heavily depends on the underlying disk. Using HDDs instead of SSDs may significantly increase seek times, reducing overall efficiency.
4. **Error Handling**:
   - Currently, the tool assumes well-formed input data and does not handle edge cases like corrupt files, missing keys, or invalid key lookups. These areas could be improved.


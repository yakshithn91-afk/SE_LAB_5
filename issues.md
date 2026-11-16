# Lab 5: Static Analysis Findings

The line numbers below refer to the original `electricity_bill.py` before fixes.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection (B605) | High security | 63 | `os.system` built a shell command from `meterIp`, allowing shell metacharacters to alter the command. | Removed the unused shell helper. No shell is started from user-controlled data. |
| Unsafe XML parsing (B314) | Medium security | 18 | `ElementTree.fromstring` can parse untrusted XML with unsafe entity behavior. | Switched to `defusedxml.ElementTree` and declared the dependency. |
| XML parser import (B405) | Low security | 3 | Bandit flagged the standard XML parser import because it can be unsafe for untrusted input. | Use the hardened `defusedxml` parser for the meter XML. |
| Hardcoded password (B105) | Low security | 13 | An unused clerk password was stored in source. | Removed the unused credential. |
| Mutable default argument (W0102) | Correctness | 42 | `extras={}` is shared across calls and can leak changes between bills. | Default `extras` to `None` and create a fresh dictionary per call. |
| Unused parameter (W0613) | Maintainability | 50 | `currency` was accepted by `averageBill` but never affected the result. | Removed the parameter and updated the call site. |
| Missing file encoding (W1514) | Portability | 57 | JSON output used the platform default encoding. | Open the output file as UTF-8. |
| Naming and documentation (C0103, C0114, C0116) | Maintainability | Multiple | CamelCase names and missing docstrings made the code harder to understand and review. | Renamed functions and variables to snake_case and added module/function docstrings. |
| Whitespace and line length (E302, E203, E501, E225) | Style | 22, 44, 72, 76 | Flake8 found spacing, blank-line, and line-length violations. | Reformatted the module and wrapped long statements. |

## Final analysis

- Pylint: **10.00/10**
- Bandit: **No issues identified**
- Flake8: **No findings**
- The demo output remained the same after fixes.

See `reports/before/` and `reports/after/` for the saved tool output.

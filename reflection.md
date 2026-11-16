# Lab 5: Reflection

The supplied handout asks for four reflection answers but does not include the question text. These responses address the purpose of the tools, the findings, the fixes, and their value to maintenance.

## 1. What did each static analysis tool contribute?

Pylint found code quality and design issues, including the shared mutable default, an unused parameter, inconsistent naming, and missing documentation. Bandit identified the shell command, embedded password, and XML parser risks. Flake8 caught formatting problems such as missing whitespace and a line that exceeded the configured length. Together, the tools covered different kinds of defects.

## 2. Which finding mattered most, and why?

The shell command built from `meterIp` was the most serious because shell metacharacters could change the command being executed. Removing the unused helper eliminated that execution path. Unsafe XML parsing was also important because input parsing sits at a trust boundary.

## 3. What was challenging about interpreting the reports?

Some findings were direct defects, such as the mutable default argument. Others needed context. The demo XML is a constant, but the meter-reading function represents an input boundary that could later accept external data. Using a hardened parser addresses the issue without relying on the demo remaining the only input source.

## 4. How did static analysis improve the program?

The tools found issues before runtime tests would necessarily expose them. The final changes reduced security risk, clarified the functions, and made output encoding explicit while preserving the example bills. Re-running the tools gave a concrete check that the reported issues were addressed.

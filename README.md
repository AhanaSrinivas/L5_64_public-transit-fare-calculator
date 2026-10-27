# Lab 5: Static Code Analysis — Public Transit Fare Calculator

**Name:** Ahana Srinivas Sivaram  
**SRN:** PES1UG24CS910  
**Section:** H  
**Lab:** Lab 5 — Static Code Analysis

## Objective

To improve Python code quality, security, and style using Pylint, Bandit, and Flake8. The tools were used to identify issues in the assigned public transit fare calculator, document the findings, implement fixes, and verify the updated program.

## About the Program

The program simulates a metro fare calculator. It calculates fares based on distance, applies peak/off-peak pricing and concession discounts, calculates daily totals, manages smart cards, finds the cheapest route, generates ticket checksums, loads stop names from XML, and sends fare files to a gate machine over SSH.

## Setup

Create and activate a Python virtual environment, then install the required packages:

```bash
python -m pip install pylint bandit flake8 paramiko cryptography defusedxml
```

## Run the Program

```bash
python fare_calculator.py
```

The program prints sample fare calculations, smart-card operations, a ticket checksum, and XML stop names.

## Static Code Analysis

The following commands were used to analyse the source and save the reports:

```bash
python -m pylint fare_calculator.py > pylint_report.txt
python -m bandit -r fare_calculator.py > bandit_report.txt
python -m flake8 fare_calculator.py > flake8_report.txt
```

The original reports are preserved separately as:

- `pylint_report_before.txt`
- `bandit_report_before.txt`
- `flake8_report_before.txt`

The updated reports are `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt`.

## Issues Identified and Fixes

The following issues were addressed:

1. **SSH host-key verification:** Replaced automatic acceptance of unknown SSH host keys with system host-key loading and rejection of unknown keys.
2. **SSH command construction:** Added fare-file validation and shell quoting when constructing the remote command.
3. **Unsafe XML parsing:** Switched to the `defusedxml` SAX parser.
4. **Weak checksum algorithm:** Replaced MD5 with SHA-256.
5. **Daily fare cap bug:** Corrected the daily total calculation so that the returned total cannot exceed the configured cap.
6. **Code quality and maintainability:** Added docstrings, replaced the lambda assignment with a named function, improved validation, and added a main guard.
7. **Formatting and style:** Corrected the formatting violations reported by Flake8.

## Verification Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.80/10 | 10.00/10 |
| Bandit | 5 reported findings | 0 reported findings |
| Flake8 | 19 violations | 0 violations |

The updated program was executed successfully. The daily total example returns 150, respecting the configured daily cap.

These results describe the checks performed by the tools; a clean static-analysis report does not guarantee the complete absence of bugs or security risks.

## Deliverables

- `fare_calculator.py` — cleaned and updated source code.
- `issues.md` — documented issues, their types, locations, descriptions, and fixes.
- `reflection.md` — reflection on the static-analysis exercise.
- `pylint_report_before.txt` and `pylint_report.txt`
- `bandit_report_before.txt` and `bandit_report.txt`
- `flake8_report_before.txt` and `flake8_report.txt`

## Conclusion

This exercise demonstrated how static-analysis tools can identify code-quality problems, security risks, and style violations. Fixing the issues improved maintainability, strengthened several security controls, and corrected a functional bug in the daily fare calculation.

# Financial Statement Validator

A Python-based audit application that validates financial statements and detects anomalies using Benford's Law analysis.

## What Does This Do?

This tool audits financial statements by checking if they mathematically make sense. It also uses Benford's Law to identify if transaction data looks suspicious - inconsistencies that might suggest errors or fraud.

## Key Features

**Financial Statement Auditing**
- Validates the fundamental accounting equation (Assets = Liabilities + Equity)
- Checks income statement calculations (Revenue - COGS = Gross Profit, etc.)
- Verifies cash-flow consistency
- Detects impossible values (negative assets, liabilities that don't make sense)
- Compares financial ratios to industry benchmarks

**Benford's Law Analysis**
- Analyzes first-digit distribution of transactions
- Calculates MAD (Mean Absolute Deviation) for conformity assessment
- Generates heatmap visualization
- Flags potential data quality issues

**Trend Analysis**
- Calculates key financial ratios (profitability, liquidity, leverage, efficiency)
- Compares company performance to industry benchmarks
- Displays variance between actual and expected values

## Quick Start

### Installation

```bash
pip install -r requirements-minimal.txt
```

## Output

The application produces:

1. **Audit Summary**: Pass/fail status with counts of errors and warnings
2. **Audit Results**: What passed, what failed, why
3. **Ratio Analysis**: Your company's ratios vs industry standards
4. **Benford Heatmap**: Visual representation of first-digit distribution + MAD-factor

## Actual Use-Cases

- Detecting potential fraud or data entry errors
- Validating transaction imports
- Checking for financial data quality
- Data analysis before actual proper investigations

## Code

### Key Classes

**FinancialStatementAuditor**
- Validates all three financial statements
- Catches mathematical inconsistencies
- Compiles detailed error/warning reports

**TrendAnalysis**
- Calculates financial ratios from statements
- Compares to industry benchmarks
- Shows variance

**Benford**
- Implements Benford's Law analysis
- Calculates MAD conformity metric
- Provides interpretation

**BenfordVisualisation**
- Creates heatmap visualization
- Displays MAD factor
- Shows professional audit report format

## Notes

- The app generates random sample data for demonstration purposes - replace with real data for actual audits
- All calculations/assumptions are based on the IRFS accounting principles
- Benford's Law works best with datasets > 500 transactions
- Negative MAD or impossible ratios usually indicate data quality issues

## Future Features

Potential additions:
- PDF report generation
- Database integration for real data
- Web interface/dashboard
- Multiple company comparison
- Export to Excel


import json
from datetime import datetime
import math


class FinancialStatementAuditor:
    """
    A financial statement auditor that performs mathematical validations

    Performs the following validations:
    - Balance Sheet validation
    - Income Statement validation
    - Cash Flow validation
    - Cross-statement Consistency validation
    - Reasonability validation
    """

    def __init__(self, balance_sheet: dict, income_statement: dict, cash_flow: dict):
        self.bs = balance_sheet
        self.is_ = income_statement
        self.cf = cash_flow

        self.errors = []
        self.warnings = []
        self.passed_checks = []
        self.audit_results = {
            'Balance Sheet': {},
            'Income Statement': {},
            'Cash Flow': {},
            'Cross-Statement': {}
        }

    # ==================== BALANCE SHEET VALIDATIONS ====================

    def validate_balance_sheet_equation(self) -> bool:
        """
        Check 1: Assets = Liabilities + Equity
        """
        bs = self.bs

        total_assets = bs['assets']['current_assets'] + bs['assets']['non_current_assets']
        total_liabilities = bs['liabilities']['current_liabilities'] + bs['liabilities']['non_current_liabilities']
        total_equity = bs['equity']['common_stock'] + bs['equity']['retained_earnings']

        # Check 1: Assets = Liabilities + Equity
        difference = total_assets - (total_liabilities + total_equity)
        check_name = "Balance Sheet Equation (A = L + E)"

        if abs(difference) == 0:
            self.passed_checks.append({
                'check': check_name,
                'status': 'PASS',
                'assets': total_assets,
                'liabilities_plus_equity': total_liabilities + total_equity,
                'difference': difference
            })
            return True
        else:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'assets': total_assets,
                'liabilities_plus_equity': total_liabilities + total_equity,
                'difference': difference,
                'message': f'Assets (${total_assets:,.2f}) != Liabilities (${total_liabilities:,.2f}) + Equity (${total_equity:,.2f})'
            })
            return False

    def validate_current_assets_composition(self) -> bool:
        """
        Check 2: Validate that major current asset components are non-negative
        """
        bs = self.bs
        check_name = "Current Assets Composition"

        # Extract current assets
        cash = bs['assets'].get('cash', 0)
        ar = bs['assets'].get('accounts_receivable', 0)
        inventory = bs['assets'].get('inventory', 0)

        for asset_name, value in [('Cash', cash), ('Accounts Receivable', ar), ('Inventory', inventory)]:
            if value is not None and value < 0:
                self.errors.append({
                    'check': check_name,
                    'status': 'FAIL',
                    'severity': 'HIGH',
                    'item': asset_name,
                    'value': value,
                    'message': f'{asset_name} is negative: ${value:,.2f}'
                })
                return False

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    def validate_liability_equity_structure(self) -> bool:
        """
        Check 3: Validate that liabilities and equity are both reasonable
        """
        bs = self.bs
        check_name = "Liability and Equity Structure"

        total_liabilities = bs['liabilities']['current_liabilities'] + bs['liabilities']['non_current_liabilities']
        total_equity = bs['equity']['common_stock'] + bs['equity']['retained_earnings']

        # Check: Total liabilities should be non-negative
        if total_liabilities < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'item': 'Total Liabilities',
                'value': total_liabilities,
                'message': 'Total Liabilities cannot be negative'
            })
            return False

        # Check: Negative equity indicates insolvency
        if total_equity < 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Total Equity',
                'value': total_equity,
                'message': 'Negative Equity indicates insolvency (liabilities > assets)'
            })

        # Check: Common stock should be non-negative
        common_stock = bs['equity']['common_stock']
        if common_stock < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'item': 'Common Stock',
                'value': common_stock,
                'message': 'Common Stock cannot be negative'
            })
            return False

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    # ==================== INCOME STATEMENT VALIDATIONS ====================

    def validate_income_statement_flow(self) -> bool:
        """
        Check 1: Revenue - COGS = Gross Profit
        Check 2: Gross Profit - OpEx = Operating Income
        Check 3: Operating Income - Interest - Taxes = Net Income
        """
        inc = self.is_
        check_results = []

        # Check 1: Revenue - COGS = Gross Profit
        revenue = inc.get('revenue', 0)
        cogs = inc.get('cost_of_goods_sold', 0)
        gross_profit_actual = inc.get('gross_profit', 0)
        gross_profit_calculated = revenue - cogs

        if abs(gross_profit_actual - gross_profit_calculated) == 0:
            check_results.append(True)
            self.passed_checks.append({
                'check': 'Gross Profit Calculation (Revenue - COGS)',
                'status': 'PASS',
                'actual': gross_profit_actual,
                'calculated': gross_profit_calculated,
                'difference': abs(gross_profit_actual - gross_profit_calculated)
            })
        else:
            self.errors.append({
                'check': 'Gross Profit Calculation',
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'revenue': revenue,
                'cogs': cogs,
                'actual_gross_profit': gross_profit_actual,
                'calculated_gross_profit': gross_profit_calculated,
                'difference': abs(gross_profit_actual - gross_profit_calculated),
                'message': f'Gross Profit mismatch: actual ${gross_profit_actual:,.2f} vs calculated ${gross_profit_calculated:,.2f}'
            })
            check_results.append(False)

        # Check 2: Gross Profit - OpEx = Operating Income
        opex = inc.get('operating_expenses', 0)
        operating_income_actual = inc.get('operating_income', 0)
        operating_income_calculated = gross_profit_actual - opex

        if abs(operating_income_actual - operating_income_calculated) == 0:
            check_results.append(True)
            self.passed_checks.append({
                'check': 'Operating Income Calculation (GP - OpEx)',
                'status': 'PASS',
                'actual': operating_income_actual,
                'calculated': operating_income_calculated
            })
        else:
            self.errors.append({
                'check': 'Operating Income Calculation',
                'status': 'WARNING',
                'severity': 'HIGH',
                'gross_profit': gross_profit_actual,
                'opex': opex,
                'actual_oi': operating_income_actual,
                'calculated_oi': operating_income_calculated,
                'message': f'Operating Income mismatch: actual ${operating_income_actual:,.2f} vs calculated ${operating_income_calculated:,.2f}'
            })
            check_results.append(False)

        # Check 3: Operating Income - Interest - Taxes = Net Income
        interest_exp = inc.get('interest_expense', 0)
        taxes = inc.get('income_tax_expense', 0)
        net_income_actual = inc.get('net_income', 0)
        net_income_calculated = operating_income_actual - interest_exp - taxes

        if abs(net_income_actual - net_income_calculated) == 0:
            check_results.append(True)
            self.passed_checks.append({
                'check': 'Net Income Calculation (OI - Interest - Taxes)',
                'status': 'PASS',
                'actual': net_income_actual,
                'calculated': net_income_calculated
            })
        else:
            self.errors.append({
                'check': 'Net Income Calculation',
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'oi': operating_income_actual,
                'interest': interest_exp,
                'taxes': taxes,
                'actual_ni': net_income_actual,
                'calculated_ni': net_income_calculated,
                'message': f'Net Income mismatch: actual ${net_income_actual:,.2f} vs calculated ${net_income_calculated:,.2f}'
            })
            check_results.append(False)

        return all(check_results)

    def validate_income_statement_logic(self) -> bool:
        """
        Check 4: Revenue >= COGS
        Check 5: COGS should not exceed revenue
        Check 6: Operating expenses should be positive
        Check 7: Interest expense should be non-negative
        Check 8: Taxes should be non-negative
        """
        inc = self.is_
        check_name = "Income Statement Logic"

        # Check 4: Revenue should be positive
        revenue = inc.get('revenue', 0)
        if revenue < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'CRITICAL',
                'item': 'Revenue',
                'value': revenue,
                'message': 'Revenue cannot be negative'
            })
            return False

        # Check 5: COGS should not exceed revenue
        cogs = inc.get('cost_of_goods_sold', 0)
        if cogs > revenue and cogs != 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'COGS > Revenue',
                'cogs': cogs,
                'revenue': revenue,
                'message': 'COGS exceeds Revenue (possible data quality issue)'
            })

        # Check 6: Operating expenses should be positive
        opex = inc.get('operating_expenses', 0)
        if opex < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'HIGH',
                'item': 'Operating Expenses',
                'value': opex,
                'message': 'Operating Expenses cannot be negative'
            })
            return False

        # Check 7: Interest expense should be non-negative
        interest = inc.get('interest_expense', 0)
        if interest < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'HIGH',
                'item': 'Interest Expense',
                'value': interest,
                'message': 'Interest Expense cannot be negative'
            })
            return False

        # Check 8: Taxes should be non-negative
        taxes = inc.get('income_tax_expense', 0)
        if taxes < 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Tax Provision',
                'value': taxes,
                'message': 'Negative tax provision (possible tax benefit/carryforward)'
            })

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    # ==================== CASH FLOW STATEMENT VALIDATIONS ====================

    def validate_cash_flow_components(self) -> bool:
        """
        Check 1: OCF + ICF + FCF = Net Change in Cash
        """
        cf = self.cf
        check_name = "Cash Flow Reconciliation"

        ocf = cf.get('operating_activities', 0)
        icf = cf.get('investing_activities', 0)
        fcf = cf.get('financing_activities', 0)
        net_change = ocf + icf + fcf

        # Check 1: Cash flow equation
        calculated_change = ocf + icf + fcf

        self.passed_checks.append({
            'check': check_name,
            'status': 'PASS',
            'ocf': ocf,
            'icf': icf,
            'fcf': fcf,
            'net_change': calculated_change
        })
        return True

    def validate_investing_cash_flow_components(self) -> bool:
        """
        Check 2: CapEx should typically be negative (outflow)
        Check 3: Depreciation should be positive (non-cash add-back)
        """
        cf = self.cf
        check_name = "Investing CF Components"

        # Note: fields may not exist in example dicts -> use get with defaults
        capex = cf.get('capital_expenditure', 0)
        depreciation = cf.get('depreciation', 0)

        # Check 2: CapEx should typically be negative (outflow)
        if capex > 0 and capex != 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Capital Expenditure',
                'value': capex,
                'message': 'CapEx is positive (typically should be negative/outflow)'
            })

        # Check 3: Depreciation should be non-negative
        if depreciation < 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'MEDIUM',
                'item': 'Depreciation',
                'value': depreciation,
                'message': 'Depreciation should be non-negative'
            })
            return False

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    def validate_financing_cash_flow_components(self) -> bool:
        """
        Check 4: Debt issuance should be positive (inflow)
        Check 5: Debt repayment should be negative (outflow)
        Check 6: Dividends should be non-positive (outflow)
        """
        cf = self.cf
        check_name = "Financing CF Components"

        # Note: fields may not exist in example dicts -> use get with defaults
        debt_issued = cf.get('debt_issuance', 0)
        debt_repaid = cf.get('debt_repayment', 0)
        dividends = cf.get('dividends_paid', 0)

        # Check 4: Debt issuance should be positive
        if debt_issued < 0 and debt_issued != 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Debt Issuance',
                'value': debt_issued,
                'message': 'Debt issuance is negative (expected to be positive)'
            })

        # Check 5: Debt repayment should be negative
        if debt_repaid > 0 and debt_repaid != 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Debt Repayment',
                'value': debt_repaid,
                'message': 'Debt repayment is positive (typically should be negative)'
            })

        # Check 6: Dividends should be non-positive
        if dividends > 0 and dividends != 0:
            self.warnings.append({
                'check': check_name,
                'status': 'WARNING',
                'item': 'Dividends Paid',
                'value': dividends,
                'message': 'Dividends paid is positive (typically should be negative)'
            })

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    # ==================== CROSS-STATEMENT VALIDATIONS ====================

    def validate_net_income_to_cash_flow(self) -> bool:
        """
        Check 1: OCF should typically be in reasonable range of NI (50% to 200% of NI)
        """
        inc = self.is_
        cf = self.cf
        check_name = "Net Income to Operating CF"

        net_income = inc.get('net_income', 0)
        ocf = cf.get('operating_activities', 0)

        # Check 1: OCF should typically be in reasonable range of NI (50% to 200% of NI)
        if net_income > 0:
            lower_bound = net_income * 0.5
            upper_bound = net_income * 2.0

            if lower_bound <= ocf <= upper_bound:
                self.passed_checks.append({
                    'check': check_name,
                    'status': 'PASS',
                    'net_income': net_income,
                    'operating_cf': ocf,
                    'within_range': True
                })
                return True
            else:
                self.warnings.append({
                    'check': check_name,
                    'status': 'WARNING',
                    'net_income': net_income,
                    'operating_cf': ocf,
                    'expected_range': f'${lower_bound:,.0f} to ${upper_bound:,.0f}',
                    'message': 'Operating CF outside expected range relative to NI (check working capital)'
                })
        else:
            self.passed_checks.append({
                'check': check_name,
                'status': 'PASS',
                'note': 'Unable to validate when Net Income ≤ 0'
            })

        return True

    def validate_balance_sheet_consistency(self) -> bool:
        """
        Check 2: Short-term debt should be <= total liabilities
        Check 3: Common stock should be <= total equity
        """
        bs = self.bs
        check_name = "Balance Sheet Item Consistency"

        total_liabilities = bs['liabilities']['current_liabilities'] + bs['liabilities']['non_current_liabilities']
        total_equity = bs['equity']['common_stock'] + bs['equity']['retained_earnings']

        # Note: fields may not exist in example dicts -> use get with defaults
        short_term_debt = bs['liabilities'].get('short_term_debt', 0)
        common_stock = bs['equity'].get('common_stock', 0)

        # Check 2: Short-term debt should be <= total liabilities
        if short_term_debt > total_liabilities and short_term_debt > 0:
            self.errors.append({
                'check': check_name,
                'status': 'FAIL',
                'severity': 'HIGH',
                'short_term_debt': short_term_debt,
                'total_liabilities': total_liabilities,
                'message': 'Short-term Debt exceeds Total Liabilities'
            })
            return False

        # Check 3: Common stock should be <= total equity
        if common_stock > total_equity and common_stock > 0:
            self.errors.append({
                'check': check_name,
                'status': 'WARNING',
                'severity': 'HIGH',
                'common_stock': common_stock,
                'total_equity': total_equity,
                'message': 'Common Stock exceeds Total Equity'
            })
            return False

        self.passed_checks.append({'check': check_name, 'status': 'PASS'})
        return True

    def validate_ratios_reasonableness(self) -> bool:
        """
        Validate that key financial ratios are within reasonable bounds
        - Check 1: Gross Margin should be 0% to 99%
        - Check 2: Operating Margin should be -100% to 100%
        - Check 3: Net Margin should be -100% to 100%
        - Check 4: Debt to Assets should be 0% to 200%
        """
        inc = self.is_
        bs = self.bs
        check_name = "Financial Ratios Reasonableness"

        revenue = inc.get('revenue', 1)  # Avoid division by zero
        gross_profit = inc.get('gross_profit', 0)
        operating_income = inc.get('operating_income', 0)
        net_income = inc.get('net_income', 0)

        total_assets = bs['assets']['current_assets'] + bs['assets']['non_current_assets']
        total_liabilities = bs['liabilities']['current_liabilities'] + bs['liabilities']['non_current_liabilities']

        # Check 1: Gross Margin should be 0% to 99%
        if revenue != 0:
            gross_margin = (gross_profit / revenue) * 100
            if -1 <= gross_margin <= 101:
                self.passed_checks.append({
                    'check': f'{check_name} - Gross Margin',
                    'status': 'PASS',
                    'value': f'{gross_margin:.2f}%'
                })
            else:
                self.warnings.append({
                    'check': f'{check_name} - Gross Margin',
                    'status': 'WARNING',
                    'value': f'{gross_margin:.2f}%',
                    'message': 'Unusual gross margin detected'
                })

        # Check 2: Operating Margin should be -100% to 100%
        if revenue != 0:
            operating_margin = (operating_income / revenue) * 100
            if -101 <= operating_margin <= 101:
                self.passed_checks.append({
                    'check': f'{check_name} - Operating Margin',
                    'status': 'PASS',
                    'value': f'{operating_margin:.2f}%'
                })
            else:
                self.warnings.append({
                    'check': f'{check_name} - Operating Margin',
                    'status': 'WARNING',
                    'value': f'{operating_margin:.2f}%',
                    'message': 'Unusual operating margin detected'
                })

        # Check 3: Net Margin should be -100% to 100%
        if revenue != 0:
            net_margin = (net_income / revenue) * 100
            if -101 <= net_margin <= 101:
                self.passed_checks.append({
                    'check': f'{check_name} - Net Margin',
                    'status': 'PASS',
                    'value': f'{net_margin:.2f}%'
                })
            else:
                self.warnings.append({
                    'check': f'{check_name} - Net Margin',
                    'status': 'WARNING',
                    'value': f'{net_margin:.2f}%',
                    'message': 'Unusual net margin detected'
                })

        # Check 4: Debt to Assets should be 0% to 200%
        if total_assets != 0:
            debt_to_assets = (total_liabilities / total_assets) * 100
            if 0 <= debt_to_assets <= 200:
                self.passed_checks.append({
                    'check': f'{check_name} - Debt to Assets',
                    'status': 'PASS',
                    'value': f'{debt_to_assets:.2f}%'
                })
            else:
                self.warnings.append({
                    'check': f'{check_name} - Debt to Assets',
                    'status': 'WARNING',
                    'value': f'{debt_to_assets:.2f}%',
                    'message': 'Debt to Assets ratio outside normal range'
                })

        return True

    # ==================== AUDIT EXECUTION ====================

    def run_all_audits(self) -> dict:
        """
        Execute all audit checks and compile results
        """
        self.validate_balance_sheet_equation()
        self.validate_current_assets_composition()
        self.validate_liability_equity_structure()

        self.validate_income_statement_flow()
        self.validate_income_statement_logic()

        self.validate_cash_flow_components()
        self.validate_investing_cash_flow_components()
        self.validate_financing_cash_flow_components()

        self.validate_net_income_to_cash_flow()
        self.validate_balance_sheet_consistency()

        self.validate_ratios_reasonableness()

        # Compile audit results
        self.audit_results = {
            'summary': {
                'total_checks': len(self.passed_checks) + len(self.errors),
                'passed': len(self.passed_checks),
                'failed': len(self.errors),
                'warnings': len(self.warnings),
                'status': 'PASSED' if not self.errors else 'FAILED',
                'audit_date': datetime.now().isoformat()
            },
            'passed_checks': self.passed_checks,
            'warnings': self.warnings,
            'errors': self.errors
        }

        return self.audit_results

    def export_audit_report(self, filename: str = None) -> str:
        """
        Export audit report to JSON file
        """
        if filename is None:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w') as f:
            json.dump(self.audit_results, f, indent=2, default=str)

        print(f"Audit report exported to: {filename}")
        return filename

    def print_audit_report(self) -> None:
        """
        Print formatted audit report to console
        """
        summary = self.audit_results['summary']

        print("=" * 70)
        print("FINANCIAL STATEMENT AUDIT VALIDATION REPORT")
        print(f"Audit Date: {summary['audit_date']}")
        print("=" * 70)
        print()

        print(f"PASSED CHECKS: {summary['passed']}")
        for check in self.passed_checks[:5]:
            print(f" - {check.get('check', 'Unknown Check')}")
        print()

        if self.warnings:
            print(f"WARNINGS: {summary['warnings']}")
            for warning in self.warnings:
                print(f" - {warning.get('check', 'Unknown Check')}: {warning.get('message', '')}")
            print()
        else:
            print(f"WARNINGS: None")
            print()

        if self.errors:
            print(f"ERRORS: {summary['failed']}")
            for error in self.errors:
                severity = error.get('severity', 'UNKNOWN')
                print(f" - [{severity}] {error.get('check', 'Unknown Check')}: {error.get('message', '')}")
            print()
        else:
            print(f"ERRORS: None")
            print()

        print("=" * 70)
        print(f"OVERALL STATUS: {summary['status']}")
        print("=" * 70)
        print()


class Benford:
    """
    Benford's Law states that in many naturally occurring datasets, the leading digit is likely to be small
    The probability of first digit d is: P(d) = log10(1 + 1/d)
    Makes sense for large datasets > 500 (e.g. transactions)
    """

    def __init__(self):
        self.expected_probabilities = self._calculate_expected_probabilities()

    def _calculate_expected_probabilities(self) -> dict[int, float]:
        probabilities = {}
        for digit in range(1, 10):
            probabilities[digit] = math.log10(1 + 1 / digit)
        return probabilities

    def _extract_first_digit(self, number: type[int, float]) -> int:
        # Convert to absolute value and string
        num_str = str(abs(number))

        # Remove decimal point and find first non-zero digit
        num_str = num_str.replace('.', '').replace('-', '')

        for char in num_str:
            if char.isdigit() and char != '0':
                return int(char)

        return -1

    def _count_first_digits(self, data: dict[int, type[int, float]]) -> dict[int, int]:
        digit_counts = {digit: 0 for digit in range(1, 10)}

        for transaction_id, amount in data.items():
            first_digit = self._extract_first_digit(amount)
            if first_digit is not None:
                digit_counts[first_digit] += 1

        return digit_counts

    def _calculate_mad(self, actual_proportions: dict[int, float], expected_probabilities: dict[int, float]) -> float:
        """
        Calculate Mean Absolute Deviation (MAD) between actual and expected distributions
        MAD = sum(|actual - expected|) / n
        """
        deviations = []
        for digit in range(1, 10):
            actual = actual_proportions.get(digit, 0)
            expected = expected_probabilities.get(digit, 0)
            deviations.append(abs(actual - expected))

        mad = sum(deviations) / len(deviations)
        return mad

    def analyze(self, transactions: dict[int, type[int, float]]) -> tuple[dict[int, dict[str, type[int, float]]], float]:
        # Count first digits
        digit_counts = self._count_first_digits(transactions)
        total_transactions = sum(digit_counts.values())

        # Calculate actual proportions
        actual_proportions = {}
        for digit in range(1, 10):
            actual_proportions[digit] = digit_counts[digit] / total_transactions if total_transactions > 0 else 0

        # Calculate global MAD (overall conformity across all digits)
        mad = self._calculate_mad(actual_proportions, self.expected_probabilities)

        # Build results dictionary
        results = {}
        for digit in range(1, 10):
            expected_count = self.expected_probabilities[digit] * total_transactions
            actual_count = digit_counts[digit]

            results[digit] = {
                'expected_value': round(expected_count, 1),
                'actual_value': actual_count
            }

        return results, round(mad, 5)

    def interpret_mad(self, mad: float) -> str:
        if mad < 0.006:
            return "Close conformity - data likely follows Benford's Law"
        elif mad < 0.012:
            return "Acceptable conformity - data reasonably follows Benford's Law"
        elif mad < 0.015:
            return "Marginally acceptable conformity - investigate further"
        else:
            return "Non-conformity - potential data quality issues or fraud"

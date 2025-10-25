# Done: make 3 financial statements randomly generate
# Done: make industry trend (comparison) analysis
# TODO: visualisation, proper data processing


import random

from calculation import FinancialStatementAuditor, TrendAnalysis, Benford

company_ratios = {
    'profitability_ratios': {
        'gross_profit_margin': 42.5,
        'operating_profit_margin': 18.3,
        'net_profit_margin': 12.1,
        'roa': 8.5,
        'roe': 16.2
    },
    'liquidity_ratios': {
        'current_ratio': 2.1,
        'quick_ratio': 1.3
    },
    'leverage_ratios': {
        'debt_to_equity': 0.85,
        'interest_coverage': 5.2
    },
    'efficiency_ratios': {
        'asset_turnover': 1.8
    }
}

industry_benchmarks = {
    'profitability_ratios': {
        'gross_profit_margin': 38.0,
        'operating_profit_margin': 15.5,
        'net_profit_margin': 10.0,
        'roa': 7.2,
        'roe': 14.5
    },
    'liquidity_ratios': {
        'current_ratio': 1.9,
        'quick_ratio': 1.1
    },
    'leverage_ratios': {
        'debt_to_equity': 0.95,
        'interest_coverage': 4.5
    },
    'efficiency_ratios': {
        'asset_turnover': 1.6
    }
}


def generate_financial_statements(amount: int = 1, is_balanced: bool = None) -> dict[str, list]:
    balance_sheets: list = []
    income_statements: list = []
    cash_flows: list = []

    for i in range(amount):
        if is_balanced is None:
            current_is_balanced: bool = random.choice([True, False])
        else:
            current_is_balanced: bool = is_balanced

        # ===== GENERATE INCOME STATEMENT =====
        revenue = random.randint(1500000, 4000000)
        cost_of_goods_sold = int(revenue * random.uniform(0.50, 0.65))
        gross_profit = revenue - cost_of_goods_sold

        operating_expenses = int(revenue * random.uniform(0.15, 0.30))
        operating_income = gross_profit - operating_expenses

        interest_expense = random.randint(20000, 80000)
        income_before_tax = operating_income - interest_expense

        tax_rate: float = random.uniform(0.20, 0.30)
        income_tax_expense = int(income_before_tax * tax_rate) if income_before_tax > 0 else 0
        net_income = income_before_tax - income_tax_expense

        dividends_paid = int(net_income * random.uniform(0.10, 0.30)) if net_income > 0 else 0
        prior_year_revenue = int(revenue * random.uniform(0.80, 0.95))

        income_statement: dict[str, int] = {
            'revenue': revenue,
            'cost_of_goods_sold': cost_of_goods_sold,
            'gross_profit': gross_profit,
            'operating_expenses': operating_expenses,
            'operating_income': operating_income,
            'interest_expense': interest_expense,
            'income_before_tax': income_before_tax,
            'income_tax_expense': income_tax_expense,
            'net_income': net_income,
            'dividends_paid': dividends_paid,
            'prior_year_revenue': prior_year_revenue,
        }

        # ===== GENERATE BALANCE SHEET =====
        cash = random.randint(50000, 200000)
        accounts_receivable = random.randint(80000, 300000)
        inventory = random.randint(100000, 400000)
        current_assets = cash + accounts_receivable + inventory

        property_plant_equipment = random.randint(500000, 1500000)
        accumulated_depreciation = -random.randint(100000, 400000)
        intangible_assets = random.randint(50000, 300000)
        non_current_assets = property_plant_equipment + accumulated_depreciation + intangible_assets

        total_assets = current_assets + non_current_assets

        accounts_payable = random.randint(80000, 250000)
        short_term_debt = random.randint(50000, 200000)
        accrued_expenses = random.randint(30000, 100000)
        current_liabilities = accounts_payable + short_term_debt + accrued_expenses

        long_term_debt = random.randint(200000, 800000)
        non_current_liabilities = long_term_debt

        total_liabilities = current_liabilities + non_current_liabilities

        # Generate equity
        if current_is_balanced:
            total_equity = total_assets - total_liabilities

            if total_equity > 0:
                max_common_stock = int(total_equity * 0.4)
                min_common_stock = int(total_equity * 0.2)
                if min_common_stock < max_common_stock:
                    common_stock = random.randint(min_common_stock, max_common_stock)
                else:
                    common_stock = min_common_stock
                retained_earnings = total_equity - common_stock
            else:
                common_stock = random.randint(100000, 300000)
                retained_earnings = total_equity - common_stock
        else:
            common_stock = random.randint(100000, 300000)
            retained_earnings = random.randint(100000, 500000)
            error_amount = random.randint(10000, 100000) * random.choice([-1, 1])
            retained_earnings += error_amount

        balance_sheet: dict[str, dict[str, int]] = {
            'assets': {
                'current_assets': current_assets,
                'cash': cash,
                'accounts_receivable': accounts_receivable,
                'inventory': inventory,
                'non_current_assets': non_current_assets,
                'property_plant_equipment': property_plant_equipment,
                'accumulated_depreciation': accumulated_depreciation,
                'intangible_assets': intangible_assets,
            },
            'liabilities': {
                'current_liabilities': current_liabilities,
                'accounts_payable': accounts_payable,
                'short_term_debt': short_term_debt,
                'accrued_expenses': accrued_expenses,
                'non_current_liabilities': non_current_liabilities,
                'long_term_debt': long_term_debt,
            },
            'equity': {
                'common_stock': common_stock,
                'retained_earnings': retained_earnings,
            }
        }

        # ==== GENERATE CASH FLOW STATEMENT ====
        # Operating activities should be related to net income
        operating_activities = int(net_income * random.uniform(0.90, 1.30))

        # Investing activities (usually negative - capital expenditures)
        investing_activities = -random.randint(100000, 300000)

        # Financing activities (debt/equity changes, dividends)
        financing_base = random.randint(-100000, 200000)
        financing_activities = financing_base - dividends_paid

        cash_flow: dict[str, int] = {
            'operating_activities': operating_activities,
            'investing_activities': investing_activities,
            'financing_activities': financing_activities,
        }

        balance_sheets.append(balance_sheet)
        income_statements.append(income_statement)
        cash_flows.append(cash_flow)

    return {'balance_sheets': balance_sheets, 'income_statements': income_statements, 'cash_flows': cash_flows}


def generate_benford_transactions(n: int) -> dict[int, float]:
    """
    Generate realistic transaction amounts that roughly follow Benford's Law.
    """
    transactions: dict = {}

    for i in range(1, n + 1):
        # Use power law distribution which naturally follows Benford
        # Transaction amounts from realistic business scenarios
        rand = random.random()

        # Generate using inverse transform of Benford-like distribution
        if rand < 0.301:  # ~30% start with 1
            base = 1
        elif rand < 0.477:  # ~17.6% start with 2
            base = 2
        elif rand < 0.602:  # ~12.5% start with 3
            base = 3
        elif rand < 0.699:  # ~9.7% start with 4
            base = 4
        elif rand < 0.778:  # ~7.9% start with 5
            base = 5
        elif rand < 0.845:  # ~6.7% start with 6
            base = 6
        elif rand < 0.903:  # ~5.8% start with 7
            base = 7
        elif rand < 0.954:  # ~5.1% start with 8
            base = 8
        else:  # ~4.6% start with 9
            base = 9

        # Add random decimal portion
        multiplier = random.uniform(1, 9.99)

        # Random magnitude (10s, 100s, 1000s, etc.)
        magnitude = 10 ** random.randint(2, 5)

        amount = base * magnitude + multiplier * (magnitude / 10)
        transactions[i] = round(amount, 2)

    return transactions


def display_dict(d: dict, i: int = 0) -> None:
    for key, value in d.items():
        if isinstance(value, dict):
            print("  - " * i + str(key) + ":")
            display_dict(value, i + 1)
        else:
            print("    " * i + str(key) + ": " + str(value))


def main():
    random.seed(100)

    # ===== AUDIT =====
    # --- Financial Statement Check ---
    print("\n" + "=" * 100 + "\n")
    financial_statements: dict = generate_financial_statements(amount=5)
    fs_for_benchmarkanalysis = {
        'balance_sheet': financial_statements['balance_sheets'][0],
        'income_statement': financial_statements['income_statements'][0],
        'cash_flow': financial_statements['cash_flows'][0]
    }

    for ele in range(len(financial_statements['balance_sheets'])):
        balance_sheet = financial_statements['balance_sheets'][ele]
        income_statement = financial_statements['income_statements'][ele]
        cash_flow = financial_statements['cash_flows'][ele]

        auditor = FinancialStatementAuditor(
            balance_sheet=balance_sheet,
            income_statement=income_statement,
            cash_flow=cash_flow)
        audit_report = auditor.run_all_audits()

        print(f"Audit results: {audit_report}")

    # --- Compare Financial Statement To Industry Benchmarks ---
    print("\n" + "=" * 100 + "\n")
    analysis = TrendAnalysis(industry_benchmarks=industry_benchmarks,
                             company_financial_statement=fs_for_benchmarkanalysis)
    company_ratios_test = analysis.calculate_ratios_from_statements()
    trend_report = analysis.calculate_variance()

    display_dict(company_ratios_test)
    print("\n" + "=" * 100 + "\n")
    display_dict(trend_report)

    # ===== BENFORD =====
    print("\n" + "=" * 100 + "\n")
    test_transactions = generate_benford_transactions(n=1000)

    benford = Benford()
    results, mad = benford.analyze(test_transactions)
    interpretation: str = benford.interpret_mad(mad)

    print(f"Benford results: {results}")
    print(f"Mad: {mad}, {interpretation}")


if __name__ == '__main__':
    main()

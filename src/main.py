import random

from calculation import FinancialStatementAuditor, Benford

balance_sheet: dict = {
    'assets': {
        'current_assets': 450000,  # Cash, AR, Inventory
        'cash': 75000,
        'accounts_receivable': 125000,
        'inventory': 250000,
        'non_current_assets': 850000,  # PP&E, Intangibles
        'property_plant_equipment': 800000,
        'accumulated_depreciation': -150000,
        'intangible_assets': 200000,
    },
    'liabilities': {
        'current_liabilities': 300000,
        'accounts_payable': 150000,
        'short_term_debt': 100000,
        'accrued_expenses': 50000,
        'non_current_liabilities': 400000,
        'long_term_debt': 400000,
    },
    'equity': {
        'common_stock': 250000,
        'retained_earnings': 350000,
    }
}

income_statement: dict = {
    'revenue': 2500000,
    'cost_of_goods_sold': 1500000,
    'gross_profit': 1000000,
    'operating_expenses': 600000,
    'operating_income': 400000,
    'interest_expense': 30000,
    'income_before_tax': 370000,
    'income_tax_expense': 92500,
    'net_income': 277500,
    'dividends_paid': 50000,
    'prior_year_revenue': 2200000,
}

cash_flow: dict = {
    'operating_activities': 320000,  # Should be close to NI
    'investing_activities': -150000,  # CapEx, acquisitions
    'financing_activities': 50000,  # Debt/equity changes
}


def generate_benford_transactions(n: int):
    """
    Generate realistic transaction amounts that roughly follow Benford's Law.
    """
    transactions = {}

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


def main():
    auditor = FinancialStatementAuditor(balance_sheet, income_statement, cash_flow)
    audit_report = auditor.run_all_audits()

    print(f"Audit results: {audit_report}\n")

    random.seed(100)
    test_transactions = generate_benford_transactions(n=1000)

    # Test with Benford class
    benford = Benford()
    results, mad = benford.analyze(test_transactions)
    interpretation: str = benford.interpret_mad(mad)

    print(f"Benford results: {results}")
    print(f"Mad: {mad}, {interpretation}")


if __name__ == '__main__':
    main()

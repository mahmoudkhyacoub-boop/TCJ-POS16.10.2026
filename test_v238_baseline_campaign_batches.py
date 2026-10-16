from pathlib import Path
import ast

source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
ast.parse(source)

# Cards use the saved baseline plus movements entered after that baseline.
start = source.index("    def ui_accountant(self):")
end = source.index("    def ui_advanced_reports(self):", start) if "    def ui_advanced_reports(self):" in source[start:] else len(source)
accountant = source[start:end]
assert "def refresh_summary_cards" in accountant
summary = accountant[accountant.index("def refresh_summary_cards"):accountant.index("def refresh():")]
assert "SELECT account_key, opening_balance, updated_at FROM accountant_accounts" in summary
assert "SELECT direction, amount FROM accountant_transactions WHERE account_key=? AND created_at>?" in summary
assert "current += sum(" in summary
assert "load_openings(); refresh_summary_cards(); refresh()" in accountant

# Marketing sends only the selected 50-customer slice and advances to the next batch.
start = source.index("    def ui_marketing_campaigns(self):")
end = source.index("    def ui_customers(self):", start)
campaign = source[start:end]
assert 'batch_var = ctk.StringVar(value="1")' in campaign
assert "(len(customers) + 49) // 50" in campaign
assert "start = (batch_number - 1) * 50" in campaign
assert "batch = customers[start:start + 50]" in campaign
assert "for customer_name, phone in batch:" in campaign
assert "batch_var.set(str(batch_number + 1))" in campaign
assert "الدفعة" in campaign
print("V238 baseline reset and 50-customer campaign batch checks passed.")

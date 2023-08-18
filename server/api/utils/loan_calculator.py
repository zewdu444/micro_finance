# loan calucatr per month payment

def loan_calculator(loan_term, requested_amount, interest_rate):
    monthly_interest_rate = ((1 + interest_rate) ** (1 / 12)) - 1
    num_payments = loan_term

    numerator = requested_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments)
    denominator = (1 + monthly_interest_rate)**num_payments - 1

    monthly_payment = numerator / denominator
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - requested_amount

    return total_payment, monthly_payment, total_interest

from engine import *

class Parameters:
    def __init__(self):
        # Example parameters
        self.age = 30
        self.face_value = 1000000  # Face value of the policy
        self.interest_rate = 0.05  # Annual interest rate
        self.mortality_rates = get_mortality_by_sex('Laki-Laki')  # Mortality rates for males
        self.num_years = 10  # Number of years for profit calculation
        self.expenses_factor = 0.5  # Expenses factor (as a proportion of premiums)
        self.profit_margin_factor = 0.05  # Profit margin factor (as a proportion of premiums)
        self.term_years = 25  # Term of the policy


if __name__=="__main__":
    _params = Parameters()
    # Calculate reserves
    premium = calculate_premium(_params.age, _params.face_value, _params.interest_rate, _params.mortality_rates)
    reserves = calculate_reserve(_params.age, _params.face_value, _params.interest_rate, _params.mortality_rates, _params.num_years, premium)
    # Calculate profit values for the next 5 years
    profit_values, loss_values = calculate_profit(_params.age, _params.face_value, premium, _params.interest_rate, _params.mortality_rates, _params.num_years, _params.term_years, _params.expenses_factor, _params.profit_margin_factor)
    
    for year, reserve in enumerate(reserves, start=_params.age):
        print(f"Reserve at age {year}:", round(reserve, 1))
    
    # Display profit values
    for year, profit in enumerate(profit_values, start=1):
        print(f"Profit for year {year}: {round(profit, 2)}")

    for year, total_loss in enumerate(loss_values, start=1):
        print(f"total_loss for year {year}: {round(total_loss, 2)}")

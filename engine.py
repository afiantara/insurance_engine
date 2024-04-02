import numpy as np
import pandas as pd
mortality4 = pd.read_csv('./tabelMortalitas.csv', sep=';')

# Function to calculate the net premium payable annually
def net_premium_annual(sum_insured, age, term, interest_rate, mortality_rate):
    death_benefit = sum_insured * np.prod(1 - mortality_rate[age:age + term])
    present_value_death_benefit = death_benefit / (1 + interest_rate) ** term
    annual_premium = present_value_death_benefit / annuity_annual(age, term, interest_rate, mortality_rate)
    return annual_premium

# Function to calculate the net premium payable quarterly
def net_premium_quarterly(sum_insured, age, term, interest_rate, mortality_rate):
    death_benefit = sum_insured * np.prod(1 - mortality_rate[age:age + term])
    present_value_death_benefit = death_benefit / (1 + interest_rate) ** term
    quarterly_premium = present_value_death_benefit / annuity_quarterly(age, term, interest_rate, mortality_rate)
    return quarterly_premium

# Function to calculate the net premium payable monthly
def net_premium_monthly(sum_insured, age, term, interest_rate, mortality_rate):
    death_benefit = sum_insured * np.prod(1 - mortality_rate[age:age + term])
    present_value_death_benefit = death_benefit / (1 + interest_rate) ** term
    monthly_premium = present_value_death_benefit / annuity_monthly(age, term, interest_rate, mortality_rate)
    return monthly_premium

# Function to calculate annual annuity factor
def annuity_annual(age, term, interest_rate, mortality_rate):
    annuity_factor = 0
    for t in range(1, term + 1):
        survival_probability = np.prod(1 - mortality_rate[age:age + t])
        annuity_factor += (1 / (1 + interest_rate)) ** t * survival_probability
    return annuity_factor

# Function to calculate quarterly annuity factor
def annuity_quarterly(age, term, interest_rate, mortality_rate):
    annuity_factor = 0
    quarterly_interest_rate = interest_rate / 4
    for t in range(1, term * 4 + 1):
        survival_probability = np.prod(1 - mortality_rate[age:age + int(np.ceil(t / 4))])
        annuity_factor += (1 / (1 + quarterly_interest_rate)) ** t * survival_probability
    return annuity_factor

# Function to calculate monthly annuity factor
def annuity_monthly(age, term, interest_rate, mortality_rate):
    annuity_factor = 0
    monthly_interest_rate = interest_rate / 12
    for t in range(1, term * 12 + 1):
        survival_probability = np.prod(1 - mortality_rate[age:age + int(np.ceil(t / 12))])
        annuity_factor += (1 / (1 + monthly_interest_rate)) ** t * survival_probability
    return annuity_factor



def expected_claim(age, face_value, interest_rate, mortality_rates):
    death_benefits_pv = 0
    for t in range(1, 111 - age):  
        #probability_of_survival = np.prod(1 - mortality_rates[age:age + t - 1]) * mortality_rates[age + t - 1]
        probability_of_survival = np.prod(1 - mortality_rates[age + t - 1]) - np.prod(1 - mortality_rates[age + t])
        death_benefits_pv += face_value * (1 / (1 + interest_rate)) ** t * probability_of_survival
        
    return death_benefits_pv

def expected_claim_term(age, term, face_value, interest_rate, mortality_rates):
    # Calculate the present value of future death benefits for a term insurance policy
    death_benefits_pv  = 0
    for t in range(1, term + 1):
        #probability_of_survival = np.prod(1 - mortality_rates[age:age + t - 1]) * mortality_rates[age + t - 1]
        probability_of_survival = np.prod(1 - mortality_rates[age + t - 1]) - np.prod(1 - mortality_rates[age + t])
        death_benefits_pv += (1 / (1 + interest_rate)) ** t * probability_of_survival
    return death_benefits_pv

def expected_claim_endowment(age, term, face_value, interest_rate, mortality_rates):
    death_benefits_pv = expected_claim_term(age, term, face_value, interest_rate, mortality_rates)
    
    endowment_benefits_pv = face_value * (1 / (1 + interest_rate)) ** term * (np.prod(1 - mortality_rates[age + term] - np.prod(1 - mortality_rates[age]) ) )
    return death_benefits_pv - endowment_benefits_pv  

def annuity_whole(age, interest_rate, mortality_rates):
    premiums_pv = 0
    for t in range(1, 111-age):  # Assuming maximum age of 111
        #probability_of_survival = np.prod(1 - mortality_rates[age:age + t - 1]) 
        probability_of_survival = np.prod(1 - mortality_rates[age + t - 1]) 
        premiums_pv += (1 / (1 + interest_rate)) ** t * probability_of_survival
    return premiums_pv

def annuity_term(age, term, interest_rate, mortality_rates):
    premiums_pv = 0
    for t in range(1, term + 1):
        #probability_of_survival = np.prod(1 - mortality_rates[age:age + t - 1]) 
        probability_of_survival = np.prod(1 - mortality_rates[age + t - 1]) 
        premiums_pv += (1 / (1 + interest_rate)) ** t * probability_of_survival
    return premiums_pv

def calculate_premium(age, face_value, interest_rate, mortality_rates):
    premium = expected_claim(age, face_value, interest_rate, mortality_rates) / annuity_whole(age, interest_rate, mortality_rates)
    return premium

def calculate_reserve(age, face_value, interest_rate, mortality_rates, num_years, premium):
    reserves = []
    for t in range(age, age + num_years + 1):
        reserve = 0
        for i in range(1, num_years + 1):
            if t - age >= i:
                #probability_of_survival = np.prod(1 - mortality_rates[age:t + i - 1]) 
                probability_of_survival = np.prod(1 - mortality_rates[age + t - 1]) - np.prod(1 - mortality_rates[age + t])
                temp = expected_claim(t, face_value, interest_rate, mortality_rates) - (premium * (1 / (1 + interest_rate)) ** i * probability_of_survival)
                reserve += temp
                
        reserves.append(reserve)
    return reserves

def calculate_profit(age, face_value, premium, interest_rate, mortality_rates, num_years, term, expenses_factor, profit_margin_factor):
    profit_values = []
    loss_values = []
    expenses_pv = 0
    total_loss = 0
    total_loading = 0
    for year in range(num_years):
        death_benefits_pv = expected_claim(age + year, face_value, interest_rate, mortality_rates)
        premiums_pv = premium * annuity_whole(age + year, interest_rate, mortality_rates)
        
        if year == 0:
            expenses = expenses_factor * premiums_pv
        elif year < term:
            expenses = 1000 * annuity_term(age + year, term, interest_rate, mortality_rates)
        else:
            expenses = 0
            
        expenses_pv += expenses
        total_loss = death_benefits_pv + expenses - premiums_pv  # Update the total_loss
        loss_values.append(total_loss)

        total_loading = annuity_term(age, term, interest_rate, mortality_rates) + profit_margin_factor
        print("nilai tunai dari benefit tahun ke :", year, "adalah ",death_benefits_pv)
        print("biaya tahun ke :", year, "adalah ",expenses)
        print("nilai tunai dari premium tahun ke :", year, "adalah ", premiums_pv)
        gross_premium = death_benefits_pv / (1 - total_loading)
        profit = gross_premium - death_benefits_pv - expenses
        profit_values.append(profit)
        
    return profit_values, loss_values

def get_mortality_by_sex(sex):
    return mortality4[sex].values
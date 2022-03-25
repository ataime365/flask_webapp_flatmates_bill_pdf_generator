
class Bill:
    """
    Object that contains data about a bill, such as
    total amount and period of the bill.
    """
    
    def __init__(self, amount, period_month):
        self.amount = amount
        self.period_month = period_month        
        
class Flatmate:
    """
    Creates a flatmate person who lives in the flat
    and pays a share of the bill.
    """
    
    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house
        
    def pays(self, bill, *flatmates): # *flatmates gives a tuple, that's why we need a for loop
        total_days_in_house = 0  # total_days_in_house__of_all_other_flatmates
        for flatmate in flatmates:
            total_days_in_house =  total_days_in_house + flatmate.days_in_house
        real_total_days = self.days_in_house + total_days_in_house
        total_amount = bill.amount
        days_coefficient = self.days_in_house / real_total_days
        amount_to_be_paid = days_coefficient * total_amount
        amount_to_be_paid = round(amount_to_be_paid, 2)
        return amount_to_be_paid
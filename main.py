import json
from datetime import datetime

class RentCalculator:
    def __init__(self):
        self.expenses = {}
        self.history = []
    
    def get_valid_input(self, prompt, input_type=float, min_value=0):
        """Get validated user input with error handling"""
        while True:
            try:
                value = input_type(input(prompt))
                if value < min_value:
                    print(f"❌ Value must be at least {min_value}. Try again.")
                    continue
                return value
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
    
    def get_expense_details(self):
        """Collect all expense details from user"""
        print("\n" + "="*50)
        print("🏠 RENT CALCULATOR - Enter Your Expenses")
        print("="*50 + "\n")
        
        self.expenses['total_rent'] = self.get_valid_input("Enter total rent of home: ₹", float, 0)
        self.expenses['light_bill'] = self.get_valid_input("Enter electricity bill: ₹", float, 0)
        self.expenses['water_bill'] = self.get_valid_input("Enter water bill: ₹", float, 0)
        self.expenses['food_bill'] = self.get_valid_input("Enter food bill: ₹", float, 0)
        self.expenses['internet'] = self.get_valid_input("Enter internet bill (0 if not applicable): ₹", float, 0)
        self.expenses['maintenance'] = self.get_valid_input("Enter maintenance charges (0 if not applicable): ₹", float, 0)
        self.expenses['other'] = self.get_valid_input("Enter other expenses (0 if none): ₹", float, 0)
        
        self.expenses['total_persons'] = self.get_valid_input("\nEnter number of persons sharing: ", int, 1)
    
    def calculate_total(self):
        """Calculate total expenses"""
        return sum([
            self.expenses['total_rent'],
            self.expenses['light_bill'],
            self.expenses['water_bill'],
            self.expenses['food_bill'],
            self.expenses['internet'],
            self.expenses['maintenance'],
            self.expenses['other']
        ])
    
    def calculate_per_person(self, total):
        """Calculate per person cost"""
        return total / self.expenses['total_persons']
    
    def get_expense_breakdown(self, total):
        """Get percentage breakdown of each expense"""
        breakdown = {}
        for expense, amount in self.expenses.items():
            if expense != 'total_persons' and amount > 0:
                percentage = (amount / total) * 100
                breakdown[expense] = {
                    'amount': amount,
                    'percentage': percentage
                }
        return breakdown
    
    def display_results(self):
        """Display detailed calculation results"""
        total = self.calculate_total()
        per_person = self.calculate_per_person(total)
        breakdown = self.get_expense_breakdown(total)
        
        print("\n" + "="*50)
        print("📊 CALCULATION RESULTS")
        print("="*50 + "\n")
        
        print("Expense Breakdown:")
        print("-" * 50)
        for expense_name, data in breakdown.items():
            name = expense_name.replace('_', ' ').title()
            print(f"{name:.<30} ₹{data['amount']:>10.2f} ({data['percentage']:>5.1f}%)")
        
        print("-" * 50)
        print(f"{'Total Expenses':.<30} ₹{total:>10.2f}\n")
        
        print("="*50)
        print(f"👥 Number of Persons: {self.expenses['total_persons']}")
        print(f"💰 Per Person Cost: ₹{per_person:.2f}")
        print("="*50 + "\n")
        
        # Save to history
        self.save_to_history(total, per_person)
        
        return total, per_person
    
    def save_to_history(self, total, per_person):
        """Save calculation to history"""
        record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total': total,
            'per_person': per_person,
            'persons': self.expenses['total_persons']
        }
        self.history.append(record)
    
    def show_savings_tip(self, total, per_person):
        """Provide savings suggestions"""
        print("\n💡 SAVINGS TIPS:")
        print("-" * 50)
        
        breakdown = self.get_expense_breakdown(total)
        
        # Find highest expense
        highest = max(breakdown.items(), key=lambda x: x[1]['amount'])
        print(f"• Your highest expense is {highest[0].replace('_', ' ').title()}")
        print(f"  Consider ways to reduce it!")
        
        if self.expenses['light_bill'] > 1000:
            print("• Your electricity bill is high. Try using LED bulbs and")
            print("  unplug devices when not in use.")
        
        if self.expenses['food_bill'] > per_person * 0.4:
            print("• Food expenses are significant. Consider cooking in bulk")
            print("  or meal planning to save money.")
        
        print()
    
    def compare_with_another_person(self):
        """Compare costs if one more/less person shares"""
        total = self.calculate_total()
        current_persons = self.expenses['total_persons']
        
        print("\n🔄 COMPARISON:")
        print("-" * 50)
        
        if current_persons > 1:
            less_person_cost = total / (current_persons - 1)
            print(f"With {current_persons - 1} person(s): ₹{less_person_cost:.2f} per person")
        
        print(f"With {current_persons} person(s): ₹{total/current_persons:.2f} per person (Current)")
        
        more_person_cost = total / (current_persons + 1)
        print(f"With {current_persons + 1} person(s): ₹{more_person_cost:.2f} per person")
        print()

def main():
    """Main function to run the calculator"""
    calculator = RentCalculator()
    
    print("\n🎯 Welcome to Rent Calculator!")
    print("Calculate and split your living expenses easily.\n")
     
    calculator.get_expense_details()
    total, per_person = calculator.display_results()
    calculator.show_savings_tip(total, per_person)
    calculator.compare_with_another_person() 
    
    # Option to calculate again
    while True:
        choice = input("Do you want to calculate again? (yes/no): ").lower()
        if choice in ['yes', 'y']:
            calculator = RentCalculator()  # Create new instance
            calculator.get_expense_details()
            total, per_person = calculator.display_results()
            calculator.show_savings_tip(total, per_person)
            calculator.compare_with_another_person()
        elif choice in ['no', 'n']:
            print("\n✅ Thank you for using Rent Calculator! Goodbye! 👋\n")
            break
        else:
            print("Please enter 'yes' or 'no'")

if __name__ == "__main__":
    main()
    
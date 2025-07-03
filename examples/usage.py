#!/usr/bin/env python3
"""
Usage examples for the sfirat-haomer package.
Demonstrates how to use the package in different scenarios.
"""

import datetime
from sfirat_haomer import get_omer_text_by_date, OmerDay, get_all_omer_days


def example_current_date():
    """Example: Get today's Omer count"""
    print("=== Current Date Example ===")
    
    result = get_omer_text_by_date()
    
    if isinstance(result, OmerDay):
        print(f"Today is day {result.day} of the Omer")
        print(f"Hebrew text: {result.text}")
    else:
        print(f"Today is not during Sefirat HaOmer period: {result}")
    
    print()


def example_gregorian_dates():
    """Example: Get Omer count for specific Gregorian dates"""
    print("=== Gregorian Date Examples ===")
    
    # Example dates (these would need to be adjusted for actual Omer period)
    test_dates = [
        datetime.date(2024, 4, 24),  # Should be 16 Nisan (Day 1)
        datetime.date(2024, 5, 1),   # Should be during Omer period
        datetime.date(2024, 6, 12),  # Should be 5 Sivan (Day 49)
        datetime.date(2024, 3, 15),  # Should be outside Omer period
    ]
    
    for date in test_dates:
        result = get_omer_text_by_date(date)
        if isinstance(result, OmerDay):
            print(f"{date.strftime('%Y-%m-%d')}: Day {result.day} - {result.text}")
        else:
            print(f"{date.strftime('%Y-%m-%d')}: {result}")
    
    print()


def example_hebrew_dates():
    """Example: Get Omer count for Hebrew dates"""
    print("=== Hebrew Date Examples ===")
    
    # Test various Hebrew dates
    hebrew_dates = [
        (16, "Nisan"),   # Day 1
        (30, "Nisan"),   # Day 15
        (1, "Iyyar"),    # Day 16
        (15, "Iyyar"),   # Day 30
        (29, "Iyyar"),   # Day 44
        (1, "Sivan"),    # Day 45
        (5, "Sivan"),    # Day 49
        (6, "Sivan"),    # Outside Omer period
        (15, "Nisan"),   # Outside Omer period
    ]
    
    for day, month in hebrew_dates:
        result = get_omer_text_by_date((day, month))
        if isinstance(result, OmerDay):
            print(f"{day} {month}: Day {result.day} - {result.text}")
        else:
            print(f"{day} {month}: {result}")
    
    print()


def example_all_omer_days():
    """Example: Get all 49 Omer days"""
    print("=== All Omer Days Example ===")
    
    try:
        all_days = get_all_omer_days()
        print(f"Total Omer days: {len(all_days)}")
        
        # Show first few days
        print("\nFirst 7 days:")
        for day in all_days[:7]:
            print(f"  Day {day.day}: {day.text}")
        
        # Show last few days
        print("\nLast 7 days:")
        for day in all_days[-7:]:
            print(f"  Day {day.day}: {day.text}")
        
        # Show some milestone days
        print("\nMilestone days:")
        milestones = [7, 14, 21, 28, 35, 42, 49]
        for milestone in milestones:
            if milestone <= len(all_days):
                day = all_days[milestone - 1]  # Convert to 0-based index
                print(f"  Day {day.day}: {day.text}")
    
    except Exception as e:
        print(f"Error getting all Omer days: {e}")
    
    print()


def example_error_handling():
    """Example: Demonstrate error handling"""
    print("=== Error Handling Examples ===")
    
    # Invalid Hebrew dates
    invalid_dates = [
        (32, "Nisan"),    # Day 32 doesn't exist in Nisan
        (30, "Iyyar"),    # Day 30 doesn't exist in Iyyar
        (15, "Adar"),     # Wrong month
        (0, "Nisan"),     # Day 0 doesn't exist
    ]
    
    for day, month in invalid_dates:
        result = get_omer_text_by_date((day, month))
        print(f"{day} {month}: {result}")
    
    # Invalid input formats
    invalid_inputs = [
        "invalid string",
        (15,),  # Tuple with only one element
        (15, "Nisan", "extra"),  # Tuple with too many elements
        ("15", "Nisan"),  # String instead of int
    ]
    
    for invalid_input in invalid_inputs:
        result = get_omer_text_by_date(invalid_input)
        print(f"{invalid_input}: {result}")
    
    print()


def interactive_example():
    """Interactive example for user input"""
    print("=== Interactive Example ===")
    
    while True:
        print("\nChoose an option:")
        print("1. Get today's Omer count")
        print("2. Enter Hebrew date (day month)")
        print("3. Enter Gregorian date (YYYY-MM-DD)")
        print("4. Show all Omer days")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            result = get_omer_text_by_date()
            if isinstance(result, OmerDay):
                print(f"\nToday is day {result.day} of the Omer")
                print(f"Hebrew text: {result.text}")
            else:
                print(f"\n{result}")
        
        elif choice == "2":
            try:
                date_input = input("Enter Hebrew date (e.g., '16 Nisan'): ").strip()
                parts = date_input.split()
                if len(parts) != 2:
                    print("Invalid format. Please use 'day month' format.")
                    continue
                
                day = int(parts[0])
                month = parts[1]
                
                result = get_omer_text_by_date((day, month))
                if isinstance(result, OmerDay):
                    print(f"\n{day} {month} is day {result.day} of the Omer")
                    print(f"Hebrew text: {result.text}")
                else:
                    print(f"\n{result}")
            
            except ValueError:
                print("Invalid day. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            try:
                date_input = input("Enter Gregorian date (YYYY-MM-DD): ").strip()
                year, month, day = map(int, date_input.split('-'))
                date = datetime.date(year, month, day)
                
                result = get_omer_text_by_date(date)
                if isinstance(result, OmerDay):
                    print(f"\n{date} is day {result.day} of the Omer")
                    print(f"Hebrew text: {result.text}")
                else:
                    print(f"\n{result}")
            
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            try:
                all_days = get_all_omer_days()
                print(f"\nAll {len(all_days)} days of Sefirat HaOmer:")
                for day in all_days:
                    print(f"Day {day.day:2d}: {day.text}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")


def main():
    """Run all examples"""
    print("Sfirat HaOmer Package Usage Examples")
    print("=" * 40)
    
    example_current_date()
    example_gregorian_dates()
    example_hebrew_dates()
    example_all_omer_days()
    example_error_handling()
    
    # Ask if user wants interactive mode
    while True:
        run_interactive = input("Would you like to run the interactive example? (y/n): ").strip().lower()
        if run_interactive in ('y', 'yes'):
            interactive_example()
            break
        elif run_interactive in ('n', 'no'):
            print("Thanks for using the Sfirat HaOmer package!")
            break
        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
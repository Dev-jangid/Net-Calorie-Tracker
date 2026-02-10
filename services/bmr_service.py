"""
BMR Service Module
Contains logic for calculating Basal Metabolic Rate (BMR) for men and women.
"""

def calculate_bmr(weight: float, height: float, age: int, sex: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation.
    
    Formula provided in text.md:
    Men’s BMR = 66.4730 + (13.7516 x weight in kg) + (5.0033 x height in cm) – (6.7550 x age in years)
    Women’s BMR = 655.0955 + (9.5634 x weight in kg) + (1.8496 x height in cm) – (4.6756 x age in years)
    
    Args:
        weight (float): Weight in kg
        height (float): Height in cm
        age (int): Age in years
        sex (str): 'Male' or 'Female'
        
    Returns:
        float: Calculated BMR in calories
    """
    if sex.lower() == 'male':
        bmr = 66.4730 + (13.7516 * weight) + (5.0033 * height) - (6.7550 * age)
    elif sex.lower() == 'female':
        bmr = 655.0955 + (9.5634 * weight) + (1.8496 * height) - (4.6756 * age)
    else:
        raise ValueError("Sex must be 'Male' or 'Female'")
        
    return bmr

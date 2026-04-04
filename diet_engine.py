def calculate_diet(weight, height, age, goal, diet_type):

    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    maintenance = bmr * 1.55

    if goal == "Fat Loss":
        calories = maintenance - 400
        protein = weight * 2
        carbs = weight * 2
        fats = weight * 0.8
    else:
        calories = maintenance + 300
        protein = weight * 2.2
        carbs = weight * 4
        fats = weight * 1

    if diet_type == "Veg":
        meals = {
            "Breakfast": "Oats + Milk + Peanut Butter",
            "Lunch": "Rice + Dal + Paneer",
            "Snacks": "Banana + Almonds",
            "Dinner": "Roti + Sabzi + Curd"
        }
    else:
        meals = {
            "Breakfast": "Oats + Eggs",
            "Lunch": "Rice + Chicken",
            "Snacks": "Boiled Eggs + Banana",
            "Dinner": "Roti + Chicken + Curd"
        }

    return {
        "Calories": round(calories),
        "Protein": round(protein),
        "Carbs": round(carbs),
        "Fats": round(fats),
        "Diet Plan": meals
    }

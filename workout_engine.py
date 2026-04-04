def generate_workout(level, goal):

    if goal == "Fat Loss":
        return {
            "Day 1": "Chest + 20 min Cardio",
            "Day 2": "Back + 20 min Cardio",
            "Day 3": "Legs + 15 min HIIT",
            "Day 4": "Shoulders + Core",
            "Day 5": "Full Body + Cardio"
        }

    else:
        if level == "Beginner":
            return {
                "Day 1": "Full Body Workout",
                "Day 2": "Rest",
                "Day 3": "Full Body Workout",
                "Day 4": "Rest",
                "Day 5": "Light Cardio"
            }
        else:
            return {
                "Day 1": "Push (Chest, Shoulders, Triceps)",
                "Day 2": "Pull (Back, Biceps)",
                "Day 3": "Legs",
                "Day 4": "Rest",
                "Day 5": "Upper Body"
            }

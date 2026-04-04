def analyze_progress(weight_list):

    if len(weight_list) < 2:
        return "Not enough data to analyze."

    if weight_list[-1] < weight_list[0]:
        return "🔥 Great progress! Keep going!"
    elif weight_list[-1] > weight_list[0]:
        return "⚠ Weight increased. Adjust calories or increase cardio."
    else:
        return "No major change detected."

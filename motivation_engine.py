def get_motivation_message(focused_minutes):
    if focused_minutes < 5:
        return "It's okay! Every minute of focus counts. Let's try again "

    elif focused_minutes < 15:
        return "Nice start! You're building focus momentum. Keep it up!"

    elif focused_minutes < 30:
        return "Great job! You stayed focused really well. Keep going!"

    else:
        return "Amazing discipline! You're in deep focus mode. Keep pushing forward!"
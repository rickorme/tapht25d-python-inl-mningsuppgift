debug_on = False

def debug_print(message):
    if debug_on:
        print(f"DEBUG: {message}")

def toggle_debug():
    global debug_on
    debug_on = not debug_on
    print(f"Debug mode {'on' if debug_on else 'off'}.")
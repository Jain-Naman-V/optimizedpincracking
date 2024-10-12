import random
import time
import threading
from queue import Queue

# Simulated device checking PIN
def device_check(pin, correct_pin):
    # Simulate timing attack vulnerability
    time.sleep(0.01 * sum([1 for x, y in zip(pin, correct_pin) if x == y]))
    
    # Simulate a simple match
    return pin == correct_pin

# SQL Injection simulation
def sql_injection_attack(correct_pin):
    injected_pin = "' OR 1=1 --"
    if device_check(injected_pin, correct_pin):
        return f"Cracked PIN (SQL Injection): {injected_pin}"
    return None

# Brute force with common PINs + personalized data
def brute_force(personal_pins, correct_pin):
    for pin in personal_pins:
        if device_check(pin, correct_pin):
            return f"Cracked PIN (Common/Personal): {pin}"
    return None

# Timing attack to reduce the search space
def timing_attack(correct_pin):
    likely_digits = []
    for i in range(6):
        max_time = 0
        best_digit = None
        for digit in range(10):
            test_pin = "".join(likely_digits + [str(digit)] + ["0"] * (5 - len(likely_digits)))
            start = time.time()
            device_check(test_pin, correct_pin)
            elapsed = time.time() - start
            if elapsed > max_time:
                max_time = elapsed
                best_digit = str(digit)
        likely_digits.append(best_digit)
    return "".join(likely_digits)

# Man-in-the-middle attack
def mitm_attack():
    decrypted_pin = "276" + "XXX"
    return decrypted_pin

# Worker function for multithreaded brute-force
def brute_force_worker(q, result, correct_pin):
    while not q.empty():
        pin = q.get()
        if device_check(pin, correct_pin):
            result[0] = pin  # Store the result in the shared list
            break
        q.task_done()

# Multithreaded brute-force search
def multithreaded_brute_force(correct_pin):
    q = Queue()
    result = [None]

    # Queue up all possible 6-digit PINs
    for attempt in range(1000000):
        pin = f"{attempt:06d}"
        q.put(pin)

    # Start threads for parallel brute-forcing
    threads = []
    for _ in range(8):  # Using 8 threads for parallelism
        t = threading.Thread(target=brute_force_worker, args=(q, result, correct_pin))
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    q.join()
    
    # Return the result once found
    return result[0]

# Main hybrid attack function with multithreading
def hybrid_attack(correct_pin, personal_pins):
    print("Starting optimized hybrid attack...\n")
    
    # Step 1: SQL Injection Attack
    print("Step 1: Attempting SQL Injection...")
    result = sql_injection_attack(correct_pin)
    if result:
        return result
    
    # Step 2: Try common PINs + personalized data (dictionary brute-force)
    print("Step 2: Trying common and personalized PINs...")
    pin = brute_force(personal_pins, correct_pin)
    if pin:
        return pin
    
    # Step 3: Timing attack for side-channel hints
    print("Step 3: Performing timing attack...")
    pin = timing_attack(correct_pin)
    if device_check(pin, correct_pin):
        return f"Cracked PIN (Timing Attack): {pin}"
    
    # Step 4: Multithreaded brute-force attack
    print("Step 4: Multithreaded brute-force...")
    pin = multithreaded_brute_force(correct_pin)
    if pin:
        return f"Cracked PIN (Multithreaded Brute-Force): {pin}"
    
    # Step 5: Man-in-the-middle attack to capture partial info
    print("Step 5: Performing MITM attack...")
    pin = mitm_attack()
    if device_check(pin, correct_pin):
        return f"Cracked PIN (MITM): {pin}"
    
    return "Failed to crack within 10 attempts"

# Input data from the user
correct_pin = input("Enter the target PIN (for simulation): ")
dob = input("Enter the target's date of birth (DDMMYY): ")
vehicle_number = input("Enter the target's vehicle number (last 4 digits): ")
mobile_number = input("Enter the target's mobile number (last 4 digits): ")

# List of common PINs (for Dictionary Attack) and personal data
common_pins = ["123456", "000000", "111111", "654321", "121212", "696969"]
personal_pins = common_pins + [dob, vehicle_number, mobile_number]

# Execute the hybrid attack
result = hybrid_attack(correct_pin, personal_pins)
print(result)

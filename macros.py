import time


def teleport_loop(switch):
    print("--- STARTING TELEPORT LOOP (Press Ctrl+C to stop) ---")

    while True:
        switch.press('PLUS', wait=1.5)
        # 6:30 Angle movement
        switch.move_stick(100, 255, duration=0.20)
        switch.press('A', wait=0.8)
        switch.press('A')
        print(" (Teleporting...)")
        time.sleep(5.5)

def hatch_eggs(switch):
    print("--- STARTING EGG HATCHING (Press Ctrl+C to stop) ---")
    print("Ensure you are on your mount in an open area!")
    time.sleep(2)

    while True:
        # Ride in a big circle by holding Right and Down
        switch.move_stick(255, 255, duration=5.0) 
        
        print("Checking for hatches...")
        for _ in range(10):
            switch.press('A', hold=0.1, wait=0.1)

def bench_sit(switch):
    print("--- STARTING BENCH SITTING (Press Ctrl+C to stop) ---")
    print("Make sure that you are in front of a bench, facing away from it")
    resetCounters=0
    try:
        while True:
            # Straight down angle
            switch.move_stick(128, 255, duration=0.20)
            switch.press('A', wait=0.8)
            switch.press('A', wait=0.8)
            switch.press('A', wait=0.8)
            switch.press('A', wait=0.8)
            switch.press('A')
            time.sleep(5.5)
            resetCounters+=1
    except KeyboardInterrupt:
        print("\n[!] Bench sitting stopped by user.")
        print(f"Total bench sits: {resetCounters}")
        raise
    
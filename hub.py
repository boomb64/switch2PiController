import time
from controller import SwitchController
import macros

def main():
    print("=========================================")
    print("  SWITCH AUTOMATION HUB  ")
    print("1. Go to 'Change Grip/Order'")
    print("2. Plug in Pi")
    print("=========================================")
    time.sleep(5)

    # 1. Connect Once
    switch = SwitchController()
    switch.connect()

    # 2. The Main Menu Loop
    while True:
        print("\n" + "="*30)
        print(" SELECT A MACRO:")
        print(" 1. Teleport Loop")
        print(" 2. Hatch Eggs")
        print(" 3. Bench Sit")
        print(" q. Quit & Disconnect")
        print("="*30)
        
        choice = input("Choice > ").strip().lower()

        if choice == 'q':
            print("Shutting down...")
            break
            
        elif choice == '1':
            try:
                # Run the macro
                macros.teleport_loop(switch)
            except KeyboardInterrupt:
                # Catch the Ctrl+C and clean up
                print("\n[!] Teleport macro stopped by user.")
                switch.release_all() # Ensure no buttons are stuck!
                time.sleep(1) # Give it a second to breathe
                
        elif choice == '2':
            try:
                macros.hatch_eggs(switch)
            except KeyboardInterrupt:
                print("\n[!] Egg Hatching stopped by user.")
                switch.release_all()
                time.sleep(1)
        
        elif choice == '3':
            try:
                macros.bench_sit(switch)
            except KeyboardInterrupt:
                print("\n[!] Bench Sitting stopped by user.")
                switch.release_all()
                time.sleep(1)
                
        else:
            print("Invalid choice. Try again.")

    # 3. Cleanup on Exit
    switch.disconnect()

if __name__ == "__main__":
    main()
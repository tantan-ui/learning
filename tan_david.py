import random
from datetime import datetime, timedelta
import time
import sys

def ip_pool(size=6, min_val=1, max_val=20):
    if size > (max_val - min_val + 1):
        raise ValueError("Pool size is bigger than the available unique numbers in range.")

    pool = set()
    while len(pool) < size:
        pool.add(random.randint(min_val, max_val))

    print(f"Your current IP Pool: {sorted(pool)}")
    return pool

def lease(minutes=5):
    return datetime.now() + timedelta(minutes=minutes)

def cleanup_expired(assignments, pool):
    """Remove expired leases and return values back to the pool."""
    now = datetime.now()
    expired_names = [name for name, (_, expiry) in assignments.items() if now >= expiry]

    for name in expired_names:
        value, _ = assignments.pop(name)
        pool.add(value)
        print(f"\n[LEASE EXPIRED] {name}'s lease ended.")
        print(f"[SYSTEM] Sending shutdown signal to {name}...")
        print(f"[SYSTEM] {name} is now disconnected.\n")
    # IMPORTANT: do NOT sys.exit() here — one client expiring should not kill the server.

def show_status(assignments, pool):
    print(f"\nPool left ({len(pool)}): {sorted(pool)}")
    if not assignments:
        print("Assignments: (none)\n")
    else:
        print("Assignments:")
        for n, (val, exp) in assignments.items():
            print(f"  {n} -> {val} (expires: {exp.strftime('%H:%M:%S')})")
        print()

def extend_lease(assignments):
    """Extend lease for a specific client."""
    if not assignments:
        print("No active assignments to extend.\n")
        return

    client = input("Which client do you want to extend? ").strip()
    if client not in assignments:
        print(f"Client '{client}' not found.\n")
        return

    value, expiry = assignments[client]
    a = input(f"Extend lease for '{client}'? (yes/no): ").strip().lower()

    if a == "yes":
        # Extend from the later of (current expiry) or (now), so you never shorten it.
        base = max(expiry, datetime.now())
        new_expiry = base + timedelta(minutes=5)
        assignments[client] = (value, new_expiry)
        print(f"Lease extended until {new_expiry.strftime('%H:%M:%S')}\n")
    else:
        print("Lease not extended.\n")

def dhcp():
    pool = ip_pool()
    assignments = {}

    print("\nEnter a name to get a value.")
    print("Commands: show, exit, extend\n")

    while True:
        cleanup_expired(assignments, pool)

        if assignments:
            time.sleep(1)  # slow down loop a bit

        cmd = input("> ").strip()

        if not cmd:
            print("Name can't be empty.")
            continue

        low = cmd.lower()

        if low == "exit":
            break

        if low == "show":
            show_status(assignments, pool)
            continue

        if low == "extend":
            extend_lease(assignments)
            continue

        # Otherwise, treat input as a client name asking for a lease
        name = cmd

        if name in assignments:
            val, exp = assignments[name]
            print(f"'{name}' already has {val} (expires: {exp.strftime('%H:%M:%S')})\n")
            continue

        if not pool:
            print("No values left in the pool!\n")
            continue

        value = pool.pop()
        expiry = lease(minutes=1)
        assignments[name] = (value, expiry)
        print(f"Assigned {value} to '{name}' (lease until {expiry.strftime('%H:%M:%S')})\n")

if __name__ == "__main__":
    dhcp()
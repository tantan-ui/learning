import random
from datetime import datetime, timedelta
import time

MAX_DEVICES_PER_IP = 5

def ip_pool(size=6, min_val=0, max_val=20):
    initial_ip = "192.168.8."
    numbers = set()
    while len(numbers) < size:
        numbers.add(random.randint(min_val, max_val))

    pool = {initial_ip + str(num) for num in numbers}
    print(f"Your current IP Pool: {sorted(pool)}")
    return pool


def lease(minutes=5):
    return datetime.now() + timedelta(minutes=minutes)


def cleanup_expired(assignments, ip_usage):
    now = datetime.now()
    expired_clients = []

    for name, (ip, expiry) in assignments.items():
        if now >= expiry:
            expired_clients.append(name)

    for name in expired_clients:
        ip, _ = assignments.pop(name)
        ip_usage[ip] -= 1
        print(f"\n[LEASE EXPIRED] {name}'s lease ended.")
        print(f"[SYSTEM] {name} is now disconnected.\n")


def check_for_extension(assignments):
    now = datetime.now()

    for name, (ip, expiry) in list(assignments.items()):
        remaining = (expiry - now).total_seconds()

        if 0 < remaining <= 60:
            print(f"\n[WARNING] {name}'s lease expires in {int(remaining)} seconds.")
            ans = input(f"Extend lease for '{name}'? (yes/no): ").strip().lower()

            if ans == "yes":
                new_expiry = datetime.now() + timedelta(minutes=1)
                assignments[name] = (ip, new_expiry)
                print(f"Lease extended until {new_expiry.strftime('%H:%M:%S')}\n")
            else:
                print("Lease not extended.\n")


def show_status(assignments, ip_usage):
    print("\nAssignments:")
    if not assignments:
        print("(none)")
    else:
        for name, (ip, exp) in assignments.items():
            print(f"  {name} -> {ip} (expires: {exp.strftime('%H:%M:%S')})")

    print("\nIP Usage:")
    for ip, count in ip_usage.items():
        print(f"  {ip}: {count}/{MAX_DEVICES_PER_IP}")

    print()


def extend_lease(assignments):
    if not assignments:
        print("No active assignments.\n")
        return

    client = input("Which client do you want to extend? ").strip()

    if client not in assignments:
        print("Client not found.\n")
        return

    ip, expiry = assignments[client]
    new_expiry = max(expiry, datetime.now()) + timedelta(minutes=5)
    assignments[client] = (ip, new_expiry)
    print(f"Lease extended until {new_expiry.strftime('%H:%M:%S')}\n")


def dhcp():
    pool = ip_pool()
    assignments = {}
    ip_usage = {ip: 0 for ip in pool}

    print("\nEnter a name to get an IP.")
    print("Commands: show, extend, exit\n")

    while True:
        cleanup_expired(assignments, ip_usage)
        check_for_extension(assignments)

        cmd = input("> ").strip()

        if not cmd:
            print("Name can't be empty.\n")
            continue

        low = cmd.lower()

        if low == "exit":
            break

        if low == "show":
            show_status(assignments, ip_usage)
            continue

        if low == "extend":
            extend_lease(assignments)
            continue

        name = cmd

        if name in assignments:
            ip, exp = assignments[name]
            print(f"{name} already has {ip} (expires: {exp.strftime('%H:%M:%S')})\n")
            continue

        available_ips = [ip for ip, count in ip_usage.items() if count < MAX_DEVICES_PER_IP]

        if not available_ips:
            print("All IPs are at maximum capacity!\n")
            continue

        ip = random.choice(available_ips)
        expiry = lease(minutes=1)

        assignments[name] = (ip, expiry)
        ip_usage[ip] += 1

        print(f"Assigned {ip} to '{name}' (lease until {expiry.strftime('%H:%M:%S')})\n")


if __name__ == "__main__":
    dhcp()
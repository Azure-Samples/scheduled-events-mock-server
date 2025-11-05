#!/usr/bin/env python3
import requests
import argparse
import time

base_url = "http://127.0.0.1"
set_scenario_url = f"{base_url}/set-scenario"
generate_event_url = f"{base_url}/generate-event"

scenarios = {
    "Live Migration": True,
    "User Reboot": True,
    "Host Agent Maintenance": True,
    "Redeploy": True,
    "User Redeploy": True,
    "Canceled Maintenance": True
}

def list_scenarios():
    print("Available scenarios:")
    for s in scenarios:
        print(f"- {s}")

def trigger_scenario(scenario, sleep_duration=5):
    if scenario not in scenarios:
        print(f"Scenario '{scenario}' is not recognized.")
        return False

    r1 = requests.post(set_scenario_url, data={"scenario": scenario})
    if r1.status_code not in [200, 302]:
        print(f"Failed to set scenario '{scenario}' (HTTP {r1.status_code})")
        return False

    success = True
    for status in ["Scheduled", "Started", "Completed"]:
        r2 = requests.post(generate_event_url, data={"event_status": status, "resources": "vmss_vm1"})
        if r2.status_code not in [200, 302]:
            print(f"Failed to generate '{status}' for scenario '{scenario}' (HTTP {r2.status_code})")
            success = False
        else:
            print(f"Triggered scenario '{scenario}' with status '{status}'")
            time.sleep(sleep_duration)

    return success

def loop_scenarios(selected_scenario=None, interval=10, sleep_duration=5):
    try:
        while True:
            if selected_scenario:
                trigger_scenario(selected_scenario, sleep_duration)
            else:
                for scenario in scenarios:
                    trigger_scenario(scenario, sleep_duration)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped loop.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger Azure Scheduled Event Scenarios")
    parser.add_argument("--list", action="store_true", help="List available scenarios")
    parser.add_argument("--scenario", type=str, help="Trigger a specific scenario")
    parser.add_argument("--all", action="store_true", help="Trigger all scenarios")
    parser.add_argument("--loop", action="store_true", help="Loop triggering")
    parser.add_argument("--interval", type=int, default=10, help="Interval in seconds for loop")
    parser.add_argument("--sleep", type=int, default=5, help="Sleep duration between scenario event status changes")

    args = parser.parse_args()

    if args.list:
        list_scenarios()
    elif args.loop:
        loop_scenarios(args.scenario if args.scenario else None, args.interval, args.sleep)
    elif args.all:
        for scenario in scenarios:
            trigger_scenario(scenario, args.sleep)
    elif args.scenario:
        trigger_scenario(args.scenario, args.sleep)
    else:
        parser.print_help()

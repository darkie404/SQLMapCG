import requests
import json
import csv
from tabulate import tabulate

# API Configuration
BASE_URL = "https://www.acko.com/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=rto"

HEADERS = {
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Connection": "keep-alive",
}

COOKIES = {
    "trackerid": "33febc-7256-4b84-9efb-fc99c9dfdf60",
    "acko_visit": "Hl1oyupruXl5pNZxqkdZSQ",
    "user_id": "j3hMTZKo1oCf4RctlFxdgw:1733332955688:cc4982d8ea5d040043af07feae033e693b8ff953",
    "__cf_bm": "3ThWHhh1QI7O4Xp8vN6iTmTlkmQkrDxs_Z3DQZhPzEM-1733509946-1.0.1.1-OM7X18upnfCvA1utZg7KWb3E7VhfRZ6MdUyfGZMLSaGRONG5XeKl8SfZI9_MVsbr_AMi2YPRByJROBtzyJ6g0A"
}

# Function to fetch vehicle data
def fetch_vehicle_data(vehicle_number):
    url = BASE_URL.format(vehicle_number=vehicle_number)
    try:
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed for {vehicle_number}. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data for {vehicle_number}: {e}")
        return None

# Function to display data in a vertical table format for each vehicle
def display_vertical_table(data, vehicle_number):
    if not data:
        print(f"No data for {vehicle_number}.")
        return

    print(f"\n--- Vehicle Details for {vehicle_number} ---")

    # Creating a list of keys and values for the table (with prioritized order)
    table = []
    for key, value in data.items():
        # If it's a nested dictionary or list, convert it to a string for display
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value, indent=4)
        # Add the entry to the table (long addresses will be shown fully)
        table.append([key, value])
    
    # Display table using tabulate, with headers for "Field" and "Value"
    print(tabulate(table, headers=["Field", "Value"], tablefmt="grid", numalign="left", stralign="left"))

# Function to save data to CSV
def save_to_csv(data_list, output_file="vehicle_data.csv"):
    try:
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Writing header (Fields)
            writer.writerow(["Vehicle Number", "Field", "Value"])

            # Writing data for each vehicle
            for data in data_list:
                vehicle_number = data.get("vehicle_number", "N/A")
                
                # Write prioritized fields first
                for key, value in data.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    writer.writerow([vehicle_number, key, value])

        print(f"\n--- Data Saved to {output_file} ---")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main function
def main():
    print("Enter vehicle numbers separated by commas (e.g., UP32DD1153,UP52BX6287):")
    user_input = input("> ")
    vehicle_numbers = [vn.strip() for vn in user_input.split(",") if vn.strip()]
    if not vehicle_numbers:
        print("No vehicle numbers provided. Exiting.")
        return

    all_data = []
    for vehicle_number in vehicle_numbers:
        print(f"\nFetching details for {vehicle_number}...")
        data = fetch_vehicle_data(vehicle_number)
        if data:
            data["vehicle_number"] = vehicle_number  # Add vehicle number for clarity
            all_data.append(data)
            display_vertical_table(data, vehicle_number)  # Show data in vertical table for each vehicle

    if all_data:
        save_to_csv(all_data)  # Save all data to CSV

if __name__ == "__main__":
    main()

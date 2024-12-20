import requests
import json
import os

# API Configuration
BASE_URL = "https://www.com/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=rto"

HEADERS = {
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Connection": "keep-alive",
}

COOKIES = {
    "trackerid": "9033febc-7256-4b84-9efb-fc99c9dfdf60",
    "user_id": "j3hMTZKo1oCf4RctlFxdgw:733332955688:cc4982d8ea5d040043af07feae033e693b8ff953",
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

# Function to save prioritized vehicle data into a text file
def save_vehicle_data_to_file(vehicle_number, data):
    if not data:
        print(f"No data available for {vehicle_number}.")
        return

    # Prepare file name and path
    file_name = f"{vehicle_number}.txt"
    file_path = os.path.join(os.getcwd(), file_name)

    # Improved field names for readability and prioritization
    prioritized_fields = [
        "asset_number",
        "owner_name",
        "registration_date",
        "make_model",
        "fuel_type",
        "vehicle_type",
        "registration_address",
        "permanent_address",
        "present_address",
        "previous_policy_expiry_date",
        "is_commercial"
    ]

    field_mapping = {
        "asset_number": "Vehicle Number",
        "asset_type": "Vehicle Type",
        "registration_year": "Registration Year",
        "registration_month": "Registration Month",
        "make_model": "Make Model",
        "vehicle_type": "Vehicle Type",
        "make_name": "Make Name",
        "fuel_type": "Fuel Type",
        "owner_name": "Owner Name",
        "previous_insurer": "Previous Insurer",
        "previous_policy_expiry_date": "Previous Policy Expiry Date",
        "is_commercial": "Is Commercial",
        "vehicle_type_v2": "Vehicle Type V2",
        "vehicle_type_processed": "Vehicle Type Processed",
        "permanent_address": "Permanent Address",
        "present_address": "Present Address",
        "registration_date": "Registration Date",
        "registration_address": "Registration Address",
        "model_name": "Model Name",
        "make_name2": "Make Name (Detailed)",
        "model_name2": "Model Name (Detailed)",
        "variant_id": "Variant ID",
        "previous_policy_expired": "Previous Policy Expired"
    }

    # Write prioritized data to the text file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Vehicle Details for {vehicle_number}\n")
            file.write("=" * 40 + "\n")

            for field in prioritized_fields:
                if field in data:
                    readable_key = field_mapping.get(field, field)
                    value = data[field]
                    # Format nested data
                    if isinstance(value, list) or isinstance(value, dict):
                        value = json.dumps(value, indent=4)
                    file.write(f"{readable_key}: {value}\n")

            file.write("\nAdditional Details:\n")
            file.write("-" * 40 + "\n")
            for key, value in data.items():
                if key not in prioritized_fields:
                    readable_key = field_mapping.get(key, key)
                    # Format nested data
                    if isinstance(value, list) or isinstance(value, dict):
                        value = json.dumps(value, indent=4)
                    file.write(f"{readable_key}: {value}\n")

        # Display saved data in the terminal
        print(f"\n--- Data for {vehicle_number} ---")
        with open(file_path, "r", encoding="utf-8") as file:
            print(file.read())
    except Exception as e:
        print(f"Error saving data for {vehicle_number}: {e}")

# Main function
def main():
    print("Enter vehicle numbers separated by commas (e.g., XY12AB1234,MH23DL9999):")
    user_input = input("> ")
    vehicle_numbers = [vn.strip() for vn in user_input.split(",") if vn.strip()]
    if not vehicle_numbers:
        print("No vehicle numbers provided. Exiting.")
        return

    for vehicle_number in vehicle_numbers:
        print(f"\nFetching details for {vehicle_number}...")
        data = fetch_vehicle_data(vehicle_number)
        save_vehicle_data_to_file(vehicle_number, data)

    input("\nPress <ENTER> to exit.")

if __name__ == "__main__":
    main()

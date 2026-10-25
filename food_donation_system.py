
import json
import os
from datetime import datetime

USERS_FILE = "food_users.json"
DONATIONS_FILE = "food_donations.json"

STATUSES = ["Available", "Claimed", "Picked Up", "Delivered"]


def load_data(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not load {filename}.")
        return []


def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print(f"Error: Could not save {filename}.")
        return False


def next_id(records, prefix, field):
    numbers = []
    for record in records:
        value = record.get(field, "")
        if value.startswith(prefix):
            try:
                numbers.append(int(value[len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_positive_quantity():
    while True:
        try:
            value = float(input("Quantity (meals): "))
            if value > 0:
                return value
            print("Quantity must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")


def valid_time(value):
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


class UserManager:
    def __init__(self):
        self.users = load_data(USERS_FILE)

    def register_user(self):
        role = input("Role (Donor/Volunteer): ").strip().lower()
        if role not in ("donor", "volunteer"):
            print("Invalid role.")
            return

        name = get_text("Name: ")
        contact = get_text("Contact information: ")

        prefix = "DONR" if role == "donor" else "VOL"
        user_id = next_id(self.users, prefix, "user_id")

        user = {
            "user_id": user_id,
            "name": name,
            "role": role.title(),
            "contact": contact
        }
        self.users.append(user)

        if save_data(USERS_FILE, self.users):
            print(f"{role.title()} registered successfully.")
            print("User ID:", user_id)
        else:
            self.users.remove(user)

    def find_user(self, user_id, role=None):
        for user in self.users:
            if user["user_id"].lower() == user_id.lower():
                if role is None or user["role"].lower() == role.lower():
                    return user
        return None


class DonationManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.donations = load_data(DONATIONS_FILE)

    def create_donation(self):
        donor_id = get_text("Enter registered Donor ID: ")
        donor = self.user_manager.find_user(donor_id, "Donor")

        if not donor:
            print("Donor not found. Register the donor first.")
            return

        food_name = get_text("Food name: ")
        quantity = get_positive_quantity()
        location = get_text("Pickup location: ")
        available_until = get_text(
            "Available until (YYYY-MM-DD HH:MM): "
        )

        if not valid_time(available_until):
            print("Invalid date/time. Use YYYY-MM-DD HH:MM.")
            return

        if datetime.strptime(available_until, "%Y-%m-%d %H:%M") <= datetime.now():
            print("Available-until time must be in the future.")
            return

        donation_id = next_id(self.donations, "DON", "donation_id")

        donation = {
            "donation_id": donation_id,
            "donor_id": donor["user_id"],
            "donor_name": donor["name"],
            "food_name": food_name,
            "quantity": quantity,
            "location": location,
            "available_until": available_until,
            "contact": donor["contact"],
            "status": "Available",
            "volunteer_id": None
        }

        self.donations.append(donation)

        if save_data(DONATIONS_FILE, self.donations):
            print("\nDonation created successfully!")
            print("Donation ID:", donation_id)
            print("Status: Available")
        else:
            self.donations.remove(donation)

    def view_donations(self, available_only=False):
        records = [
            donation for donation in self.donations
            if not available_only or self.is_available(donation)
        ]

        if not records:
            print("No matching donations found.")
            return

        print("\n===== FOOD DONATIONS =====")
        for donation in records:
            print("\nDonation ID:", donation["donation_id"])
            print("Food:", donation["food_name"])
            print("Quantity:", donation["quantity"], "meals")
            print("Location:", donation["location"])
            print("Available until:", donation["available_until"])
            print("Contact:", donation["contact"])
            print("Status:", donation["status"])
            if donation["volunteer_id"]:
                print("Volunteer:", donation["volunteer_id"])

    @staticmethod
    def is_available(donation):
        if donation["status"] != "Available":
            return False
        try:
            expiry = datetime.strptime(
                donation["available_until"], "%Y-%m-%d %H:%M"
            )
            return expiry > datetime.now()
        except (ValueError, TypeError):
            return False

    def find_donation(self, donation_id):
        for donation in self.donations:
            if donation["donation_id"].lower() == donation_id.lower():
                return donation
        return None

    def claim_donation(self):
        volunteer_id = get_text("Enter registered Volunteer ID: ")
        volunteer = self.user_manager.find_user(volunteer_id, "Volunteer")

        if not volunteer:
            print("Volunteer not found. Register the volunteer first.")
            return

        donation_id = get_text("Donation ID to claim: ")
        donation = self.find_donation(donation_id)

        if not donation:
            print("Donation not found.")
            return

        if not self.is_available(donation):
            print("Donation is unavailable, expired, or already claimed.")
            return

        donation["status"] = "Claimed"
        donation["volunteer_id"] = volunteer["user_id"]

        if save_data(DONATIONS_FILE, self.donations):
            print("Donation", donation_id, "successfully claimed!")
            print("Status: Claimed")
            print("Volunteer:", volunteer["user_id"])
        else:
            donation["status"] = "Available"
            donation["volunteer_id"] = None

    def advance_status(self):
        donation_id = get_text("Donation ID: ")
        donation = self.find_donation(donation_id)

        if not donation:
            print("Donation not found.")
            return

        current = donation["status"]

        if current not in STATUSES[:-1]:
            print("Donation is already delivered.")
            return

        next_status = STATUSES[STATUSES.index(current) + 1]

        if current == "Available":
            print("A volunteer must claim the donation first.")
            return

        donation["status"] = next_status

        if save_data(DONATIONS_FILE, self.donations):
            print("Donation status updated:", current, "->", next_status)
        else:
            donation["status"] = current


def main():
    users = UserManager()
    donations = DonationManager(users)

    while True:
        print("\n===== FOOD DONATION MANAGEMENT =====")
        print("1. Register Donor/Volunteer")
        print("2. Create Food Donation")
        print("3. View Available Donations")
        print("4. Claim Donation")
        print("5. Update Donation Status")
        print("6. View All Donations")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            users.register_user()
        elif choice == "2":
            donations.create_donation()
        elif choice == "3":
            donations.view_donations(available_only=True)
        elif choice == "4":
            donations.claim_donation()
        elif choice == "5":
            donations.advance_status()
        elif choice == "6":
            donations.view_donations()
        elif choice == "7":
            print("Food Donation Management System closed.")
            break
        else:
            print("Invalid option. Choose 1-7.")


if __name__ == "__main__":
    main()

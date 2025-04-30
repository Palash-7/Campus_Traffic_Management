

import json
import os
import re
from typing import List, Dict, Any, Optional

class ResidentManager:
    def __init__(self, file_path: str = 'resident.json'):
        """Initialize the ResidentManager with the path to the resident.json file."""
        self.file_path = file_path
        self.residents = self.load_residents()

    def load_residents(self) -> List[Dict[str, Any]]:
        """Load the resident data from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Creating a new file.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding {self.file_path}. Starting with an empty list.")
            return []

    def save_residents(self) -> None:
        """Save the resident data to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.residents, file, indent=2)
        print(f"Data saved to {self.file_path}")

    def add_resident(self, vehicle_number: str, name: str, phone: str, 
                    campus_id: str, email: str) -> bool:
        """Add a new resident to the database."""
        
        if not self._validate_inputs(vehicle_number, name, phone, campus_id, email):
            return False
            
        
        if self.find_resident_by_vehicle(vehicle_number):
            print(f"Vehicle {vehicle_number} already registered.")
            return False
            
        new_resident = {
            "VehicleNumber": vehicle_number.upper(),
            "OwnerName": name,
            "OwnerPhone": phone,
            "OwnerCampusID": campus_id,
            "OwnerEmail": email
        }
        
        self.residents.append(new_resident)
        print(f"Added: {name}'s vehicle {vehicle_number}")
        return True

    def delete_resident(self, vehicle_number: str) -> bool:
        """Delete a resident by vehicle number."""
        for i, resident in enumerate(self.residents):
            if resident["VehicleNumber"].upper() == vehicle_number.upper():
                removed = self.residents.pop(i)
                print(f"Removed: {removed['OwnerName']}'s vehicle {vehicle_number}")
                return True
        
        print(f"Vehicle number {vehicle_number} not found.")
        return False
    
    def update_resident(self, vehicle_number: str, **kwargs) -> bool:
        """Update a resident's information by vehicle number."""
        for resident in self.residents:
            if resident["VehicleNumber"].upper() == vehicle_number.upper():
                
                if "OwnerPhone" in kwargs and not self._validate_phone(kwargs["OwnerPhone"]):
                    return False
                if "OwnerEmail" in kwargs and not self._validate_email(kwargs["OwnerEmail"]):
                    return False
                
                
                for key, value in kwargs.items():
                    if key in resident:
                        resident[key] = value
                
                print(f"Updated: {resident['OwnerName']}'s vehicle {vehicle_number}")
                return True
        
        print(f"Vehicle number {vehicle_number} not found.")
        return False
    
    def find_resident_by_vehicle(self, vehicle_number: str) -> Optional[Dict[str, Any]]:
        """Find a resident by vehicle number."""
        for resident in self.residents:
            if resident["VehicleNumber"].upper() == vehicle_number.upper():
                return resident
        return None
    
    def find_residents_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Find residents by name (partial match)."""
        matches = []
        name_lower = name.lower()
        for resident in self.residents:
            if name_lower in resident["OwnerName"].lower():
                matches.append(resident)
        return matches
    
    def find_residents_by_campus_id(self, campus_id: str) -> List[Dict[str, Any]]:
        """Find residents by campus ID."""
        matches = []
        for resident in self.residents:
            if resident["OwnerCampusID"].upper() == campus_id.upper():
                matches.append(resident)
        return matches
    
    def get_all_residents(self) -> List[Dict[str, Any]]:
        """Get all residents."""
        return self.residents
    
    def _validate_inputs(self, vehicle_number: str, name: str, phone: str, 
                        campus_id: str, email: str) -> bool:
        """Validate all input fields."""
        if not self._validate_vehicle_number(vehicle_number):
            print("Invalid vehicle number format.")
            return False
        
        if not name or len(name.strip()) < 3:
            print("Name must be at least 3 characters.")
            return False
            
        if not self._validate_phone(phone):
            print("Invalid phone number format. Use +91XXXXXXXXXX format.")
            return False
            
        if not campus_id or not campus_id.startswith("CMP"):
            print("Campus ID must start with CMP.")
            return False
            
        if not self._validate_email(email):
            print("Invalid email format. Must end with @campus.edu")
            return False
            
        return True
        
    def _validate_vehicle_number(self, vehicle_number: str) -> bool:
        """Validate vehicle number format."""
        
        
        pattern = r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}$'
        return bool(re.match(pattern, vehicle_number.upper()))
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        
        pattern = r'^\+91[0-9]{10}$'
        return bool(re.match(pattern, phone))
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        
        return email.lower().endswith('@campus.edu')

    def display_resident(self, resident: Dict[str, Any]) -> None:
        """Display a single resident's information."""
        print(f"Vehicle Number: {resident['VehicleNumber']}")
        print(f"Owner Name: {resident['OwnerName']}")
        print(f"Phone: {resident['OwnerPhone']}")
        print(f"Campus ID: {resident['OwnerCampusID']}")
        print(f"Email: {resident['OwnerEmail']}")
        print("-" * 40)

def main():
    manager = ResidentManager('resident.json')
    
    while True:
        print("\nCampus Resident Vehicle Registration Management")
        print("1. Add a new resident")
        print("2. Delete a resident")
        print("3. Update resident information")
        print("4. Find resident by vehicle number")
        print("5. Find residents by name")
        print("6. Find residents by campus ID")
        print("7. Display all residents")
        print("0. Save and exit")
        
        choice = input("Enter your choice (0-7): ")
        
        if choice == '0':
            manager.save_residents()
            print("Exiting program...")
            break
            
        elif choice == '1':
            vehicle_number = input("Enter vehicle number: ")
            name = input("Enter owner name: ")
            phone = input("Enter phone number (format: +91XXXXXXXXXX): ")
            campus_id = input("Enter campus ID: ")
            email = input("Enter email: ")
            
            if manager.add_resident(vehicle_number, name, phone, campus_id, email):
                manager.save_residents()
                
        elif choice == '2':
            vehicle_number = input("Enter vehicle number to delete: ")
            if manager.delete_resident(vehicle_number):
                manager.save_residents()
                
        elif choice == '3':
            vehicle_number = input("Enter vehicle number to update: ")
            resident = manager.find_resident_by_vehicle(vehicle_number)
            
            if resident:
                print("Current information:")
                manager.display_resident(resident)
                print("Enter new information (leave blank to keep current value):")
                
                name = input(f"Name [{resident['OwnerName']}]: ")
                phone = input(f"Phone [{resident['OwnerPhone']}]: ")
                campus_id = input(f"Campus ID [{resident['OwnerCampusID']}]: ")
                email = input(f"Email [{resident['OwnerEmail']}]: ")
                
                updates = {}
                if name: updates["OwnerName"] = name
                if phone: updates["OwnerPhone"] = phone
                if campus_id: updates["OwnerCampusID"] = campus_id
                if email: updates["OwnerEmail"] = email
                
                if updates and manager.update_resident(vehicle_number, **updates):
                    manager.save_residents()
            
        elif choice == '4':
            vehicle_number = input("Enter vehicle number to search: ")
            resident = manager.find_resident_by_vehicle(vehicle_number)
            
            if resident:
                print("\nFound resident:")
                manager.display_resident(resident)
            else:
                print(f"No resident found with vehicle number {vehicle_number}")
                
        elif choice == '5':
            name = input("Enter name to search: ")
            residents = manager.find_residents_by_name(name)
            
            if residents:
                print(f"\nFound {len(residents)} residents:")
                for resident in residents:
                    manager.display_resident(resident)
            else:
                print(f"No residents found with name containing '{name}'")
                
        elif choice == '6':
            campus_id = input("Enter campus ID to search: ")
            residents = manager.find_residents_by_campus_id(campus_id)
            
            if residents:
                print(f"\nFound {len(residents)} residents:")
                for resident in residents:
                    manager.display_resident(resident)
            else:
                print(f"No residents found with campus ID {campus_id}")
                
        elif choice == '7':
            residents = manager.get_all_residents()
            print(f"\nDisplaying all {len(residents)} residents:")
            for resident in residents:
                manager.display_resident(resident)
                
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
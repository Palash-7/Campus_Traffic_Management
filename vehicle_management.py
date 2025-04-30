import json
import os
from datetime import datetime
import random
import string
from typing import List, Dict, Optional
import time 
from collections import Counter, defaultdict

class Vehicle:
    def __init__(self, registration_number: str, model: str = None, is_campus_vehicle: bool = False, owner=None):
        self.registration_number = registration_number
        self.model = model
        self.is_campus_vehicle = is_campus_vehicle
        self.owner = owner

    def get_vehicle_details(self):
        return self

    def update_vehicle_details(self, registration_number: str, model: str):
        self.registration_number = registration_number
        self.model = model


class User:
    def __init__(self, user_id: str, name: str, email: str, phone_number: str, user_type: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.user_type = user_type

    def login(self, username: str, password: str) -> bool:
        
        return True

    def logout(self):
        
        pass

    def update_profile(self, email: str, phone: str):
        self.email = email
        self.phone_number = phone

    def get_user_info(self) -> str:
        return f"{self.name} ({self.user_id}) - {self.user_type}"


class CampusResident(User):
    def __init__(self, resident_id: str, name: str, email: str, phone_number: str):
        super().__init__(resident_id, name, email, phone_number, "Campus Resident")
        self.resident_id = resident_id
        self.vehicles: List[Vehicle] = []

    def register_vehicle(self, vehicle: Vehicle):
        vehicle.is_campus_vehicle = True
        vehicle.owner = self
        self.vehicles.append(vehicle)

    def view_vehicle_list(self) -> List[Vehicle]:
        return self.vehicles


class ExternalVisitor(User):
    def __init__(self, visitor_id: str, name: str, email: str, phone_number: str, purpose_of_visit: str = None):
        super().__init__(visitor_id, name, email, phone_number, "External Visitor")
        self.visitor_id = visitor_id
        self.vehicle = None
        self.purpose_of_visit = purpose_of_visit

    def register_entry(self, vehicle: Vehicle, purpose: str):
        self.vehicle = vehicle
        self.purpose_of_visit = purpose
        vehicle.owner = self
        print(f"External visitor {self.name} registered with vehicle {vehicle.registration_number}")

    def register_exit(self):
        print(f"External visitor {self.name} exited with vehicle {self.vehicle.registration_number}")


class SecurityPersonnel(User):
    def __init__(self, personnel_id: str, name: str, email: str, phone_number: str):
        super().__init__(personnel_id, name, email, phone_number, "Security Personnel")
        self.personnel_id = personnel_id

    def verify_vehicle(self, vehicle: Vehicle) -> bool:
        
        return vehicle.is_campus_vehicle

    def record_security_violation(self, vehicle: Vehicle, description: str):
        violation = ViolationRecord()
        violation.record_violation(vehicle, "Campus", description)
        return violation

    def query_vehicle_history(self, registration_number: str) -> List["VehicleEntryLog"]:
        
        return []


class VehicleEntryLog:
    def __init__(self):
        self.entry_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.entry_time = None
        self.exit_time = None
        self.vehicle = None
        self.driver = None

    def record_entry(self, vehicle: Vehicle, driver: User = None, entry_time: datetime = None):
        self.vehicle = vehicle
        self.driver = driver
        self.entry_time = entry_time or datetime.now()
        print(f"Vehicle {vehicle.registration_number} entered at {self.entry_time}")

    def record_exit(self, vehicle: Vehicle, exit_time: datetime = None):
        if self.vehicle and self.vehicle.registration_number == vehicle.registration_number:
            self.exit_time = exit_time or datetime.now()
            print(f"Vehicle {vehicle.registration_number} exited at {self.exit_time}")
            duration = self.calculate_duration()
            print(f"Vehicle was on campus for {duration} seconds")
            return True
        return False

    def calculate_duration(self):
        if self.entry_time and self.exit_time:
            return (self.exit_time - self.entry_time).total_seconds()
        return 0


class ViolationRecord:
    def __init__(self):
        self.violation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.time = None
        self.location = ""
        self.description = ""
        self.vehicle = None
        self.violation_type = ""

    def record_violation(self, vehicle: Vehicle, location: str, description: str, time: datetime = None):
        self.vehicle = vehicle
        self.location = location
        self.description = description
        self.time = time or datetime.now()
        
        
        if ': ' in description:
            self.violation_type = description.split(': ')[0]
        else:
            self.violation_type = "General Violation"
            
        print(f"Violation recorded for vehicle {vehicle.registration_number} at {self.location}: {self.description}")
        self.send_alert()

    def generate_violation_report(self, vehicle: Vehicle):
        
        report = Report(
            f"Violation Report - {vehicle.registration_number}",
            f"Violation at {self.location}: {self.description}",
            "System"
        )
        return report

    def send_alert(self):
        print(f"🚨 ALERT: Security personnel notified about violation by vehicle {self.vehicle.registration_number}")


class Report:
    def __init__(self, title: str, content: str, generated_by: str):
        self.report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.title = title
        self.content = content
        self.generated_on = datetime.now()
        self.generated_by = generated_by

    def generate(self):
        print(f"Generating report: {self.title}")

    def export(self, format: str):
        print(f"Exporting report {self.title} in {format} format")
        
        return None

    def view_report(self) -> str:
        return f"Report: {self.title}\nContent: {self.content}\nGenerated on: {self.generated_on}\nBy: {self.generated_by}"
    
    def export_to_file(self, filepath: str) -> bool:
        try:
            with open(filepath, 'a') as file:
                file.write(f"{'='*80}\n")
                file.write(f"REPORT ID: {self.report_id}\n")
                file.write(f"TITLE: {self.title}\n")
                file.write(f"GENERATED ON: {self.generated_on.strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"GENERATED BY: {self.generated_by}\n")
                file.write(f"\n{self.content}\n\n")
            return True
        except Exception as e:
            print(f"Error exporting report to file: {str(e)}")
            return False


class Clock:
    def __init__(self):
        self.current_time = datetime.now()

    def get_current_time(self) -> datetime:
        return self.current_time

    def exceed_time(self, start_time: datetime, threshold_hours: int = 8) -> bool:
        difference = (self.current_time - start_time).total_seconds() / 3600  
        return difference > threshold_hours


class SystemAdmin(User):
    def __init__(self, admin_id: str, name: str, email: str, phone_number: str):
        super().__init__(admin_id, name, email, phone_number, "System Admin")
        self.admin_id = admin_id

    def generate_reports(self) -> List[Report]:
        
        reports = []
        
        reports.append(Report("Daily Traffic Summary", "Summary of campus traffic for today", self.name))
        return reports

    def manage_user_accounts(self):
        print(f"Admin {self.name} is managing user accounts")


class CampusTrafficSystem:
    def __init__(self):
        self.campus_residents = {}  
        self.external_visitors = {}  
        self.vehicles = {}  
        self.active_vehicles = {}  
        self.violation_records = []
        self.event_log = []  
        self.completed_entries = {}  
        self.load_campus_residents()
        
    def load_campus_residents(self):
        """Load campus residents from the JSON file"""
        try:
            with open('resident.json', 'r') as file:
                residents_data = json.load(file)
                
                
                if isinstance(residents_data, dict) and 'residents' in residents_data:
                    residents = residents_data['residents']
                else:
                    residents = residents_data
                
                for resident_info in residents:
                    
                    vehicle = Vehicle(
                        registration_number=resident_info['VehicleNumber'],
                        is_campus_vehicle=True
                    )
                    
                    
                    resident = CampusResident(
                        resident_id=resident_info['OwnerCampusID'],
                        name=resident_info['OwnerName'],
                        email=resident_info['OwnerEmail'],
                        phone_number=resident_info['OwnerPhone']
                    )
                    
                    
                    resident.register_vehicle(vehicle)
                    
                    
                    self.campus_residents[resident.resident_id] = resident
                    self.vehicles[vehicle.registration_number] = vehicle
                    
                print(f"Loaded {len(self.campus_residents)} campus residents from resident.json")
        except FileNotFoundError:
            print("Warning: resident.json file not found. No campus residents loaded.")
        except json.JSONDecodeError:
            print("Error: resident.json file is not valid JSON format.")
        except Exception as e:
            print(f"Error loading resident data: {str(e)}")

    def save_external_visitors(self):
        """Save external visitors to the JSON file"""
        visitors_data = []
        
        for visitor in self.external_visitors.values():
            if visitor.vehicle:
                visitor_info = {
                    "VehicleNumber": visitor.vehicle.registration_number,
                    "OwnerName": visitor.name,
                    "OwnerPhone": visitor.phone_number,
                    "OwnerCampusID": visitor.visitor_id,
                    "OwnerEmail": visitor.email,
                    "PurposeOfVisit": visitor.purpose_of_visit
                }
                visitors_data.append(visitor_info)
        
        try:
            with open('external.json', 'w') as file:
                json.dump(visitors_data, file, indent=2)
            print(f"Saved {len(visitors_data)} external visitors to external.json")
        except Exception as e:
            print(f"Error saving external visitor data: {str(e)}")

    def process_vehicle_entry(self, vehicle_number: str, timestamp_str: str):
        """Process a vehicle entry event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "VEHICLE_ENTRY",
            "vehicle_number": vehicle_number,
            "timestamp": timestamp,
            "is_resident": vehicle_number in self.vehicles
        }
        self.event_log.append(event_data)
        
        
        if vehicle_number in self.vehicles:
            vehicle = self.vehicles[vehicle_number]
            print(f"Campus vehicle {vehicle_number} entry detected")
            
            
            entry_log = VehicleEntryLog()
            entry_log.record_entry(vehicle, vehicle.owner, timestamp)
            self.active_vehicles[vehicle_number] = entry_log
            
        else:
            
            print(f"External visitor vehicle {vehicle_number} entry detected")
            
            
            visitor_id = f"EV{random.randint(1000, 9999)}"
            visitor_name = f"Visitor-{visitor_id}"
            visitor_email = f"{visitor_name.lower()}@visitor.com"
            visitor_phone = f"+91{random.randint(7000000000, 9999999999)}"
            
            
            visitor = ExternalVisitor(
                visitor_id=visitor_id,
                name=visitor_name,
                email=visitor_email,
                phone_number=visitor_phone,
                purpose_of_visit="Campus Visit"
            )
            
            vehicle = Vehicle(
                registration_number=vehicle_number,
                is_campus_vehicle=False
            )
            
            visitor.register_entry(vehicle, "Campus Visit")
            
            
            self.external_visitors[visitor_id] = visitor
            self.vehicles[vehicle_number] = vehicle
            
            
            entry_log = VehicleEntryLog()
            entry_log.record_entry(vehicle, visitor, timestamp)
            self.active_vehicles[vehicle_number] = entry_log
            
            
            self.save_external_visitors()

    def process_vehicle_exit(self, vehicle_number: str, timestamp_str: str):
        """Process a vehicle exit event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "VEHICLE_EXIT",
            "vehicle_number": vehicle_number,
            "timestamp": timestamp
        }
        self.event_log.append(event_data)
        
        if vehicle_number in self.active_vehicles:
            entry_log = self.active_vehicles[vehicle_number]
            vehicle = self.vehicles.get(vehicle_number)
            
            if vehicle and entry_log.record_exit(vehicle, timestamp):
                print(f"Vehicle {vehicle_number} has exited the campus")
                
                
                self.completed_entries[vehicle_number] = entry_log
                
                
                del self.active_vehicles[vehicle_number]
            else:
                print(f"Error processing exit for vehicle {vehicle_number}")
        else:
            print(f"Warning: No entry record found for exiting vehicle {vehicle_number}")

    def process_traffic_violation(self, vehicle_number: str, violation_type: str, 
                                 location: str, timestamp_str: str, description: str):
        """Process a traffic violation event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "TRAFFIC_VIOLATION",
            "vehicle_number": vehicle_number,
            "violation_type": violation_type,
            "location": location,
            "timestamp": timestamp,
            "description": description
        }
        self.event_log.append(event_data)
        
        if vehicle_number in self.vehicles:
            vehicle = self.vehicles[vehicle_number]
            
            violation = ViolationRecord()
            full_description = f"{violation_type}: {description}"
            violation.record_violation(vehicle, location, full_description, timestamp)
            violation.violation_type = violation_type
            
            self.violation_records.append(violation)
        else:
            print(f"Warning: Vehicle {vehicle_number} not in system when processing violation")

    def process_parking_violation(self, vehicle_number: str, violation_type: str, 
                                 location: str, timestamp_str: str, description: str):
        """Process a parking violation event"""
        
        timestamp = datetime.fromisoformat(timestamp_str)
        event_data = {
            "event_type": "PARKING_VIOLATION",
            "vehicle_number": vehicle_number,
            "violation_type": violation_type,
            "location": location,
            "timestamp": timestamp,
            "description": description
        }
        self.event_log.append(event_data)
        
        
        self.process_traffic_violation(vehicle_number, violation_type, location, timestamp_str, description)

    def process_timeout(self, vehicle_number: str, timestamp_str: str, description: str):
        """Process a timeout event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "TIMEOUT",
            "vehicle_number": vehicle_number,
            "timestamp": timestamp,
            "description": description
        }
        self.event_log.append(event_data)
        
        if vehicle_number in self.active_vehicles and vehicle_number in self.vehicles:
            vehicle = self.vehicles[vehicle_number]
            entry_log = self.active_vehicles[vehicle_number]
            
            
            violation = ViolationRecord()
            violation.record_violation(vehicle, "Campus", description, timestamp)
            violation.violation_type = "TIMEOUT"
            self.violation_records.append(violation)
            
            print(f"⚠️ TIMEOUT: Vehicle {vehicle_number} has been on campus too long")
        else:
            print(f"Warning: Vehicle {vehicle_number} not in system when processing timeout")

    def process_unauthorized_access(self, vehicle_number: str, location: str, 
                                   timestamp_str: str, description: str):
        """Process an unauthorized access event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "UNAUTHORIZED_ACCESS",
            "vehicle_number": vehicle_number,
            "location": location,
            "timestamp": timestamp,
            "description": description
        }
        self.event_log.append(event_data)
        
        if vehicle_number in self.vehicles:
            vehicle = self.vehicles[vehicle_number]
            
            
            violation = ViolationRecord()
            violation.record_violation(vehicle, location, description, timestamp)
            violation.violation_type = "UNAUTHORIZED_ACCESS"
            self.violation_records.append(violation)
            
            print(f"🚫 UNAUTHORIZED ACCESS: Vehicle {vehicle_number} at {location}")
        else:
            print(f"Warning: Vehicle {vehicle_number} not in system when processing unauthorized access")

    def process_after_hours_entry(self, vehicle_number: str, timestamp_str: str, description: str):
        """Process an after hours entry event"""
        timestamp = datetime.fromisoformat(timestamp_str)
        
        
        event_data = {
            "event_type": "AFTER_HOURS_ENTRY",
            "vehicle_number": vehicle_number,
            "timestamp": timestamp,
            "description": description
        }
        self.event_log.append(event_data)
        
        if vehicle_number in self.vehicles:
            vehicle = self.vehicles[vehicle_number]
            
            
            violation = ViolationRecord()
            violation.record_violation(vehicle, "Campus Entry", description, timestamp)
            violation.violation_type = "AFTER_HOURS_ENTRY"
            self.violation_records.append(violation)
            
            print(f"🕒 AFTER HOURS: Vehicle {vehicle_number} entered campus after hours")
        else:
            print(f"Warning: Vehicle {vehicle_number} not in system when processing after hours entry")

    def process_event(self, event_line: str):
        """Process a single event from the event.txt file"""
        parts = event_line.strip().split(':')
        
        if len(parts) < 3:
            print(f"Invalid event format: {event_line}")
            return
            
        event_type = parts[0]
        
        if event_type == "VEHICLE_ENTRY":
            self.process_vehicle_entry(parts[1], parts[2])
            
        elif event_type == "VEHICLE_EXIT":
            self.process_vehicle_exit(parts[1], parts[2])
            
        elif event_type == "TRAFFIC_VIOLATION":
            if len(parts) >= 6:
                self.process_traffic_violation(parts[1], parts[2], parts[3], parts[4], parts[5])
            else:
                print(f"Invalid traffic violation format: {event_line}")
                
        elif event_type == "PARKING_VIOLATION":
            if len(parts) >= 6:
                self.process_parking_violation(parts[1], parts[2], parts[3], parts[4], parts[5])
            else:
                print(f"Invalid parking violation format: {event_line}")
                
        elif event_type == "TIMEOUT":
            if len(parts) >= 4:
                self.process_timeout(parts[1], parts[2], parts[3])
            else:
                print(f"Invalid timeout format: {event_line}")
                
        elif event_type == "UNAUTHORIZED_ACCESS":
            if len(parts) >= 5:
                self.process_unauthorized_access(parts[1], parts[2], parts[3], parts[4])
            else:
                print(f"Invalid unauthorized access format: {event_line}")
                
        elif event_type == "AFTER_HOURS_ENTRY":
            if len(parts) >= 4:
                self.process_after_hours_entry(parts[1], parts[2], parts[3])
            else:
                print(f"Invalid after hours entry format: {event_line}")
        
        else:
            print(f"Unknown event type: {event_type}")

    def process_events_file(self, filename="event.txt"):
        """Process all events from the event.txt file"""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        self.process_event(line)
                        time.sleep(1)
                        
            
            self.save_external_visitors()
            
            
            print("\n--- TRAFFIC SYSTEM SUMMARY ---")
            print(f"Processed {len(self.vehicles)} unique vehicles")
            print(f"  - {len(self.campus_residents)} campus residents")
            print(f"  - {len(self.external_visitors)} external visitors")
            print(f"Recorded {len(self.violation_records)} violations")
            print(f"{len(self.active_vehicles)} vehicles still on campus")
            
        except FileNotFoundError:
            print(f"Error: {filename} not found")
        except Exception as e:
            print(f"Error processing events file: {str(e)}")

    def generate_event_report(self, filename="report.txt"):
        """Generate a comprehensive report based on processed events and terminal outputs"""
        
        try:
            with open(filename, 'w') as file:
                file.write("CAMPUS VEHICLE TRAFFIC MANAGEMENT SYSTEM REPORT\n")
                file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"{'='*80}\n\n")
        except Exception as e:
            print(f"Error initializing report file: {str(e)}")
            return
        
        
        analytics_report = Report(
            title="Traffic Analytics Report",
            content=self._generate_analytics_content(),
            generated_by="System"
        )
        analytics_report.export_to_file(filename)
        
        
        violation_stats_report = Report(
            title="Violation Statistics Report",
            content=self._generate_violation_statistics(),
            generated_by="System"
        )
        violation_stats_report.export_to_file(filename)
        
        
        time_analysis_report = Report(
            title="Vehicle Time Analysis Report",
            content=self._generate_time_analysis(),
            generated_by="System"
        )
        time_analysis_report.export_to_file(filename)
        
        
        user_analysis_report = Report(
            title="Resident vs Visitor Analysis",
            content=self._generate_user_analysis(),
            generated_by="System"
        )
        user_analysis_report.export_to_file(filename)
        
        
        event_frequency_report = Report(
            title="Event Frequency Analysis",
            content=self._generate_event_frequency_analysis(),
            generated_by="System"
        )
        event_frequency_report.export_to_file(filename)
        
        print(f"Analytical report generated: {filename}")

    def _generate_analytics_content(self):
        """Generate analytics content based on the processed events"""
        content = "TRAFFIC SYSTEM ANALYTICS\n"
        content += "-" * 50 + "\n"
        
        
        total_vehicles = len(self.vehicles)
        content += f"Total vehicles processed: {total_vehicles}\n"
        
        
        event_counts = Counter(event["event_type"] for event in self.event_log)
        content += "\nEvent Distribution:\n"
        for event_type, count in event_counts.items():
            percentage = (count / len(self.event_log)) * 100
            content += f"  - {event_type}: {count} ({percentage:.1f}%)\n"
        
        
        vehicles_with_violations = set(v.vehicle.registration_number for v in self.violation_records if v.vehicle)
        violation_percentage = (len(vehicles_with_violations) / total_vehicles) * 100 if total_vehicles else 0
        content += f"\nVehicles with violations: {len(vehicles_with_violations)} ({violation_percentage:.1f}%)\n"
        
        
        resident_violations = 0
        visitor_violations = 0
        
        for violation in self.violation_records:
            if violation.vehicle and violation.vehicle.is_campus_vehicle:
                resident_violations += 1
            else:
                visitor_violations += 1
                
        content += f"\nViolations by Campus Residents: {resident_violations}\n"
        content += f"Violations by External Visitors: {visitor_violations}\n"
        
        if self.violation_records:
            resident_percentage = (resident_violations / len(self.violation_records)) * 100
            visitor_percentage = (visitor_violations / len(self.violation_records)) * 100
            content += f"  - Campus Resident Violation Rate: {resident_percentage:.1f}%\n"
            content += f"  - External Visitor Violation Rate: {visitor_percentage:.1f}%\n"
        
        return content

    def _generate_violation_statistics(self):
        """Generate statistics about violations"""
        if not self.violation_records:
            return "VIOLATION STATISTICS\n" + "-" * 50 + "\nNo violations recorded during this period."
        
        content = "VIOLATION STATISTICS\n"
        content += "-" * 50 + "\n"
        
        
        violation_types = Counter()
        for violation in self.violation_records:
            violation_types[violation.violation_type] += 1
        
        content += "Violations by Type:\n"
        for violation_type, count in violation_types.most_common():
            percentage = (count / len(self.violation_records)) * 100
            content += f"  - {violation_type}: {count} ({percentage:.1f}%)\n"
        
        
        violation_locations = Counter(v.location for v in self.violation_records)
        
        content += "\nViolations by Location:\n"
        for location, count in violation_locations.most_common():
            percentage = (count / len(self.violation_records)) * 100
            content += f"  - {location}: {count} ({percentage:.1f}%)\n"
        
        
        offender_counts = Counter()
        for violation in self.violation_records:
            if violation.vehicle:
                offender_counts[violation.vehicle.registration_number] += 1
        
        if offender_counts:
            content += "\nRepeat Offenders (2+ violations):\n"
            repeat_offenders = [(reg_num, count) for reg_num, count in offender_counts.items() if count >= 2]
            
            if repeat_offenders:
                for reg_num, count in sorted(repeat_offenders, key=lambda x: x[1], reverse=True):
                    vehicle = self.vehicles.get(reg_num)
                    owner_name = vehicle.owner.name if vehicle and vehicle.owner else "Unknown"
                    content += f"  - {reg_num} (Owner: {owner_name}): {count} violations\n"
            else:
                content += "  No repeat offenders identified\n"
        
        return content

    def _generate_time_analysis(self):
        """Generate analysis about time spent on campus"""
        content = "VEHICLE TIME ANALYSIS\n"
        content += "-" * 50 + "\n"
        
        
        durations = []
        for reg_num, entry_log in self.completed_entries.items():
            if entry_log.entry_time and entry_log.exit_time:
                duration = entry_log.calculate_duration()
                durations.append((reg_num, duration))
        
        if durations:
            avg_duration = sum(d[1] for d in durations) / len(durations)
            max_duration = max(durations, key=lambda x: x[1])
            min_duration = min(durations, key=lambda x: x[1])
            
            content += f"Average time spent on campus: {avg_duration/60:.1f} minutes\n"
            
            
            max_vehicle = self.vehicles.get(max_duration[0])
            max_owner = max_vehicle.owner.name if max_vehicle and max_vehicle.owner else "Unknown"
            content += f"Longest stay: {max_duration[0]} (Owner: {max_owner}) - {max_duration[1]/60:.1f} minutes\n"
            
            
            min_vehicle = self.vehicles.get(min_duration[0])
            min_owner = min_vehicle.owner.name if min_vehicle and min_vehicle.owner else "Unknown"
            content += f"Shortest stay: {min_duration[0]} (Owner: {min_owner}) - {min_duration[1]/60:.1f} minutes\n"
            
            
            short_visits = len([d for d in durations if d[1] < 30*60])  
            medium_visits = len([d for d in durations if 30*60 <= d[1] < 120*60])  
            long_visits = len([d for d in durations if d[1] >= 120*60])  
            
            content += "\nVisit Duration Distribution:\n"
            content += f"  - Short visits (<30 min): {short_visits} ({short_visits/len(durations)*100:.1f}%)\n"
            content += f"  - Medium visits (30min-2hr): {medium_visits} ({medium_visits/len(durations)*100:.1f}%)\n"
            content += f"  - Long visits (>2hr): {long_visits} ({long_visits/len(durations)*100:.1f}%)\n"
        else:
            content += "No complete entry/exit records available for time analysis.\n"
        
        
        if self.active_vehicles:
            content += f"\nVehicles Still on Campus: {len(self.active_vehicles)}\n"
            for reg_num, entry_log in self.active_vehicles.items():
                vehicle = self.vehicles.get(reg_num)
                owner = vehicle.owner.name if vehicle and vehicle.owner else "Unknown"
                entry_time = entry_log.entry_time.strftime('%H:%M:%S') if entry_log.entry_time else "Unknown"
                content += f"  - {reg_num} (Owner: {owner}): Entered at {entry_time}\n"
        
        return content

    def _generate_user_analysis(self):
        """Generate analysis comparing campus residents vs external visitors"""
        content = "RESIDENT VS VISITOR ANALYSIS\n"
        content += "-" * 50 + "\n"
        
        
        resident_count = len(self.campus_residents)
        visitor_count = len(self.external_visitors)
        total_users = resident_count + visitor_count
        
        if total_users == 0:
            content += "No users registered in the system.\n"
            return content
        
        
        resident_percentage = (resident_count / total_users) * 100 if total_users else 0
        visitor_percentage = (visitor_count / total_users) * 100 if total_users else 0
        
        content += f"Total Users: {total_users}\n"
        content += f"  - Campus Residents: {resident_count} ({resident_percentage:.1f}%)\n"
        content += f"  - External Visitors: {visitor_count} ({visitor_percentage:.1f}%)\n"
        
        
        resident_events = 0
        visitor_events = 0
        
        for event in self.event_log:
            vehicle_num = event.get("vehicle_number")
            if vehicle_num:
                vehicle = self.vehicles.get(vehicle_num)
                if vehicle and vehicle.is_campus_vehicle:
                    resident_events += 1
                else:
                    visitor_events += 1
        
        total_events = resident_events + visitor_events
        if total_events:
            content += f"\nEvents by User Type:\n"
            content += f"  - Campus Resident Events: {resident_events} ({resident_events/total_events*100:.1f}%)\n"
            content += f"  - External Visitor Events: {visitor_events} ({visitor_events/total_events*100:.1f}%)\n"
        
        
        resident_violations = sum(1 for v in self.violation_records if v.vehicle and v.vehicle.is_campus_vehicle)
        visitor_violations = sum(1 for v in self.violation_records if v.vehicle and not v.vehicle.is_campus_vehicle)
        
        
        if resident_count:
            resident_violation_rate = resident_violations / resident_count
            content += f"\nViolation Rate per Resident: {resident_violation_rate:.2f}\n"
        
        if visitor_count:
            visitor_violation_rate = visitor_violations / visitor_count
            content += f"Violation Rate per Visitor: {visitor_violation_rate:.2f}\n"
        
        
        resident_entries = [datetime.fromisoformat(e["timestamp"].isoformat()) 
                          for e in self.event_log 
                          if e["event_type"] == "VEHICLE_ENTRY" and e.get("is_resident", False)]
        
        visitor_entries = [datetime.fromisoformat(e["timestamp"].isoformat()) 
                         for e in self.event_log 
                         if e["event_type"] == "VEHICLE_ENTRY" and not e.get("is_resident", False)]
        
        if resident_entries:
            avg_resident_hour = sum(e.hour for e in resident_entries) / len(resident_entries)
            content += f"\nAverage Campus Resident arrival time: {int(avg_resident_hour):02d}:{int((avg_resident_hour % 1) * 60):02d}\n"
        
        if visitor_entries:
            avg_visitor_hour = sum(e.hour for e in visitor_entries) / len(visitor_entries)
            content += f"Average External Visitor arrival time: {int(avg_visitor_hour):02d}:{int((avg_visitor_hour % 1) * 60):02d}\n"
        
        return content

    def _generate_event_frequency_analysis(self):
        """Generate analysis about event frequency over time"""
        content = "EVENT FREQUENCY ANALYSIS\n"
        content += "-" * 50 + "\n"
        
        if not self.event_log:
            content += "No events recorded for frequency analysis.\n"
            return content
        
        
        events_by_hour = defaultdict(int)
        for event in self.event_log:
            if "timestamp" in event:
                hour = event["timestamp"].hour
                events_by_hour[hour] += 1
        
        content += "Event Frequency by Hour of Day:\n"
        for hour in sorted(events_by_hour.keys()):
            count = events_by_hour[hour]
            percentage = (count / len(self.event_log)) * 100
            hour_str = f"{hour:02d}:00 - {(hour+1) % 24:02d}:00"
            content += f"  - {hour_str}: {count} events ({percentage:.1f}%)\n"
        
        
        if events_by_hour:
            peak_hour = max(events_by_hour.items(), key=lambda x: x[1])
            content += f"\nPeak Hour: {peak_hour[0]:02d}:00 - {(peak_hour[0]+1) % 24:02d}:00 with {peak_hour[1]} events\n"
        
        
        event_types = Counter(event["event_type"] for event in self.event_log)
        
        content += "\nEvent Type Distribution:\n"
        for event_type, count in event_types.most_common():
            percentage = (count / len(self.event_log)) * 100
            content += f"  - {event_type}: {count} ({percentage:.1f}%)\n"
        
        
        entries = event_types.get("VEHICLE_ENTRY", 0)
        violations = sum(event_types.get(e, 0) for e in 
                      ["TRAFFIC_VIOLATION", "PARKING_VIOLATION", "TIMEOUT", 
                       "UNAUTHORIZED_ACCESS", "AFTER_HOURS_ENTRY"])
        
        if entries:
            violation_ratio = violations / entries
            content += f"\nViolation to Entry Ratio: {violation_ratio:.2f}\n"
            content += f"  (On average, each vehicle entry results in {violation_ratio:.2f} violations)\n"
        
        return content
    def export_entry_exit_log(self, filename="entry_exit_log.txt"):
        try:
            with open(filename, 'w') as file:
                file.write("ENTRY-EXIT LOG\n")
                file.write("=" * 80 + "\n\n")
                for reg_num, log in self.completed_entries.items():
                    entry_time = log.entry_time.strftime('%Y-%m-%d %H:%M:%S') if log.entry_time else "N/A"
                    exit_time = log.exit_time.strftime('%Y-%m-%d %H:%M:%S') if log.exit_time else "N/A"
                    duration = log.calculate_duration() / 60  
                    owner = log.driver.name if log.driver else "Unknown"
                    file.write(f"Vehicle: {reg_num}\n")
                    file.write(f"  Owner: {owner}\n")
                    file.write(f"  Entry Time: {entry_time}\n")
                    file.write(f"  Exit Time: {exit_time}\n")
                    file.write(f"  Duration on Campus: {duration:.1f} minutes\n")
                    file.write("-" * 80 + "\n")
            print(f"Entry-exit log saved to {filename}")
        except Exception as e:
            print(f"Error exporting entry-exit log: {e}")

    def export_violation_log(self, filename="violation_log.txt"):
        try:
            with open(filename, 'w') as file:
                file.write("VIOLATION LOG\n")
                file.write("=" * 80 + "\n\n")
                for v in self.violation_records:
                    time = v.time.strftime('%Y-%m-%d %H:%M:%S') if v.time else "N/A"
                    reg_num = v.vehicle.registration_number if v.vehicle else "Unknown"
                    file.write(f"Vehicle: {reg_num}\n")
                    file.write(f"  Time: {time}\n")
                    file.write(f"  Location: {v.location}\n")
                    file.write(f"  Violation Type: {v.violation_type}\n")
                    file.write(f"  Description: {v.description}\n")
                    file.write("-" * 80 + "\n")
            print(f"Violation log saved to {filename}")
        except Exception as e:
            print(f"Error exporting violation log: {e}")

    
    
import unittest
from datetime import datetime
from vehicle_management import Vehicle, CampusResident, ExternalVisitor, ViolationRecord, VehicleEntryLog

class TestVehicleManagement(unittest.TestCase):

    def test_vehicle_creation(self):
        vehicle = Vehicle("ABC123", "Sedan", True)
        self.assertEqual(vehicle.registration_number, "ABC123")
        self.assertEqual(vehicle.model, "Sedan")
        self.assertTrue(vehicle.is_campus_vehicle)

    def test_register_vehicle(self):
        resident = CampusResident("R001", "John Doe", "john@example.com", "1234567890")
        vehicle = Vehicle("XYZ789", "SUV")
        resident.register_vehicle(vehicle)
        self.assertIn(vehicle, resident.vehicles)
        self.assertTrue(vehicle.is_campus_vehicle)
        self.assertEqual(vehicle.owner, resident)

    def test_violation_record(self):
        vehicle = Vehicle("DEF456", "Truck")
        violation = ViolationRecord()
        violation.record_violation(vehicle, "Main Gate", "Speeding")
        self.assertEqual(violation.vehicle, vehicle)
        self.assertEqual(violation.location, "Main Gate")
        self.assertEqual(violation.description, "Speeding")
        self.assertIsNotNone(violation.time)

    def test_vehicle_entry_log(self):
        vehicle = Vehicle("LMN123", "Bike")
        entry_log = VehicleEntryLog()
        entry_time = datetime(2025, 4, 24, 10, 0, 0)
        entry_log.record_entry(vehicle, entry_time=entry_time)
        self.assertEqual(entry_log.vehicle, vehicle)
        self.assertEqual(entry_log.entry_time, entry_time)

    def test_vehicle_exit_log(self):
        vehicle = Vehicle("LMN123", "Bike")
        entry_log = VehicleEntryLog()
        entry_time = datetime(2025, 4, 24, 10, 0, 0)
        exit_time = datetime(2025, 4, 24, 12, 0, 0)
        entry_log.record_entry(vehicle, entry_time=entry_time)
        result = entry_log.record_exit(vehicle, exit_time=exit_time)
        self.assertTrue(result)
        self.assertEqual(entry_log.exit_time, exit_time)
        self.assertEqual(entry_log.calculate_duration(), 7200)  # 2 hours in seconds

if __name__ == "__main__":
    unittest.main()
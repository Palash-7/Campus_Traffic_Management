import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
from vehicle_management import CampusTrafficSystem

# test_vehicle_management.py


class TestCampusTrafficSystem(unittest.TestCase):
    def setUp(self):
        self.system = CampusTrafficSystem()

    @patch("builtins.open", new_callable=mock_open, read_data="""\
VEHICLE_ENTRY:TN23RY9945:2025-04-23T08:15:30
VEHICLE_EXIT:TN23RY9945:2025-04-23T14:20:15
TRAFFIC_VIOLATION:TN23RY9945:SPEEDING:CAMPUS_MAIN_ROAD:2025-04-23T09:10:25:Exceeded speed limit by 20km/h
PARKING_VIOLATION:UP17WF7925:NO_PARKING_ZONE:ADMIN_BLOCK:2025-04-23T10:15:40:Parked in restricted area
TIMEOUT:KA15HJ8490:2025-04-23T16:15:30:Vehicle present on campus for more than 8 hours
UNAUTHORIZED_ACCESS:XY12AB3456:RESTRICTED_AREA:2025-04-23T13:10:45:Attempted access to faculty parking
AFTER_HOURS_ENTRY:MH26DO8952:2025-04-23T19:00:15:Entry outside permitted hours
""")
    def test_process_events_file(self, mock_file):
        self.system.process_events_file("event.txt")

        # Check event log
        self.assertEqual(len(self.system.event_log), 7)

        # Check vehicle entry
        entry_event = self.system.event_log[0]
        self.assertEqual(entry_event["event_type"], "VEHICLE_ENTRY")
        self.assertEqual(entry_event["vehicle_number"], "TN23RY9945")
        self.assertEqual(entry_event["timestamp"], datetime.fromisoformat("2025-04-23T08:15:30"))

        # Check vehicle exit
        exit_event = self.system.event_log[1]
        self.assertEqual(exit_event["event_type"], "VEHICLE_EXIT")
        self.assertEqual(exit_event["vehicle_number"], "TN23RY9945")
        self.assertEqual(exit_event["timestamp"], datetime.fromisoformat("2025-04-23T14:20:15"))

        # Check traffic violation
        violation_event = self.system.event_log[2]
        self.assertEqual(violation_event["event_type"], "TRAFFIC_VIOLATION")
        self.assertEqual(violation_event["vehicle_number"], "TN23RY9945")
        self.assertEqual(violation_event["violation_type"], "SPEEDING")
        self.assertEqual(violation_event["location"], "CAMPUS_MAIN_ROAD")
        self.assertEqual(violation_event["description"], "Exceeded speed limit by 20km/h")

        # Check parking violation
        parking_event = self.system.event_log[3]
        self.assertEqual(parking_event["event_type"], "PARKING_VIOLATION")
        self.assertEqual(parking_event["vehicle_number"], "UP17WF7925")
        self.assertEqual(parking_event["violation_type"], "NO_PARKING_ZONE")
        self.assertEqual(parking_event["location"], "ADMIN_BLOCK")
        self.assertEqual(parking_event["description"], "Parked in restricted area")

        # Check timeout
        timeout_event = self.system.event_log[4]
        self.assertEqual(timeout_event["event_type"], "TIMEOUT")
        self.assertEqual(timeout_event["vehicle_number"], "KA15HJ8490")
        self.assertEqual(timeout_event["description"], "Vehicle present on campus for more than 8 hours")

        # Check unauthorized access
        unauthorized_event = self.system.event_log[5]
        self.assertEqual(unauthorized_event["event_type"], "UNAUTHORIZED_ACCESS")
        self.assertEqual(unauthorized_event["vehicle_number"], "XY12AB3456")
        self.assertEqual(unauthorized_event["location"], "RESTRICTED_AREA")
        self.assertEqual(unauthorized_event["description"], "Attempted access to faculty parking")

        # Check after-hours entry
        after_hours_event = self.system.event_log[6]
        self.assertEqual(after_hours_event["event_type"], "AFTER_HOURS_ENTRY")
        self.assertEqual(after_hours_event["vehicle_number"], "MH26DO8952")
        self.assertEqual(after_hours_event["description"], "Entry outside permitted hours")

if __name__ == "__main__":
    unittest.main()
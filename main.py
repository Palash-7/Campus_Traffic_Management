from vehicle_management import CampusTrafficSystem
import os

def main():
    print("Starting Campus Vehicle Traffic Management System...")
    print("="*60)
    
    
    system = CampusTrafficSystem()
    
    
    system.process_events_file()
    
    
    system.generate_event_report()
    system.export_entry_exit_log()
    system.export_violation_log()

    
    print("="*60)
    print("System processing complete")
    print("Report generated: report.txt")
    print("Current Working Directory:", os.getcwd())
if __name__ == "__main__":
    main()
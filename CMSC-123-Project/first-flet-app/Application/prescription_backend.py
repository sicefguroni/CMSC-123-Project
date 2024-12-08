import json
from datetime import datetime
from typing import List, Dict, Optional

class PrescriptionManager:
    def __init__(self, storage_file: str = 'prescriptions.json'):
        """
        Initialize the Prescription Manager with optional storage file

        Args:
            storage_file (str): Path to JSON file for storing prescriptions
        """
        self.storage_file = storage_file
        self.prescriptions: List[Dict] = self.load_prescriptions()

    def load_prescriptions(self) -> List[Dict]:
        """
        Load prescriptions from JSON file

        returns:
            List of prescription dictionaries
        """
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)

            # Ensure each prescription has an ID
            for index, prescription in enumerate(prescriptions, 1):
                if 'id' not in prescription:
                    prescription['id'] = index
            
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_prescription(self):
        """
        Save prescriptions to JSON file
        """
        with open(self.storage_file, 'w') as f:
            json.dump(self.prescriptions, f, indent=4)

    def add_prescription(self, prescription: Dict) -> bool:
        """
        Add a new prescription

        Args:
            prescription (Dict): Prescription details

        Returns:
            bool: True if successfully added, False otherwise
        """        

        required_fields = [
            'medication', 'dosage', 'frequency', 'doctor', 'appointment_date',
            'appointment_time', 'start_date', 'end_date'
        ]

        for field in required_fields:
            if not prescription.get(field):
                print(f"Missing required field: {field}")
                return False
                
        # Generate unique ID
        prescription['id'] = (max([p.get('id', 0) for p in self.prescriptions]) + 1) if self.prescriptions else 1

        # Add timestamp
        prescription['created_at'] = datetime.now().isoformat()

        # Add to prescription list
        self.prescriptions.append(prescription)

        # Save to file
        self.save_prescription()

        return True
    
    def get_all_prescriptions(self) -> List[Dict]:
        """
        Retrieve all prescriptions

        Returns:
            List of prescription dictionaries
        """
        return self.prescriptions
    
    def get_prescription_by_id(self, prescription_id: int) -> Optional[Dict]:
        """
        Retrieve a specific prescription by ID

        Args:
            prescription_id (int): Unique identifier for prescription

        Returns:
            Prescription dictionary or None if not found    
        """
        for prescription in self.prescriptions:
            if prescription['id'] == prescription_id:
                return prescription
            
        return None
    
    def update_prescription(self, prescription_id: int, updated_data: Dict) -> bool:
        """
        Update an existing prescription

        Args:
            prescription_id (int): ID of prescriptions to update
            update_data (Dict): New prescription details

        Returns:
            bool: True if successfully updated, False otherwise
        """
        for index, prescription in enumerate(self.prescriptions):
            if prescription['id'] == prescription_id:
                # Update only provided fields
                self.prescriptions[index].update(updated_data)
                self.prescriptions[index]['updated at'] = datetime.now().isoformat()
                self.save_prescription()
                return True
        return False
    
    def delete_prescription(self, prescription_id: int) -> bool:
        """
        Delete a prescription

        Args:
            prescription_id (int): ID of prescription to delete

        Returns:
            bool: True if successfully deleted, False otherwise 
        """
        for prescription in self.prescriptions:
            if prescription['id'] == prescription_id:
                self.prescriptions.remove(prescription)
                self.save_prescription()
                return True
        return False
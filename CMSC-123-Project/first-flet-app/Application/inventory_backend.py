import json
import os

class MedicationInventory:
    def __init__(self, tablet_file='tablet_inventory.json', fluid_file='fluid_inventory.json'):
        """
        Initialize the medication inventory with file paths for persistence
        
        Args:
            tablet_file (str): Path to save tablet medication inventory
            fluid_file (str): Path to save fluid medication inventory
        """
        self.tablet_file = tablet_file
        self.fluid_file = fluid_file
        
        # Ensure data directory exists
        os.makedirs('inventory_data', exist_ok=True)
        
        # Full paths with directory
        self.tablet_path = os.path.join('inventory_data', tablet_file)
        self.fluid_path = os.path.join('inventory_data', fluid_file)
        
        # Load existing inventories or initialize empty lists
        self.tablet_inventory = self.load_tablet_inventory()
        self.fluid_inventory = self.load_fluid_inventory()

    def load_tablet_inventory(self):
        """
        Load tablet medication inventory from JSON file
        
        Returns:
            list: List of tablet medications
        """
        try:
            with open(self.tablet_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_fluid_inventory(self):
        """
        Load fluid medication inventory from JSON file
        
        Returns:
            list: List of fluid medications
        """
        try:
            with open(self.fluid_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tablet_inventory(self):
        """
        Save tablet medication inventory to JSON file
        """
        with open(self.tablet_path, 'w') as f:
            json.dump(self.tablet_inventory, f, indent=4)

    def save_fluid_inventory(self):
        """
        Save fluid medication inventory to JSON file
        """
        with open(self.fluid_path, 'w') as f:
            json.dump(self.fluid_inventory, f, indent=4)

    def add_tablet_medication(self, name, dosage, stock):
        """
        Add a new tablet medication to the inventory
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mg
            stock (int): Number of tablets in stock
        """
        # Check for existing medication to prevent duplicates
        for med in self.tablet_inventory:
            if med['name'] == name and med['dosage'] == dosage:
                # If medication exists, update stock instead of adding duplicate
                med['stock'] += stock
                self.save_tablet_inventory()
                return

        # If no existing medication found, add new
        new_med = {
            "name": name,
            "dosage": dosage,
            "stock": stock
        }
        self.tablet_inventory.append(new_med)
        self.save_tablet_inventory()

    def add_fluid_medication(self, name, dosage, stock):
        """
        Add a new fluid medication to the inventory
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mL
            stock (int): Volume of fluid in stock
        """
        # Check for existing medication to prevent duplicates
        for med in self.fluid_inventory:
            if med['name'] == name and med['dosage'] == dosage:
                # If medication exists, update stock instead of adding duplicate
                med['stock'] += stock
                self.save_fluid_inventory()
                return

        # If no existing medication found, add new
        new_med = {
            "name": name,
            "dosage": dosage,
            "stock": stock
        }
        self.fluid_inventory.append(new_med)
        self.save_fluid_inventory()

    def update_tablet_stock(self, name, dosage, stock_change):
        """
        Update stock of a specific tablet medication
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mg
            stock_change (int): Amount to change stock by (positive or negative)
        
        Returns:
            bool: True if update successful, False otherwise
        """
        for med in self.tablet_inventory:
            if med['name'] == name and med['dosage'] == dosage:
                # Ensure stock doesn't go negative
                if med['stock'] + stock_change >= 0:
                    med['stock'] += stock_change
                    self.save_tablet_inventory()
                    return True
                return False
        return False

    def update_fluid_stock(self, name, dosage, stock_change):
        """
        Update stock of a specific fluid medication
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mL
            stock_change (int): Amount to change stock by (positive or negative)
        
        Returns:
            bool: True if update successful, False otherwise
        """
        for med in self.fluid_inventory:
            if med['name'] == name and med['dosage'] == dosage:
                # Ensure stock doesn't go negative
                if med['stock'] + stock_change >= 0:
                    med['stock'] += stock_change
                    self.save_fluid_inventory()
                    return True
                return False
        return False

    def remove_tablet_medication(self, name, dosage):
        """
        Remove a specific tablet medication from inventory
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mg
        
        Returns:
            bool: True if removal successful, False otherwise
        """
        for idx, med in enumerate(self.tablet_inventory):
            if med['name'] == name and med['dosage'] == dosage:
                del self.tablet_inventory[idx]
                self.save_tablet_inventory()
                return True
        return False

    def remove_fluid_medication(self, name, dosage):
        """
        Remove a specific fluid medication from inventory
        
        Args:
            name (str): Name of the medication
            dosage (int): Dosage in mL
        
        Returns:
            bool: True if removal successful, False otherwise
        """
        for idx, med in enumerate(self.fluid_inventory):
            if med['name'] == name and med['dosage'] == dosage:
                del self.fluid_inventory[idx]
                self.save_fluid_inventory()
                return True
        return False

    def get_tablet_inventory(self):
        """
        Get the current tablet medication inventory
        
        Returns:
            list: Current tablet medication inventory
        """
        return self.tablet_inventory

    def get_fluid_inventory(self):
        """
        Get the current fluid medication inventory
        
        Returns:
            list: Current fluid medication inventory
        """
        return self.fluid_inventory

# Example usage
if __name__ == "__main__":
    # Demonstrating backend functionality
    inventory = MedicationInventory()
    
    # Adding medications
    inventory.add_tablet_medication("Paracetamol", 500, 50)
    inventory.add_fluid_medication("Ibuprofen Syrup", 100, 200)
    
    # Printing current inventory
    print("Tablet Inventory:", inventory.get_tablet_inventory())
    print("Fluid Inventory:", inventory.get_fluid_inventory())
    
    # Updating stock
    inventory.update_tablet_stock("Paracetamol", 500, -10)
    inventory.update_fluid_stock("Ibuprofen Syrup", 100, -50)
    
    # Removing medication
    inventory.remove_tablet_medication("Paracetamol", 500)
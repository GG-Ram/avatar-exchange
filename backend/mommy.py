class Mommy:
    def __init__(self, name="Mommy"):
        self.name = name
        self.equipped = {
            "hat": None,
            "hair": None,
            "shirt": None,
            "pants": None,
            "shoes": None
        }
        self.owned_accessories = []  # List of accessories the user owns
    
    def equip_accessory(self, accessory, slot):
        """
        Equip an accessory to a specific slot
        
        Args:
            accessory: The Accessory object to equip
            slot: The slot name ("hat", "hair", "shirt", "pants", "shoes")
        
        Returns:
            bool: True if successful, False if failed
        """
        if slot not in self.equipped:
            print(f"Invalid slot: {slot}")
            return False
        
        if accessory not in self.owned_accessories:
            print(f"You don't own {accessory.name}!")
            return False
        
        # Unequip previous accessory in this slot
        if self.equipped[slot]:
            print(f"Unequipping {self.equipped[slot].name}")
        
        self.equipped[slot] = accessory
        print(f"Equipped {accessory.name} to {slot}")
        return True
    
    def unequip_slot(self, slot):
        """Remove accessory from a slot"""
        if slot not in self.equipped:
            print(f"Invalid slot: {slot}")
            return False
        
        if self.equipped[slot]:
            print(f"Unequipped {self.equipped[slot].name} from {slot}")
            self.equipped[slot] = None
            return True
        
        print(f"No accessory in {slot} slot")
        return False
    
    def add_owned_accessory(self, accessory):
        """Add an accessory to owned collection"""
        if accessory not in self.owned_accessories:
            self.owned_accessories.append(accessory)
            print(f"Added {accessory.name} to inventory")
            return True
        print(f"Already own {accessory.name}")
        return False
    
    def get_equipped_accessories(self):
        """Get all currently equipped accessories"""
        return {slot: acc for slot, acc in self.equipped.items() if acc is not None}
    
    def to_dict(self):
        return {
            'owned_accessories': [acc.to_dict() for acc in self.owned_accessories],
            'equipped': {
                slot: acc.to_dict() if acc else None 
                for slot, acc in self.equipped.items()
            }
        }
    
from . models import Lot, Movement
from django.core.exceptions import ValidationError

class InventoryService:
    @staticmethod
    def stock_out(item, quantity_needed, reference, notes=""):
        """
        Handles stock out movement following FIFO principle
        """


        # Get lots with available quantity, ordered by received_date (FIFO)
        available_lots = Lot.objects.filter(
            item=item,
            available_quantity__gt=0
        ).order_by('received_date')
        
        remaining_quantity = quantity_needed
        movements_created = []
        
        for lot in available_lots:
            if remaining_quantity <= 0:
                break
            
            available_in_lot = lot.available_quantity
            quantity_to_take = min(remaining_quantity, available_in_lot)
            
            if quantity_to_take > 0:
                movement = Movement.objects.create(
                    lot=lot,
                    movement_type='OUT',
                    quantity=quantity_to_take,
                    reference=reference,
                    notes=notes
                )
                movements_created.append(movement)
                remaining_quantity -= quantity_to_take
        
        if remaining_quantity > 0:
            raise ValidationError(f"Insufficient stock. Short by {remaining_quantity} units")
        
        return movements_created
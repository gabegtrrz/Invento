# Models
from . models import Lot, Movement

# Utils
import uuid
from datetime import date
from django.core.exceptions import ValidationError



class InventoryService:
    
    @staticmethod
    def generate_lot_number():
        """
        Generates a unique lot number (UUID1) back-trackable to
        - the exact time it was made; and
        - the mac address of the user
        """

        return str(uuid.uuid1())


    @staticmethod
    def stock_in(item, quantity, unit_cost, performed_by,
                 expiry_date=None, received_date=None, notes=''):
        '''
        handles stock in movement -- creating new lot and corresponding movement.
        '''

        if received_date is None:
            received_date = date.today()

        auto_lot_number = InventoryService.generate_lot_number()
        
        lot = Lot.objects.create(
            item = item,
            lot_number = auto_lot_number,
            initial_quantity = quantity,
            received_date = received_date,
            expiry_date = expiry_date,
            unit_cost = unit_cost,
        )

        movement = Movement.objects.create(
            movement_type = 'IN',
            lot = lot,
            quantity = quantity,
            purchase_price = unit_cost,
            performed_by = performed_by,
            notes = notes
            # date is set to auto_now_add in model
        )

        return lot, movement

    @staticmethod
    def stock_out(item, quantity_needed, performed_by, notes=""):
        '''
        handles stock out operation following FIFO principle.
        '''

        # Get lots with available quanitity
        # order themm by received_date (FIFO)
        available_lots = Lot.objects.filter(
            item = item,
            available_quanitity__gt=0
        ).order_by('received_date')

        # Remaining_quanity will be the remaining needed quantity which we will subtract every quantity we gather from the lots
        # The goal is to have 0 remaining
        # if Not zero -> error
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
                    notes=notes
                    # date is set to auto_now_add in model
                )
                movements_created.append(movement)
                remaining_quantity -= quantity_to_take
        
        if remaining_quantity > 0:
            raise ValidationError(f"Insufficient stock. Short by {remaining_quantity} units")
        
        return movements_created
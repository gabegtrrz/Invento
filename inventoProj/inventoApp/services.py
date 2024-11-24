# Models
from .models import Lot, Movement

# Utils
import uuid
from datetime import date
from django.core.exceptions import ValidationError
from django.db import transaction


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
    def stock_in(
        item,
        quantity,
        unit_cost,
        performed_by,
        expiry_date=None,
        received_date=None,
        notes="",
    ):
        """
        handles stock in movement -- creating new lot and corresponding movement.
        """

        if received_date is None:
            received_date = date.today()

        auto_lot_number = InventoryService.generate_lot_number()

        lot = Lot.objects.create(
            item=item,
            lot_number=auto_lot_number,
            initial_quantity=quantity,
            received_date=received_date,
            expiry_date=expiry_date,
            unit_cost=unit_cost,
        )

        movement = Movement.objects.create(
            movement_type="IN",
            lot=lot,
            quantity=quantity,
            purchase_price=unit_cost,
            performed_by=performed_by,
            notes=notes,
            # date is set to auto_now_add in model
        )

        return lot, movement

    def stock_out(item, quantity, performed_by, notes=""):
        """
        Handles stock out operation following FIFO principle.
        """

        # Get lots with available quantity
        available_lots = []
        for lot in Lot.objects.filter(item=item).order_by("received_date"):
            if lot.available_quantity > 0:
                available_lots.append(lot)

        # Remaining_quantity will be the remaining needed quantity which we will subtract every quantity we gather from the lots
        # The goal is to have 0 remaining
        remaining_quantity = quantity
        movements_created = []

        with transaction.atomic():
            for lot in available_lots:
                if remaining_quantity <= 0:
                    break

                available_in_lot = lot.available_quantity
                quantity_to_take = min(remaining_quantity, available_in_lot)

                if quantity_to_take > 0:
                    movement = Movement.objects.create(
                        lot=lot,
                        movement_type="OUT",
                        quantity=quantity_to_take,
                        notes=notes,
                        performed_by=performed_by,
                        # date is set to auto_now_add in model
                    )
                    movements_created.append(movement)
                    remaining_quantity -= quantity_to_take

            if remaining_quantity > 0:
                raise ValidationError(
                    f"Insufficient stock. Short by {remaining_quantity} units"
                )

        return movements_created


"""
    @staticmethod
    def stock_out(item, quantity, performed_by, notes=""):
        
        handles stock out operation following FIFO principle.
        

        # Get lots with available quantity
        # order them by received_date (FIFO)
        available_lots = Lot.objects.filter(
            item = item,
            available_quantity__gt=0
        ).order_by('received_date')

        # Remaining_quantity will be the remaining needed quantity which we will subtract every quantity we gather from the lots
        # The goal is to have 0 remaining
        # if Not zero -> error
        remaining_quantity = quantity
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
"""

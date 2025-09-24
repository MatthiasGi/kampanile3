"""
Additional GPIO related functionality for operating the input pins.

This module handles loading and monitoring of input pins defined in the
database. It sets up a background thread that continuously checks the state of
the input pins and triggers associated actions when a change is detected.
"""

import time
from threading import Thread

from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from ..models import Input
from .pin import Pin

INPUT_PINS = {}


def load_inputs():
    inputs = Input.objects.exclude(
        Q(active=False) | Q(pin__isnull=True) | Q(pin__exact="")
    )

    # Check if all pins exist and are unique
    pin_ids = set()
    for input in inputs:
        pin = input.board_pin
        if pin is None:
            input.deactivate(_("The specified pin does not exist on this board."))
            return  # Function will be called again by the signal handler
        if pin.id in pin_ids:
            input.deactivate(
                _("The specified pin is already used by another active input.")
            )
            return  # Function will be called again by the signal handler
        pin_ids.add(pin.id)

    # Determine pins not longer used anymore
    old_pin_ids = set(INPUT_PINS.keys()).difference(pin_ids)
    for id in old_pin_ids:
        INPUT_PINS[id].deinit()
        del INPUT_PINS[id]

    # Add new pins and update existing ones
    for input in inputs:
        id = input.board_pin.id
        if id not in INPUT_PINS:
            INPUT_PINS[id] = Pin(input)
        INPUT_PINS[id].update_settings()


def check_inputs():
    for pin in INPUT_PINS.values():
        pin.check()


def init_thread():
    def loop():
        while True:
            check_inputs()
            time.sleep(0.01)

    load_inputs()
    thread = Thread(target=loop, daemon=True)
    thread.start()


@receiver(post_delete, sender=Input)
@receiver(post_save, sender=Input)
def _input_change_handler(sender, **kwargs):
    load_inputs()

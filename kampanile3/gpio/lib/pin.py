from datetime import datetime, timedelta

import digitalio
from adafruit_debouncer import Debouncer

from ..models import Input


class Pin:
    def __init__(self, input: Input):
        self.input = input
        self.pin = digitalio.DigitalInOut(input.board_pin)
        self.last_value = self.pin.value
        self.next_trigger = None

    def deinit(self):
        self.pin.deinit()

    def update_settings(self):
        self.input.refresh_from_db()
        self.pin.switch_to_input(pull=self.input.pull_setting)
        if self.input.deadtime:
            self.deadtime = self.input.deadtime
        else:
            self.deadtime = None
            self.next_trigger = None
        self.debouncer = Debouncer(self.pin) if self.input.debounce else None

    def trigger(self):
        if self.deadtime is not None:
            self.next_trigger = datetime.now() + timedelta(milliseconds=self.deadtime)
        self.input.trigger()

    @property
    def deadtime_passed(self) -> bool:
        if self.next_trigger is None:
            return True
        if self.next_trigger > datetime.now():
            return False
        self.next_trigger = None
        return True

    def check(self):
        if not self.deadtime_passed:
            return
        if self.debouncer:
            self._check_debouncer()
        else:
            self._check_signal()

    def _check_debouncer(self):
        self.debouncer.update()
        if not (self.debouncer.fell or self.debouncer.rose):
            return
        match self.input.behaviour:
            case Input.Behaviour.ON_INPUT_CHANGE:
                self.trigger()
            case Input.Behaviour.ON_INPUT_HIGH if self.debouncer.rose:
                self.trigger()
            case Input.Behaviour.ON_INPUT_LOW if not self.debouncer.fell:
                self.trigger()

    def _check_signal(self):
        current_value = self.pin.value
        if current_value == self.last_value:
            return
        self.last_value = current_value
        match self.input.behaviour:
            case Input.Behaviour.ON_INPUT_CHANGE:
                self.trigger()
            case Input.Behaviour.ON_INPUT_HIGH if current_value:
                self.trigger()
            case Input.Behaviour.ON_INPUT_LOW if not current_value:
                self.trigger()

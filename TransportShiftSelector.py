# Written by Donovan Bartish aka DRockstar
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement

class TransportShiftSelector(ModeSelectorComponent):
    """ Shift Button """

    def __init__(self, parent, transport, transport_buttons, transport_view_modes, shift_modes, shift_button):
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False
        self._invert_assignment = False
        self._parent = parent
        self._transport = transport
        self._transport_buttons = transport_buttons
        self._transport_view_modes = transport_view_modes
        self._shift_modes = shift_modes
        self._shift_button = shift_button
        self._undo_button = None
        self._redo_button = None
        self._session_record_button = None
        self._record_automation_button = None
        self._metronome_button = None
        self._tap_tempo_button = None
        
    def disconnect(self):
        self._toggle_pressed = False
        self._invert_assignment = False
        self._parent = None
        self._transport = None
        self._transport_buttons = None
        self._transport_view_modes = None
        self._control_modes = None
        self._shift_modes = None
        self._shift_button = None
        self._undo_button = None
        self._redo_button = None
        self._session_record_button = None
        self._record_automation_button = None
        self._metronome_button = None
        self._tap_tempo_button = None
        ModeSelectorComponent.disconnect(self)

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)

    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()

    def number_of_modes(self):
        return 2

    def update(self):
        if self.is_enabled():
        
            if self._mode_index == 0:
                self._set_undo_button(None)
                self._set_redo_button(None)
                self._transport.set_overdub_button(None)
                self._set_session_record_button(None)
                self._set_record_automation_button(None)
                self._set_metronome_button(None)
                self._set_tap_tempo_button(None)
                self._shift_modes.set_mode_toggle(self._shift_button)
                self._shift_modes.update()
                self._transport_view_modes.update()
                
            elif self._mode_index == 1:
                self._stop_song()
                self._parent.reset_controls()
                self._shift_modes.set_mode_toggle(None)
                self._set_undo_button(self._transport_buttons[1])
                self._set_redo_button(self._transport_buttons[2])
                self._transport.set_overdub_button(self._transport_buttons[3])
                self._set_metronome_button(self._transport_buttons[4])
                self._set_tap_tempo_button(self._transport_buttons[5])
                self._set_record_automation_button(self._transport_buttons[6])
                self._set_session_record_button(self._shift_button)
                self._parent.show_message("#### TRANSPORT SHIFT ####   PADS:    "
                + "2: UNDO    3: REDO    4: OVERDUB    5: METRONOME    "
                + "6: TAP TEMPO    7: AUTOMATION RECORD    8: SESSION RECORD    ")

    def _toggle_value(self, value):
        assert self._mode_toggle != None or AssertionError
        assert value in range(128) or AssertionError
        self._toggle_pressed = value > 0
        self._recalculate_mode()

    def _recalculate_mode(self):
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())
        
    def _stop_song(self):
        self.song().stop_playing()

    def _set_undo_button(self, button):
        if (button is not self._undo_button):
            if (self._undo_button != None):
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = button
            if (self._undo_button != None):
                self._undo_button.add_value_listener(self._undo_value)

    def _undo_value(self, value):
        if value > 0:
            if self.song().can_undo:
                self.song().undo()
        if self.song().can_undo:
            self._undo_button.turn_on()
        else:
            self._undo_button.turn_off()

    def _set_redo_button(self, button):
        if (button is not self._redo_button):
            if (self._redo_button != None):
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = button
            if (self._redo_button != None):
                self._redo_button.add_value_listener(self._redo_value)

    def _redo_value(self, value):
        if value > 0:
            if self.song().can_redo:
                self.song().redo()
        if self.song().can_redo:
            self._redo_button.turn_on()
        else:
            self._redo_button.turn_off()

    def _set_session_record_button(self, button):
        if (button is not self._session_record_button):
            if (self._session_record_button != None):
                self._session_record_button.remove_value_listener(self._session_record_value)
            self._session_record_button = button
            if (self._session_record_button != None):
                self._session_record_button.add_value_listener(self._session_record_value)

    def _session_record_value(self, value):
        if value > 0:
            self.song().session_record = not (self.song().session_record)
        if (self.song().session_record):
            self._session_record_button.turn_on()
        else:
            self._session_record_button.turn_off()

    def _set_record_automation_button(self, button):
        if (button is not self._record_automation_button):
            if (self._record_automation_button != None):
                self._record_automation_button.remove_value_listener(self._record_automation_value)
            self._record_automation_button = button
            if (self._record_automation_button != None):
                self._record_automation_button.add_value_listener(self._record_automation_value)

    def _record_automation_value(self, value):
        if value > 0:
            self.song().session_automation_record = not (self.song().session_automation_record)
        if (self.song().session_automation_record):
            self._record_automation_button.turn_on()
        else:
            self._record_automation_button.turn_off()

    def _set_metronome_button(self, button):
        if (button is not self._metronome_button):
            if (self._metronome_button != None):
                self._metronome_button.remove_value_listener(self._metronome_value)
            self._metronome_button = button
            if (self._metronome_button != None):
                self._metronome_button.add_value_listener(self._metronome_value)

    def _metronome_value(self, value):
        if value > 0:
            self.song().metronome = not (self.song().metronome)
        if self.song().metronome:
            self._metronome_button.turn_on()
        else:
            self._metronome_button.turn_off()

    def _set_tap_tempo_button(self, button):
        if (button is not self._tap_tempo_button):
            if (self._tap_tempo_button != None):
                self._tap_tempo_button.remove_value_listener(self._tap_tempo_value)
            self._tap_tempo_button = button
            if (self._tap_tempo_button != None):
                self._tap_tempo_button.add_value_listener(self._tap_tempo_value)

    def _tap_tempo_value(self, value):
        if value > 0:
            self.song().tap_tempo()
            self._tap_tempo_button.turn_on()
        else:
            self._tap_tempo_button.turn_off()




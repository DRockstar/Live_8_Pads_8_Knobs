# Written by Donovan Bartish aka DRockstar
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement

class ShiftSelector(ModeSelectorComponent):
    """ Shift Button """

    def __init__(self, parent, transport, mixer, session, device, device_nav, encoders, 
    pads, transport_buttons, transport_view_modes, control_modes):
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False
        self._invert_assignment = False
        self._parent = parent
        self._transport = transport
        self._mixer = mixer
        self._session = session
        self._device = device
        self._device_nav = device_nav
        self._encoders = encoders
        self._pads = pads
        self._transport_buttons = transport_buttons
        self._transport_view_modes = transport_view_modes
        self._control_modes = control_modes
        self._all_buttons = pads + transport_buttons

    def disconnect(self):
        self._toggle_pressed = False
        self._invert_assignment = False
        self._parent = None
        self._transport = None
        self._mixer = None
        self._session = None
        self._device = None
        self._device_nav = None
        self._encoders = None
        self._pads = None
        self._transport_buttons = None
        self._transport_view_modes = None
        self._control_modes = None
        self._all_buttons = None
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
                self._transport_view_modes.update()
                self._control_modes.set_mode_buttons(None)
                self._mixer.master_strip().set_volume_control(None)
                self._control_modes.set_controls(self._encoders, self._pads, self._transport_buttons)
                
            elif self._mode_index == 1:
                self._parent.reset_controls()
                self._mixer.master_strip().set_volume_control(self._encoders[7])
                self._control_modes.set_mode_buttons(self._all_buttons)
                self._parent.show_message("  #### SHIFT PRESSED ####   "
                + "PAD 1: VOLUMES    PAD 2: PANS    PAD 3: SENDS    PAD 4: DEVICE CONTROL      ")
                
    def _toggle_value(self, value):
        assert self._mode_toggle != None or AssertionError
        assert value in range(128) or AssertionError
        self._toggle_pressed = value > 0
        self._recalculate_mode()

    def _recalculate_mode(self):
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())

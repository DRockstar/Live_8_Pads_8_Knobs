# Compiled and Written by Donovan Bartish aka DRockstar
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement

class ControlModeSelector(ModeSelectorComponent):

    def __init__(self, parent, mixer, session, device, device_nav):
        ModeSelectorComponent.__init__(self)
        self._parent = parent
        self._mixer = mixer
        self._session = session
        self._device = device
        self._device_nav = device_nav
        self._controls = None
        self._pads = None
        self._transport_buttons = None
        self.sends_index = 0
        self.send_button_up = None
        self.send_button_down = None
        self.send_controls = []
        self._modes_buttons = []
        self._pads_len = None
        self._transport_len = None
        self._clip_launch_button = None
        self._clip_stop_button = None
        self._mode_index = 0

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._parent = None
        self._mixer = None
        self._session = None
        self._device = None
        self._device_nav = None
        self._controls = None
        self._pads = None
        self._transport_buttons = None
        self.sends_index = 0
        self.send_button_up = None
        self.send_button_down = None
        self.send_controls = []
        self._modes_buttons = []
        self._pads_len = None
        self._transport_len = None
        self._clip_launch_button = None
        self._clip_stop_button = None

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)
        
    def set_lengths(self, pads, transport_buttons):
        self._pads_len = len(pads)
        self._transport_len = len(transport_buttons)

    def set_mode_buttons(self, buttons):
        assert isinstance(buttons, (tuple, type(None))) or AssertionError
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                assert isinstance(button, ButtonElement) or AssertionError
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

    def set_controls(self, controls, pads, transport_buttons):
        self._controls = controls
        self._pads = pads
        self._transport_buttons = transport_buttons
        self.update()

    def number_of_modes(self):
        # Max number of modes? 16 pads + 8 transport buttons, should be enough!?!
        return 24

    def update(self):
        if (self.is_enabled() and self._controls != None and self._pads != None 
        and self._mode_index in range(self.number_of_modes())):
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()
            mode = self._mode_index

            if mode == 0 or (mode - self._pads_len) == 0:
                self._session.set_track_bank_buttons(self._pads[1], self._pads[0])
                self._mixer.set_select_buttons(self._pads[3], self._pads[2])
                self._mixer.selected_strip().set_mute_button(self._pads[4])
                self._mixer.selected_strip().set_solo_button(self._pads[5])
                self._mixer.selected_strip().set_arm_button(self._pads[6])
                self._set_volume_controls()
                self._parent.show_message("#### VOLUME MODE ####  PADS:    "
                + "1: BANK LEFT    2: BANK RIGHT    3: PREV TRACK    4: NEXT TRACK    "
                + "5: MUTE    6: SOLO    7: RECORD")

            elif mode == 1 or (mode - self._pads_len) == 1:
                self._session.set_track_bank_buttons(self._pads[1], self._pads[0])
                self._mixer.set_select_buttons(self._pads[3], self._pads[2])
                self._mixer.selected_strip().set_mute_button(self._pads[4])
                self._mixer.selected_strip().set_solo_button(self._pads[5])
                self._mixer.selected_strip().set_arm_button(self._pads[6])
                self._set_pan_controls()
                self._parent.show_message("#### PAN MODE ####  PADS:    "
                + "1:  BANK LEFT    2: BANK RIGHT    3: PREV TRACK    4: NEXT TRACK    "
                + "5: MUTE    6: SOLO    7: RECORD")

            elif mode == 2 or (mode - self._pads_len) == 2:
                self._session.set_track_bank_buttons(self._pads[1], self._pads[0])
                self._mixer.selected_strip().set_mute_button(self._pads[4])
                self._mixer.selected_strip().set_solo_button(self._pads[5])
                self._mixer.selected_strip().set_arm_button(self._pads[6])
                self._set_send_nav(self._pads[3], self._pads[2])
                self._update_send_index(self.sends_index)

            elif mode == 3 or (mode - self._pads_len) == 3:
                self._device_nav.set_device_nav_buttons(self._pads[0], self._pads[1])
                self._device.set_bank_nav_buttons(self._pads[2], self._pads[3])
                self._device.set_on_off_button(self._pads[4])
                self._device.set_lock_button(self._pads[5])
                self._mixer.selected_strip().set_arm_button(self._pads[6])
                self._device.set_parameter_controls(self._controls)
                self._parent.show_message("#### DEVICE MODE ####  PADS:    "
                + "1: PREV DEVICE    2: NEXT DEVICE    3: PREV BANK    4: NEXT BANK    "
                + "5: DEVICE ON/OFF    6: DEVICE LOCK    7: RECORD")

            elif mode == 4 or (mode - self._pads_len) == 4:
                self.application().view.show_view('Session')
                self._session._num_tracks = 1
                self._session._do_show_highlight()
                scene = self._session.scene(0)
                self._session.set_track_bank_buttons(self._pads[1], self._pads[0])
                self._session.set_scene_bank_buttons(self._pads[3], self._pads[2])
                scene.set_launch_button(self._pads[4])
                self._set_clip_launch_button(self._pads[5])
                self._set_clip_stop_button(self._pads[6])
                strip = self._mixer.channel_strip(0)
                strip.set_volume_control(self._controls[0])
                strip.set_pan_control(self._controls[1])
                self.send_controls = []
                for index in range(len(self._controls) - 2):
                    self.send_controls.append(self._controls[index + 2])
                strip.set_send_controls(tuple(self.send_controls))
                self._parent.show_message("#### CLIPS MODE ####  PADS:    "
                + "1: CLIP LEFT    2: CLIP RIGHT    3: CLIP UP    4: CLIP DOWN    "
                + "5: LAUNCH SCENE    6: LAUNCH CLIP    7: STOP CLIP")

            else:
                self._mode_index = 0
                self.update()

    def _set_volume_controls(self):
        for index in range(len(self._controls)):
            strip = self._mixer.channel_strip(index)
            strip.set_volume_control(self._controls[index])

    def _set_pan_controls(self):
        for index in range(len(self._controls)):
            strip = self._mixer.channel_strip(index)
            strip.set_pan_control(self._controls[index])

    def _set_send_nav(self, send_up, send_down):
        if (send_up is not self.send_button_up):
            if (self.send_button_up != None):
                self.send_button_up.remove_value_listener(self._send_up_value)
            self.send_button_up = send_up
            if (self.send_button_up != None):
                self.send_button_up.add_value_listener(self._send_up_value)
        if (send_down is not self.send_button_down):
            if (self.send_button_down != None):
                self.send_button_down.remove_value_listener(self._send_down_value)
            self.send_button_down = send_down
            if (self.send_button_down != None):
                self.send_button_down.add_value_listener(self._send_down_value)

    def _send_up_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self.send_button_up, ButtonElement)
        if value is 127 or not self.send_button_up.is_momentary():
            if self.sends_index == (len(self.song().return_tracks) - 1):
                self.sends_index = 0
            else:
                new_sends_index = self.sends_index + 1
                self.sends_index = new_sends_index
        self._update_send_index(self.sends_index)

    def _send_down_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self.send_button_down, ButtonElement)
        if value is 127 or not self.send_button_down.is_momentary():
            if self.sends_index == 0:
                self.sends_index = (len(self.song().return_tracks) - 1)
            else:
                new_sends_index = self.sends_index - 1
                self.sends_index = new_sends_index
        self._update_send_index(self.sends_index)

    def _update_send_index(self, sends_index):
        send_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        for index in range(len(self._controls)):
            self.send_controls = []
            strip = self._mixer.channel_strip(index)
            for i in range(12):
                self.send_controls.append(None)
            self.send_controls[sends_index] = self._controls[index]
            strip.set_send_controls(tuple(self.send_controls))
        self._parent.show_message("#### SEND " + send_letters[sends_index] + " MODE ####  PADS:    "
         + "1: BANK LEFT     2: BANK RIGHT    3: SENDS DOWN    4: SENDS UP    "
         + "5: MUTE    6: SOLO    7: RECORD")

    def _set_clip_launch_button(self, button):
        if (button is not self._clip_launch_button):
            if (self._clip_launch_button != None):
                self._clip_launch_button.remove_value_listener(self._fire_clip_slot)
            self._clip_launch_button = button
            if (self._clip_launch_button != None):
                self._clip_launch_button.add_value_listener(self._fire_clip_slot)

    def _fire_clip_slot(self, value):
        self.song().view.highlighted_clip_slot.fire()
        
    def _set_clip_stop_button(self, button):
        if (button is not self._clip_stop_button):
            if (self._clip_stop_button != None):
                self._clip_stop_button.remove_value_listener(self._stop_clip_slot)
            self._clip_stop_button = button
            if (self._clip_stop_button != None):
                self._clip_stop_button.add_value_listener(self._stop_clip_slot)

    def _stop_clip_slot(self, value):
        self.song().view.highlighted_clip_slot.stop()

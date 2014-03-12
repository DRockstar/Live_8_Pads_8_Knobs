# Code Hackery by Donovan Bartish, aka DRockstar
from __future__ import with_statement
import Live
from consts import *
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from SpecialSessionComponent import SpecialSessionComponent
from BestBankDeviceComponent import BestBankDeviceComponent
from ShiftSelector import ShiftSelector
from ControlModeSelector import ControlModeSelector
from DeviceNavComponent import DeviceNavComponent
from TransportViewModeSelector import TransportViewModeSelector # Donovan
from SpecialMixerComponent import SpecialMixerComponent # Donovan

def make_button(cc_no):
    is_momentary = True
    if NOTE_MODE == 0:
        return ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no)
    else:
        return ButtonElement(is_momentary, MIDI_NOTE_TYPE, GLOBAL_CHANNEL, cc_no)

def make_encoder(cc_no, midi_mapmode):
    return EncoderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no, midi_mapmode)


class MiniLab_PLUS(ControlSurface):
    """ Script for the Arturia MiniLab based on several MIDI Remote Scripts """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._c_instance = c_instance 
            self._suggested_input_port = 'Arturia_MINILAB'
            self._suggested_output_port = 'Arturia_MINILAB'
            PAD_TRANSLATIONS = (
             (0, 3, DRUMPAD_NOTES[0], GLOBAL_CHANNEL),
             (1, 3, DRUMPAD_NOTES[1], GLOBAL_CHANNEL),
             (2, 3, DRUMPAD_NOTES[2], GLOBAL_CHANNEL),
             (3, 3, DRUMPAD_NOTES[3], GLOBAL_CHANNEL),
             (0, 2, DRUMPAD_NOTES[4], GLOBAL_CHANNEL),
             (1, 2, DRUMPAD_NOTES[5], GLOBAL_CHANNEL),
             (2, 2, DRUMPAD_NOTES[6], GLOBAL_CHANNEL),
             (3, 2, DRUMPAD_NOTES[7], GLOBAL_CHANNEL),
             (0, 1, DRUMPAD_NOTES[8], GLOBAL_CHANNEL),
             (1, 1, DRUMPAD_NOTES[9], GLOBAL_CHANNEL),
             (2, 1, DRUMPAD_NOTES[10], GLOBAL_CHANNEL),
             (3, 1, DRUMPAD_NOTES[11], GLOBAL_CHANNEL),
             (0, 0, DRUMPAD_NOTES[12], GLOBAL_CHANNEL),
             (1, 0, DRUMPAD_NOTES[13], GLOBAL_CHANNEL),
             (2, 0, DRUMPAD_NOTES[14], GLOBAL_CHANNEL),
             (3, 0, DRUMPAD_NOTES[15], GLOBAL_CHANNEL)
             )
            self.set_pad_translations(PAD_TRANSLATIONS)
            midi_mapmode = Live.MidiMap.MapMode.absolute
            if ENCODER_MODE == 1:
                midi_mapmode = Live.MidiMap.MapMode.absolute_14_bit
            elif ENCODER_MODE == 2:
                midi_mapmode = Live.MidiMap.MapMode.relative_binary_offset
            elif ENCODER_MODE == 3:
                midi_mapmode = Live.MidiMap.MapMode.relative_signed_bit
            elif ENCODER_MODE == 4:
                midi_mapmode = Live.MidiMap.MapMode.relative_signed_bit2
            elif ENCODER_MODE == 5:
                midi_mapmode = Live.MidiMap.MapMode.relative_smooth_binary_offset
            elif ENCODER_MODE == 6:
                midi_mapmode = Live.MidiMap.MapMode.relative_smooth_signed_bit
            elif ENCODER_MODE == 7:
                midi_mapmode = Live.MidiMap.MapMode.relative_smooth_signed_bit2
            elif ENCODER_MODE == 8:
                midi_mapmode = Live.MidiMap.MapMode.relative_smooth_two_compliment
            elif ENCODER_MODE == 9:
                midi_mapmode = Live.MidiMap.MapMode.relative_two_compliment
            transport_buttons = tuple([ make_button(TRANSPORTS[index]) for index in range(len(TRANSPORTS)) ])
            pads = tuple([ make_button(PADS[index]) for index in range(len(PADS)) ])
            encoders = tuple([ make_encoder(ENCODERS[index], midi_mapmode) for index in range(len(ENCODERS)) ])
            shift_button = make_button(SHIFT)
            self.suppress_session_highlight = True
            session = SpecialSessionComponent(NUM_TRACKS, NUM_SCENES)
            self.set_highlighting_session_component(session)
            self.suppress_session_highlight = False
            session.set_track_banking_increment(1)
            mixer = SpecialMixerComponent(NUM_TRACKS)
            session.set_mixer(mixer)
            transport = TransportComponent()
            transport_view_modes = TransportViewModeSelector(transport, session, transport_buttons)
            self._device_selection_follows_track_selection = True
            device = BestBankDeviceComponent()
            self.set_device_component(device)
            device_nav = DeviceNavComponent()
            control_modes = ControlModeSelector(self, mixer, session, device, device_nav)
            shift_modes = ShiftSelector(self, transport, mixer, session, device, device_nav, 
            encoders, pads, transport_buttons, transport_view_modes, control_modes)
            shift_modes.set_mode_toggle(shift_button)
            self.transport = transport
            self.transport_view_modes = transport_view_modes
            self.mixer = mixer
            self.session = session
            self.device = device
            self.device_nav = device_nav
            self.control_modes = control_modes
            self.encoders = encoders
            
    def reset_controls(self):
        self.transport.set_stop_button(None)
        self.transport.set_play_button(None)
        self.transport.set_seek_buttons(None, None)
        self.session.set_scene_bank_buttons(None, None)
        #self.session.set_select_buttons(None, None)
        self.transport.set_loop_button(None)
        self.transport.set_record_button(None)
        self.transport.set_overdub_button(None)
        self.transport_view_modes._set_session_view_button(None)
        scene = self.session.scene(0)
        scene.set_launch_button(None)
        self.session.set_track_bank_buttons(None, None)
        self.mixer.set_select_buttons(None, None)
        self.mixer.selected_strip().set_mute_button(None)
        self.mixer.selected_strip().set_solo_button(None)
        self.mixer.selected_strip().set_arm_button(None)
        self.mixer.master_strip().set_volume_control(None)
        self.mixer.master_strip().set_pan_control(None)
        for index in range(len(self.encoders)):
            strip = self.mixer.channel_strip(index)
            strip.set_volume_control(None)
            strip.set_pan_control(None)
            strip.set_send_controls(
            (None, None, None, None, None, None, None, None, None, None, None, None))
        self.device_nav.set_device_nav_buttons(None, None)
        self.device.set_bank_nav_buttons(None, None)
        self.device.set_on_off_button(None)
        self.device.set_lock_button(None)
        self.device.set_parameter_controls(None)
        self.control_modes._set_send_nav(None, None)
        self.control_modes._set_clip_launch_button(None)
        self.control_modes._set_clip_stop_button(None)
        self.control_modes.set_controls(None, None, None)
    
    def show_message(self, message):
        self._c_instance.show_message(message)

    def disconnect(self):
        self.transport = None
        self.transport_view_modes = None
        self.mixer = None
        self.session = None
        self.device = None
        self.device_nav = None
        self.control_modes = None
        self.encoders = []
        ControlSurface.disconnect(self)
        

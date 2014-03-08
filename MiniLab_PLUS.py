# Code Hackery by Donovan Bartish, aka DRockstar
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
#from _Framework.DeviceComponent import DeviceComponent
from Axiom_DirectLink.BestBankDeviceComponent import BestBankDeviceComponent # Donovan
from ShiftSelector import ShiftSelector
from ControlModeSelector import ControlModeSelector
from DeviceNavComponent import DeviceNavComponent
from TransportViewModeSelector import TransportViewModeSelector # Donovan
from SpecialMixerComponent import SpecialMixerComponent # Donovan


NUM_TRACKS = 8
NUM_SCENES = 1
GLOBAL_CHANNEL = 15
ENCODER_CC = [33, 34, 35, 36, 37, 38, 39, 40]
# Transport: Stop, Play, Rewind, Fast Forward, Loop, Record
TRANSPORT_CC = [116, 117, 114, 115, 113, 118, 60]
# Minus one pad to account for shift button
PAD_CC = [99, 100, 101, 102, 98, 61, 59] 
SHIFT_CC = 58
ENCODER_MODE = Live.MidiMap.MapMode.relative_smooth_binary_offset
# Donovan changed MIDI notes, channel 16, notice reverse order of the drum rack rows
PAD_TRANSLATIONS = (
 (0, 3, 36, 15),
 (1, 3, 37, 15),
 (2, 3, 38, 15),
 (3, 3, 39, 15),
 (0, 2, 40, 15),
 (1, 2, 41, 15),
 (2, 2, 42, 15),
 (3, 2, 43, 15),
 (0, 1, 44, 15),
 (1, 1, 45, 15),
 (2, 1, 46, 15),
 (3, 1, 47, 15),
 (0, 0, 48, 15),
 (1, 0, 49, 15),
 (2, 0, 50, 15),
 (3, 0, 51, 15)
 )

def make_button(cc_no):
    is_momentary = True
    return ButtonElement(is_momentary, MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no)

def make_encoder(cc_no):
    return EncoderElement(MIDI_CC_TYPE, GLOBAL_CHANNEL, cc_no, ENCODER_MODE)


class MiniLab_PLUS(ControlSurface):
    """ Script for the Arturia MiniLab based on several MIDI Remote Scripts """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._c_instance = c_instance 
            self._suggested_input_port = 'Arturia_MINILAB'
            self._suggested_output_port = 'Arturia_MINILAB'
            self.set_pad_translations(PAD_TRANSLATIONS)
            transport_buttons = tuple([ make_button(TRANSPORT_CC[index]) for index in range(len(TRANSPORT_CC)) ])
            pads = tuple([ make_button(PAD_CC[index]) for index in range(len(PAD_CC)) ])
            encoders = tuple([ make_encoder(ENCODER_CC[index]) for index in range(len(ENCODER_CC)) ])
            shift_button = make_button(SHIFT_CC)
            stop_button = transport_buttons[0]
            play_button = transport_buttons[1]
            rwd_button = transport_buttons[2]
            ffwd_button = transport_buttons[3]
            loop_button = transport_buttons[4]
            record_button = transport_buttons[5]
            self.suppress_session_highlight = True
            session = SessionComponent(NUM_TRACKS, NUM_SCENES)
            self.set_highlighting_session_component(session)
            self.suppress_session_highlight = False
            session.set_track_banking_increment(1)
            mixer = SpecialMixerComponent(NUM_TRACKS)
            session.set_mixer(mixer)
            transport = TransportComponent()
            transport_view_modes = TransportViewModeSelector(transport, session, stop_button, play_button, rwd_button, ffwd_button, loop_button, record_button)
            self._device_selection_follows_track_selection = True
            #device = DeviceComponent()
            device = BestBankDeviceComponent()
            self.set_device_component(device)
            device_nav = DeviceNavComponent()
            control_modes = ControlModeSelector(self, mixer, session, device, device_nav)
            shift_modes = ShiftSelector(self, transport, mixer, session, device, device_nav, encoders, pads, transport_buttons, transport_view_modes, control_modes)
            shift_modes.set_mode_toggle(shift_button)
            self.transport = transport
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
        scene = self.session.scene(0)
        scene.set_launch_button(None)
        self.session.set_track_bank_buttons(None, None)
        self.mixer.set_select_buttons(None, None)
        self.mixer.selected_strip().set_mute_button(None)
        self.mixer.selected_strip().set_solo_button(None)
        self.mixer.selected_strip().set_arm_button(None)
        self.mixer.master_strip().set_volume_control(None)
        for index in range(len(self.encoders)):
            strip = self.mixer.channel_strip(index)
            strip.set_volume_control(None)
            strip.set_pan_control(None)
            strip.set_send_controls((None, None, None, None, None, None, None, None, None, None, None, None))
        self.device_nav.set_device_nav_buttons(None, None)
        self.device.set_bank_nav_buttons(None, None)
        self.device.set_on_off_button(None)
        self.device.set_lock_button(None)
        self.device.set_parameter_controls(None)
        self.control_modes._set_send_nav(None, None)
        self.control_modes.set_controls(None, None, None)
    
    def show_message(self, message):
        self._c_instance.show_message(message)

    def disconnect(self):
        self.transport = None
        self.mixer = None
        self.session = None
        self.device = None
        self.device_nav = None
        self.control_modes = None
        self.encoders = []
        ControlSurface.disconnect(self)
        

# Modified by Donovan Bartish aka DRockstar from Oxygen 3rd Gen script
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.ClipSlotComponent import ClipSlotComponent

class TransportViewModeSelector(ModeSelectorComponent):
    """ Class that reassigns specific buttons based on the views visible in Live """

    def __init__(self, transport, session, transport_buttons):
        # Donovan assert instead of raise for Live 9?
        assert isinstance(transport, TransportComponent) or AssertionError
        assert isinstance(session, SessionComponent) or AssertionError
        ModeSelectorComponent.__init__(self)
        self._transport = transport
        self._session = session
        self._stop_button = transport_buttons[0]
        self._play_button = transport_buttons[1]
        self._rwd_button = transport_buttons[2]
        self._ffwd_button = transport_buttons[3]
        self._loop_button = transport_buttons[4]
        self._record_button = transport_buttons[5]
        self._view_button = transport_buttons[6]
        self.session_view_button = None
        self.view = Live.Application.get_application().view
        self.application().view.add_is_view_visible_listener('Session', self._on_view_changed)
        self.update()

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._transport = None
        self._session = None
        self._stop_button = None
        self._play_button = None
        self._ffwd_button = None
        self._rwd_button = None
        self._loop_button = None
        self._record_button = None
        self._view_button = None
        self.session_view_button = None
        self.application().view.remove_is_view_visible_listener('Session', self._on_view_changed)

    def update(self):
        if self.is_enabled():
            scene = self._session.scene(0)
            #self._transport.set_stop_button(self._stop_button)
            self._transport.set_play_button(self._play_button)
            self._transport.set_record_button(self._record_button)
            self._set_session_view_button(self._view_button)
            if self._mode_index == 0:
                self._transport.set_seek_buttons(self._ffwd_button, self._rwd_button)
                self._session.set_scene_bank_buttons(None, None)
                self._transport.set_loop_button(self._loop_button)
                # These select buttons are a pita, selecting None produces errors
                #self._session.set_select_buttons(None, None)
                scene.set_launch_button(None)
            else:
                self._transport.set_seek_buttons(None, None)
                self._transport.set_loop_button(None)
                #self._session.set_select_buttons(self._ffwd_button, self._rwd_button)
                self._session.set_scene_bank_buttons(self._ffwd_button, self._rwd_button)
                scene.set_launch_button(self._loop_button)

    def _on_view_changed(self):
        if self.application().view.is_view_visible('Session'):
            self._mode_index = 1
        else:
            self._mode_index = 0
        self.update()

    def _set_session_view_button(self, button):
        if (button is not self.session_view_button):
            if (self.session_view_button != None):
                self.session_view_button.remove_value_listener(self._session_view_value)
            self.session_view_button = button
            if (self.session_view_button != None):
                self.session_view_button.add_value_listener(self._session_view_value)
        
    def _session_view_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self.session_view_button, ButtonElement)
        if value is 127 or not self._view_button.is_momentary():
            if not self.view.is_view_visible('Session'):
                self.view.show_view('Session')
            else:
                self.view.show_view('Arranger')




import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ButtonElement import ButtonElement

INITIAL_SCROLLING_DELAY = 5 #5
INTERVAL_SCROLLING_DELAY = 1 #1
SCENE_FOLLOWS_SESSION_BOX = True
TRACK_FOLLOWS_SESSION_BOX = True

class SpecialSessionComponent(SessionComponent):
    
    def __init__(self, num_tracks, num_scenes):
        self._tracks_and_listeners = []
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._scene_up_button = None
        self._scene_down_button = None
        self._scroll_up_ticks_delay = -1
        self._scroll_down_ticks_delay = -1
        self._register_timer_callback(self._on_custom_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_custom_timer)
        for index in range(len(self._tracks_and_listeners)):
            track = self._tracks_and_listeners[index][0]
            listener = self._tracks_and_listeners[index][2]
        SessionComponent.disconnect(self)
        self._scene_up_button = None
        self._scene_down_button = None

    def refresh_state(self):
        pass

    def _is_scrolling(self):
        return 0 in (self._scroll_up_ticks_delay, self._scroll_down_ticks_delay)

    def on_enabled_changed(self):
        self._scroll_up_ticks_delay = -1
        self._scroll_down_ticks_delay = -1
        self.update()
        self._do_show_highlight()

    def set_scene_bank_buttons(self, up_button, down_button):
        if up_button is not self._scene_up_button:
            if self._scene_up_button != None:
                self._scene_up_button.remove_value_listener(self._bank_up_value)
            self._scene_up_button = up_button
            if self._scene_up_button != None:
                self._scene_up_button.add_value_listener(self._bank_up_value)
        if down_button is not self._scene_down_button:
            if self._scene_down_button != None:
                self._scene_down_button.remove_value_listener(self._bank_down_value)
            self._scene_down_button = down_button
            if self._scene_down_button != None:
                self._scene_down_button.add_value_listener(self._bank_down_value)

    def _bank_up_value(self, value):
        if not value in range(128):
            raise AssertionError
        if not self._scene_up_button != None:
            raise AssertionError
        if self.is_enabled():
            button_is_momentary = self._scene_up_button.is_momentary()
            if button_is_momentary:
                if value != 0:
                    self._scroll_up_ticks_delay = INITIAL_SCROLLING_DELAY
                    if len(self.song().scenes) > self._scene_offset + 1:
                        self._scene_up_button.turn_on()
                else:
                    self._scroll_up_ticks_delay = -1
                    self._scene_up_button.turn_off()
            if not self._is_scrolling():
                if value is not 0 or not button_is_momentary:
                    self.set_offsets(self._track_offset, self._scene_offset + 1)
            if SCENE_FOLLOWS_SESSION_BOX and self.song().view.selected_scene != self.song().scenes[self._scene_offset]:
                self.song().view.selected_scene = self.song().scenes[self._scene_offset]

    def _bank_down_value(self, value):
        if not value in range(128):
            raise AssertionError
        if not self._scene_down_button != None:
            raise AssertionError
        if self.is_enabled():
            button_is_momentary = self._scene_down_button.is_momentary()
            if button_is_momentary:
                if value != 0:
                    self._scroll_down_ticks_delay = INITIAL_SCROLLING_DELAY
                    if self._scene_offset > 0:
                        self._scene_down_button.turn_on()
                else:
                    self._scroll_down_ticks_delay = -1
                    self._scene_down_button.turn_off()
            if not self._is_scrolling():
                if value is not 0 or not button_is_momentary:
                    self.set_offsets(self._track_offset, max(0, self._scene_offset - 1))
            if SCENE_FOLLOWS_SESSION_BOX and self.song().view.selected_scene != self.song().scenes[self._scene_offset]:
                self.song().view.selected_scene = self.song().scenes[self._scene_offset]

    def prepare_bank_right(self):
        self.set_offsets(self.track_offset() + self._track_banking_increment, self.scene_offset())
        if TRACK_FOLLOWS_SESSION_BOX:
            selected_track = self.song().view.selected_track
            all_tracks = self.song().visible_tracks + self.song().return_tracks
            if selected_track != all_tracks[-1]:
                index = list(all_tracks).index(selected_track)
                self.song().view.selected_track = all_tracks[index + 1]

    def _bank_right(self):
        return self.prepare_bank_right()

    def prepare_bank_left(self):
        self.set_offsets(max(self.track_offset() - self._track_banking_increment, 0), self.scene_offset())
        if TRACK_FOLLOWS_SESSION_BOX:
            selected_track = self.song().view.selected_track
            all_tracks = self.song().visible_tracks + self.song().return_tracks
            if selected_track != all_tracks[0]:
                index = list(all_tracks).index(selected_track)
                self.song().view.selected_track = all_tracks[index - 1]

    def _bank_left(self):
        return self.prepare_bank_left()

    def set_track_banking_increment(self, increment):
        SessionComponent.set_track_banking_increment(self, increment)
        self._horizontal_banking.update()

    def _on_custom_timer(self):
        if self.is_enabled():
            scroll_delays = [
                self._scroll_up_ticks_delay,
                self._scroll_down_ticks_delay]
            if scroll_delays.count(-1) < 4:
                scenes_increment = 0
                if self._scroll_down_ticks_delay > -1:
                    if self._is_scrolling():
                        scenes_increment -= 1
                        self._scroll_down_ticks_delay = INTERVAL_SCROLLING_DELAY
                    self._scroll_down_ticks_delay -= 1
                if self._scroll_up_ticks_delay > -1:
                    if self._is_scrolling():
                        scenes_increment += 1
                        self._scroll_up_ticks_delay = INTERVAL_SCROLLING_DELAY
                    self._scroll_up_ticks_delay -= 1
                new_scene_offset = max(0, self._scene_offset + scenes_increment)
                if new_scene_offset != self._scene_offset:
                    self.set_offsets(self._track_offset, new_scene_offset)
            if self._is_scrolling():
                if SCENE_FOLLOWS_SESSION_BOX and self.song().view.selected_scene != self.song().scenes[self._scene_offset]:
                    self.song().view.selected_scene = self.song().scenes[self._scene_offset]



"""WaitTimer - Visuell väntetimer för barn."""

import gi
from waittimer.i18n import _
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk
import random

CSS = """
window {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.time-display {
    font-size: 120px;
    font-weight: 900;
    font-family: monospace;
    color: white;
    text-shadow: 0 0 30px rgba(100, 200, 255, 0.5);
}
.time-display-warning {
    font-size: 120px;
    font-weight: 900;
    font-family: monospace;
    color: #ff6b6b;
    text-shadow: 0 0 30px rgba(255, 100, 100, 0.5);
}
.time-display-done {
    font-size: 120px;
    font-weight: 900;
    font-family: monospace;
    color: #51cf66;
    text-shadow: 0 0 40px rgba(81, 207, 102, 0.7);
}
.preset-button {
    font-size: 24px;
    font-weight: bold;
    padding: 16px 32px;
    border-radius: 16px;
    min-width: 100px;
}
.status-label {
    font-size: 32px;
    color: rgba(255, 255, 255, 0.8);
}
.celebration-label {
    font-size: 64px;
}
.progress-label {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.6);
}
.control-button {
    font-size: 20px;
    padding: 12px 24px;
    border-radius: 12px;
}
"""

CELEBRATIONS = [
    "🎉 GRATTIS! 🎉",
    "⭐ BRA JOBBAT! ⭐",
    "🏆 DU KLARADE DET! 🏆",
    "🌟 FANTASTISKT! 🌟",
    "🎊 HURRA! 🎊",
]


class WaitTimerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="se.waittimer.app")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.remaining = 0
        self.total = 0
        self.running = False
        self.timer_id = None

        # Window
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("WaitTimer")
        self.win.set_default_size(600, 700)

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)
        main_box.set_valign(Gtk.Align.CENTER)
        main_box.set_halign(Gtk.Align.CENTER)

        # Status label
        self.status_label = Gtk.Label(label=_("Choose a time to wait!")
        self.status_label.add_css_class("status-label")
        main_box.append(self.status_label)

        # Time display
        self.time_label = Gtk.Label(label=_("00:00")
        self.time_label.add_css_class("time-display")
        main_box.append(self.time_label)

        # Progress text
        self.progress_label = Gtk.Label(label=_("")
        self.progress_label.add_css_class("progress-label")
        main_box.append(self.progress_label)

        # Celebration label (hidden by default)
        self.celebration_label = Gtk.Label(label=_("")
        self.celebration_label.add_css_class("celebration-label")
        self.celebration_label.set_visible(False)
        main_box.append(self.celebration_label)

        # Preset buttons
        preset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        preset_box.set_halign(Gtk.Align.CENTER)
        preset_box.set_margin_top(20)

        for minutes in [5, 10, 15, 30]:
            btn = Gtk.Button(label=f"{minutes} min")
            btn.add_css_class("preset-button")
            btn.add_css_class("suggested-action")
            btn.connect("clicked", self.on_preset, minutes)
            preset_box.append(btn)

        self.preset_box = preset_box
        main_box.append(preset_box)

        # Control buttons
        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        control_box.set_halign(Gtk.Align.CENTER)
        control_box.set_margin_top(10)

        self.pause_btn = Gtk.Button(label=_("⏸ Pause")
        self.pause_btn.add_css_class("control-button")
        self.pause_btn.connect("clicked", self.on_pause)
        self.pause_btn.set_visible(False)
        control_box.append(self.pause_btn)

        self.stop_btn = Gtk.Button(label=_("⏹ Cancel")
        self.stop_btn.add_css_class("control-button")
        self.stop_btn.add_css_class("destructive-action")
        self.stop_btn.connect("clicked", self.on_stop)
        self.stop_btn.set_visible(False)
        control_box.append(self.stop_btn)

        main_box.append(control_box)

        self.win.set_content(main_box)
        self.win.present()

    def on_preset(self, btn, minutes):
        self.start_timer(minutes * 60)

    def start_timer(self, seconds):
        if self.timer_id:
            GLib.source_remove(self.timer_id)

        self.remaining = seconds
        self.total = seconds
        self.running = True

        self.celebration_label.set_visible(False)
        self.preset_box.set_visible(False)
        self.pause_btn.set_visible(True)
        self.stop_btn.set_visible(True)
        self.pause_btn.set_label("⏸ Pausa")

        self.status_label.set_text("Vänta lite till...")
        self.update_display()
        self.timer_id = GLib.timeout_add(1000, self.tick)

    def tick(self):
        if not self.running:
            return True

        self.remaining -= 1
        self.update_display()

        if self.remaining <= 0:
            self.timer_done()
            return False

        return True

    def update_display(self):
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.time_label.set_text(f"{mins:02d}:{secs:02d}")

        # Update progress
        if self.total > 0:
            pct = ((self.total - self.remaining) / self.total) * 100
            self.progress_label.set_text(f"{pct:.0f}% klart")

        # Color changes based on remaining time
        self.time_label.remove_css_class("time-display")
        self.time_label.remove_css_class("time-display-warning")
        self.time_label.remove_css_class("time-display-done")

        if self.remaining <= 10:
            self.time_label.add_css_class("time-display-warning")
            self.status_label.set_text("Nästan klar!")
        else:
            self.time_label.add_css_class("time-display")

    def timer_done(self):
        self.running = False
        self.timer_id = None

        self.time_label.remove_css_class("time-display")
        self.time_label.remove_css_class("time-display-warning")
        self.time_label.add_css_class("time-display-done")
        self.time_label.set_text("00:00")

        self.status_label.set_text("Tiden är ute!")
        self.progress_label.set_text("100% klart")

        # Show celebration
        self.celebration_label.set_text(random.choice(CELEBRATIONS))
        self.celebration_label.set_visible(True)

        self.pause_btn.set_visible(False)
        self.stop_btn.set_visible(False)

        # Animate celebration, then show presets again
        self._celebrate_count = 0
        GLib.timeout_add(500, self.animate_celebration)

    def animate_celebration(self):
        self._celebrate_count += 1
        if self._celebrate_count % 2 == 0:
            self.celebration_label.set_text(random.choice(CELEBRATIONS))
        else:
            self.celebration_label.set_text("🎉🌟⭐🎊🏆")

        if self._celebrate_count >= 8:
            self.celebration_label.set_text(random.choice(CELEBRATIONS))
            # Show presets again after celebration
            GLib.timeout_add(2000, self.reset_ui)
            return False
        return True

    def reset_ui(self):
        self.preset_box.set_visible(True)
        self.status_label.set_text("Välj en tid att vänta!")
        self.celebration_label.set_visible(False)
        self.progress_label.set_text("")
        self.time_label.remove_css_class("time-display-done")
        self.time_label.add_css_class("time-display")
        self.time_label.set_text("00:00")
        return False

    def on_pause(self, btn):
        self.running = not self.running
        if self.running:
            self.pause_btn.set_label("⏸ Pausa")
            self.status_label.set_text("Vänta lite till...")
        else:
            self.pause_btn.set_label(_("▶ Continue"))
            self.status_label.set_text("Pausad")

    def on_stop(self, btn):
        self.running = False
        if self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = None
        self.reset_ui()


def main():
    app = WaitTimerApp()
    app.run()


if __name__ == "__main__":
    main()

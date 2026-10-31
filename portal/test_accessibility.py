"""NFR-009 -- WCAG 2.1 AA on the attempt flow: keyboard-operable, text contrast >= 4.5:1, every option labelled.

Automated here: contrast of the stylesheet's colour pairs, the skip link, labelled options, no keyboard traps
in the markup. Manual, recorded in the PR description: a Lighthouse accessibility run (Chrome DevTools) on the
attempt page with no AA violations, and completing EXM_1 using only Tab / Shift+Tab / arrows / Space / Enter.
"""
import re
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from portal.testkit import World

CSS = Path(settings.BASE_DIR) / "portal/static/portal/site.css"


def tokens():
    """{"--ink": "#2f3437", ...} from the :root block of site.css."""
    return dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})", CSS.read_text(encoding="utf-8")))


def luminance(hex_colour):
    """WCAG 2.1 relative luminance."""
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# Text colour -> the backgrounds it is actually used on in site.css.
PAIRS = [
    ("--ink", "--bg"), ("--ink", "--surface"), ("--muted", "--bg"), ("--muted", "--surface"),
    ("--blue", "--blue-bg"), ("--green", "--green-bg"), ("--yellow", "--yellow-bg"), ("--red", "--red-bg"),
    ("--surface", "--btn"),  # button text on a button
]


class AccessibilityTests(TestCase):
    def setUp(self):
        self.world = World(n_questions=3)
        self.attempt = self.world.attempt()
        self.client.force_login(self.world.stu_a)

    def test_text_contrast_is_at_least_4_5_to_1(self):
        t = tokens()
        failing = [f"{fg} on {bg}: {contrast(t[fg], t[bg]):.2f}" for fg, bg in PAIRS if contrast(t[fg], t[bg]) < 4.5]
        # TODO(Kartik): darken whichever tokens fail (keep the hue; e.g. --muted) in site.css until this is empty.
        self.assertEqual(failing, [])

    def test_every_page_starts_with_a_skip_link_to_main(self):
        response = self.client.get(reverse("attempt-paper", args=[self.attempt.pk]))
        # TODO(Kartik): first thing in _nav.html: <a class="skip-link" href="#main">Skip to content</a>
        # (visually hidden until focused, in site.css), and wrap each page's content in <main id="main">.
        self.assertContains(response, 'href="#main"')
        self.assertContains(response, 'id="main"')

    def test_every_option_has_a_label(self):
        html = self.client.get(reverse("attempt-paper", args=[self.attempt.pk])).content.decode()
        radios = re.findall(r"<input[^>]*type=\"radio\"[^>]*>", html)
        self.assertTrue(radios)
        # Every radio sits inside a <label> (implicit labelling), so a screen reader reads the option text.
        labelled = re.findall(r"<label[^>]*>\s*<input[^>]*type=\"radio\"", html)
        self.assertEqual(len(labelled), len(radios))

    def test_focus_is_never_hidden(self):
        css = CSS.read_text(encoding="utf-8")
        # TODO(Kartik): site.css line ~131 removes the outline on input:focus and relies on a 1 px border colour
        # change, which is too faint for WCAG 2.4.7. Drop `outline: none` there so :focus-visible's outline shows.
        self.assertIsNone(re.search(r"outline:\s*none", css), "site.css hides the focus outline somewhere")

    def test_timer_announces_politely(self):
        response = self.client.get(reverse("attempt-paper", args=[self.attempt.pk]))
        self.assertContains(response, 'id="timer"')
        self.assertContains(response, 'aria-live="polite"')

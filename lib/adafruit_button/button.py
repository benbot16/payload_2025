# SPDX-FileCopyrightText: 2019 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_button.button`
================================================================================

UI Buttons for displayio


* Author(s): Limor Fried

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

from micropython import const
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_button.button_base import ButtonBase, _check_color

__version__ = "1.9.2"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"


class Button(ButtonBase):
    # pylint: disable=too-many-instance-attributes, too-many-locals
    """Helper class for creating UI buttons for ``displayio``.

    :param x: The x position of the button.
    :param y: The y position of the button.
    :param width: The width of the button in pixels.
    :param height: The height of the button in pixels.
    :param name: The name of the button.
    :param style: The style of the button. Can be RECT, ROUNDRECT, SHADOWRECT, SHADOWROUNDRECT.
                  Defaults to RECT.
    :param fill_color: The color to fill the button. Defaults to 0xFFFFFF.
    :param outline_color: The color of the outline of the button.
    :param label: The text that appears inside the button. Defaults to not displaying the label.
    :param label_font: The button label font.
    :param label_color: The color of the button label text. Defaults to 0x0.
    :param selected_fill: Inverts the fill color.
    :param selected_outline: Inverts the outline color.
    :param selected_label: Inverts the label color.
    """

    def _empty_self_group(self):
        while len(self) > 0:
            self.pop()

    def _create_body(self):
        if (self.outline_color is not None) or (self.fill_color is not None):
            if self.style == Button.RECT:
                self.body = Rect(
                    0,
                    0,
                    self.width,
                    self.height,
                    fill=self._fill_color,
                    outline=self._outline_color,
                )
            elif self.style == Button.ROUNDRECT:
                self.body = RoundRect(
                    0,
                    0,
                    self.width,
                    self.height,
                    r=10,
                    fill=self._fill_color,
                    outline=self._outline_color,
                )
            elif self.style == Button.SHADOWRECT:
                self.shadow = Rect(
                    2, 2, self.width - 2, self.height - 2, fill=self.outline_color
                )
                self.body = Rect(
                    0,
                    0,
                    self.width - 2,
                    self.height - 2,
                    fill=self._fill_color,
                    outline=self._outline_color,
                )
            elif self.style == Button.SHADOWROUNDRECT:
                self.shadow = RoundRect(
                    2,
                    2,
                    self.width - 2,
                    self.height - 2,
                    r=10,
                    fill=self._outline_color,
                )
                self.body = RoundRect(
                    0,
                    0,
                    self.width - 2,
                    self.height - 2,
                    r=10,
                    fill=self._fill_color,
                    outline=self._outline_color,
                )
            if self.shadow:
                self.append(self.shadow)

    RECT = const(0)
    ROUNDRECT = const(1)
    SHADOWRECT = const(2)
    SHADOWROUNDRECT = const(3)

    def __init__(
        self,
        *,
        x,
        y,
        width,
        height,
        name=None,
        style=RECT,
        fill_color=0xFFFFFF,
        outline_color=0x0,
        label=None,
        label_font=None,
        label_color=0x0,
        selected_fill=None,
        selected_outline=None,
        selected_label=None,
        label_scale=None
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            name=name,
            label=label,
            label_font=label_font,
            label_color=label_color,
            selected_label=selected_label,
            label_scale=label_scale,
        )

        self.body = self.fill = self.shadow = None
        self.style = style

        self._fill_color = _check_color(fill_color)
        self._outline_color = _check_color(outline_color)

        # Selecting inverts the button colors!
        self._selected_fill = _check_color(selected_fill)
        self._selected_outline = _check_color(selected_outline)

        if self.selected_fill is None and fill_color is not None:
            self.selected_fill = (~self._fill_color) & 0xFFFFFF
        if self.selected_outline is None and outline_color is not None:
            self.selected_outline = (~self._outline_color) & 0xFFFFFF

        self._create_body()
        if self.body:
            self.append(self.body)

        self.label = label

    def _subclass_selected_behavior(self, value):
        if self._selected:
            new_fill = self.selected_fill
            new_out = self.selected_outline
        else:
            new_fill = self._fill_color
            new_out = self._outline_color
        # update all relevant colors!
        if self.body is not None:
            self.body.fill = new_fill
            self.body.outline = new_out

    @property
    def group(self):
        """Return self for compatibility with old API."""
        print(
            "Warning: The group property is being deprecated. "
            "User code should be updated to add the Button directly to the "
            "Display or other Groups."
        )
        return self

    def contains(self, point):
        """Used to determine if a point is contained within a button. For example,
        ``button.contains(touch)`` where ``touch`` is the touch point on the screen will allow for
        determining that a button has been touched.
        """
        return (self.x <= point[0] <= self.x + self.width) and (
            self.y <= point[1] <= self.y + self.height
        )

    @property
    def fill_color(self):
        """The fill color of the button body"""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, new_color):
        self._fill_color = _check_color(new_color)
        if not self.selected:
            self.body.fill = self._fill_color

    @property
    def outline_color(self):
        """The outline color of the button body"""
        return self._outline_color

    @outline_color.setter
    def outline_color(self, new_color):
        self._outline_color = _check_color(new_color)
        if not self.selected:
            self.body.outline = self._outline_color

    @property
    def selected_fill(self):
        """The fill color of the button body when selected"""
        return self._selected_fill

    @selected_fill.setter
    def selected_fill(self, new_color):
        self._selected_fill = _check_color(new_color)
        if self.selected:
            self.body.fill = self._selected_fill

    @property
    def selected_outline(self):
        """The outline color of the button body when selected"""
        return self._selected_outline

    @selected_outline.setter
    def selected_outline(self, new_color):
        self._selected_outline = _check_color(new_color)
        if self.selected:
            self.body.outline = self._selected_outline

    @property
    def width(self):
        """The width of the button"""
        return self._width

    @width.setter
    def width(self, new_width):
        self._width = new_width
        self._empty_self_group()
        self._create_body()
        if self.body:
            self.append(self.body)
        self.label = self.label

    @property
    def height(self):
        """The height of the button"""
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height
        self._empty_self_group()
        self._create_body()
        if self.body:
            self.append(self.body)
        self.label = self.label

    def resize(self, new_width, new_height):
        """Resize the button to the new width and height given
        :param new_width int the desired width
        :param new_height int the desired height
        """
        self._width = new_width
        self._height = new_height
        self._empty_self_group()
        self._create_body()
        if self.body:
            self.append(self.body)
        self.label = self.label

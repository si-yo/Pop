#from mods.utils.imports import *
# Standard library
import time

# Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    ListProperty,
    BooleanProperty,
    NumericProperty,
)
from kivy.graphics import (
    ScissorPush,
    ScissorPop,
    Color,
    RoundedRectangle,
    Rectangle,
)

# KivyMD
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
# ——————————————————————————————————————————————————————
# ClipWidget : masque le contenu hors de la zone
# ——————————————————————————————————————————————————————
class ClipWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._upd, size=self._upd)
        Clock.schedule_once(lambda dt: self._upd(), 0)
        with self.canvas.before:
            self._sc = ScissorPush()
        with self.canvas.after:
            ScissorPop()

    def _upd(self, *a):
        self._sc.x      = int(self.x)
        self._sc.y      = int(self.y)
        self._sc.width  = int(self.width)
        self._sc.height = int(self.height)


# ——————————————————————————————————————————————————————
# DraggableHeader : barre custom pour déplacer en normal/max
# ——————————————————————————————————————————————————————
class DraggableHeader(BoxLayout):
    
    def __init__(self,title, **kwargs):
        super().__init__(orientation="horizontal",
                         size_hint_y=None, height=dp(34), **kwargs)
        self.title = title
        self.padding = (dp(8), 0)
        self.spacing = dp(4)

        # fond clair arrondi en haut
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self._bg = RoundedRectangle(radius=[10,10,0,0])
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        # titre centré
        self.lbl = Label(text=self.title,
                         size_hint_x=1,
                         valign="middle",
                         color=(0,0,0,1))
        self.add_widget(self.lbl)

        # boutons minimise / maximise / ferme
        btn_kw = {
            "size_hint": (None, 1),
            "width": dp(28),
            # Force the icon to use the custom color instead of the theme default
            "theme_text_color": "Custom",
            "text_color": (0, 0, 0, 1)  # RGBA: black
        }
        self.btn_min   = MDIconButton(icon="window-minimize", **btn_kw)
        self.btn_max   = MDIconButton(icon="window-maximize", **btn_kw)
        self.btn_close = MDIconButton(icon="window-close",    **btn_kw)
        self.add_widget(self.btn_min)
        self.add_widget(self.btn_max)
        self.add_widget(self.btn_close)

        # variables de drag
        self._dragging = False
        self._dx = self._dy = 0

        # bind drag au label (on pourrait binder toute la barre)
        self.lbl.bind(on_touch_down=self._start,
                      on_touch_move=self._move,
                      on_touch_up=self._end)

    def _upd_bg(self, *l):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _start(self, w, touch):
        if w.collide_point(*touch.pos):
            self._dragging = True
            pop = self.parent.parent  # header → root BoxLayout → Pop
            self._dx = pop.x - touch.x
            self._dy = pop.y - touch.y
            return True

    def _move(self, w, touch):
        if self._dragging:
            pop = self.parent.parent
            nx = touch.x + self._dx
            ny = touch.y + self._dy
            # clamp dans la fenêtre
            nx = max(0, min(nx, Window.width  - pop.width))
            ny = max(0, min(ny, Window.height - pop.height))
            pop.pos = (nx, ny)
            return True

    def _end(self, w, touch):
        if self._dragging:
            self._dragging = False
            return True


# ——————————————————————————————————————————————————————
# Pop : la « fenêtre » custom
# ——————————————————————————————————————————————————————
class Pop(MDCard):
    state           = StringProperty("normal")     # normal / minimized / maximized
    popup_pos       = ListProperty([100, 100])
    original_size   = ListProperty([800, 800])
    original_pos    = ListProperty([100, 100])
    _resizing       = BooleanProperty(False)
    _content_height = NumericProperty(0)

    def __init__(self,title="", content=None, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)
                # — en normal/max : fond transparent + pas d'ombre —
        self.md_bg_color = (0.5, 0.5, 0.5, 1)
        self.elevation   = 1
        # — stocker le style d'origine —
        self._orig_bg_color = list(self.md_bg_color)
        self._orig_elevation = self.elevation

        self._tooltip = None
        self.bind(popup_pos=lambda inst, val: self._hide_tooltip())
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_touch_down=self._on_window_touch_down)

        # position & taille initiales
        self.size = tuple(self.original_size)
        self.pos  = tuple(self.popup_pos)
        self.bind(popup_pos=lambda i,v: setattr(self, 'pos', v))

        # rayon arrondi partout
        self.radius = [10]*4

        # contenu
        self.root = BoxLayout(orientation='vertical')
        # → header draggable
        self.header = DraggableHeader(title)
        self.header.title = title
        self.header.btn_close.bind(on_release=lambda *_: self.dismiss())
        self.header.btn_min.  bind(on_release=lambda *_: self.toggle_minimize())
        self.header.btn_max.  bind(on_release=lambda *_: self.toggle_maximize())
        self.root.add_widget(self.header)
        # → zone de contenu clipée
        self.content_widget = content
        self.clip = ClipWidget()
        self.clip.add_widget(self.content_widget)
        self.root.add_widget(self.clip)
        self.add_widget(self.root)
        Clock.schedule_once(self._store_content_height, 0.1)
        self._dragging = False
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._last_click_time = 0
        self._double_click_threshold = 0.3
        # timestamp du dernier clic droit
        self._last_right_click_time = 0
        # seuil pour double-clic (en secondes)
        self._right_double_click_threshold = 0.3


    def _store_content_height(self, dt):
        self._content_height = self.clip.height

    # — mode cercle / minimisé —
    def toggle_minimize(self):
        if self.state != "minimized":
            # restaurer fond/bloc ombre
            self.md_bg_color = self._orig_bg_color
            self.elevation   = self._orig_elevation

            # mémoriser pour le restore
            self.original_size = self.size[:]
            self.original_pos  = self.pos[:]

            # ne garder que le cercle
            self.clear_widgets()
            dia = dp(50)
            self.size   = (dia, dia)
            self.radius = [dia/2]*4

            self.state = "minimized"
        else:
            # repasser en transparent + shadow=0
            self.md_bg_color = (0.5, 0.5, 0.5, 1)
            self.elevation   = 1

            # rebuild contenu normal/max
            self.clear_widgets()
            self.add_widget(self.root)

            # clamp pour rester visible
            w, h = self.original_size
            x, y = self.original_pos
            x = max(0, min(x, Window.width  - w))
            y = max(0, min(y, Window.height - h))
            self.pos  = (x, y)
            self.size = (w, h)
            self.radius = [10]*4

            self.state = "normal"

    # — plein écran / restituer —
    def toggle_maximize(self):
        if self.state == "minimized":
            self.toggle_minimize()
        if self.state != "maximized":
            # mémoriser avant
            self.original_size = self.size[:]
            self.original_pos  = self.pos[:]
            # plein écran transparent
            self.pos  = (0, 0)
            self.size = Window.size[:]
            self.state = "maximized"
        else:
            # restaurer
            self.pos  = tuple(self.original_pos)
            self.size = tuple(self.original_size)
            self.state = "normal"

    def dismiss(self,inst=None):
        if self.parent:
            self.parent.remove_widget(self)

    def open(self, win=Window):
        win.add_widget(self)
        

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            parent = self.parent
            if parent:
                parent.remove_widget(self)
                parent.add_widget(self)
        # 2) ensuite on garde toute ta logique (minimize / resize / drag…)
        if not super().collide_point(*touch.pos):
            return False
        if not self.collide_point(*touch.pos):
            return False
        if self.state == "minimized" and self.collide_point(*touch.pos):
            current_time = time.time()
            if current_time - self._last_click_time < self._double_click_threshold:
                self.toggle_minimize()  # Restaurer en mode normal
                self._last_click_time = 0
                return True
            else:
                self._last_click_time = current_time
            self._dragging = True
            self._drag_offset_x = self.x - touch.x
            self._drag_offset_y = self.y - touch.y
            return True

        if self.state == "normal":
            dirs = self._get_resize_direction(touch)
            self._dragging = True
            if dirs:
                self._resizing = True
                self._resize_direction = dirs
                self._resize_start_size = self.size[:]
                self._resize_start_pos = self.pos[:]
                self._resize_start_touch = touch.pos
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._dragging and self.state == "minimized":
            # déplacer librement mais clamp pour ne pas sortir
            dia = self.width  # cercle minimisé
            new_x = touch.x + self._drag_offset_x
            new_y = touch.y + self._drag_offset_y

            new_x = max(0, min(new_x, Window.width - dia))
            new_y = max(0, min(new_y, Window.height - dia))

            self.popup_pos = [new_x, new_y]
            return True

        if self._resizing and self.state == "normal":
            dx = touch.x - self._resize_start_touch[0]
            dy = touch.y - self._resize_start_touch[1]
            new_x, new_y = self._resize_start_pos
            new_width, new_height = self._resize_start_size

            if "left" in self._resize_direction:
                new_x += dx
                new_width -= dx
            if "right" in self._resize_direction:
                new_width += dx
            if "bottom" in self._resize_direction:
                new_y += dy
                new_height -= dy
            if "top" in self._resize_direction:
                new_height += dy

            new_width = max(150, new_width)
            new_height = max(100, new_height)
            self.size = (new_width, new_height)
            self.popup_pos = (new_x, new_y)
            return True

        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._dragging and self.state == "minimized":
            self._dragging = False
            return True
        if self._resizing and self.state == "normal":
            self._resizing = False
            self._resize_direction = None
            return True
        return super().on_touch_up(touch)

    def _get_resize_direction(self, touch):
        widget_x, widget_y = self.to_window(self.x, self.y, relative=False)
        widget_right = widget_x + self.width
        widget_top = widget_y + self.height
        margin = dp(10)
        directions = []
        touch_x, touch_y = touch.pos
        if touch_x - widget_x <= margin:
            directions.append("left")
        if widget_right - touch_x <= margin:
            directions.append("right")
        if touch_y - widget_y <= margin:
            directions.append("bottom")
        if widget_top - touch_y <= margin:
            directions.append("top")
        return directions if directions else None


    def _show_tooltip(self):
        if self._tooltip:
            return  # déjà affiché
        # création du label
        tooltip = Label(
            text=self.header.title,
            size_hint=(None, None),
            padding=(dp(6), dp(4)),
        )
        tooltip.texture_update()
        tw, th = tooltip.texture.size
        tooltip.size = (tw + dp(12), th + dp(8))
        # positionner juste au-dessus du cercle
        tooltip.pos = (
            self.x + self.width/2 - tooltip.width/2,
            self.y + self.height + dp(4),
        )
        # fond semi-transparent
        with tooltip.canvas.before:
            Color(0, 0, 0, 0.75)
            tooltip._bg_rect = Rectangle(size=tooltip.size, pos=tooltip.pos)
        # pour maintenir le pos/size du fond quand on redimensionne
        tooltip.bind(pos=lambda w, v: setattr(w._bg_rect, 'pos', v))
        tooltip.bind(size=lambda w, v: setattr(w._bg_rect, 'size', v))
        # on ajoute au même parent que le Pop
        if self.parent:
            self.parent.add_widget(tooltip)
        else:
            self.add_widget(tooltip)
        self._tooltip = tooltip

    def _hide_tooltip(self):
        if not self._tooltip:
            return
        # retirer le label
        if self._tooltip.parent:
            self._tooltip.parent.remove_widget(self._tooltip)
        self._tooltip = None

    def _store_content_height(self, dt):
        self._content_height = self.content_widget.height

    def _on_window_touch_down(self, window, touch):
        # on ne s'intéresse qu'aux clics droits
        if touch.button == 'right':
            # si je suis en mode normal et que le clic est hors de mon card
            if self.state != "minimized" and not self.collide_point(*touch.pos):
                now = time.time()
                # double-clic ?
                if now - self._last_right_click_time < self._right_double_click_threshold:
                    self.toggle_minimize()
                    # réinitialise pour éviter triple-clic
                    self._last_right_click_time = 0
                else:
                    self._last_right_click_time = now
        # ne pas bloquer la propagation des autres événements
        return False

    def set_pos(self, val):
        # Méthode déjà appelée depuis le binding sur popup_pos
        self.x, self.y = val
        # Si vous préférez le faire ici, vous pouvez aussi :
        # self._hide_tooltip()



    def on_mouse_pos(self, window, pos):
        # si minimisé et qu’on survole
        if self.state == "minimized" and self.collide_point(*pos):
            self._show_tooltip()
        else:
            self._hide_tooltip()
    def collide_point(self, x, y):
        """
        On redéfinit la collision :
        - en mode normal, on garde le rectangle habituel
        - en mode minimized, on ne renvoie True que si (x,y) est
          dans le cercle affiché
        """
        if self.state == "minimized":
            # centre du cercle
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            r = self.width / 2
            return (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2
        else:
            return super().collide_point(x, y)


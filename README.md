# Pop<br>

Pop is a Kivy/KivyMD component that provides a customizable and movable "window" with support for minimizing, maximizing, resizing, and a hover tooltip. <br>

<p align="center">
<a href="https://youtu.be/4xKg6wrlKkk">
<img src="https://img.youtube.com/vi/4xKg6wrlKkk/0.jpg" alt="Pop Presentation Preview" width="480"/>
</a>
</p>

> **Presentation Video:** [Discover Pop on YouTube](https://youtu.be/4xKg6wrlKkk)<br>

---

## Key Features<br>

- **Moveable**: Click and drag on the title bar to reposition the window.<br>
- **Minimize/Restore**: Toggles between a minimized circle and the original size, with double-click and right-click animations.<br>
- **Maximize/Restore**: Toggles to full screen and returns to the saved size.<br>
- **Resizable** : Borders detected to dynamically adjust width and height.<br>
- **Content Clip**: Automatically hides anything that exceeds the content area.<br>
- **Tooltip**: Displays the title on hover when minimized.<br>
- KivyMD Styles (MDCard, MDIconButton) for elegant integration.<br>

---

## Installation<br>

Make sure you have Python 3.10+ and install the dependencies:<br>

```bash
pip install kivy kivymd
```
Then, place the pop.py module (containing the ClipWidget, DraggableHeader, and Pop classes) in your project, for example:<br>

your_project/<br>
├── main.py<br>
└── mods/<br>
└── widgets/<br>
└── pop.py<br>

⸻

Usage<br>

1. Import the class<br>
```python
from mods.widgets.pop import Pop
from kivy.uix.label import Label
```
2. Create and open a Pop
```python
# Create some content, here a simple Label
content = Label(text="Hello Pop!", size_hint=(1, 1))

# Instantiate the Pop window
pop = Pop(
title="My Custom Pop",
content=content,
original_size=[400, 300],
popup_pos=[50, 50]
)

# Add Pop to the main window
pop.open()
```

Your users will then be able to:<br>
• Click and drag the bar to move the window.<br>
• Minimize to Clicking the "-" button or double-clicking.<br>
• Maximize by clicking the "□" button.<br>
• Restore the original size by clicking the "□" button again.<br>
• Resize by dragging the edges (10px sensitivity).

⸻

Quick API<br>

Property Type Description<br>
state StringProperty "normal", "minimized", or "maximized"<br>
original_size ListProperty Saved size for restoration<br>
popup_pos ListProperty Current position of the popup

Method Description<br>
toggle_minimize() Toggles between minimized and normal size<br>
toggle_maximize() Toggles between full screen and normal size<br>
dismiss() Closes and removes the popup from the parent<br>
open(win=Window) Adds the popup to the win window

⸻

Customization<br>
• Styles: Change md_bg_color, elevation, or radius after creation.<br>
• Throttle: Adjust the double_click_threshold for the double-click speed.<br>
• Tooltip: Change the appearance of the label in _show_tooltip().

# Pop<br>

Pop est un composant Kivy/KivyMD qui fournit une « fenêtre » personnalisable et déplaçable, avec support de la minimisation, de la maximisation, du redimensionnement, et d’un tooltip au survol.  <br>

<p align="center">
  <a href="https://youtu.be/4xKg6wrlKkk">
    <img src="https://img.youtube.com/vi/4xKg6wrlKkk/0.jpg" alt="Aperçu de la présentation Pop" width="480"/>
  </a>
</p>

> **Vidéo de présentation :** [Découvrir Pop sur YouTube](https://youtu.be/4xKg6wrlKkk)<br>

---

## Caractéristiques principales<br>

- **Déplacable** : clique-glisse sur la barre de titre pour repositionner la fenêtre.<br>
- **Minimisation / restauration** : bascule entre un cercle réduit et la taille originale, avec animation de double-clic et clic droit.<br>
- **Maximisation / restauration** : bascule en plein écran et revient à la taille enregistrée.<br>
- **Redimensionnable** : bordures détectées pour ajuster dynamiquement largeur et hauteur.<br>
- **Clip du contenu** : masque automatiquement tout ce qui dépasse de la zone de contenu.<br>
- **Tooltip** : affiche le titre au survol lorsque minimisé.<br>
- Styles KivyMD (MDCard, MDIconButton) pour une intégration élégante.<br>

---

## Installation<br>

Assurez-vous d’avoir Python 3.10+ et installez les dépendances :<br>

```bash
pip install kivy kivymd
```
Puis, placez le module pop.py (contenant les classes ClipWidget, DraggableHeader, et Pop) dans votre projet, par exemple :<br>

your_project/<br>
├── main.py<br>
└── mods/<br>
    └── widgets/<br>
        └── pop.py<br>


⸻

Utilisation<br>

1. Importer la classe<br>
```python
from mods.widgets.pop import Pop
from kivy.uix.label import Label
```
2. Créer et ouvrir une Pop
```python
# Crée un contenu, ici un simple Label
content = Label(text="Bonjour Pop !", size_hint=(1, 1))

# Instancie la fenêtre Pop
pop = Pop(
    title="Ma Pop Personnalisée",
    content=content,
    original_size=[400, 300],
    popup_pos=[50, 50]
)

# Ajoute Pop à la fenêtre principale
pop.open()
```

Vos utilisateurs pourront alors :<br>
	•	Cliquer-glisser la barre pour déplacer la fenêtre.<br>
	•	Minimiser en cliquant sur le bouton « – » ou faire un double-clic.<br>
	•	Maximiser en cliquant sur le bouton « □ ».<br>
	•	Restaurer la taille originale par un nouveau clic sur « □ ».<br>
	•	Redimensionner en glissant sur les bords (10 px de sensibilité).

⸻

API rapide<br>

Propriété	Type	Description<br>
state	StringProperty	"normal", "minimized" ou "maximized"<br>
original_size	ListProperty	Taille sauvegardée pour restauration<br>
popup_pos	ListProperty	Position actuelle de la Pop

Méthode	Description<br>
toggle_minimize()	Bascule entre minimisé et taille normale<br>
toggle_maximize()	Bascule entre plein écran et taille normale<br>
dismiss()	Ferme et supprime la Pop du parent<br>
open(win=Window)	Ajoute la Pop à la fenêtre win


⸻

Personnalisation<br>
	•	Styles : changez md_bg_color, elevation ou radius après création.<br>
	•	Throttle : ajustez le seuil double_click_threshold pour la vitesse de double-clic.<br>
	•	Tooltip : modifiez l’apparence du label dans _show_tooltip().


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


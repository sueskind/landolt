intro_texts = [
    """Im Folgenden werden dir sogenannte Landolt-C-Reize gezeigt, d. h. es wird irgendwo in der Umgebung des Fixationskreuzes kurz ein Kreis mit einer Öffnung gezeigt, die entweder nach links, oben, rechts oder nach unten zeigt.

(Drücke die Leertaste)
""",

    """Deine Aufgabe ist es, die Öffnung der Ringe zu erkennen und entsprechend mit den Pfeiltasten zu antworten, also die Pfeiltaste 'oben' zu drücken, wenn die Öffnung oben ist, die Pfeiltaste 'links', wenn die Öffnung links ist, usw.

(Drücke die Leertaste)""",

    """WICHTIG ist dabei, dass du das gesamte Experiment über, das Fixationskreuz im Zentrum des Bildschirms fixierst.
Um zu überprüfen, ob dein Blick auch tatsächlich auf das Fixationskreuz fokussiert ist, wird bei manchen Trails (ein Trial ist das kurze Anzeigen eines Landolt-C-Reizes) das Fixationskreuz ein kleines Stück nach links oder rechts verdreht.
Wenn du das bemerkst, sollst du NICHT die erkannte Öffnung des Landolt-C-Reizes angeben, sondern nur die Leertaste drücken. 
Sobald das Fixationskreuz wieder in einer Ursprungsposition, also aufrecht im Zentrum des Bildschirms ist, reagiere bitte wieder auf die Öffnung des Landolt-C-Reizes.

(Drücke die Leertaste)"""
]

soundcheck_text = """Nach jedem Trail erhältst du Feedback zur Richtigkeit deiner Antwort in Form von verschiedenen Tönen oder eines verbalen Feedbacks. 

Du kannst jetzt auf die Taste P drücken, um dir ein Beispiel eines positiven Feedbacks anzuhören.

Wenn du auf die Taste N drückst, kannst du dir das Beispiel eines negativen Feedbacks anhören.

Drücke nun die Leertaste, um mit dem Versuch zu beginnen!
"""

break_texts = {
    0.25: """Du hast nun ungefähr ein Viertel der Übung geschafft. Du kannst dir daher eine kleine Pause nehmen.

Drücke die Leertaste, um wieder mit der Aufgabe fortzufahren!""",

    0.5: """Du hast nun ungefähr die Hälfte der Übung geschafft. Du kannst dir daher eine kleine Pause nehmen.

Drücke die Leertaste, um wieder mit der Aufgabe fortzufahren!""",

    0.75: """Du hast nun ungefähr drei Viertel der Übung geschafft. Du kannst dir daher eine kleine Pause nehmen.

Drücke die Leertaste, um wieder mit der Aufgabe fortzufahren!"""
}

end_text = """Du hast die heutige Übungseinheit absolviert.

Drücke die Leertaste, um die Einheit zu beenden"""

feedback_text_fmt = """Dein Abstand zwischen dem Zielreiz und den beiden äußeren Kreisen hat sich
von {:.2f} auf {:.2f} Grad Sehwinkel geändert."""

intro_texts = [
    """Im Folgenden werden dir sogenannte Landolt-C-Reize gezeigt, d. h. es wird irgendwo in der Umgebung des Fixationskreuzes kurz ein Kreis mit einer Öffnung gezeigt, die entweder nach links, oben, rechts oder nach unten zeigt.""",
    """Deine Aufgabe ist es, die Öffnung der Ringe zu erkennen und entsprechend mit den Pfeiltasten zu antworten, also die Pfeiltaste 'oben' zu drücken, wenn die Öffnung oben ist, die Pfeiltaste 'links', wenn die Öffnung links ist, usw.""",
    """WICHTIG ist dabei, dass du das gesamte Experiment über, das Fixationskreuz im Zentrum des Bildschirms fixierst.
Um zu überprüfen, ob dein Blick auch tatsächlich auf das Fixationskreuz fokussiert ist, wird bei manchen Trails (ein Trial ist das kurze Anzeigen eines Landolt-C-Reizes) das Fixationskreuz ein kleines Stück nach links oder rechts verdreht.
Wenn du das bemerkst, sollst du NICHT die erkannte Öffnung des Landolt-C-Reizes angeben, sondern nur die Leertaste drücken. 
Sobald das Fixationskreuz wieder in einer Ursprungsposition, also aufrecht im Zentrum des Bildschirms ist, reagiere bitte wieder auf die Öffnung des Landolt-C-Reizes."""
]

soundcheck_text = """Nach jedem Trail erhältst du Feedback zur Richtigkeit deiner Antwort in Form von verschiedenen Tönen oder eines verbalen Feedbacks. 

Du kannst jetzt auf die Taste P drücken, um dir ein Beispiel eines positiven Feedbacks anzuhören.
Wenn du auf die Taste N drückst, kannst du dir das Beispiel eines negativen Feedbacks anhören.

Drücken Sie nun die Leertaste, um mit dem Versuch zu beginnen!
"""

break_texts = {
    0.25: """Sie haben nun ungefähr ein Viertel der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.

Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!""",

    0.5: """Sie haben nun ungefähr die Hälfte der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.

Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!""",

    0.75: """Sie haben nun ungefähr drei Viertel der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.

Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!"""
}

end_text = """Sie haben die heutige Übungseinheit absolviert.

Drücken sie die Leertaste, um die Einheit zu beenden"""

feedback_text_fmt = """Ihr Abstand zwischen dem Zielreiz und den beiden äußeren Kreisen hat sich
von {:.2f} auf {:.2f} Grad Sehwinkel geändert"""

"""
ÉTAPE 1 — Programmation procédurale
Système de notes étudiantes : saisie, calcul, classement, validation
"""
 
# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────
NOTE_MIN = 0
NOTE_MAX = 20
MATIERES_VALIDES = ["Maths", "Français", "Histoire", "Physique", "Anglais"]
 
 
# ─────────────────────────────────────────────
# Fonctions de validation
# ─────────────────────────────────────────────
def est_note_valide(note):
    """Vérifie qu'une note est dans le barème [0, 20]."""
    return isinstance(note, (int, float)) and NOTE_MIN <= note <= NOTE_MAX
 
 
def valider_notes(notes_dict):
    """
    Détecte les notes manquantes ou hors barème dans un dictionnaire.
    
    Args:
        notes_dict (dict): {matiere: note} — note peut être None si manquante
    
    Returns:
        dict: {'manquantes': [...], 'hors_bareme': [...]}
    """
    problemes = {"manquantes": [], "hors_bareme": []}
    for matiere, note in notes_dict.items():
        if note is None:
            problemes["manquantes"].append(matiere)
        elif not est_note_valide(note):
            problemes["hors_bareme"].append((matiere, note))
    return problemes
 
 
# ─────────────────────────────────────────────
# Fonctions de calcul
# ─────────────────────────────────────────────
def calculer_moyenne(notes_dict):
    """
    Calcule la moyenne des notes valides d'un étudiant.
    
    Args:
        notes_dict (dict): {matiere: note}
    
    Returns:
        float | None: moyenne arrondie à 2 décimales, ou None si aucune note valide
    """
    notes_valides = [n for n in notes_dict.values() if n is not None and est_note_valide(n)]
    if not notes_valides:
        return None
    return round(sum(notes_valides) / len(notes_valides), 2)
 
 
def calculer_moyennes_classe(classe):
    """
    Calcule la moyenne de chaque étudiant d'une classe.
    
    Args:
        classe (dict): {nom_etudiant: {matiere: note}}
    
    Returns:
        dict: {nom_etudiant: moyenne}
    """
    return {nom: calculer_moyenne(notes) for nom, notes in classe.items()}
 
 
def moyenne_par_matiere(classe):
    """
    Calcule la moyenne de la classe pour chaque matière.
    
    Args:
        classe (dict): {nom_etudiant: {matiere: note}}
    
    Returns:
        dict: {matiere: moyenne_classe}
    """
    totaux = {}
    compteurs = {}
 
    for notes in classe.values():
        for matiere, note in notes.items():
            if note is not None and est_note_valide(note):
                totaux[matiere] = totaux.get(matiere, 0) + note
                compteurs[matiere] = compteurs.get(matiere, 0) + 1
 
    return {
        mat: round(totaux[mat] / compteurs[mat], 2)
        for mat in totaux
    }
 
 
# ─────────────────────────────────────────────
# Fonctions d'affichage
# ─────────────────────────────────────────────
def afficher_classement(classe):
    """Affiche le classement des étudiants par ordre décroissant de moyenne."""
    moyennes = calculer_moyennes_classe(classe)
    # sorted retourne une liste de tuples (nom, moyenne), classés du meilleur au moins bon
    classement = sorted(
        [(nom, moy) for nom, moy in moyennes.items() if moy is not None],
        key=lambda x: x[1],
        reverse=True
    )
 
    print("\n" + "═" * 40)
    print("       CLASSEMENT DE LA CLASSE")
    print("═" * 40)
    for rang, (nom, moy) in enumerate(classement, start=1):
        barre = "█" * int(moy)
        print(f"  {rang:>2}. {nom:<18} {moy:>5.2f}/20  {barre}")
    print("═" * 40)
 
 
def afficher_bulletin(nom, notes_dict):
    """Affiche le bulletin détaillé d'un étudiant."""
    print(f"\n{'─'*40}")
    print(f"  BULLETIN — {nom.upper()}")
    print(f"{'─'*40}")
 
    problemes = valider_notes(notes_dict)
 
    for matiere, note in notes_dict.items():
        if note is None:
            statut = "⚠ MANQUANTE"
            print(f"  {matiere:<15} {statut}")
        elif not est_note_valide(note):
            print(f"  {matiere:<15} {note} ← HORS BARÈME")
        else:
            mention = " ★" if note >= 16 else ""
            print(f"  {matiere:<15} {note:>5.1f}/20{mention}")
 
    moy = calculer_moyenne(notes_dict)
    print(f"{'─'*40}")
    if moy is not None:
        print(f"  Moyenne générale : {moy:.2f}/20")
    else:
        print("  Moyenne : non calculable (notes invalides)")
 
    if problemes["manquantes"]:
        print(f"  ⚠ Notes manquantes : {', '.join(problemes['manquantes'])}")
    if problemes["hors_bareme"]:
        for mat, val in problemes["hors_bareme"]:
            print(f"  ✗ Note hors barème en {mat} : {val}")
 
 
def afficher_stats_matieres(classe):
    """Affiche les statistiques par matière."""
    print("\n" + "═" * 40)
    print("     MOYENNES PAR MATIÈRE")
    print("═" * 40)
    moy_mat = moyenne_par_matiere(classe)
    for matiere, moy in sorted(moy_mat.items(), key=lambda x: x[1], reverse=True):
        print(f"  {matiere:<15} {moy:>5.2f}/20")
    print("═" * 40)
 
 
# ─────────────────────────────────────────────
# Saisie interactive
# ─────────────────────────────────────────────
def saisir_note(matiere):
    """
    Demande une note à l'utilisateur avec gestion des erreurs.
    
    Returns:
        float | None: la note saisie, ou None si absente
    """
    while True:
        saisie = input(f"  Note en {matiere} (Entrée = absent) : ").strip()
        if saisie == "":
            return None
        try:
            note = float(saisie)
            if est_note_valide(note):
                return note
            else:
                print(f"  ✗ La note doit être entre {NOTE_MIN} et {NOTE_MAX}.")
        except ValueError:
            print("  ✗ Veuillez entrer un nombre valide.")
 
 
def saisir_etudiant():
    """Saisit les notes d'un étudiant pour toutes les matières."""
    nom = input("Nom de l'étudiant : ").strip()
    if not nom:
        print("✗ Le nom ne peut pas être vide.")
        return None, None
 
    notes = {}
    for matiere in MATIERES_VALIDES:
        notes[matiere] = saisir_note(matiere)
 
    return nom, notes
 
 
# ─────────────────────────────────────────────
# Programme principal
# ─────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════╗")
    print("║   SYSTÈME DE NOTES ÉTUDIANTES v1.0   ║")
    print("║       Programmation procédurale       ║")
    print("╚══════════════════════════════════════╝\n")
 
    # Données de démonstration (pour ne pas saisir manuellement)
    classe = {
        "Alice Martin": {
            "Maths": 17.5, "Français": 14, "Histoire": 16,
            "Physique": 18, "Anglais": 15
        },
        "Bob Dupont": {
            "Maths": 12, "Français": None,  # note manquante
            "Histoire": 11, "Physique": 9.5, "Anglais": 13
        },
        "Clara Ndiaye": {
            "Maths": 8, "Français": 19, "Histoire": 14,
            "Physique": 25,  # hors barème volontaire
            "Anglais": 16
        },
        "David Traoré": {
            "Maths": 5, "Français": 7, "Histoire": 6,
            "Physique": 4, "Anglais": 8
        },
    }
 
    # Affichage des bulletins individuels
    for nom, notes in classe.items():
        afficher_bulletin(nom, notes)
 
    # Classement général
    afficher_classement(classe)
 
    # Stats par matière
    afficher_stats_matieres(classe)
 
    # Option : saisie interactive
    print("\n" + "─" * 40)
    reponse = input("Voulez-vous saisir un nouvel étudiant ? (o/n) : ").strip().lower()
    if reponse == "o":
        nom, notes = saisir_etudiant()
        if nom:
            classe[nom] = notes
            afficher_bulletin(nom, notes)
            afficher_classement(classe)
 
 
if __name__ == "__main__":
    main()
 

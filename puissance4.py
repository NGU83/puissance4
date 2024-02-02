# Importation des modules Tkinter nécessaires
import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Définition de la classe Puissance4 qui gère le jeu
class Puissance4:
    # def __init__(self, root):
    def __init__(self, root=None): # Modification pour unittest
        # Initialisation de l'interface graphique et des paramètres du jeu
        # self.root = root
        self.root = root or tk.Tk()  # Utilisez root s'il est fourni, sinon créez un nouveau Tkinter Tk()

        self.root.title("Puissance 4")
        self.lignes = 6
        self.colonnes = 7
        self.joueurs = ['', '']
        self.joueur_actuel_indice = 0
        self.grille = [['' for _ in range(self.colonnes)] for _ in range(self.lignes)]
        self.algorithme_ia = None
        self.profondeur_minimax = 3  # Choisir une profondeur appropriée pour l'algorithme Minimax
        
        # Initialisation du menu, du plateau de jeu et du bouton de réinitialisation
        self.init_menu()
        self.init_grille()
        self.bouton_vider()
        self.demarrer_jeu(False)

    # Ajoutez cette méthode pour permettre l'initialisation avec une configuration spécifique
    # pour unittest
    @classmethod
    def init_with_config(cls, config):
        root = config.get('root', None)
        instance = cls(root=root)
        # Initialisez d'autres attributs de l'instance si nécessaire
        return instance
    
    # Méthode pour initialiser le menu du jeu
    def init_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        jeu_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Jeu", menu=jeu_menu)

        jeu_menu.add_command(label="Joueur seul", command=lambda: self.demarrer_jeu(False))
        jeu_menu.add_command(label="A deux joueurs", command=lambda: self.demarrer_jeu(True))
        
        self.algo_menu = tk.Menu(jeu_menu, tearoff=0)
        jeu_menu.add_cascade(label="Contre l'IA", menu=self.algo_menu)
        self.init_algorithme_options()

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="Règles du jeu", command=self.affiche_regles)
        help_menu.add_command(label="Comment jouer", command=self.affiche_insctructions)


    def init_algorithme_options(self):
        algorithmes = ["Algorithme Simple", "Algorithme Sophistiqué", "Algorithme Minimax"]
        self.selected_algo = tk.StringVar()
        self.selected_algo.set(algorithmes[0])

        for algo in algorithmes:
            self.algo_menu.add_radiobutton(label=algo, variable=self.selected_algo, value=algo, command=self.update_selected_algo)

    def update_selected_algo(self):
        if self.selected_algo.get() == "Algorithme Simple":
            self.algorithme_ia = self.algorithme_simple
        elif self.selected_algo.get() == "Algorithme Sophistiqué":
            self.algorithme_ia = self.algorithme_sophistique
        elif self.selected_algo.get() == "Algorithme Minimax":
            self.algorithme_ia = self.algorithme_minimax
        
        self.demarrer_jeu_contre_ia()


    # Méthode pour initialiser le plateau de jeu
    def init_grille(self):
        self.Canvas = tk.Canvas(self.root, width=self.colonnes * 100, height=self.lignes * 100, bg='#add8e6')
        self.Canvas.pack()

        self.mode_jeu_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.mode_jeu_label.pack()
        
        self.dessin_jeu()
    
    # pour unittest
    def afficher_grille(self, grille):
        for row in grille:
            print(" ".join(row))

    # Méthode pour dessiner le plateau de jeu
    def dessin_jeu(self):
        for ligne in range(self.lignes):
            for col in range(self.colonnes):
                x1 = col * 100
                y1 = ligne * 100
                x2 = x1 + 100
                y2 = y1 + 100

                self.Canvas.create_oval(x1, y1, x2, y2, outline='#add8e6', fill='white', width=2)

        self.Canvas.bind("<Button-1>", self.detection_clic)

    # Méthode pour initialiser le bouton de réinitialisation
    def bouton_vider(self):
        reset_button = tk.Button(self.root, text="Vider", command=self.vider_init)
        reset_button.pack()

    def vider_init(self):
        self.jeu_reset()
        self.demarrer_jeu(False)

    # Méthode appelée lorsqu'un clic est effectué sur le plateau de jeu
    def detection_clic(self, event):
        col = event.x // 100
        self.placer_jeton(col)

    # Méthode pour placer un jeton dans la colonne spécifiée
    def placer_jeton(self, col):
        for ligne in range(self.lignes - 1, -1, -1):
            if self.grille[ligne][col] == '':
                self.grille[ligne][col] = self.joueur_actuel()
                self.jeton(ligne, col)
                if self.verif_gagnant(ligne, col):
                    self.affiche_gagnant()
                    self.jeu_reset()
                    self.demarrer_jeu(False)
                else:
                    self.joueur_suivant()
                    if self.joueur_actuel() == 'IA':
                        self.joueur_ia()
                break

    # Méthode pour dessiner un jeton sur le plateau de jeu
    def jeton(self, ligne, col):
        x1 = col * 100 + 10
        y1 = ligne * 100 + 10
        x2 = x1 + 80
        y2 = y1 + 80

        color = 'red' if self.joueur_actuel() == self.joueurs[0] else 'yellow'
        self.Canvas.create_oval(x1, y1, x2, y2, outline=color, fill=color)

    # Méthode pour permettre à l'IA de jouer
    def joueur_ia(self):
        available_colonnes = [col for col in range(self.colonnes) if self.grille[0][col] == '']
        if available_colonnes:
            col = self.algorithme_ia(available_colonnes)
            self.placer_jeton(col)

    # Méthode pour vérifier s'il y a un gagnant après chaque coup
    def verif_gagnant(self, ligne, col):
        # Vérification horizontale
        if self.verif_ligne(ligne, col, 0, 1) or self.verif_ligne(ligne, col, 0, -1):
            return True

        # Vérification verticale
        if self.verif_ligne(ligne, col, 1, 0):
            return True

        # Vérification diagonale (/)
        if self.verif_ligne(ligne, col, -1, 1) or self.verif_ligne(ligne, col, 1, -1):
            return True

        # Vérification diagonale (\)
        if self.verif_ligne(ligne, col, -1, -1) or self.verif_ligne(ligne, col, 1, 1):
            return True

        return False

    # Méthode pour vérifier une ligne dans une direction spécifique
    def verif_ligne(self, ligne, col, ligne_modif, col_modif):
        count = 1
        player = self.joueur_actuel()

        # Vérification dans une direction
        for i in range(1, 4):
            new_ligne = ligne + i * ligne_modif
            new_col = col + i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and self.grille[new_ligne][new_col] == player:
                count += 1
            else:
                break

        # Vérification dans l'autre direction
        for i in range(1, 4):
            new_ligne = ligne - i * ligne_modif
            new_col = col - i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and self.grille[new_ligne][new_col] == player:
                count += 1
            else:
                break

        return count >= 4

    # Méthode pour afficher le gagnant de la partie
    def affiche_gagnant(self):
        nom_gagnant = self.joueurs[0] if self.joueur_actuel_indice == 0 else self.joueurs[1]
        messagebox.showinfo("Gagnant", f"{nom_gagnant} a gagné !")

    # Méthode pour réinitialiser le jeu
    def jeu_reset(self):
        self.joueur_actuel_indice = 0
        self.joueurs = ['', '']
        self.grille = [['' for _ in range(self.colonnes)] for _ in range(self.lignes)]
        self.Canvas.delete("all")
        self.dessin_jeu()

    # Méthode pour passer au joueur suivant
    def joueur_suivant(self):
        self.joueur_actuel_indice = 1 - self.joueur_actuel_indice

    # Méthode pour obtenir le nom du joueur actuel
    def joueur_actuel(self):
        return self.joueurs[self.joueur_actuel_indice]

    # Méthode pour commencer une nouvelle partie avec un ou deux joueurs
    def demarrer_jeu(self, deux_joueurs):
        self.jeu_reset()
        if deux_joueurs:
            self.entrer_noms_joueurs()
            mode_jeu = "Jeu à deux joueurs"
        else:
            self.joueurs = ["Joueur Rouge", "Joueur Jaune"]
            mode_jeu = "Joueur seul"

        self.mode_jeu_label.config(text=mode_jeu)

    # Méthode pour demander les noms des joueurs           
    def entrer_noms_joueurs(self):
        for i in range(2):
            # Mettre la boîte de dialogue en premier plan
            # self.root.focus_force()
            # self.root.grab_set()
            nom_joueur = simpledialog.askstring("Nom du Joueur", f"Entrez le nom du Joueur {i + 1}")

            if nom_joueur:
                self.joueurs[i] = nom_joueur
            else:
                self.joueurs[i] = f"Joueur {i + 1}"

            # Libérer la prise sur la fenêtre
            # self.root.grab_release()


    # Méthode pour commencer une partie contre l'IA
    def demarrer_jeu_contre_ia(self):
        self.jeu_reset()
        mode_jeu = "Jeu contre l'IA"
        self.mode_jeu_label.config(text=mode_jeu)
        self.entrer_noms_joueurs()
        
        self.joueurs[1] = 'IA'  # Définir le deuxième joueur comme l'IA
        if self.joueur_actuel() == 'IA':
            self.joueur_ia()

            
    # Méthode pour afficher les règles du jeu
    def affiche_regles(self):
        regles_text = "Le Puissance 4 est un jeu de stratégie où deux joueurs s'affrontent. Le plateau de jeu est une grille de 6 lignes sur 7 colonnes.\n\nLe but du jeu est d'aligner 4 jetons de sa couleur horizontalement, verticalement ou en diagonale avant l'adversaire.\n\nChaque joueur joue à tour de rôle en plaçant un jeton dans une colonne. Le jeton tombe alors en bas de la colonne.\n\nLe premier joueur à aligner 4 jetons de sa couleur remporte la partie."

        messagebox.showinfo("Règles du jeu", regles_text)

    # Méthode pour afficher les instructions sur la façon de jouer
    def affiche_insctructions(self):
        insctructions_text = "Cliquez sur une colonne pour placer votre jeton dans cette colonne. Les jetons tombent en bas de la colonne.\n\nL'objectif est d'aligner 4 jetons de votre couleur horizontalement, verticalement ou en diagonale avant votre adversaire.\n\nLe joueur 1 commence toujours la partie, et les joueurs alternent les tours."

        messagebox.showinfo("Comment jouer", insctructions_text)
    
    
    ##################################################################
    # Algorithme simple :
    # Choix d'une colonne aléatoire
    ##################################################################
    # Debut
    def algorithme_simple(self, available_colonnes):
        return random.choice(available_colonnes)
    # Fin

    #################################################################
    # Algorithme sophistiqué
    #################################################################
    # Debut
    def algorithme_sophistique(self, available_colonnes):
        for col in available_colonnes:
            # Tester si en jouant dans cette colonne, le joueur actuel gagnera
            copie_grille = [ligne.copy() for ligne in self.grille]
            self.simuler_coup(col, copie_grille, self.joueur_actuel())
            if self.check_victoire_simulee(copie_grille, self.joueur_actuel()):
                return col

        for col in available_colonnes:
            # Tester si en jouant dans cette colonne, l'adversaire gagnera
            copie_grille = [ligne.copy() for ligne in self.grille]
            adversaire = self.joueurs[1] if self.joueur_actuel() == self.joueurs[0] else self.joueurs[0]
            self.simuler_coup(col, copie_grille, adversaire)
            if self.check_victoire_simulee(copie_grille, adversaire):
                return col

        # Aucune menace détectée, jouer dans une colonne aléatoire
        return random.choice(available_colonnes)

    def simuler_coup(self, col, copie_grille, joueur):
        for ligne in range(self.lignes - 1, -1, -1):
            if copie_grille[ligne][col] == '':
                copie_grille[ligne][col] = joueur
                break

    def check_victoire_simulee(self, copie_grille, joueur):
        for ligne in range(self.lignes):
            for col in range(self.colonnes):
                if copie_grille[ligne][col] == joueur:
                    if self.check_victoire_simulee_direction(copie_grille, ligne, col, 0, 1):
                        return True
                    if self.check_victoire_simulee_direction(copie_grille, ligne, col, 1, 0):
                        return True
                    if self.check_victoire_simulee_direction(copie_grille, ligne, col, -1, 1):
                        return True
                    if self.check_victoire_simulee_direction(copie_grille, ligne, col, 1, -1):
                        return True
        return False

    def check_victoire_simulee_direction(self, copie_grille, ligne, col, ligne_modif, col_modif):
        count = 1
        joueur = copie_grille[ligne][col]

        for i in range(1, 4):
            new_ligne = ligne + i * ligne_modif
            new_col = col + i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and copie_grille[new_ligne][new_col] == joueur:
                count += 1
            else:
                break

        for i in range(1, 4):
            new_ligne = ligne - i * ligne_modif
            new_col = col - i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and copie_grille[new_ligne][new_col] == joueur:
                count += 1
            else:
                break

        return count >= 4
    # Fin

    ###################################################
    # Algorithme Minimax
    ###################################################
    # Debut

    def algorithme_minimax(self, available_colonnes):
        # Appel de la fonction Minimax pour trouver la meilleure colonne
        _, best_col = self.minimax(self.grille, self.profondeur_minimax, True)

        return best_col

    def minimax(self, grille, profondeur, joueur_maximisant):
        score = self.evaluer_grille(grille)

        if profondeur == 0 or score == 100 or score == -100:
            return score, None

        if joueur_maximisant:
            max_eval = float('-inf')
            best_col = None

            for col in range(self.colonnes):
                if grille[0][col] == '':
                    copie_grille = [ligne.copy() for ligne in grille]
                    self.simuler_coup(col, copie_grille, self.joueur_actuel())
                    eval, _ = self.minimax(copie_grille, profondeur - 1, False)

                    if eval > max_eval:
                        max_eval = eval
                        best_col = col

            return max_eval, best_col

        else:
            min_eval = float('inf')
            best_col = None

            for col in range(self.colonnes):
                if grille[0][col] == '':
                    copie_grille = [ligne.copy() for ligne in grille]
                    self.simuler_coup(col, copie_grille, self.joueurs[1] if self.joueur_actuel() == self.joueurs[0] else self.joueurs[0])
                    eval, _ = self.minimax(copie_grille, profondeur - 1, True)

                    if eval < min_eval:
                        min_eval = eval
                        best_col = col

            return min_eval, best_col

    def evaluer_grille(self, grille):
        if self.verif_gagnant_simulee(grille, self.joueur_actuel()):
            return 100
        elif self.verif_gagnant_simulee(grille, self.joueurs[1] if self.joueur_actuel() == self.joueurs[0] else self.joueurs[0]):
            return -100
        else:
            return 0

    def verif_gagnant_simulee(self, grille, joueur):
        for ligne in range(self.lignes):
            for col in range(self.colonnes):
                if grille[ligne][col] == joueur:
                    if self.check_victoire_simulee_direction(grille, ligne, col, 0, 1):
                        return True
                    if self.check_victoire_simulee_direction(grille, ligne, col, 1, 0):
                        return True
                    if self.check_victoire_simulee_direction(grille, ligne, col, -1, 1):
                        return True
                    if self.check_victoire_simulee_direction(grille, ligne, col, 1, -1):
                        return True
        return False

    def check_victoire_simulee_direction(self, grille, ligne, col, ligne_modif, col_modif):
        count = 1
        joueur = grille[ligne][col]

        for i in range(1, 4):
            new_ligne = ligne + i * ligne_modif
            new_col = col + i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and grille[new_ligne][new_col] == joueur:
                count += 1
            else:
                break

        for i in range(1, 4):
            new_ligne = ligne - i * ligne_modif
            new_col = col - i * col_modif

            if 0 <= new_ligne < self.lignes and 0 <= new_col < self.colonnes and grille[new_ligne][new_col] == joueur:
                count += 1
            else:
                break

        return count >= 4
    
    # Fin


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Puissance4(root)
    root.mainloop()

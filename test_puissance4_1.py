# Tests pour l'interface graphiquejeu_menu
# exécuter les tests à l'aide de la commande py -3 -m unittest test_puissance4_1.py

import unittest
from unittest.mock import patch
from puissance4 import Puissance4
import tkinter as tk

class TkinterTestCase(unittest.TestCase):
    def test_minimax(self):
        root = tk.Tk()  # Créer une instance de Tk
        game = Puissance4(root)
        available_cols = [0, 1, 2, 3, 4, 5, 6]
        col = game.algorithme_minimax(available_cols)
        self.assertIn(col, available_cols)

    def test_algorithme_simple(self):
        root = tk.Tk()  # Créer une instance de Tk
        game = Puissance4(root)
        available_cols = [0, 1, 2, 3, 4, 5, 6]
        col = game.algorithme_simple(available_cols)
        self.assertIn(col, available_cols)

    def test_algorithme_sophistique(self):
        root = tk.Tk()  # Créer une instance de Tk
        game = Puissance4(root)
        available_cols = [0, 1, 2, 3, 4, 5, 6]
        col = game.algorithme_sophistique(available_cols)
        self.assertIn(col, available_cols)

    def test_entrer_noms_joueurs(self):
        # Créer une instance factice de tk.Tk
        root = tk.Tk()

        # Créer une instance de Puissance4 avec la racine factice
        game = Puissance4(root)

        # Définir la sortie attendue de la boîte de dialogue
        with patch("tkinter.simpledialog.askstring", return_value="Nom du Joueur 1"):
            game.entrer_noms_joueurs()
            self.assertEqual(game.joueurs[0], "Nom du Joueur 1")

        with patch("tkinter.simpledialog.askstring", return_value="Nom du Joueur 2"):
            game.entrer_noms_joueurs()
            self.assertEqual(game.joueurs[1], "Nom du Joueur 2")

if __name__ == '__main__':
    unittest.main()

# Tests pour l'algorithme Minimax
# exécuter les tests à l'aide de la commande py -3 -m unittest test_puissance4_2.py

import unittest
from puissance4 import Puissance4

class TestPuissance4(unittest.TestCase):
    def setUp(self):
        # Initialisation pour les tests
        self.puissance4 = Puissance4.init_with_config({'root': None})

    def test_minimax(self):
        # Test avec une grille vide, le résultat doit être une colonne aléatoire
        grille_vide = [['' for _ in range(self.puissance4.colonnes)] for _ in range(self.puissance4.lignes)]
        _, best_col_vide = self.puissance4.minimax(grille_vide, self.puissance4.profondeur_minimax, True)
        self.assertIn(best_col_vide, range(self.puissance4.colonnes))

        # Test avec une grille gagnante pour le joueur actuel
        grille_gagnante = [
            ['X', 'O', 'X', 'O', '', '', ''],
            ['O', 'X', 'X', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '']
        ]
        _, best_col_gagnante = self.puissance4.minimax(grille_gagnante, self.puissance4.profondeur_minimax, True)
        self.assertEqual(best_col_gagnante, 4)  # Colonne gagnante

        # Test avec une grille où l'adversaire a déjà gagné, l'algorithme ne doit pas choisir la colonne gagnante
        grille_adversaire_gagnant = [
            ['O', 'X', 'O', 'X', '', '', ''],
            ['X', 'O', 'O', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '']
        ]
        _, best_col_adversaire_gagnant = self.puissance4.minimax(grille_adversaire_gagnant, self.puissance4.profondeur_minimax, True)
        self.assertNotEqual(best_col_adversaire_gagnant, 3)  # Colonne gagnante

if __name__ == '__main__':
    unittest.main()


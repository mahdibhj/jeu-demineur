"""
Module contenant la description de la classe Partie qui permet de jouer une partie du jeu démineur.
Dois être démarré en appelant la méthode jouer(). Cette classe contient les informations sur une
partie et utilise un objet tableau_mines (une instance de la classe Tableau).
"""

from tableau import Tableau


class Partie:
    """
    Contient les informations sur une partie du jeu Démineur, qui se jouera avec
    un tableau de mines. Des méthodes sont disponibles pour faire avancer la partie
    et interagir avec l'utilisateur.

    Attributes:
        tableau_mines (Tableau): Le tableau de cases où les mines sont cachées avec lequel se
                déroule la partie.
        partie_terminee (bool): True lorsque l'utilisateur a terminé de jouer la partie (victoire ou défaite)
    """

    def __init__(self):
        """
        Initialisation de la Partie.

        Note: L'instance de la classe Tableau, qui sera manipulée par les méthodes de la classe,
              sera initialisée lors de l'appel de la méthode Partie.jouer().
        """
        self.tableau_mines = None
        self.partie_terminee = False


    def jouer(self):
        """
        Tant que la partie n'est pas terminée, on joue un tour de la partie.
        Une fois la partie terminée, on affiche le tableau de cases complètement dévoilée
        et on indique un message sur l'issue de la partie (victoire ou défaite).
        Il s'agit d'une victoire si le tableau ne contient plus de cases à dévoiler.
        """
        x = int(input("veuillez entrer le nombre de colonnes: "))

        y = int(input("veuillez entrer le nombre de lignes: "))

        z = int(input("veuillez entrer le nombre de mines: "))

        self.tableau_mines = Tableau(x,y,z)

        compteur_tours = 0
        while not self.partie_terminee and not self.tableau_mines.nombre_cases_a_devoiler() == z :
            compteur_tours += 1
            print(f'\n===> Tour #{compteur_tours} <===')
            self.tableau_mines.afficher_tableau()
            self.tour()

        if self.tableau_mines.contient_cases_sans_mines_a_devoiler():
            self.tableau_mines.afficher_solution()
            print("Game Over, you lost")
        elif self.tableau_mines.nombre_cases_a_devoiler() == z:
            self.tableau_mines.afficher_solution()
            print("Congratulations! you won!")
        else:
            ("weird ending, check code")

    def tour(self):
        """
        Jouer un tour, c'est-à-dire:

        À chaque tour:
            - On demande à l'utilisateur les coordonnées d'une case à dévoiler
            - On effectue le dévoilement en cascade en démarrant à cette case
            - On détecte si une mine a été actionnée,
              auquel cas affecte True à l'attribut self.partie_terminee.
            - On détecte si toutes les cases ont été dévoilées,
              auquel cas affecte True à l'attribut self.partie_terminee.
        """
        x, y = self.demander_coordonnees_case_a_devoiler()

        if self.tableau_mines.contient_mine(x, y):
            self.partie_terminee = True
        case = self.tableau_mines.obtenir_case(x, y)
        self.tableau_mines.devoilement_en_cascade(x, y)


    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Méthode qui valide les coordonnées reçues en paramètres.
        Les coordonnées doivent:
            1) être des caractères numériques;
            2) être à l'intérieur des valeurs possibles des rangées et des colonnes
                du tableau; et
            3) correspondre à une case qui n'a pas encore été dévoilée.

        Args:
            rangee_x (str):     Chaîne de caractères contenant la rangée
            colonne_y (str):    Chaîne de caractères contenant  la colonne

        Returns:
            bool : True si les coordonnées sont valides, False autrement.
        """
        # TO DO: À programmer.
        if type(rangee_x) is int and type(colonne_y) is int and self.tableau_mines.valider_coordonnees_a_devoiler(rangee_x, colonne_y):
            print('x,y ok')
            return True
        else:
            return False

    def demander_coordonnees_case_a_devoiler(self):
        """
        Méthode qui demande à l'utilisateur d'entrer la coordonnée de la case qu'il veut dévoiler.
        Cette coordonnée comporte un numéro de rangée et un numéro de colonne.
        Tant que les coordonnées ne sont pas valides, on redemande de nouvelles coordonnées.
        Une fois les coordonnées validées, on retourne les deux numéros sous forme d'entiers.

        Returns:
            int: Numéro de la rangée
            int: Numéro de la colonne

        """
        # TO DO: À programmer.
        xy_valid = False
        while xy_valid == False:
            x = int(input("veuillez entrer le num de ligne: "))
            y = int(input("veuillez entrer le num de colonne: "))
            xy_valid = self.valider_coordonnees(x,y)
        return x,y

from case import Case
from random import randint

class Tableau:



    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=5):
      
        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):        
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne
        return rangee_valide and colonne_valide

    def obtenir_case(self, rangee_x, colonne_y):
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None

        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1))

        liste_coordonnees_cases_voisines = []
        # TO DO
        for coords in voisinage :
            voisin_coords = list(tuple(map(lambda i, j: i + j, (rangee_x, colonne_y), coords)))
            if self.valider_coordonnees(voisin_coords[0],voisin_coords[1]):
                liste_coordonnees_cases_voisines.append( tuple(map(lambda i, j: i + j, (rangee_x, colonne_y), coords)) )
        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        for rangee_x in range(1, self.dimension_rangee + 1):
            for colonne_y in range(1, self.dimension_colonne + 1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()

        coordonnees_mines = []
        i=0
        #print(self.dictionnaire_cases)
        while i < self.nombre_mines:
            x_coord = randint(1, self.dimension_rangee)
            y_coord = randint(1, self.dimension_colonne)
            mine_coords = (x_coord,y_coord)
            mine_case = self.dictionnaire_cases[(x_coord, y_coord)]
            if mine_coords not in coordonnees_mines:
                i+=1
                mine_case.ajouter_mine()
                coordonnees_mines.append(mine_coords)
                mine_voisins = self.obtenir_voisins(x_coord,y_coord)
                for voisin_coords in  mine_voisins:
                    voisin_case = self.dictionnaire_cases[voisin_coords]
                    voisin_case.ajouter_une_mine_voisine()
            else:
                pass


    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):


        if self.valider_coordonnees(rangee_x, colonne_y):
            case_element = self.dictionnaire_cases[rangee_x, colonne_y]
            if case_element.est_devoilee == False:
                return True
            else:
                return False


    def afficher_solution(self):
        self.tout_devoiler()
        self.afficher_tableau()

    def tout_devoiler(self):
        """
        Méthode qui dévoile toutes les cases du tableau
        """
        for case in self.dictionnaire_cases:
            self.devoiler_case(self.obtenir_case(case[0], case[1]))
            #case.devoiler() = True

    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu des cases dévoilées
        (mine ou nombre de mines voisines) ou un point pour les cases non dévoilées.

        Vous pouvez vous inspirer de la méthode afficher_solution
        """
        print()  # Retour de ligne

        for rangee_x in range(0, self.dimension_rangee + 1):

            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne + 1):
                if rangee_x == 0 and colonne_y == 0:
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |'
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y % 10}'
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|'
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)
                    car = case_xy.obtenir_apparence()

                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")

            # À la fin de chaque ligne
            print()  # Retour de ligne
            if rangee_x == 0:  # Ligne horizontale de l'en-tête
                print('--+-' + '--' * self.dimension_colonne)

    def nombre_cases_a_devoiler(self):
        nombre_cases = 0
        for coords in self.dictionnaire_cases:
            case = self.obtenir_case(coords[0], coords[1])
            if case.est_devoilee == False:
                nombre_cases += 1
        return nombre_cases
    def contient_cases_sans_mines_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases sans mines à dévoiler.

        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """
        cases_a_devoiler = False
        for coords in self.dictionnaire_cases:
            case = self.obtenir_case(coords[0], coords[1])
            if case.est_minee == False and case.est_devoilee == False:
                cases_a_devoiler = True
        return cases_a_devoiler

    def devoilement_en_cascade(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile la case aux coordonnées en argument (utilisez  la méthode
        devoiler_case du tableau), et qui, si elle est vide, appelle le dévoilement
        en cascade pour chacun de ses voisins, lorsque ceux-ci ne soient pas déjà dévoilés

        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler

        Returns:

        """
        # PARTIE 1, on obtient et dévoile la case
        case = self.obtenir_case(rangee_x, colonne_y)
        self.devoiler_case(case)

        # PARTIE 2, on dévoile les voisins

        if case.nombre_mines_voisines == 0 and case.est_minee == False:
            cases_voisins = self.obtenir_voisins(rangee_x, colonne_y)


            for coords_voisin in cases_voisins :
                case_voisin = self.obtenir_case(coords_voisin[0], coords_voisin[1])
                #print('ABC')

                #print(cases_voisins)
                if case_voisin.nombre_mines_voisines == 0 and not case_voisin.est_devoilee:
                    for new_case in self.obtenir_voisins(coords_voisin[0], coords_voisin[1]):
                        cases_voisins.append(new_case)
                self.devoiler_case(case_voisin)





    def devoiler_case(self, case):
        """
        Méthode qui dévoile le contenu de la case reçue en argument.
        Si la case ne contient pas de mine, on décrémente l'attribut qui représente le nombre de
        cases sans mine à dévoiler.

        Args:
            case (Case) : La case à dévoiler
        """
        # TO DO: À compléter
        case.est_devoilee = True
        if self.nombre_cases_sans_mine_a_devoiler > 0:
            self.nombre_cases_sans_mine_a_devoiler -= 1
        pass

    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine

        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """
        # TO DO: À compléter
        case = self.obtenir_case(rangee_x, colonne_y)
        if case.est_minee :
            return True
        else :
            return False


#### Tests unitaires ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_sans_mines_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
           tableau_test.dimension_rangee - tableau_test.nombre_mines


def test_valider_coordonnees():
    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x + 1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y + 1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)


def test_obtenir_case():
    tableau_test = Tableau()
    case1 = tableau_test.obtenir_case(3, 3)
    assert case1 == tableau_test.obtenir_case(3, 3)
    assert case1 != tableau_test.obtenir_case(3, 4)
    assert tableau_test.obtenir_case(10, 10) is None


def test_valider_coordonnees_a_devoiler():
    tableau_test = Tableau()
    assert tableau_test.valider_coordonnees_a_devoiler(3, 3)
    tableau_test.obtenir_case(3, 3).devoiler()
    assert not tableau_test.valider_coordonnees_a_devoiler(3, 3)
    assert not tableau_test.valider_coordonnees_a_devoiler(10, 10)


def test_obtenir_voisins():
    tableau_test = Tableau()
    voisins = tableau_test.obtenir_voisins(3, 3)
    voisins_attendus = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]
    for i in range(len(voisins_attendus)):
        assert voisins[i] in voisins_attendus
        assert voisins_attendus[i] in voisins
    assert len(tableau_test.obtenir_voisins(3, 3)) == 8
    assert len(tableau_test.obtenir_voisins(1, 1)) == 3
    assert len(tableau_test.obtenir_voisins(5, 5)) == 3


def test_devoiler_case():
    tableau_test_1 = Tableau(5, 5, 0)
    n_mines = tableau_test_1.nombre_cases_sans_mine_a_devoiler
    case = tableau_test_1.obtenir_case(3, 3)
    assert not case.est_devoilee
    tableau_test_1.devoiler_case(case)
    assert case.est_devoilee
    assert tableau_test_1.nombre_cases_sans_mine_a_devoiler == n_mines - 1

    tableau_test_2 = Tableau(5, 5, 25)
    n_mines = tableau_test_2.nombre_cases_sans_mine_a_devoiler
    case = tableau_test_2.obtenir_case(3, 3)
    tableau_test_2.devoiler_case(case)
    assert tableau_test_2.nombre_cases_sans_mine_a_devoiler == n_mines



def test_case_contient_mine():
    tableau_test_1 = Tableau(5, 5, 25)
    assert tableau_test_1.contient_mine(3, 3)
    tableau_test_2 = Tableau(5, 5, 0)
    assert not tableau_test_2.contient_mine(3, 3)


def test_contient_cases_a_devoiler():
    tableau_test = Tableau(5, 5, 25)
    assert not tableau_test.contient_cases_sans_mines_a_devoiler()
    tableau_test = Tableau(5, 5, 24)
    assert tableau_test.contient_cases_sans_mines_a_devoiler()


if __name__ == '__main__':
    tableau_test = Tableau()
    print('\nTABLEAU:')
    tableau_test.afficher_tableau()
    print('\nSOLUTION:')
    tableau_test.afficher_solution()

    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_case()
    test_valider_coordonnees_a_devoiler()
    test_obtenir_voisins()
    test_devoiler_case()
    test_case_contient_mine()
    test_contient_cases_a_devoiler()
    print('Tests réussis!')


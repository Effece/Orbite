"""

/// ORBITE \\\

Prérequis :
 - tkinter               (*)
 - tkinter.colorchooser  (*)
 - tkinter.scrolledtext  (*)
 - time                  (sleep)
 - math                  (sin, cos)
 - traceback (optionnel) (*)

Modules intérieurs :
 - point
 - orbfuncs

Fonctionnement :
Chaque point est défini d'après un très large ensemble d'arguments, principalement parent, dif_x, dif_y, orbite et t_orbite.
  dif_x    : distance x au parent
  dif_y    : distance y au parent
  orbite   : fonction de déplacement du point (cercle, carre, lambda...)
  t_orbite : taille de l'orbite
Avec ces arguments, le point se déplace, d'après sa propre et celle de son parent. Dans le programme, chaque point qui bouge fait bouger l'ensemble
de ses enfants avec lui, des mêmes valeurs.

Créer une fonction orbite :
Une fonction orbite doit renvoyer un tuple (x, y) où x et y représentent les distances x et y à parcourir.

Attributs utiles pour une fonction orbite (d'un point) :
 - t_orbite      : taille de l'orbite                                                                      | int
 - x, y          : coordonnées actuelles sur le Canvas                                                     | int
 - or_x, or_y    : coordonnées sur l'orbite                                                                | int
 - o_x, o_y      : coordonnées d'origine, au lancement du programme                                        | int
 - parent        : point centre d'orbite (possède les mêmes attributs)                                     | <point>
 - child         : liste des enfants                                                                       | list
 - angle         : degré d'orientation actuel (à mettre à jour dans la fonction)                           | int
 - min_angle     : angle minimal                                                                           | int
 - max_angle     : angle maximal                                                                           | int
 - rotation_sens : sens de rotation                                                                        | str
 - inv_rotation  : indique si le sens de rotation doit changer après un tour complet / une limite atteinte | int
 - speed         : vitesse

Affichage d'execution :
 - win   : fenêtre de la simulation
 > can   : canvas de la simulation
 - panel : gestionnaire des attributs principaux des points
           inclut une ligne de commande
 > infos : groupe nommé des attributs et des changements pour un point
 > term  : entrée de texte executable
 - shell : console avec historique d'execution de code pendant la simulation
 > term  : entrée de texte executable
 > hist  : historique des commandes

Classes :
 - new_win     : fenêtre de la simulation
 - new_can     : canvas de la simulation
 - new_panel   : gestionnaire des attributs principaux des points
 - new_shell   : console avec historique d'execution de code pendant la simulation
 - point       : point se déplaçant dans le canvas
 > fake_parent : faux parent avec attributs d'un point ; permet d'initialiser un point immobile
 > infos_panel : groupe nommé des attributs et des changements pour un point
 - create      : fenêtre de création d'un point

Utilisation du panel :
Le panel contient l'ensemble des informations sur les points, regroupées dans un LabelFrame, nommé d'après la couleur du point.
Le parent est référencé, d'après sa couleur.
En-dessous, un tableau contient l'ensemble des coordonnées utiles du point, soit celles d'origine, les actuels et celles sur orbite, en x et y.
Quelques widgets permettent de gérer la trainée : son activation, sa taille. Un bouton permet de la détruire.
La vitesse du point est changeable avec un Scale.
Afin de répartir convenablement les points, les LabelFrames peuvent être repositionnés (en row et column).

Creation d'un point :
La création d'un point peut se faire par la commande 'create()' ou par le menu de la fenêtre de simulation. Chaque élément doit être rempli pour
créer le point sans erreur.
Un point ne doit pas avoir le même nom qu'une variable déjà existante.

"""

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### MODULES ###

from point import *
from orbfuncs import *

#####

import tkinter as tk
import tkinter.colorchooser
import tkinter.scrolledtext

from time import sleep

import traceback

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### FENETRE DE LA SIMULATION ###

class new_win(tk.Tk):
    """Fenêtre de la simulation"""

    def __init__(self, title = 'Simulation'):
        """
        In :
          title : titre de la fenêtre
          < str
          > 'Simulation'
        """

        tk.Tk.__init__(self)
        self.title(title)

        self.menu = tk.Menu(self)
        self.submenu = tk.Menu(self.menu, tearoff = False)
        self.submenu.add_command(label = 'Pause', command = lambda event = None: exec('global end; end = not end'))
        self.submenu.add_command(label = 'Créer un point', command = lambda event = None: create())
        self.menu.add_cascade(label = 'Commandes', menu = self.submenu)
        self.config(menu = self.menu)

        return

win = new_win()

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CANVAS DE LA SIMULATION ###

class new_can(tk.Canvas):
    """Canvas de la simulation"""

    def __init__(self, master = win):
        """
        In :
          master : fenêtre du canvas
          < <tk.Tk>
          > win
        """

        self.master = master

        self.width, self.height = 800, 600
        self.bg = 'black'
        
        tk.Canvas.__init__(self, master, width = self.width, height = self.height, bg = self.bg)
        self.grid()

        return

can = new_can()

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### GESTIONNAIRE ###

class new_panel(tk.Tk):
    """
    Gestionnaire des attributs principaux des points
    Inclut une ligne de commande
    """

    def __init__(self, title = 'Panel'):
        """
        In :
          title : titre de la fenêtre
          < str
          > 'Panel'
        """

        tk.Tk.__init__(self)
        self.title(title)

        self.terminal = tk.Entry(self, text = 'Terminal', width = 40)
        self.terminal.grid(row = 0, column = 0, sticky = 'w')
        self.terminal.bind('<Return>', self.execute)

        return

    def execute(self, event = None):
        """Execute le code entré dans le terminal"""
        """
        In :
          event : objet tkinter
          < <tk.event>
          > None
        """

        try:
            
            exec(self.terminal.get())
            
        except Exception:
            pass

        return

panel = new_panel()

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CONSOLE ###

class new_shell(tk.Tk):
    """Console avec historique d'execution de code pendant la simulation"""

    def __init__(self, title = 'Shell'):
        """
        In :
          title : titre de la fenêtre
          < str
          > 'Shell'
        """

        tk.Tk.__init__(self)
        self.title(title)

        self.write_space = tk.Frame(self)

        self.terminal = tk.Entry(self.write_space, width = 90, font = 'TkFixedFont')
        self.exec_b = tk.Button(self.write_space, text = 'Executer', command = self.execute, width = 10)

        self.terminal.bind('<Return>', self.execute)

        self.terminal.grid(row = 0, column = 0, sticky = 'w')
        self.exec_b.grid(row = 0, column = 1, sticky = 'w')

        self.history = tk.Frame(self, width = 100)
        self.hists = []
        self.hists_l = []

        self.write_space.grid(row = 0, column = 0, sticky = 'w')
        self.history.grid(row = 2, column = 0, sticky = 'w')

        return

    def execute(self, event = None):
        """
        Execute le code entré dans le terminal
        Affiche un historique des entrées ainsi que les erreurs ou les réponses
        """
        """
        In :
          event : objet tkinter
          < <tk.event>
          > None
        """

        t = self.terminal.get()

        self.terminal.delete(0, tk.END)

        self.hists.append(t)

        lab = tk.Label(self.history, text = f'>>> {t}', font = 'TkFixedFont')
        lab.grid(sticky = 'w')
        self.hists_l.append(lab)

        try:

            exec(t)

        except Exception as e:

            lab = tk.Label(self.history, text = f'{e.__class__.__name__}: {e}', fg = 'red', font = 'TkFixedFont')
            lab.grid(sticky = 'w')
            self.hists_l.append(lab)
            print(traceback.format_exc())

        return

shell = new_shell()

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATEUR DE POINT ###

class create(tk.Tk):
    """Fenêtre temporaire de création d'un point"""

    def __init__(self):

        tk.Tk.__init__(self)
        self.title('Point creator')

        self.c1 = tk.Frame(self, width = 40)
        self.c2 = tk.Frame(self, width = 40)

        self.f1 = tk.LabelFrame(self.c1, text = 'Repérage')
        self.f2 = tk.LabelFrame(self.c1, text = 'Positionnement')
        self.f3 = tk.LabelFrame(self.c2, text = 'Orbite')
        self.f4 = tk.LabelFrame(self.c2, text = 'Rotation et orientation')

        ##### F1

        self.parent_V = tk.StringVar(self)
        self.name_V = tk.StringVar(self)

        self.parent_opt = tuple([k.outline for k in point.ALL])

        self.parent_V.set(self.parent_opt[0])
        self.name_V.set('g')

        self.name = tk.Entry(self.f1, textvar = self.name_V)
        self.parent = tk.OptionMenu(self.f1, self.parent_V, *self.parent_opt)
        self.color_f = tk.Frame(self.f1)
        self.width = tk.Scale(self.f1, from_ = 1, to = 10, orient = 'horizontal')

        self.width.set(5)

        self.color_V = tk.StringVar(self)
        self.color_V.set('white')
        
        self.color = tk.Entry(self.color_f, textvar = self.color_V)
        self.colorchooser = tk.Button(self.color_f, text = 'Utliser la palette', command = self.use_colorchooser)

        self.color.grid(row = 0, column = 0, sticky = 'w')
        self.colorchooser.grid(row = 0, column = 1, sticky = 'w')

        tk.Label(self.f1, text = 'Nom de la variable :').grid(row = 0, column = 0, sticky = 'w')
        tk.Label(self.f1, text = 'Parent :').grid(row = 1, column = 0, sticky = 'w')
        tk.Label(self.f1, text = 'Couleur :').grid(row = 2, column = 0, sticky = 'w')
        tk.Label(self.f1, text = 'Epaisseur :').grid(row = 3, column = 0, sticky = 'w')

        self.name.grid(row = 0, column = 1, sticky = 'w')
        self.parent.grid(row = 1, column = 1, sticky = 'w')
        self.color_f.grid(row = 2, column = 1, sticky = 'w')
        self.width.grid(row = 3, column = 1, sticky = 'w')

        ##### F2

        self.dif_x = tk.Scale(self.f2, from_ = 5, to = 250, resolution = 5, orient = 'horizontal')
        self.dif_y = tk.Scale(self.f2, from_ = 5, to = 250, resolution = 5, orient = 'horizontal')
        self.t_orbite = tk.Scale(self.f2, from_ = 5, to = 250, resolution = 5, orient = 'horizontal')

        self.dif_x.set(50)
        self.dif_y.set(50)
        self.t_orbite.set(100)

        tk.Label(self.f2, text = 'Différence x :').grid(row = 0, column = 0, sticky = 'w')
        tk.Label(self.f2, text = 'Différence y :').grid(row = 1, column = 0, sticky = 'w')
        tk.Label(self.f2, text = "Taille d'orbite :").grid(row = 2, column = 0, sticky = 'w')

        self.dif_x.grid(row = 0, column = 1, sticky = 'w')
        self.dif_y.grid(row = 1, column = 1, sticky = 'w')
        self.t_orbite.grid(row = 2, column = 1, sticky = 'w')

        ##### F3

        self.orbite_V = tk.StringVar(self)
        self.def_orbite = lambda obj: (0, 0)

        self.orbite_opt = ('Fonction complexe', 'Lambda simple', 'cercle', 'carre')

        self.orbite_V.set(self.orbite_opt[2])
        self.def_orbite = eval(self.orbite_V.get())

        self.orbite = tk.OptionMenu(self.f3, self.orbite_V, command = self.analyse_orbite, *self.orbite_opt)
        self.result = tk.Label(self.f3, text = self.orbite_V.get())

        self.orbite.grid(row = 0, column = 0, sticky = 'w')
        self.result.grid(row = 1, column = 0, sticky = 'w')

        ##### F4

        self.angle = tk.Scale(self.f4, from_ = 0, to = 360, orient = 'horizontal')
        self.min_angle = tk.Scale(self.f4, from_ = 0, to = 360, orient = 'horizontal', command = self.adapt_angle)
        self.max_angle = tk.Scale(self.f4, from_ = 0, to = 360, orient = 'horizontal', command = self.adapt_angle)

        self.min_angle.set(0)
        self.max_angle.set(360)
        self.angle.set(0)

        tk.Label(self.f4, text = 'Angle actuel :').grid(row = 0, column = 0, sticky = 'w')
        tk.Label(self.f4, text = 'Angle minimal :').grid(row = 1, column = 0, sticky = 'w')
        tk.Label(self.f4, text = 'Angle maximal :').grid(row = 2, column = 0, sticky = 'w')

        self.angle.grid(row = 0, column = 1, sticky = 'w')
        self.min_angle.grid(row = 1, column = 1, sticky = 'w')
        self.max_angle.grid(row = 2, column = 1, sticky = 'w')

        self.rotation_sens_V = tk.StringVar(self)
        self.inv_rotation_V = tk.BooleanVar(self)

        self.rotation_sens_V.set('right')
        self.inv_rotation_V.set(False)

        self.rotation_sens_f = tk.Frame(self.f4)
        self.inv_rotation = tk.Checkbutton(self.f4, var = self.inv_rotation_V)

        tk.Radiobutton(self.rotation_sens_f, text = 'Droite', var = self.rotation_sens_V, value = 'right').grid(row = 0, column = 0, sticky = 'w')
        tk.Radiobutton(self.rotation_sens_f, text = 'Gauche', var = self.rotation_sens_V, value = 'left').grid(row = 0, column = 1, sticky = 'w')

        tk.Label(self.f4, text = 'Sens de rotation :').grid(row = 3, column = 0, sticky = 'w')
        tk.Label(self.f4, text = 'Inverser la rotation :').grid(row = 4, column = 0, sticky = 'w')

        self.rotation_sens_f.grid(row = 3, column = 1, sticky = 'w')
        self.inv_rotation.grid(row = 4, column = 1, sticky = 'w')

        #####

        self.c1.grid(row = 0, column = 0, sticky = 'nw')
        self.c2.grid(row = 0, column = 1, sticky = 'nw')

        self.f1.grid(row = 0, column = 0, sticky = 'nw')
        self.f2.grid(row = 1, column = 0, sticky = 'nw')
        self.f3.grid(row = 0, column = 0, sticky = 'nw')
        self.f4.grid(row = 1, column = 0, sticky = 'nw')

        tk.Button(self, text = 'Créer le point', command = self.__del__).grid(row = 1, column = 0, sticky = 'w')

        self.end = False

        while not self.end:
            try:
                self.update()
            except Exception:
                try:
                    self.destroy()
                    # win.destroy()
                except Exception:
                    try:
                        pass
                        # win.destroy()
                    except Exception:
                        pass

        return

    def __del__(self):
        """Supprime la fenêtre"""

        parent = self.parent_V.get()
        for k in point.ALL:
            if k.outline == parent:
                parent = k
                break

        try:
            exec(f'global {self.name.get()}')
            exec(f'{self.name_V.get()} = point(can, panel, parent, self.dif_x.get(), self.dif_y.get(), self.def_orbite, self.t_orbite.get(), outline = self.color_V.get(), width = self.width.get(), angle = self.angle.get(), min_angle = self.min_angle.get(), max_angle = self.max_angle.get(), rotation_sens = self.rotation_sens_V.get(), inv_rotation = self.inv_rotation_V.get())')
        except Exception:
            pass

        self.end = True
        self.destroy()

        return

    def use_colorchooser(self):
        """Permet l'utilisation du widget ColorChooser"""

        color = tkinter.colorchooser.askcolor()

        self.color_V.set(color[1])

        return

    def analyse_orbite(self, event = None):
        """Analyse et créer si besoin des fenêtres pour définir la fonction orbite d'un point en création"""

        global comp_end

        comp_end = False

        o = self.orbite_V.get()

        if o in self.orbite_opt[:2]: # complexe

            if o == self.orbite_opt[0]: # fonction complexe

                comp = tk.Tk()
                comp.title('Complexe function')

                tk.Label(comp, text = "Commencer par 'def [nom](obj): [...]' ; conclure par '[...]\\n[nom]' (sans parenthèse)").grid(row = 0, column = 0, sticky = 'w')

                st = tkinter.scrolledtext.ScrolledText(comp)
                st.grid(row = 1, column = 0, sticky = 'w')

                tk.Button(comp, text = 'Continuer', command = lambda: exec('global comp_end; comp_end = True')).grid(row = 2, column = 0, sticky = 'w')

                while not comp_end:
                    try:
                        comp.update()
                    except Exception:
                        try:
                            comp.destroy()
                        except Exception:
                            pass

                try:
                    exec(st.get(1.0, tk.END))
                except Exception:
                    self.def_orbite = lambda obj: (0, 0)
                    # return

                self.def_orbite = eval(st.get(1.0, tk.END).split('\n')[-2])
                self.result.config(text = st.get(1.0, tk.END))

                try:
                    comp.destroy()
                except Exception:
                    pass

            elif o == self.orbite_opt[1]:

                comp = tk.Tk()
                comp.title('Simple lambda')

                tk.Label(comp, text = 'Changement x :').grid(row = 0, column = 0, sticky = 'w')
                tk.Label(comp, text = 'Changement y :').grid(row = 1, column = 0, sticky = 'w')

                x, y = 0, 0

                tk.Button(comp, text = 'Continuer', command = lambda: exec('global comp_end; comp_end = True')).grid(row = 2, column = 0, sticky = 'w')

                change_x = tk.Entry(comp)
                change_y = tk.Entry(comp)

                change_x.grid(row = 0, column = 1, sticky = 'w')
                change_y.grid(row = 1, column = 1, sticky = 'w')

                while not comp_end:
                    try:
                        comp.update()
                    except Exception:
                        try:
                            pass
                            # comp.destroy()
                        except Exception:
                            self.def_orbite = lambda obj: (0, 0)

                x, y = change_x.get(), change_y.get()

                self.def_orbite = lambda obj: (int(x), int(y))
                self.result.config(text = f'lambda obj: ({int(x)}, {int(y)})')

                try:
                    comp.destroy()
                except Exception:
                    pass

        else:

            self.def_orbite = eval(o)
            self.result.config(text = o)

        comp_end = True

        return

    def adapt_angle(self, event = None):
        """Adapte les Scales d'angle pour éviter des incohérrences"""
        """
        In :
          event : objet tkinter
          < <tk.event>
          > None
        """

        min_a = self.min_angle.get()
        max_a = self.max_angle.get()

        self.angle.config(from_ = min_a, to = max_a)
        self.min_angle.config(to = max_a)
        self.max_angle.config(from_ = min_a)

        return

comp_end = True

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DE POINTS ###

a = point(can, panel, None, can.width / 2, can.height / 2, lambda obj: (0, 0), 50, outline = 'yellow')

# b = point(a, 100, 100, carre, 200, tail = False)

# b = point(a, 50, 50, lambda obj: (1, 2), 100)

# c = point(b, 25, 25, carre, 50, tail = True)
# d = point(b, 100, 100, carre, 200)
# e = point(a, 20, 20, carre, 40)

b = point(can, panel, a, -50, -50, cercle, 100, speed = 1, outline = 'blue', tail = False, name = "POINTTT")

# c = point(b, -10, -10, cercle, 20, speed = 13, outline = 'grey', tail = False, tail_size = 2)
# d = point(c, -25, -25, cercle, 50, 4, outline = 'green', tail = True, tail_size = 5, rotation_sens = 'left')

# d = point(a, 50, 50, carre, 100, outline = 'red')

# c = point(a, -50, -50, cercle, 100, speed = 1, outline = 'green')

# b = point(a, 0, 0, cercle, 100, max_angle = 1, min_angle = -1, inv_rotation = True, speed = 5)

# c = point(b, -25, -25, carre, 100, outline = 'blue', tail = True, speed = 5)

# c = point(b, -25, -25, cercle, 50, outline = 'red', tail = True, speed = 5, rotation_sens = 'right', tail_size = 5)
# d = point(b, -25, -25, cercle, 50, outline = 'green', tail = True, speed = 5, rotation_sens = 'left', tail_size = 5)

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### SCRIPT ###

def_end = False
end = True

while not def_end:
    
    try:
        win.update()
        panel.update()
        shell.update()
    except Exception:
        try:
            win.destroy()
            panel.destroy()
            shell.destroy()
            break
        except Exception:
            try:
                panel.destroy()
                shell.destroy()
                break
            except Exception:
                try:
                    shell.destroy()
                except Exception:
                    break

    if end:
        continue

    point.move_all()
    sleep(0.01)

try:
    win.mainloop()
except Exception:
    pass

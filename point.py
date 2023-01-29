import tkinter as tk

"""----------------------------------------------------------------------------------------------------------------------------------------------------"""
### POINT ###

class point:
    """Point se déplaçant dans le canvas"""

    ALL = []

    def __init__(self, can, panel, parent, dif_x, dif_y, orbite, t_orbite, speed = 1, tail = False, outline = 'white', width = 5, tail_size = 1, angle = 0, min_angle = 0, max_angle = 360, rotation_sens = 'right', inv_rotation = False, name = None):
        """
        In :
          can           : canvas du point
          < <tk.Canvas>
          panel         : fenêtre servant de panel
          < <new_panel>
          parent        : point centre d'orbite (possède les mêmes attributs)
          < <point>
          dif_x         : différence x au parent
          < int
          dif_y         : différence y au parent
          < int
          orbite        : fonction de déplacement du point (cercle, carre, lambda...)
          < function
          t_orbite      : taille de l'orbite
          < int
          speed         : vitesse
          < int
          > 1
          tail          : indique si une trainée doit être laissée
          < bool
          > False
          outline       : couleur du point
          < str
          > 'white'
          width         : taille du point
          < int
          > 5
          tail_size     : taille de l'orbite
          < int
          > 1
          angle         : degré d'orientation au lancement (à mettre à jour dans la fonction)
          < int
          > 0
          min_angle     : angle minimal
          < int
          > 0
          max_angle     : angle maximal
          < int
          > 360
          rotation_sens : sens de rotation
          < str
          > 'right'
          inv_rotation  : indique si le sens de rotation doit changer après un tour complet / une limite atteinte
          < bool
          > False
          name          : nom du point
          < str
          > None
        """

        point.ALL.append(self)

        self.can = can
        self.panel = panel

        if parent == None:

            self.parent = point.fake_parent()

            self.x, self.y = dif_x, dif_y
            self.dif_x, self.dif_y = 0, 0
            
        else:
            
            self.parent = parent
            parent.child.append(self)

            self.dif_x, self.dif_y = dif_x, dif_y
            self.x, self.y = self.parent.x - self.dif_x, self.parent.y - self.dif_y

        self.o_x, self.o_y = self.x, self.y

        self.child = []

        self.name = name

        self.outline = outline
        self.width = width
        self.tail, self.tail_size = tail, tail_size
        self.tail_objs = []
        self.view = self.can.create_oval(self.x, self.y, self.x, self.y, width = self.width, outline = self.outline)
        self.name_view = self.can.create_text(self.x - 25, self.y - 25, text = self.name, fill = self.outline)

        self.orbite = orbite
        self.t_orbite = t_orbite
        
        self.or_x, self.or_y = 0, 0
        
        self.angle, self.max_angle, self.min_angle = angle, max_angle, min_angle
        
        self.speed = speed

        self.rotation_sens, self.inv_rotation = rotation_sens, inv_rotation

        self.panel = point.infos_panel(self)

        return

    def move(self, x, y):
        """Déplace un point et ses enfants"""
        """
        In :
          x : distance à parcourir en x
          < int
          y : distance à parcourir en y
          < int
        """

        self.x += x
        self.y += y

        self.panel.x_V.set(int(self.x))
        self.panel.y_V.set(int(self.y))
        self.panel.angle_V.set(int(self.angle))

        self.can.move(self.view, x, y)
        self.can.move(self.name_view, x, y)

        for k in self.child:
            k.move(x, y)

        return

    def move_orbite(self):
        """Déplace un point d'après son orbite"""

        x, y = self.orbite(self)
        self.or_x += x
        self.or_y += y
        self.move(x, y)

        self.panel.or_x_V.set(int(self.or_x))
        self.panel.or_y_V.set(int(self.or_y))

        self.use_tail()

        return

    def move_all(cls):
        """Déplace l'ensemble des points"""

        for k in cls.ALL:
            if k.orbite(k) != (0, 0):
                try:
                    k.move_orbite()
                except tk.TclError:
                    pass
                    # print(traceback.format_exc())
                    # return
        return

    move_all = classmethod(move_all)

    def coords(self, x, y):
        """Déplace un point et ses enfants à des nouvelles coordonnées x et y"""
        """
        In :
          x : nouvelle position x
          < int
          y : nouvelle position y
          < int
        """

        dif_x, dif_y = self.x - x, self.y - y

        for k in self.child:
            k.move(- dif_x, - dif_y)

        self.x, self.y = x, y

        self.panel.x_V.set(int(self.x))
        self.panel.y_V.set(int(self.y))
        
        self.can.coords(self.view, x, y, x, y)
        self.can.coords(self.name_view, x - 25, y - 25)

        self.use_tail()

        return

    def change_parent(self, new_parent):
        """Change le parent d'un point"""
        """
        In :
          new_parent : nouveau parent
          < <point>
        """

        self.parent.child.remove(self)

        self.parent = new_parent
        self.parent.child.append(self)

        return

    def use_tail(self):
        """Vérifie si la trainée est activée et l'applique"""

        if self.tail:
            self.tail_objs.append(self.can.create_oval(self.x, self.y, self.x, self.y, width = self.tail_size, outline = self.outline))

        return

    def destroy_tail(self, fr = 0, to = -1):
        """Détruit une part ou la totalité de la trainée"""
        """
        In :
          fr : début la part à détruire
          < int
          > 0
          to : fin de la part à détruire
          < int
          > -1
        """

        try:
            
            for k in self.tail_objs[fr : to]:
                self.can.delete(k)
            self.can.delete(self.tail_objs[to])

            del self.tail_objs[fr : to]
            del self.tail_objs[to]
                
        except IndexError:
            pass

        return

    class fake_parent:
        """faux parent avec attributs d'un point ; permet d'initialiser un point immobile"""

        def __init__(self):

            self.x, self.y = 0, 0
            self.o_x, self.o_y = 0, 0
            self.child = []
            self.or_x, self.or_y = 0, 0
            self.dif_x, self.dif_y = 0, 0
            self.outline = 'black'
            self.view = 0
            
            return

    class infos_panel(tk.LabelFrame):
        """Groupe nommé des attributs et des changements pour un point"""

        def __init__(self, parent):
            """
            In :
              parent : point dont les informations seront affichées
              < <point>
            """

            self.parent = parent

            name = self.parent.outline
            name = name[0].upper() + name[1:]
            tk.LabelFrame.__init__(self, self.parent.panel, text = name)
            self.grid()

            infos = self.grid_info()

            self.c1 = tk.Frame(self)
            self.c2 = tk.Frame(self)

            self.c1.grid(row = 1, column = 0, sticky = 'nw')
            self.c2.grid(row = 1, column = 1, sticky = 'nw')

            self.coords = tk.Frame(self.c1)
            
            self.x_V, self.y_V = tk.IntVar(self), tk.IntVar(self)
            self.x_V.set(int(self.parent.x))
            self.y_V.set(int(self.parent.y))

            self.or_x_V, self.or_y_V = tk.IntVar(self), tk.IntVar(self)
            self.or_x_V.set(int(self.parent.or_x))
            self.or_y_V.set(int(self.parent.or_y))

            self.x = tk.Label(self.coords, textvar = self.x_V)
            self.y = tk.Label(self.coords, textvar = self.y_V)

            self.o_x = tk.Label(self.coords, text = int(self.parent.o_x))
            self.o_y = tk.Label(self.coords, text = int(self.parent.o_y))

            self.or_x = tk.Label(self.coords, textvar = self.or_x_V)
            self.or_y = tk.Label(self.coords, textvar = self.or_y_V)

            self.x.grid(row = 1, column = 2)
            self.y.grid(row = 2, column = 2)
            self.o_x.grid(row = 1, column = 1)
            self.o_y.grid(row = 2, column = 1)
            self.or_x.grid(row = 1, column = 3)
            self.or_y.grid(row = 2, column = 3)

            tk.Label(self.coords, text = 'x').grid(row = 1, column = 0)
            tk.Label(self.coords, text = 'y').grid(row = 2, column = 0)
            tk.Label(self.coords, text = 'Origine').grid(row = 0, column = 1)
            tk.Label(self.coords, text = 'Actuels').grid(row = 0, column = 2)
            tk.Label(self.coords, text = 'Sur orbite').grid(row = 0, column = 3)

            self.tail_V = tk.BooleanVar(self)
            self.angle_V = tk.IntVar(self)
            
            self.tail_V.set(self.parent.tail)
            self.angle_V.set(self.parent.angle)

            self.tail = tk.Checkbutton(self.c2, text = 'Trainee', var = self.tail_V, command = self.change_tail)
            self.tail_size = tk.Scale(self.c2, from_ = 1, to = 20, orient = 'horizontal', command = self.update_tail_size)
            self.destroy_tail = tk.Button(self.c2, text = 'Detruire la trainee', command = self.parent.destroy_tail)

            self.tail.grid(row = 0, column = 0, sticky = 'w')
            self.tail_size.grid(row = 1, column = 0, sticky = 'w')
            self.destroy_tail.grid(row = 2, column = 0, sticky = 'w')

            self.speed_f = tk.Frame(self.c1)
            self.angle_f = tk.Frame(self.c1)
            
            self.speed = tk.Scale(self.speed_f, from_ = 1, to = 20, orient = 'horizontal', command = self.update_speed)
            self.angle = tk.Label(self.angle_f, textvar = self.angle_V)

            self.speed.grid(row = 0, column = 1, sticky = 'w')
            self.angle.grid(row = 0, column = 1, sticky = 'w')

            self.tail_size.set(self.parent.tail_size)
            self.speed.set(self.parent.speed)

            self.grid_pos = tk.Frame(self)

            self.grid_row_V, self.grid_column_V = tk.IntVar(self), tk.IntVar(self)
            self.grid_row_opt, self.grid_column_opt = tuple([k1 for k1 in range(1, 11)]), tuple([k2 for k2 in range(1, 11)])

            self.grid_row_V.set(infos['row'])
            self.grid_column_V.set(infos['column'] + 1)
            
            self.grid_row = tk.OptionMenu(self.grid_pos, self.grid_row_V, command = self.update_grid, *self.grid_row_opt)
            self.grid_column = tk.OptionMenu(self.grid_pos, self.grid_column_V, command = self.update_grid, *self.grid_column_opt)

            self.grid_row.grid(row = 0, column = 1, sticky = 'e')
            self.grid_column.grid(row = 0, column = 2, sticky = 'e')

            tk.Label(self.speed_f, text = 'Vitesse :').grid(row = 0, column = 0, sticky = 'w')
            tk.Label(self.angle_f, text = 'Angle actuel :').grid(row = 0, column = 0, sticky = 'w')
            tk.Label(self.grid_pos, text = 'Position :').grid(row = 0, column = 0, sticky = 'e')

            self.coords.grid(row = 0, column = 0, sticky = 'w')
            self.speed_f.grid(row = 1, column = 0, sticky = 'w')
            self.angle_f.grid(row = 2, column = 0, sticky = 'w')
            self.grid_pos.grid(row = 2, column = 0, sticky = 'e')

            tk.Label(self, text = f'Parent : {self.parent.parent.outline}').grid(row = 0, column = 0, sticky = 'w')

            return

        def new_grid(self, row = None, column = None, sticky = None):
            """Permet de repositionner le LabelFrame dans la fenêtre"""
            """
            In :
              row    : nouvelle ligne ; ancienne conservée si None
              < int
              > None
              column : nouvelle colonne ; ancienne conservée si None
              < int
              > None
              sticky : nouvel allignement ; ancien conservé si None
              < str < tk.N / tk.S / tk.W / tk.E
              > None
            """

            infos = self.grid_info()

            r, c, s = row, column, sticky
            if r == None:
                r = infos['row']
            if c == None:
                c = infos['column']
            if s == None:
                s = infos['sticky']

            self.grid_forget()
            self.grid(row = r, column = c, sticky = s)

            return

        def change_tail(self, event = None):
            """Change l'activation de la trainée du point"""
            """
            In :
              event : objet tkinter
              < <tk.event>
              > None
            """

            self.parent.tail = not self.parent.tail

            return

        def update_tail_size(self, event = None):
            """Change la taille de la trainée du parent"""
            """
            In :
              event : objet tkinter
              < <tk.event>
              > None
            """

            self.parent.tail_size = int(self.tail_size.get())

            for k in self.parent.tail_objs:
                self.can.itemconfig(k, width = self.parent.tail_size)

            return

        def update_speed(self, event = None):
            """Change la vitesse du parent"""
            """
            In :
              event : objet tkinter
              < <tk.event>
              > None
            """

            self.parent.speed = int(self.speed.get())

            return

        def update_grid(self, event = None):
            """Change le positionnement du LabelFrame dans la fenêtre"""
            """
            In :
              event : objet tkinter
              < <tk.event>
              > None
            """

            self.new_grid(row = self.grid_row_V.get(), column = self.grid_column_V.get() - 1)

            return

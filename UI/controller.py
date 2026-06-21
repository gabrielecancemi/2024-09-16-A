import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        latitudine = self._view.txt_latitude.value
        longitudine = self._view.txt_longitude.value
        shape = self._view.ddshape.value

        if shape is None or shape == "":
            self._view.txt_result1.controls.append(ft.Text("Selezionare una forma", color="red"))
            self._view.update_page()
            return

        if latitudine == "" or longitudine == "":
            self._view.txt_result1.controls.append(ft.Text("Inserire valori di latitudine e longitudine validi", color="red"))
            self._view.update_page()
            return

        try:
            latitudine = float(latitudine)
            longitudine = float(longitudine)
        except:
            self._view.txt_result1.controls.append(ft.Text("Inserire valori di latitudine e longitudine numerici", color="red"))
            self._view.update_page()
            return

        lat, lon = self._model.get_min_max()

        if latitudine > lat[1] or latitudine < lat[0]:
            self._view.txt_result1.controls.append(ft.Text(f"Inserire valori di latitudine compresi tra {lat[0]} e {lat[1]}", color="red"))
            self._view.update_page()
            return

        if longitudine > lon[1] or longitudine < lon[0]:
            self._view.txt_result1.controls.append(ft.Text(f"Inserire valori di longitudine compresi tra {lon[0]} e {lon[1]}", color="red"))
            self._view.update_page()
            return

        self._model.make_graph(latitudine, longitudine, shape)
        n, m = self._model.dim_grafo()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {n}", color="green"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {m}", color="green"))
        nodi, archi = self._model.get_info()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi di grado maggiore sono: {m}", color="green"))
        for n in nodi:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]} -> degree: {n[1]}"))

        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono: {m}", color="green"))
        for a in archi:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0]} <-> {a[1]} | peso = {a[2]}"))

        self._view.btn_path.disabled = False

        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()

        percorso, punteggio = self._model.get_percorso()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso con punteggio: {punteggio}", color="green"))
        for n in percorso:
            self._view.txt_result2.controls.append(ft.Text(f"{n[0]} | densità = {n[1]}"))
        self._view.update_page()


    def fill_ddshape(self):
        for s in self._model.get_all_shapes():
            self._view.ddshape.options.append(ft.dropdown.Option(s))

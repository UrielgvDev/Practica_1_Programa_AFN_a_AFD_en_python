import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AFNtoAFDConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Convertir un AFN a AFD :)")

        # Cargar y configurar la imagen de fondo
        self.background_image = ImageTk.PhotoImage(Image.open("imagen1.png"))  # Reemplaza con la ruta de tu imagen
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)


        self.language_label = tk.Label(master, text="Lenjuage:")
        self.language_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)

        self.language_entry = tk.Entry(master)
        self.language_entry.grid(row=0, column=1, columnspan=2, pady=5)

        self.states_label = tk.Label(master, text="Estados:")
        self.states_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        self.states_entry = tk.Entry(master) 
        self.states_entry.grid(row=1, column=1, columnspan=2, pady=5)

        self.transitions_label = tk.Label(master, text="Transiciones :")
        self.transitions_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        self.transitions_text = tk.Text(master, height=5, width=30)
        self.transitions_text.grid(row=2, column=1, columnspan=2, pady=5)

        self.convert_button = tk.Button(master, text="Convertir :)", command=self.convert_afn_to_afd)
        self.convert_button.grid(row=3, column=1, pady=10)

    def convert_afn_to_afd(self):
        language = set(self.language_entry.get().split(','))
        states = set(self.states_entry.get().split(','))
        transitions = [line.split(',') for line in self.transitions_text.get("1.0", tk.END).splitlines() if line]

        # Algoritmo para la conversión AFN a AFD
        afn_to_afd_result = self.afn_to_afd(language, states, transitions)

        # Se muestra el resultado en un cuadro de mensaje
        result_message = "Resultado de la conversión de AFN a AFD:\n\n" + afn_to_afd_result
        messagebox.showinfo("Resultado de la conversión", result_message)

    def afn_to_afd(self, language, states, transitions):
        afd_states = set()
        afd_transitions = []

        # Función para obtener el conjunto alcanzable desde un conjunto de estados con un símbolo
        def get_reachable_states(current_states, symbol):
            reachable_states = set()
            for state in current_states:
                for transition in transitions:
                    if transition[0] == state and transition[1] == symbol:
                        reachable_states.add(transition[2])
            return reachable_states

        # Inicialización con el estado inicial del AFN
        initial_state = set(['q0'])
        afd_states.add(tuple(initial_state))
        unprocessed_states = [tuple(initial_state)]

        while unprocessed_states:
            current_state = unprocessed_states.pop()

            for symbol in language:
                reachable_states = set()
                for sub_state in current_state:
                    reachable_states |= get_reachable_states([sub_state], symbol)

                if reachable_states:
                    afd_states.add(tuple(reachable_states))
                    afd_transitions.append((current_state, symbol, tuple(reachable_states)))

                    if tuple(reachable_states) not in afd_states:
                        unprocessed_states.append(tuple(reachable_states))

        # Formatea el resultado
        result = f"Estados: {', '.join(map(str, afd_states))}\n"
        result += f"Transiciones:\n"
        for transition in afd_transitions:
            result += f"{transition[0]} --({transition[1]})--> {transition[2]}\n"

        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = AFNtoAFDConverter(root)
    root.mainloop()

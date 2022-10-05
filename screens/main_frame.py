from tkinter import *
from tkinter.ttk import *

from shared import Observer
from simulation import Client, CashMachine


class CashMachineStatusPanel(Frame, Observer):
    def __init__(self, master, cash_machine):
        super().__init__(master, height=50)

        self.cash_machine = cash_machine
        self.cash_machine.attach(self)

        self.label = Label(
            self,
            text=cash_machine.name,
            width=20
        )
        self.status_label = Label(
            self,
            text="Disponível",
            width=10
        )
        self.progress_bar = Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
        )

        self.label.place(
            relx=0.00, rely=0.20, relwidth=0.25, relheight=0.8
        )
        self.status_label.place(
            relx=0.25, rely=0.20, relwidth=0.25, relheight=0.8
        )
        self.progress_bar.place(
            relx=0.50, rely=0.10, relwidth=0.50, relheight=0.8
        )

    def notify(self):
        if self.cash_machine.available:
            self.status_label.configure(text="Disponível")
        else:
            self.status_label.configure(text="Indisponível")

        self.progress_bar["value"] = self.cash_machine.progress


class ClientStatusPanel(Frame, Observer):
    def __init__(self, master, client):
        super().__init__(master, height=25)

        self.client = client
        self.client.attach(self)

        self.name_var = StringVar()
        self.status_var = StringVar()
        self.cash_machine_var = StringVar()
        self.attendament_time_var = StringVar()

        self.name_var.set(self.client.name)
        self.status_var.set(self.client.status)
        self.cash_machine_var.set("...")
        self.attendament_time_var.set("...")

        self.name_label = Label(
            self,
            textvariable=self.name_var
        )

        self.status_label = Label(
            self,
            textvariable=self.status_var
        )

        self.cash_machine_label = Label(
            self,
            textvariable=self.cash_machine_var
        )

        self.attendament_time = Label(
            self,
            textvariable=self.attendament_time_var
        )

        self.name_label.place(relx=0.00, relwidth=0.25, height=25)
        self.status_label.place(relx=0.25, relwidth=0.25, height=25)
        self.cash_machine_label.place(relx=0.50, relwidth=0.25, height=25)
        self.attendament_time.place(relx=0.75, relwidth=0.32, height=25)

    def notify(self):
        self.status_var.set(self.client.status)

        if not self.client.status == "Na fila":
            self.cash_machine_var.set(self.client.cash_machine.name)

        if self.client.status == "Atendido":
            self.attendament_time_var.set(str(self.client.elapsed_time))


class AddClientPanel(Frame):
    def __init__(self, master, clients_panel):
        super().__init__(master, height=40)

        self.new_client_name = StringVar()
        self.new_client_code = 1
        self.new_client_name.set(f"Client {self.new_client_code}")

        self.clients_panel = clients_panel

        self.entry_name = Entry(
            self,
            state="readonly",
            textvariable=self.new_client_name,
            font=("arial", 16)
        )

        self.entry_period = Entry(
            self,
            font=("arial", 16)
        )

        self.button = Button(
            self,
            text="Adicionar",
            command=self.on_add_clicked
        )

        self.entry_name.place(relwidth=0.6, relheight=0.8)
        self.entry_period.place(relx=0.61, relwidth=0.2, relheight=0.8)
        self.button.place(relx=0.82, relwidth=0.18, relheight=0.8)

    def on_add_clicked(self):
        client = Client(
            client_name=f"Client {self.new_client_code}",
            attendance_period=int(self.entry_period.get()),
            code=self.new_client_code
        )

        ClientStatusPanel(self.clients_panel, client).pack(fill=X)

        client.start()

        self.new_client_code += 1
        self.new_client_name.set(f"Client {self.new_client_code}")


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.main_frame = Frame(self.master)
        self.main_frame.place(relx=0.1, relheight=1, relwidth=0.8)

        self.cash_machines_panel = Frame(self.main_frame)
        for cash_machine in CashMachine.instances:
            panel = CashMachineStatusPanel(
                self.cash_machines_panel,
                cash_machine
            )
            panel.pack(fill="x")

        self.clients_panel = Frame(self.main_frame)

        self.cash_machines_panel.pack(fill=X)

        AddClientPanel(self.main_frame, self.clients_panel).pack(fill=X)

        self.clients_panel.pack(fill=BOTH, expand=True)


def main():
    nCaixas = 5

    for i in range(nCaixas):
        CashMachine(id=i).start()

    window = Tk()
    window.geometry("800x600")

    main_frame = Frame(window)
    main_frame.place(relx=0.1, relheight=1, relwidth=0.8)

    cash_machines_panel = Frame(main_frame)
    for cash_machine in CashMachine.instances:
        panel = CashMachineStatusPanel(cash_machines_panel, cash_machine)
        panel.pack(fill="x")

    clients_panel = Frame(main_frame)

    cash_machines_panel.pack(fill=X)

    AddClientPanel(main_frame, clients_panel).pack(fill=X)

    clients_panel.pack(fill=BOTH, expand=True)

    window.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk
from turtle import back

from shared import Observer
from simulation import Client, CashMachine


class CashMachineStatusPanel(tk.Frame, Observer):
    def __init__(self, master, cash_machine):
        super().__init__(master, height=50)

        self.cash_machine = cash_machine
        self.cash_machine.attach(self)

        self.label = tk.Label(
            self,
            text=cash_machine.name,
            width=20
        )
        self.status_label = tk.Label(
            self,
            text="Available",
            width=10
        )
        self.progress_bar = ttk.Progressbar(
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
            self.status_label.configure(text="Available")
        else:
            self.status_label.configure(text="Unvailable")

        self.progress_bar["value"] = self.cash_machine.progress


class ClientStatusPanel(tk.Frame, Observer):
    def __init__(self, master, client):
        super().__init__(master, height=25)

        self.client = client
        self.client.attach(self)

        self.name_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.cash_machine_var = tk.StringVar()
        self.attendament_time_var = tk.StringVar()

        self.name_var.set(self.client.name)
        self.status_var.set(self.client.status)
        self.cash_machine_var.set("...")
        self.attendament_time_var.set("...")

        self.name_label = tk.Label(
            self,
            textvariable=self.name_var
        )

        self.status_label = tk.Label(
            self,
            textvariable=self.status_var
        )

        self.cash_machine_label = tk.Label(
            self,
            textvariable=self.cash_machine_var
        )

        self.attendament_time = tk.Label(
            self,
            textvariable=self.attendament_time_var
        )

        self.name_label.place(relx=0.00, relwidth=0.25, height=25)
        self.status_label.place(relx=0.25, relwidth=0.25, height=25)
        self.cash_machine_label.place(relx=0.50, relwidth=0.25, height=25)
        self.attendament_time.place(relx=0.75, relwidth=0.32, height=25)

    def notify(self):
        self.status_var.set(self.client.status)

        if not self.client.status == "On queue":
            self.cash_machine_var.set(self.client.cash_machine.name)

        if self.client.status == "Attendament Finished":
            self.attendament_time_var.set(str(self.client.elapsed_time))


class AddClientPanel(tk.Frame):
    def __init__(self, master, clients_panel):
        super().__init__(master, height=40)

        self.new_client_name = tk.StringVar()
        self.new_client_code = 1
        self.new_client_name.set(f"Client {self.new_client_code}")

        self.clients_panel = clients_panel

        self.entry_name = tk.Entry(
            self,
            state="readonly",
            textvariable=self.new_client_name,
            font=("arial", 16)
        )

        self.entry_period = tk.Entry(
            self,
            font=("arial", 16)
        )

        self.button = tk.Button(
            self,
            text="Add",
            font=("arial", 16),
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

        ClientStatusPanel(self.clients_panel, client).pack(fill=tk.X)

        client.start()

        self.new_client_code += 1
        self.new_client_name.set(f"Client {self.new_client_code}")


def main():
    nCaixas = 2

    for i in range(nCaixas):
        CashMachine(id=i).start()

    window = tk.Tk()
    window.geometry("800x600")

    main_frame = tk.Frame(window)
    main_frame.place(relx=0.1, relheight=1, relwidth=0.8)

    cash_machines_panel = tk.Frame(main_frame)
    for cash_machine in CashMachine.instances:
        panel = CashMachineStatusPanel(cash_machines_panel, cash_machine)
        panel.pack(fill="x")

    clients_panel = tk.Frame(main_frame)

    cash_machines_panel.pack(fill=tk.X)

    AddClientPanel(main_frame, clients_panel).pack(fill=tk.X)

    clients_panel.pack(fill=tk.BOTH, expand=True)

    window.mainloop()


if __name__ == "__main__":
    main()

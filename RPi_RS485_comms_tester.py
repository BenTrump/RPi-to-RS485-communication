
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import tkinter as tk
from threading import Timer


class Main(tk.Frame):
    def __init__(self, gui, *args, **kwargs):
        tk.Frame.__init__(self, master=gui.master, *args, **kwargs)
        self.grid(row=0, column=0)
        self.gui = gui

        self.btn_write_multi_regs = tk.Button(self, text="Write to multiple registers", height=2, width=20)
        self.btn_write_multi_regs.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_write_multi_regs.config(font="Arial 12 bold", command=self.write_to_multi_regs)
        self.btn_write_single_reg = tk.Button(self, text="Write to single register", height=2, width=20)
        self.btn_write_single_reg.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_write_single_reg.config(font="Arial 12 bold", command=self.btn_write_single_reg)
        self.btn_read_regs = tk.Button(self, text="Read holding registers", height=2, width=20)
        self.btn_read_regs.grid(row=3, column=1, padx=(10, 0), pady=(10, 0))
        self.btn_read_regs.config(font="Arial 12 bold", command=self.read_holding_reg)

        self.lbl_slave_id = tk.Label(self, text="Slave ID: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_slave_id.grid(row=1, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_reg_start = tk.Label(self, text="Start Reg: ", font="Arial 12 bold", anchor=tk.E, width=10)
        self.lbl_reg_start.grid(row=1, column=5, padx=(25, 0), pady=(10, 0))
        self.lbl_data_entry = tk.Label(self, text="Output data: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_data_entry.grid(row=2, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_data_return = tk.Label(self, text="Return data: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_data_return.grid(row=3, column=3, padx=(10, 0), pady=(10, 0))
        self.lbl_comms_status = tk.Label(self, text="Status: ", font="Arial 12 bold", anchor=tk.E, width=15)
        self.lbl_comms_status.grid(row=4, column=3, padx=(10, 0), pady=(10, 0))

        self.txt_slave_id = tk.Entry(self, font="Arial 12 bold", relief="sunken", width=5)
        self.txt_slave_id.grid(row=1, column=4, padx=(10,  0), pady=(10, 0), sticky=tk.W)
        self.txt_data_entry = tk.Entry(self, font="Arial 12 bold", relief="sunken", width=15)
        self.txt_data_entry.grid(row=2, column=4, padx=(10, 0), pady=(10, 0), columnspan=3, sticky=tk.W)
        self.txt_data_return = tk.Label(self, font="Arial 12 bold", relief="sunken", width=15, bg="white", bd=1)
        self.txt_data_return.grid(row=3, column=4, padx=(10, 0), pady=(10, 0), columnspan=3, sticky=tk.W)
        self.txt_reg_start = tk.Entry(self, font="Arial 12 bold", relief="sunken", width=10)
        self.txt_reg_start.grid(row=1, column=6, padx=(10, 0), pady=(10, 0))

        self.display_status = tk.Label(self, relief="raised", width=15, height=2, bg="sky blue", font="Arial 12 bold")
        self.display_status.grid(row=4, column=4, padx=(10, 0), pady=(10, 0), columnspan=3, sticky=tk.W)

    def write_to_multi_regs(self):
        try:
            data = self.txt_data_entry.get().split()
            slave_id = int(self.txt_slave_id.get())
            reg_start = int(self.txt_reg_start.get())
            fixed_data = list(map(int, data))
            self.gui.client.write_registers(values=fixed_data, address=reg_start, unit=slave_id)
            self.display_status.config(bg="green")
        except AttributeError:
            self.display_status.config(bg="red")
        timer = Timer(2.0, self.normal_status)
        timer.start()
        self.txt_data_return.config(text=" ")

        # Todo: make the display status a better color

    def write_to_single_reg(self):
        try:
            data = self.txt_data_entry.get().split()
            data = int(data[0])
            slave_id = int(self.txt_slave_id.get())
            reg_start = int(self.txt_reg_start.get())
            self.gui.client.write_register(value=data, address=reg_start, unit=slave_id)
            self.display_status.config(bg="green")
        except AttributeError:
            self.display_status.config(bg="red")
        timer = Timer(2.0, self.normal_status)
        timer.start()
        self.txt_data_return.config(text=" ")

    def read_holding_reg(self):
        try:
            slave_id = int(self.txt_slave_id.get())
            reg_start = int(self.txt_reg_start.get())
            register_data = self.gui.client.read_holding_registers(reg_start, 4, unit=slave_id)
            self.txt_data_return.config(text=register_data.registers)
            self.display_status.config(bg="green")
        except AttributeError:
            self.display_status.config(bg="red")
        timer = Timer(2.0, self.normal_status)
        timer.start()
        self.txt_data_entry.delete(0, "end")

    def normal_status(self):
        self.display_status.config(bg="sky blue")


class GUI:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("RS485 Communication Tester")
        self.master.geometry("800x400")
        self.main = Main(self)

        self.client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1,
                                   bytesize=8, parity="N", baudrate=9600, timeout=0.3)
        connection = self.client.connect()
        print(connection)

        self.master.mainloop()


test = GUI()

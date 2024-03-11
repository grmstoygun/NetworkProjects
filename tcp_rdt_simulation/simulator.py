import tkinter as tk
from PIL import Image, ImageTk
import os.path

class CustomProtocolSimulator:
    packet_count = 0
    cummulative_ack_count = 0
    def __init__(self, master):
        self.master = master
        self.master.title("Custom Protocol Simulator")
        self.create_frames()
        self.create_gui_elements()

    def create_frames(self):
        self.left_upper = tk.Frame(self.master, bd=1, bg="#FFF7E4", relief="raised")
        self.left_upper.grid(row=0, column=0,padx=2, pady = 2, sticky="nsew")

        self.right_upper = tk.Frame(self.master, bd=1, bg="#FFF7E4", relief="raised")
        self.right_upper.grid(row=0, column=1, padx=2, pady = 2,sticky="nsew")

        self.left_lower = tk.Frame(self.master, bd=1, bg="#FFF7E4", relief="raised")
        self.left_lower.grid(row=1, column=0, padx=2, pady = 2, sticky="nsew")

        self.right_lower = tk.Frame(self.master, bd=1, bg="#FFF7E4", relief="raised")
        self.right_lower.grid(row=1, column=1, padx=2, pady = 2, sticky="nsew")

        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

    def create_gui_elements(self):

        self.lbl_rdtsm = tk.Label(self.left_upper, text="Reliable Data Transfer Service Model",bg="#FFF7E4", font=("Helvetica", 14))
        self.lbl_rdtsm.grid(row=0, column=2)
        self.lbl_rdtsm_image = tk.Label(self.left_upper)
        self.lbl_rdtsm_image.grid(row=2, column=2)

        self.lbl_state_diagram = tk.Label(self.right_upper, text="State Diagrams", bg="#FFF7E4", font=("Helvetica", 14))
        self.lbl_state_diagram.grid(row=0, column=0)

        self.lbl_sender_state = tk.Label(self.right_upper, text="Sender:", bg="#FFF7E4", font=("Helvetica", 10))
        self.lbl_sender_state.grid(row=1, column=0)
        self.lbl_state_sender_image = tk.Label(self.right_upper)
        self.lbl_state_sender_image.grid(row=2, column=0)

        self.lbl_reciever_state = tk.Label(self.right_upper, text="Receiver:", bg="#FFF7E4", font=("Helvetica", 10))
        self.lbl_reciever_state.grid(row=1, column=1)
        self.lbl_state_reciever_image = tk.Label(self.right_upper)
        self.lbl_state_reciever_image.grid(row=2, column=1)


        self.lbl_operation_sequence = tk.Label(self.left_lower, text="Operation Sequence Diagram",bg="#FFF7E4", font=("Helvetica", 14))
        self.lbl_operation_sequence.grid(row=0, column=2)

        self.lbl_operation_sequence_sender = tk.Label(self.left_lower, text="Sender:",bg="#FFF7E4", font=("Helvetica", 10))
        self.lbl_operation_sequence_sender.grid(row=1, column=0)

        self.lbl_operation_sequence_reciever = tk.Label(self.left_lower, text="Reciever:",bg="#FFF7E4", font=("Helvetica", 10))
        self.lbl_operation_sequence_reciever.grid(row=1, column=4)

        self.txt_osd_output_sender = tk.Text(self.left_lower, wrap=tk.WORD, width=15, height=20)
        self.txt_osd_output_sender.grid(row=2, column=0)

        self.txt_osd_transfer = tk.Text(self.left_lower, wrap=tk.WORD, width=15, height=20)
        self.txt_osd_transfer.grid(row=2, column=2)

        self.txt_osd_output_reciever = tk.Text(self.left_lower, wrap=tk.WORD, width=15, height=20)
        self.txt_osd_output_reciever.grid(row=2, column=4)

        self.lbl_command_prompt = tk.Label(self.right_lower, text="Command Prompt",bg="#FFF7E4", font=("Helvetica", 14))
        self.lbl_command_prompt.pack()

        self.txt_command_output = tk.Text(self.right_lower, wrap=tk.WORD, width=50, height=10)
        self.txt_command_output.pack()

        protocol_options = ["rdt 1.0", "rdt 2.0", "rdt 3.0", "tcp"]
        self.protocol = tk.StringVar()
        self.protocol.set(protocol_options[0])
        option1 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=protocol_options[0], variable=self.protocol, onvalue=protocol_options[0], offvalue="", command=self.set_initial_states)
        option1.pack()
        option2 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=protocol_options[1], variable=self.protocol, onvalue=protocol_options[1], offvalue="", command=self.set_initial_states)
        option2.pack()
        option3 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=protocol_options[2], variable=self.protocol, onvalue=protocol_options[2], offvalue="", command=self.set_initial_states)
        option3.pack()
        option4 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=protocol_options[3], variable=self.protocol, onvalue=protocol_options[3], offvalue="", command=self.set_initial_states)
        option4.pack()

        self.set_initial_states()

        simulate_button = tk.Button(self.right_lower, text="Run Simulation", command=self.simulate_custom_protocol, fg="black", bg="green", width=16, height=2)
        simulate_button.pack()

        self.command_label = tk.Label(self.right_lower,bg="#FFF7E4", text="Enter command:") 
        self.command_label.pack()

        self.command_input = tk.Entry(self.right_lower, width=16)
        self.command_input.pack()

        run_command_button = tk.Button(self.right_lower, text="Run Command", command=self.on_run_command_button_click, fg ="black", bg = "blue", width=16, height=2)
        run_command_button.pack()

        
    def set_initial_states(self):
        prot = self.protocol.get()
        if(prot == "rdt 1.0"):
            reciever_image_path = "./images/rdt1reciever.png"
            sender_image_path = "./images/rdt1sender.png"
        elif(prot == "rdt 2.0"):
            reciever_image_path = "./images/rdt2reciever.png"
            sender_image_path = "./images/rdt2sender.png"
        elif(prot == "rdt 3.0"):
            reciever_image_path = "./images/rdt3reciever.png"
            sender_image_path = "./images/rdt3sender.png"  
        elif(prot == "tcp"):
            reciever_image_path = "./images/tcpserverclosed.png"
            sender_image_path = "./images/tcpclientclosed.png"
        set_image = self.load_image(reciever_image_path, (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        set_image = self.load_image(sender_image_path, (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image

    def load_image(self, image_path, size):
        path = os.path.dirname(os.path.abspath(__file__))
        img = Image.open(os.path.join(path, image_path))
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def simulate_custom_protocol(self):
        prot = self.protocol.get()   
        if prot == "rdt 1.0":
            self.rdt_1_0_simulation()
        elif prot == "rdt 2.0":
            self.rdt_2_0_simulation()
        elif prot == "rdt 3.0":
            self.rdt_3_0_simulation()
        elif prot == "tcp":
            self.tcp_send_syn()

    def on_run_command_button_click(self):
        input = self.command_input.get()
        if input == "rdt 1.0 normal":
            self.rdt_1_0_wait()
        elif input == "stop":
            self.stop_simulation()
        elif input == "rdt 2.0 normal" or input == "rdt 2.0 lost":
            self.rdt_2_0_wait()
        elif input == "rdt 3.0 normal" or input == "rdt 3.0 lost packet" or input == "rdt 3.0 lost ack" or input == "rdt 3.0 premature timeout":
            self.rdt_3_0_wait()
        elif input == "tcp normal" or input == "tcp lost packet" or input == "tcp lost ack" or input == "tcp premature timeout":
            self.tcp_wait()

    def stop_simulation(self):
        self.packet_count = 0
        self.cummulative_ack_count = 0
        self.lbl_rdtsm_image.config(image=None)
        self.lbl_rdtsm_image.image = None
        self.lbl_state_sender_image.config(image=None)
        self.lbl_state_sender_image.image = None
        self.lbl_state_reciever_image.config(image=None)
        self.lbl_state_reciever_image.image = None
        self.txt_osd_output_reciever.delete("1.0", "end")
        self.txt_osd_output_sender.delete("1.0", "end")
        self.txt_osd_transfer.delete("1.0", "end")
        self.txt_command_output.delete("1.0", "end")
        self.lbl_command_prompt.config(text="")

    def rdt_1_0_simulation(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/base.png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "Command options: \nrdt 1.0 normal\n")


    def rdt_1_0_wait(self):
        self.txt_command_output.insert(tk.END, "Enter stop to stop simulation \n")
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt1senderselected.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.rdt_1_0_send_data)


    def rdt_1_0_send_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "packet=make_pkt(data)\nudt_send(packet)\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.packet_count+=1
        self.txt_osd_output_sender.insert(tk.END, f"Packet {self.packet_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")

        self.master.after(3000, self.rdt_1_0_recieve_data)

    def rdt_1_0_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(packet)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt1recieverselected.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"Packet {self.packet_count}\n")
        self.master.after(3000, self.rdt_1_0_deliver_data)

    def rdt_1_0_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "extract(packet,data) && deliver_data(data)\n")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "-----------------------------------\n")
        self.master.after(2000, self.on_run_command_button_click)


    def rdt_2_0_simulation(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/base.png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "Command options: \nrdt 2.0 normal\nrdt 2.0 lost\n")

    def rdt_2_0_wait(self):
        self.txt_command_output.insert(tk.END, "Enter 'stop' to stop simulation \n")
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt2senderwait.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.rdt_2_0_send_data)

    def rdt_2_0_send_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "sndpkt=make_pkt(data, checksum)\nudt_send(sndpkt)\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt2senderack.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.packet_count+=1
        self.txt_osd_output_sender.insert(tk.END, f"Packet {self.packet_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")

        self.master.after(3000, self.rdt_2_0_recieve_data)

    def rdt_2_0_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\n")
        if self.command_input.get() == "rdt 2.0 lost":
            self.txt_command_output.insert(tk.END, "corrupt(rcvpkt)\n")
        elif self.command_input.get() == "rdt 2.0 normal":
            self.txt_command_output.insert(tk.END, "notcorrupt(rcvpkt)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt2recieverselected.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"Packet {self.packet_count}\n")
        self.master.after(3000, self.rdt_2_0_deliver_data)

    def rdt_2_0_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        if self.command_input.get() == "rdt 2.0 lost":
            self.txt_command_output.insert(tk.END, "sndpkt=make_pkt(NAK)\nudt_send(sndpkt)\n")
            self.txt_osd_output_reciever.insert(tk.END, f"NAK {self.packet_count}\n")
            set_image = self.load_image("./images/udt_send().png", (450, 300))
            self.lbl_rdtsm_image.config(image=set_image)
            self.lbl_rdtsm_image.image = set_image
        elif self.command_input.get() == "rdt 2.0 normal":
            self.txt_command_output.insert(tk.END, "extract(packet,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK)\nudt_send(sndpkt)")
            set_image = self.load_image("./images/deliver_data().png", (450, 300))
            self.lbl_rdtsm_image.config(image=set_image)
            self.lbl_rdtsm_image.image = set_image
            self.txt_osd_output_reciever.insert(tk.END, f"ACK {self.packet_count}\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        self.master.after(3000, self.rdt_2_0_check_ack)

    def rdt_2_0_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        if self.command_input.get() == "rdt 2.0 lost":
            self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nisNAK(rcvpkt)\n")
            self.txt_osd_output_sender.insert(tk.END, f"NAK {self.packet_count}\n")
            self.packet_count -=1
            set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
            self.lbl_rdtsm_image.config(image=set_image)
            self.lbl_rdtsm_image.image = set_image
            self.master.after(3000, self.rdt_2_0_send_data)
        elif self.command_input.get() == "rdt 2.0 normal":
            self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nisACK(rcvpkt)\n")
            self.txt_osd_output_sender.insert(tk.END, f"ACK {self.packet_count}\n")
            self.txt_command_output.insert(tk.END, "-----------------------------------\n")
            self.master.after(3000, self.rdt_2_0_wait)


    def rdt_3_0_simulation(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/base.png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "Command options: \nrdt 3.0 normal\nrdt 3.0 lost packet\nrdt 3.0 lost ack\nrdt 3.0 premature timeout\n")

    def rdt_3_0_wait(self):
        self.txt_command_output.insert(tk.END, "Enter 'stop' to stop simulation \n")
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderwait0.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.rdt_3_0_send_data)

    def rdt_3_0_send_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "sndpkt=make_pkt(0, data, checksum)\nudt_send(sndpkt)\nstart_timer\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderack0.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"Packet 0\n")
        if self.command_input.get() == "rdt 3.0 lost packet":
            self.txt_osd_transfer.insert(tk.END, "--------X\n")
            self.master.after(5000, self.rdt_3_0_lost_resend)
        elif self.command_input.get() == "rdt 3.0 normal" or self.command_input.get() == "rdt 3.0 premature timeout":
            self.txt_osd_transfer.insert(tk.END, "------------->\n")
            self.master.after(3000, self.rdt_3_0_normal_recieve_data)
        elif self.command_input.get() == "rdt 3.0 lost ack":
            self.txt_osd_transfer.insert(tk.END, "------------->\n")
            self.master.after(3000, self.rdt_3_0_lost_ack_recieve_data)

    def rdt_3_0_normal_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq0(rcvpkt)\n")
        if self.command_input.get() != "rdt 3.0 lost ack":
            set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
            self.lbl_rdtsm_image.config(image=set_image)
            self.lbl_rdtsm_image.image = set_image
            set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
            self.lbl_state_reciever_image.config(image=set_image)
            self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"Packet 0\n")
        if self.command_input.get() == "rdt 3.0 premature timeout":
            self.master.after(3000, self.rdt_3_0_premature_deliver_data)
        else:
            self.master.after(3000, self.rdt_3_0_normal_deliver_data)

    def rdt_3_0_normal_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, 0, checksum)\nudt_send(sndpkt)\n")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"ACK 0\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.rdt_3_0_normal_check_ack)

    def rdt_3_0_normal_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nisACK(rcvpkt,0)\nstop_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"ACK 0\n")
        self.master.after(3000, self.rdt_3_0_loop_for_1)

    def rdt_3_0_premature_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, 0, checksum)\nudt_send(sndpkt)")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"Packet 0\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        
        self.txt_command_output.insert(tk.END, "extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, 0, checksum)\nudt_send(sndpkt)\n")
        self.txt_osd_output_reciever.insert(tk.END, f"ACK 0\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.rdt_3_0_premature_check_ack)

    def rdt_3_0_premature_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_osd_output_reciever.insert(tk.END, f"ACK 0\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        self.txt_osd_output_sender.insert(tk.END, f"ACK 0\n")
        self.txt_osd_output_sender.insert(tk.END, f"ACK 0\n")
        self.master.after(3000, self.rdt_3_0_loop_for_1)

    def rdt_3_0_lost_resend(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"Packet 0\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.rdt_3_0_normal_recieve_data)

    def rdt_3_0_lost_ack_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq0(rcvpkt)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"Packet 0\n")
        self.master.after(3000, self.rdt_3_0_lost_ack_deliver_data)

    def rdt_3_0_lost_ack_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, 0, checksum)\nudt_send(sndpkt)")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"ACK 0\n")
        self.txt_osd_transfer.insert(tk.END, "X----------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.rdt_3_0_lost_ack_check_ack)

    def rdt_3_0_lost_ack_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"Packet 0\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.rdt_3_0_normal_recieve_data)
        
    def rdt_3_0_loop_for_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderwait1.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.rdt_3_0_send_data_1)

    def rdt_3_0_send_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "sndpkt=make_pkt(1, data, checksum)\nudt_send(sndpkt)\nstart_timer\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderack1.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"Packet 1\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.rdt_3_0_recieve_data_1)

    def rdt_3_0_recieve_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq1(rcvpkt)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"Packet 1\n")
        self.master.after(3000, self.rdt_3_0_deliver_data_1)

    def rdt_3_0_deliver_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, 1, checksum)\nudt_send(sndpkt)\n")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_osd_output_reciever.insert(tk.END, f"ACK 1\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.rdt_3_0__check_ack_1)

    def rdt_3_0__check_ack_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_rcv(rcvpkt)\nisACK(rcvpkt,1)\nstop_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"ACK 1\n")
        self.master.after(3000, self.rdt_3_0_wait)

    def tcp_send_syn(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/tcpclientsyn_sent.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        set_image = self.load_image("./images/tcpserverlisten.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_command_output.insert(tk.END, "Establishing tcp connection...\nSend SYN\n")
        self.txt_osd_output_sender.insert(tk.END, f"SYN=1\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_recieve_syn)

    def tcp_recieve_syn(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/tcpserversyn_rcvd.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "Recieve SYN\nsend SYN & ACK\n")
        self.txt_osd_output_reciever.insert(tk.END, f"SYN=1\n")
        self.txt_osd_output_reciever.insert(tk.END, f"SYN=1&&ACK\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        self.master.after(3000, self.tcp_recieve_ack)

    def tcp_recieve_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/tcpclientestablished.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        set_image = self.load_image("./images/tcpserverestablished.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"SYN=1&&ACK\n")
        self.master.after(3000, self.tcp_simulate)

    def tcp_simulate(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        set_image = self.load_image("./images/base.png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "Command options: \ntcp normal\ntcp lost packet\ntcp lost ack\ntcp premature timeout\n")

    def tcp_wait(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.insert(tk.END, "Enter 'close' to close TCP connection.\n")
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderwait0.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.tcp_send_data)

    def tcp_send_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "Sending 10 bytes\nsndpkt=make_pkt(0, data, checksum)\nudt_send(sndpkt)\nstart_timer\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderack0.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"Seq={self.cummulative_ack_count}\n")
        if self.command_input.get() == "tcp lost packet":
            self.txt_osd_transfer.insert(tk.END, "--------X\n")
            self.master.after(5000, self.tcp_lost_resend)
        elif self.command_input.get() == "tcp normal" or self.command_input.get() == "tcp premature timeout":
            self.txt_osd_transfer.insert(tk.END, "------------->\n")
            self.master.after(3000, self.tcp_normal_recieve_data)
        elif self.command_input.get() == "tcp lost ack":
            self.txt_osd_transfer.insert(tk.END, "------------->\n")
            self.master.after(3000, self.tcp_lost_ack_recieve_data)


    def tcp_normal_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq{self.cummulative_ack_count}(rcvpkt)\n")
        if self.command_input.get() != "tcp lost ack":
            set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
            self.lbl_rdtsm_image.config(image=set_image)
            self.lbl_rdtsm_image.image = set_image
            set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
            self.lbl_state_reciever_image.config(image=set_image)
            self.lbl_state_reciever_image.image = set_image
        if self.command_input.get() == "tcp premature timeout":
            self.master.after(3000, self.tcp_premature_deliver_data)
        else:
            self.master.after(3000, self.tcp_normal_deliver_data)

    def tcp_normal_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, {self.cummulative_ack_count}, checksum)\nudt_send(sndpkt)\n")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.cummulative_ack_count+=10
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        self.txt_osd_output_reciever.insert(tk.END, f"ACK {self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_normal_check_ack)

    def tcp_normal_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"rdt_rcv(rcvpkt)\nisACK(rcvpkt,{self.cummulative_ack_count})\nstop_timer\n")
        self.master.after(3000, self.tcp_loop_for_1)

    def tcp_lost_resend(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"Seq={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_normal_recieve_data)

    def tcp_lost_ack_recieve_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq{self.cummulative_ack_count}(rcvpkt)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.master.after(3000, self.tcp_lost_ack_deliver_data)
    
    def tcp_lost_ack_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, {self.cummulative_ack_count}, checksum)\nudt_send(sndpkt)")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.cummulative_ack_count+=10
        self.txt_osd_output_reciever.insert(tk.END, f"ACK={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "X----------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_lost_ack_check_ack)

    def tcp_lost_ack_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"Seq={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_normal_recieve_data)

    def tcp_premature_deliver_data(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, {self.cummulative_ack_count}, checksum)\nudt_send(sndpkt)")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.txt_command_output.insert(tk.END, "timeout\nudt_send(sndpkt)\nstart_timer\n")
        self.txt_osd_output_sender.insert(tk.END, f"Seq={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        
        self.txt_command_output.insert(tk.END, f"extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, {self.cummulative_ack_count}, checksum)\nudt_send(sndpkt)\n")
        self.cummulative_ack_count+=10
        self.txt_osd_output_reciever.insert(tk.END, f"ACK={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_premature_check_ack)

    def tcp_premature_check_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_osd_output_reciever.insert(tk.END, f"ACK {self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        self.master.after(3000, self.tcp_loop_for_1)

    def tcp_loop_for_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, "rdt_send(data)\n")
        set_image = self.load_image("./images/rdt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderwait1.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.tcp_send_data_1)

    def tcp_send_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"sndpkt=make_pkt({self.cummulative_ack_count}, data, checksum)\nudt_send(sndpkt)\nstart_timer\n")
        set_image = self.load_image("./images/udt_send().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3senderack1.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"Seq={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_recieve_data_1)

    def tcp_recieve_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"rdt_rcv(rcvpkt)\nnotcorrupt(rcvpkt)\nhas_seq{self.cummulative_ack_count}(rcvpkt)\n")
        set_image = self.load_image("./images/rdt_rcv().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        set_image = self.load_image("./images/rdt3reciever1.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_deliver_data_1)

    def tcp_deliver_data_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"extract(rcpvkt,data)\ndeliver_data(data)\nsndpkt=make_pkt(ACK, {self.cummulative_ack_count}, checksum)\nudt_send(sndpkt)\n")
        set_image = self.load_image("./images/deliver_data().png", (450, 300))
        self.lbl_rdtsm_image.config(image=set_image)
        self.lbl_rdtsm_image.image = set_image
        self.cummulative_ack_count+=10
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        self.txt_osd_output_reciever.insert(tk.END, f"ACK={self.cummulative_ack_count}\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/rdt3reciever0.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp__check_ack_1)

    def tcp__check_ack_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        if self.command_input.get() == "close":
            return self.tcp_fin_wait_1()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"rdt_rcv(rcvpkt)\nisACK(rcvpkt, {self.cummulative_ack_count})\nstop_timer\n")
        self.master.after(3000, self.tcp_send_data)

    def tcp_fin_wait_1(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Closing connection...\nSend FIN\n")
        set_image = self.load_image("./images/tcpclientfin_wait1.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"FIN\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_close_wait)

    def tcp_close_wait(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Recieve FIN\nSend ACK\n")
        self.txt_osd_output_reciever.insert(tk.END, f"\n")
        self.txt_osd_output_reciever.insert(tk.END, f"ACK\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/tcpserverclose_wait.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_fin_wait_2)

    def tcp_fin_wait_2(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Recieve ACK\n")
        set_image = self.load_image("./images/tcpclientfin_wait2.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.master.after(3000, self.tcp_last_ack)

    def tcp_last_ack(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Send FIN\n")
        self.txt_osd_output_reciever.insert(tk.END, f"FIN\n")
        self.txt_osd_transfer.insert(tk.END, "<-------------\n")
        set_image = self.load_image("./images/tcpserverlast_ack.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.tcp_time_wait)

    def tcp_time_wait(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Recieve FIN\nSend ACK\n")
        set_image = self.load_image("./images/tcpclienttime_wait.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        self.txt_osd_output_sender.insert(tk.END, f"\n")
        self.txt_osd_output_sender.insert(tk.END, f"ACK\n")
        self.txt_osd_transfer.insert(tk.END, "------------->\n")
        self.master.after(3000, self.tcp_closed)

    def tcp_closed(self):
        if self.command_input.get() == "stop":
            return self.stop_simulation()
        self.txt_command_output.delete("1.0", "end")
        self.txt_command_output.insert(tk.END, f"Recieve ACK\n")
        set_image = self.load_image("./images/tcpclientclosed.png", (450, 300))
        self.lbl_state_sender_image.config(image=set_image)
        self.lbl_state_sender_image.image = set_image
        set_image = self.load_image("./images/tcpserverclosed.png", (450, 300))
        self.lbl_state_reciever_image.config(image=set_image)
        self.lbl_state_reciever_image.image = set_image
        self.master.after(3000, self.stop_simulation)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomProtocolSimulator(root)
    root.mainloop()

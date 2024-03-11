import tkinter as tk
from tkinter import StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

class NetworkSimulationUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Routing Algorithms")
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
        

        self.lbl_n = tk.Label(self.right_lower, text="Enter number of nodes:",bg="#FFF7E4", font=("Helvetica", 14))
        self.lbl_n.pack()

        self.n_input = tk.Entry(self.right_lower, width=16)
        self.n_input.pack()

        algorithm_options = ["Link State", "Distance Vector"]
        self.algorithm = tk.StringVar()
        self.algorithm.set(algorithm_options[0])
        option1 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=algorithm_options[0], variable=self.algorithm, onvalue=algorithm_options[0], offvalue="")
        option1.pack()
        option2 = tk.Checkbutton(self.right_lower, bg="#FFF7E4",text=algorithm_options[1], variable=self.algorithm, onvalue=algorithm_options[1], offvalue="")
        option2.pack()

        run_command_button = tk.Button(self.right_lower, text="Start Simulation", command=self.start, fg ="black", bg = "grey", width=16, height=2)
        run_command_button.pack()

        self.next_iteration_button = tk.Button(self.right_lower, text="Next Iteration", command=self.next_iteration)
        self.next_iteration_button.pack()
        self.next_iteration_button["state"] = "disabled" 
        self.next_iteration_button_pressed = StringVar()
        self.iteration = 1

    def start(self):
        for widget in self.left_upper.winfo_children():
            widget.destroy()
        for widget in self.right_upper.winfo_children():
            widget.destroy()
        self.lbl_topology = tk.Label(self.left_upper, text="Network Topology",bg="#FFF7E4", font=("Helvetica", 10))
        self.lbl_topology.grid(row=0, column=0)

        G = self.generate_graph()
        chosen_algorithm = self.algorithm.get()
        if(chosen_algorithm == "Link State"):
            route_info, elapsed_time = self.compute_routes_dijkstra(G)
            self.display_routing_info_dijkstra(route_info, elapsed_time, G)
            self.display_forwarding_tables_dijkstra(route_info, G)
            plt.show()
        if(chosen_algorithm == "Distance Vector"):
            routes = self.distance_vector_algorithm(G)
            self.display_routing_info_dv(routes, G)
            plt.show()


    def generate_graph(self):
        num_nodes = int(self.n_input.get())
        if num_nodes <= 0:
            raise ValueError("Number of nodes should be a positive integer.")
            
        G = nx.fast_gnp_random_graph(num_nodes, 0.7)
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = random.randint(1, 10)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black',
                font_size=8, edge_color='gray', width=2, edge_cmap=plt.cm.Blues, font_family='sans-serif')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.left_upper)
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        return G
    
    def compute_routes_dijkstra(self, G):
        start_time = time.time()

        all_route_info = {}
        for start_node in range(G.number_of_nodes()):
            for end_node in range(G.number_of_nodes()):
                if start_node != end_node:
                    path, total_cost = self.dijkstra_algorithm(G, start_node, end_node)
                    total_hops = len(path) - 1
                    packet_delay = total_cost
                    all_route_info[(start_node, end_node)] = {'path': path, 'hops': total_hops, 'cost': total_cost, 'delay': packet_delay}

        end_time = time.time()
        elapsed_time = end_time - start_time
        return all_route_info, elapsed_time

    def dijkstra_algorithm(self, graph, start, end):
        visited = {start: 0}
        path = {}
        nodes = set(graph.nodes)
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None or visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break
            nodes.remove(min_node)
            current_weight = visited[min_node]
            for neighbor in graph.neighbors(min_node):
                weight = current_weight + graph[min_node][neighbor]['weight']
                if neighbor not in visited or weight < visited[neighbor]:
                    visited[neighbor] = weight
                    path[neighbor] = min_node
        current = end
        path_list = [current]
        while current != start:
            current = path[current]
            path_list.append(current)
        path_list.reverse()
        return path_list, visited[end]

    def display_routing_info_dijkstra(self, all_route_info,elapsed_time, G):
        for widget in self.right_upper.winfo_children():
            widget.destroy()
        print(f"Running time of Link State Algorithm is: {elapsed_time:.20f} seconds")
        if(G.number_of_nodes() > 5):
            with open("route_info.txt", "w") as file:
                for start_node in range(G.number_of_nodes()):
                    for end_node in range(G.number_of_nodes()):
                        if start_node != end_node:
                            info = all_route_info[(start_node, end_node)]
                            file.write(f"Routing Information ({start_node} to {end_node}): Path: {info['path']}, Hops: {info['hops']}, Cost: {info['cost']}, Delay: {info['delay']} ms\n")
            return
        for start_node in range(G.number_of_nodes()):
            for end_node in range(G.number_of_nodes()):
                if start_node != end_node:
                    info = all_route_info[(start_node, end_node)]
                    routing_info_frame = tk.Frame(self.right_upper)
                    routing_info_frame.grid(row=start_node, column=end_node, padx=5, pady=5, sticky="nsew")

                    label = tk.Label(routing_info_frame, text=f"Routing Information ({start_node} to {end_node}):", font=("Helvetica", 10, "bold"))
                    label.grid(row=0, column=0, columnspan=2, pady=5)

                    path_label = tk.Label(routing_info_frame, text=f"Path: {info['path']}", font=("Helvetica", 8))
                    path_label.grid(row=1, column=0, pady=2)

                    hops_label = tk.Label(routing_info_frame, text=f"Hops: {info['hops']}", font=("Helvetica", 8))
                    hops_label.grid(row=1, column=1, pady=2)

                    cost_label = tk.Label(routing_info_frame, text=f"Cost: {info['cost']}", font=("Helvetica", 8))
                    cost_label.grid(row=2, column=0, pady=2)

                    delay_label = tk.Label(routing_info_frame, text=f"Delay: {info['delay']} ms", font=("Helvetica", 8))
                    delay_label.grid(row=2, column=1, pady=2)


    def display_forwarding_tables_dijkstra(self, all_route_info, G):
        for widget in self.left_lower.winfo_children():
            widget.destroy()

        if(G.number_of_nodes() > 5):
            with open("forwarding_tables.txt", "w") as file:
                for node in range(G.number_of_nodes()):
                    file.write(f"Forwarding Table for Node {node}: \n")
                    for dest_node in range(G.number_of_nodes()):
                        if node != dest_node:
                            info = all_route_info[(node, dest_node)]
                            file.write(f"Dest: {dest_node}, Next Hop: {info['path'][1]}\n")
            return
        for node in range(G.number_of_nodes()):
            table_frame = tk.Frame(self.left_lower)
            table_frame.grid(row=node // 2, column=node%2, padx=5, pady=5, sticky="nsew")

            label = tk.Label(table_frame, text=f"Forwarding Table for Node {node}:", font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=0, columnspan=2, pady=5)

            row_index = 1
            for dest_node in range(G.number_of_nodes()):
                if node != dest_node:
                    info = all_route_info[(node, dest_node)]
                    dest_label = tk.Label(table_frame, text=f"Dest: {dest_node}", font=("Helvetica", 8, "bold"))
                    dest_label.grid(row=row_index, column=0, pady=2)

                    next_hop_label = tk.Label(table_frame, text=f"Next Hop: {info['path'][1]}", font=("Helvetica", 8))
                    next_hop_label.grid(row=row_index, column=1, pady=2)

                    row_index += 1

    def distance_vector_algorithm(self, G):
        distance_vectors = {node: {nodes: {'cost': float('inf'), 'next_hop': None}
                                   for nodes in G.nodes()} for node in G.nodes()}

        for node in G.nodes():
            distance_vectors[node][node] = {'cost': 0, 'next_hop': node}

        times = []

        converged = False
        while not converged:
            self.next_iteration_button["state"] = "normal"
            
            self.master.wait_variable(self.next_iteration_button_pressed)
            self.next_iteration_button_pressed = StringVar()

            self.next_iteration_button["state"] = "disabled"
            start_time = time.time()
            converged = True
            for node in G.nodes():
                for destination in G.nodes():
                    for neighbor in G.neighbors(node):
                        cost_through_neighbor = distance_vectors[neighbor][destination]['cost'] + G[node][neighbor]['weight']
                        if cost_through_neighbor < distance_vectors[node][destination]['cost']:
                            distance_vectors[node][destination]['cost'] = cost_through_neighbor
                            distance_vectors[node][destination]['next_hop'] = neighbor
                            converged = False
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Running time of Distance Vector Algorithm for iteration {self.iteration} is: {elapsed_time:.20f} seconds")
            times.append(elapsed_time)
            self.display_forwarding_tables_dv(self.iteration, distance_vectors, G)
            self.iteration += 1
        
        total_time = 0
        for one_time in times:
            total_time += one_time

        print(f"Total running time of Distance Vector Algorithm is: {total_time:.20f} seconds")
        

        return distance_vectors
    
    def display_routing_info_dv(self, distance_vectors, G):
        for widget in self.right_upper.winfo_children():
            widget.destroy()

        if G.number_of_nodes() > 5:
            with open("route_info.txt", "w") as file:
                for start_node in range(G.number_of_nodes()):
                    for end_node in range(G.number_of_nodes()):
                        if start_node != end_node:
                            info = self.compute_paths(start_node, end_node, distance_vectors)
                            file.write(f"Routing Information ({start_node} to {end_node}): Path: {info['path']}, Hops: {info['hops']}, Cost: {info['cost']}, Delay: {info['delay']} ms\n")
            return

        for start_node in range(G.number_of_nodes()):
            for end_node in range(G.number_of_nodes()):
                if start_node != end_node:
                    info = self.compute_paths(start_node, end_node, distance_vectors)
                    routing_info_frame = tk.Frame(self.right_upper)
                    routing_info_frame.grid(row=start_node, column=end_node, padx=5, pady=5, sticky="nsew")

                    label = tk.Label(routing_info_frame, text=f"Routing Information ({start_node} to {end_node}):", font=("Helvetica", 10, "bold"))
                    label.grid(row=0, column=0, columnspan=2, pady=5)

                    path_label = tk.Label(routing_info_frame, text=f"Path: {info['path']}", font=("Helvetica", 8))
                    path_label.grid(row=1, column=0, pady=2)

                    hops_label = tk.Label(routing_info_frame, text=f"Hops: {info['hops']}", font=("Helvetica", 8))
                    hops_label.grid(row=1, column=1, pady=2)

                    cost_label = tk.Label(routing_info_frame, text=f"Cost: {info['cost']}", font=("Helvetica", 8))
                    cost_label.grid(row=2, column=0, pady=2)

                    delay_label = tk.Label(routing_info_frame, text=f"Delay: {info['delay']} ms", font=("Helvetica", 8))
                    delay_label.grid(row=2, column=1, pady=2)

    def compute_paths(self, start_node, end_node, distance_vectors): 
        info = {'cost': distance_vectors[start_node][end_node]['cost'], 'path':"[", 'hops':0, 'delay':0} 
        info['delay'] = info['cost']
        while start_node != end_node:
            info["path"] += f"{start_node}, "
            info["hops"] += 1
            start_node = distance_vectors[start_node][end_node]['next_hop']
        info["path"] += f"{start_node}]"
        return info

    def display_forwarding_tables_dv(self,iteration, distance_vectors, G):
        for widget in self.left_lower.winfo_children():
            widget.destroy()

        if G.number_of_nodes() > 5:
            if self.iteration == 1:
                with open("forwarding_tables.txt", "w") as file:
                    file.write(f"\nIteration: 1\n")
                    for node in range(G.number_of_nodes()):
                        file.write(f"Forwarding Table for Node {node}: \n")
                        for dest_node in range(G.number_of_nodes()):
                            if node != dest_node:
                                info = distance_vectors[node][dest_node]
                                file.write(f"Dest: {dest_node}, Next Hop: {info['next_hop']}\n")
                return
            with open("forwarding_tables.txt", "a") as file:
                file.write(f"\nIteration: {iteration}\n")
                for node in range(G.number_of_nodes()):
                    file.write(f"Forwarding Table for Node {node}: \n")
                    for dest_node in range(G.number_of_nodes()):
                        if node != dest_node:
                            info = distance_vectors[node][dest_node]
                            file.write(f"Dest: {dest_node}, Next Hop: {info['next_hop']}\n")
            return
        for node in range(G.number_of_nodes()):
            table_frame = tk.Frame(self.left_lower)
            table_frame.grid(row=node // 2, column=node % 2, padx=5, pady=5, sticky="nsew")

            label = tk.Label(table_frame, text=f"Forwarding Table for Node {node}:", font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=0, columnspan=2, pady=5)

            row_index = 1
            for dest_node in range(G.number_of_nodes()):
                if node != dest_node:
                    info = distance_vectors[node][dest_node]
                    dest_label = tk.Label(table_frame, text=f"Dest: {dest_node}", font=("Helvetica", 8, "bold"))
                    dest_label.grid(row=row_index, column=0, pady=2)

                    next_hop_label = tk.Label(table_frame, text=f"Next Hop: {info['next_hop']}", font=("Helvetica", 8))
                    next_hop_label.grid(row=row_index, column=1, pady=2)

                    row_index += 1


    def next_iteration(self):
            self.next_iteration_button_pressed.set(True)

def main():
    root = tk.Tk()
    ui = NetworkSimulationUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

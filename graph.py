import csv
import itertools

class Course:
    def __init__(self, name):
        self.name:      str = name
        self.degree:    int = 0
        self.neighbors: list = []

    def __repr__(self):
        # repr_str = f'Name={self.name}\nDegree={self.degree}\n'
        # return repr_str + f'Neighbors={[x.name for x in self.neighbors]}\n'
        return self.name


class Graph:    
    def __init__(self, data_file):
        self.nodes: list[Course]                    = []
        self.edges: list[tuple[Course, Course]]     = []

        self.people_dict: dict[str: Course]         = {}

        try:
            with open(data_file) as data:
                for row in csv.DictReader(data):
                    course = Course(row['Course'])
                    self.nodes.append(course)

                    for key, value in row.items():
                        if value == '1': 
                            if key in self.people_dict.keys(): 
                                self.people_dict[key].append(course)
                            else: self.people_dict[key] = [course]
                
                for _, course_taken in self.people_dict.items():
                    for edge in itertools.combinations(course_taken, 2):
                        pos = (edge[0], edge[1]) if edge[0].name < edge[1].name else (edge[1], edge[0])

                        if pos not in self.edges: self.edges.append(pos)
        except:
            print('Invalid, unrecognized or nonexistent file. Proceeding.')

        for edge in self.edges:
            edge[0].degree += 1
            edge[1].degree += 1

            if edge[1] not in edge[0].neighbors: edge[0].neighbors.append(edge[1])
            if edge[0] not in edge[1].neighbors: edge[1].neighbors.append(edge[0])

    # Procedural abstraction

    def max_nodes(self, nodes_list: list[Course]) -> Course:
        max_num, max_node = -1, None
        for course in nodes_list:
            if course.degree > max_num:
                max_num = course.degree
                max_node = course
        return max_node

    def not_neighbors_to(self, nodes_to_check: list[Course], used_nodes: list[Course]) -> list[Course]:
        not_neighbors = []
        for node in self.nodes:
            cant_use = []
            for x in nodes_to_check:
                for n in x.neighbors: cant_use.append(n)

            if node not in cant_use + used_nodes: 
                not_neighbors.append(node)
        return not_neighbors

    # Real shit

    def color_nodes(self):
        colored_regions = [[]]
        used_nodes = []

        while len(used_nodes) < len(self.nodes):
            nodes_list = [node for node in self.nodes if node not in used_nodes]
            while len(nodes_list) > 0:
                max_node = Graph.max_nodes(self, nodes_list)

                colored_regions[-1].append(max_node)
                used_nodes.append(max_node)

                nodes_list = Graph.not_neighbors_to(self, colored_regions[-1], used_nodes)

            colored_regions.append([])

        return colored_regions[:-1]
    
    def generate_files(self):
        nodes_file = open('nodes.csv', 'w', encoding = 'utf8')
        edges_file = open('edges.csv', 'w', encoding = 'utf8')
        nodes_writer, edges_writer = csv.writer(nodes_file), csv.writer(edges_file)
        nodes_writer.writerow(['Id', 'Label'])
        edges_writer.writerow(['Source', 'Target', 'Type', 'Subject'])

        idx = 1
        node_dict = {}

        for node in self.nodes:
            nodes_writer.writerow([str(idx), node.name])
            node_dict[node] = idx
            idx += 1

        for edge in self.edges:
            source = node_dict[edge[0]]
            target = node_dict[edge[1]]

            source_name = ''.join(filter(str.isalpha, edge[0].name))
            target_name = ''.join(filter(str.isalpha, edge[1].name))
            if source_name != target_name: source_name = source_name + '-' + target_name
                
            edges_writer.writerow([source, target, 'Undirected', source_name])
            
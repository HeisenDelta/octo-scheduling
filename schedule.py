import csv
import re
import random
from rich.console import Console
from rich.table import Table
from graph import Graph, Course

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

class Schedule(Graph):
    def __init__(self, datafile):
        super().__init__(datafile)
        
        self.headers = None
        with open(datafile, 'r', encoding = 'utf8') as rfile:
            reader = csv.reader(rfile)
            self.headers = next(reader)

    def init_from_data(self, nodes: list[Course], edges: list[tuple[Course, Course]]):
        self.nodes = nodes
        self.edges = edges
        self.people_dict = {}

    # Procedural Abstraction

    def fmt_list(x: list):
         return ' / '.join([''.join([z for z in y.name if z.isalpha()]) for y in x])
    
    # Real shit

    def write_schedule_to_file(self, filename, randomize = False):

        file_obj = open(filename, 'w', encoding = 'utf8')
        writer = csv.writer(file_obj)

        writer.writerow(['Day', 'Period'] + self.headers[1:])

        period_count = 0
        timetable = Graph.color_nodes(self)
        if randomize: random.shuffle(timetable)

        for period in timetable:
            day = DAYS[period_count // 6]
            period_number = (period_count % 6) + 1
            class_choices = []

            for person in self.headers[1:]: 
                class_taken = list(set(self.people_dict[person]) & set(period))
                assert len(class_taken) <= 1
                
                if class_taken: class_choices.append(re.sub(r'\d', '', class_taken[0].name))
                else: class_choices.append('')
 
            writer.writerow([str(day), str(period_number)] + class_choices)
            period_count += 1

    def pretty_print_schedule(self):
        timetable = Graph.color_nodes(self)
        num_days = (len(timetable) // 6) + 1
        timetable += [''] * ((num_days * 6) - len(timetable))

        table = Table(title = 'Schedule')
        for day in DAYS[:num_days]: table.add_column(day)
        for i in range(6):
            table.add_row(*[Schedule.fmt_list(y) for y in [timetable[(j * 6) + i] for j in range(num_days)]])

        console = Console()
        console.print(table)

    def individual_schedule(self, person_name):
        timetable = Graph.color_nodes(self)
        num_days = (len(timetable) // 6) + 1
        timetable += [''] * ((num_days * 6) - len(timetable))

        periods = []
        for period in timetable:
            class_taken = list(set(self.people_dict[person_name]) & set(period))
            assert len(class_taken) <= 1

            if class_taken: periods.append(re.sub(r'\d', '', class_taken[0].name))
            else: periods.append('_')
        
        table = Table(title = person_name + "'s Schedule")
        for day in DAYS[:num_days]: table.add_column(day)

        for i in range(6):
            table.add_row(*[y for y in [periods[(j * 6) + i] for j in range(num_days)]])

        console = Console()
        console.print(table)

if __name__ == '__main__':
    sched = Schedule(datafile = 'csv/school/pos_classes.csv')
    nodes_dict = {node.name: node for node in sched.nodes}

    timetable = sched.color_nodes()

    sched.write_schedule_to_file('csv/school/sched1.csv', randomize = False)
    sched.pretty_print_schedule()
    
    sched.individual_schedule(person_name = 'Ariya')

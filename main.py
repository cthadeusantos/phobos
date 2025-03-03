from source.phobos import Phobos
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

def new_system():
    print("Now we insert the vertices (point) of system\n")

    while True:
        vertex = input("Please insert a vertex (letter or digit) - to exit type * : ")
        if vertex == '*':
            break
        weight = float(input(f"Please insert the weight of {vertex}: "))
        system.add_vertex(vertex, weight)

    print("Now we insert the edges of system\n") 
    while True:
        source = input("Please insert a source vertex (letter or digit) - to exit type * : ")
        if source == '*':
            break
        if source not in system.adjacency_list():
            print(f"Vertex {source} not exist try again")
            continue
        target = input("Please insert a target vertex (letter or digit) - to exit type * : ")
        if target == '*':
            break
        if target not in system.adjacency_list():
            print(f"Vertex {target} not exist try again - you must type source and target vertices again!")
            continue    
        distance = float(input(f"Please insert a distance between {source} and {target}: "))
        cable_id = int(input(f"Please insert an ID cable number between {source} and {target}: "))
        method_id = int(input(f"Please insert an ID to installation method to cable between {source} and {target}: "))

        distributed = 0 # There is not distributed or increase/decrease load in edge
        question1 = input(f"There is a distributed or increase/decrease between {source} and {target}")
        if question1.upper() == "Y":
            question2 = input(f"That is a distributed load (D) or increase/decrease load (Z)? (default is D): ")
            if question2.upper() == "Z":
                distributed = 2 # increase/decrease load
            else:
                distributed = 1 # distributed load
            weight = float(input(f"Please insert a load weight from {source} to {target}: "))
        
        cable_instance = Cable().setting(cable_db.get_cable_especifications(id=cable_id, installation=method_id))

        system.update_edge(source,target, weight, distance, cable=cable_instance, distributed=distributed)

    vline = float(input("Please insert the line voltage: "))
    vphase = float(input("Please insert the phase voltage: "))
    pf = float(input("Please insert the power factor of system: "))
    
    while True:
        root = input("Please insert the root vertex of system: ")
        if root not in system.adjacency_list():
            print(f"{root} is not a vertex in system.")
            continue
        break

    answer = input("Would you like to save (y/n)? SAVE is highly recommend.")
    if answer.upper() != "N":
        file = FileIO()
        data = system.struct_data_to_save()
        
        filename = input("What the name of file do you want to save? ")
        filename = ''.join((filename,'.dp'))
        answer = ''.join(('data/', filename))

        file.save(data, answer)
        print(f"The {filename} was saved at data folder.")

    answer = input("Would you like to compute your system now (y/n)? ")
    if answer.upper() != "N":
        system.compute_system()

def read_file():
    pass

if __name__ == "__main__":

    cable_database = 'databases/mt.db'
    cable_db = CableDBMT(cable_database)

    system = Phobos()

    print("Phobos 0.0.1\nCOMPUTE DROP VOLTAGE\n")
    
    while True:
        answer = input("Please select:\n0. Exit\n1. Read an existing file\n2. Enter a new system and save\nYour choice: ")
        if answer == '0':
            exit()
        elif answer == '1':
            read_file()
        elif answer == '2':
            new_system()
        else:
            pass

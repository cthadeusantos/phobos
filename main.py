from source.phobos import Phobos
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

if __name__ == "__main__":
    file = FileIO()
    a = Phobos()

    a.add_vertex('A', 10)
    a.add_vertex('B', 11)
    a.add_vertex('C', 12)
    a.add_vertex('D', 14)
    a.add_vertex('E', 15)
    a.add_vertex('F', 16)
    a.add_vertex('G', 17)
    a.add_vertex('H', 18)
    a.add_vertex('I', 19)

    cable_database = 'databases/mt.db'

    cable_db = CableDBMT(cable_database)

    cable1 = Cable().setting(cable_db.get_cable_especifications(id=180, installation=2))
    cable2 = Cable().setting(cable_db.get_cable_especifications(id=150, installation=1))
    cable3 = Cable().setting(cable_db.get_cable_especifications(id=88, installation=0))

    a.update_edge('A','C', 21, 100, cable=cable1)
    a.update_edge('A','B', 22, 101, cable=cable1)
    a.update_edge('B','D', 23, 102, cable=cable2)
    a.update_edge('B','E', 24, 103, cable=cable2)
    a.update_edge('E','I', 25, 104, cable=cable1)
    a.update_edge('C','F', 26, 105, cable=cable3)
    a.update_edge('C','H', 26, 106, cable=cable3)
    a.update_edge('G','F', 28, 107, cable=cable3)

    data = a.struct_data_to_save()

    file.save(data, 'data/test.json')
    #data = file.read('data/test.json')
    #print(data)
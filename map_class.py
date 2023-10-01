import xml.etree.ElementTree as ET


class RailMap:
    def __init__(self, source=None):
        self.ways = None
        self.start = None
        self.end = None
        self.objects = None
        if source is None:
            self.build_default()
        else:
            self.load(source)

    def build_default(self):
        self.ways = [['Перегон Ш-А', 1], ["1 путь", 2], ["2 путь", 2], ["ТО локомотива", 1], ["Бригада ПТО", 1],
                     ["Сигналист", 1], ["Перегон А-Б", 1]]
        self.start = 6
        self.end = 22

    def save(self, name):
        root = ET.Element('xml')
        table = ET.SubElement(root, 'table')
        table.set('start', str(self.start))
        table.set('end', str(self.end))
        for way in self.ways:
            way_el = ET.Element('way')
            table.append(way_el)
            way_el.set('name', way[0])
            way_el.set('height', str(way[1]))
        file2write = ET.ElementTree()
        file2write._setroot(root)
        file2write.write(name + '.xml', encoding="UTF-8", xml_declaration=True)

    def load(self, name):
        tree = ET.parse(name)
        root = tree.getroot()
        table = root[0]
        self.start = int(table.attrib['start'])
        self.end = int(table.attrib['end'])
        self.ways = []
        for way in table:
            self.ways.append([way.attrib['name'], int(way.attrib['height'])])

# def build_xml_empty():
#     rows = ['Перегон Ш-А', "1 путь", "2 путь", "ТО локомотива", "Бригада ПТО", "Сигналист", "Перегон А-Б"]
#     cols = list(range(6, 22))
#     r_width = 1
#     min_approx = 2
#
#     root = ET.Element('xml')
#     table = ET.SubElement(root, 'table')
#     table.set('rows', str(len(rows)))
#     table.set('cols', str(len(cols)))
#     for i in range(len(rows)):
#         row = ET.Element('row')
#         table.append(row)
#         row.set('name', rows[i])
#         row.set('width', str(r_width))
#         for j in range(len(cols)):
#             col = ET.Element('col')
#             row.append(col)
#             col.set('date_t', str(cols[i]))
#             col.set('min_approx', str(min_approx))
#     return root

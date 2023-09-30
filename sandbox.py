import flet as ft
import time

import xml.etree.ElementTree as ET

def build_xml_empty():
    rows = ['Перегон Ш-А', "1 путь", "2 путь", "ТО локомотива", "Бригада ПТО", "Сигналист", "Перегон А-Б"]
    cols = list(range(6, 22))
    r_width = 1
    min_approx = 2
    
    root = ET.Element('xml')
    table = ET.SubElement(root, 'table')
    table.set('rows', str(len(rows)))
    table.set('cols', str(len(cols)))
    for i in range(len(rows)):
        row = ET.Element('row')
        table.append(row)
        row.set('name', rows[i])
        row.set('width', str(r_width))
        for j in range(len(cols)):
            col = ET.Element('col')
            row.append(col)
            col.set('date_t', str(cols[i]))
            col.set('min_approx', str(min_approx)) 
    return root

# def main(page: ft.Page):
#     a = ft.Text(value="Hello, world!", color="green")
#     page.controls.append(a)
#     page.update()
#     t = ft.Text()
#     page.add(t) # it's a shortcut for page.controls.append(t) and then page.update()

#     page.add(
#     ft.Row(controls=[
#         ft.Text("A"),
#         ft.Text("B"),
#         ft.Text("C")
#     ])
#     )
    
#     for i in range(10):
#         t.value = f"Step {i}"
#         page.update()
#         time.sleep(1)


# def main(page: ft.Page):
#     def pick_files_result(e: ft.FilePickerResultEvent):
#         selected_files.value = (
#             ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
#         )
#         selected_files.update()

#     pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
#     selected_files = ft.Text()

#     page.overlay.append(pick_files_dialog)

#     page.add(
#         ft.Row(
#             [
#                 ft.ElevatedButton(
#                     "Pick files",
#                     icon=ft.icons.UPLOAD_FILE,
#                     on_click=lambda _: pick_files_dialog.pick_files(
#                         allow_multiple=True
#                     ),
#                 ),
#                 selected_files,
#             ]
#         )
#     )

# ft.app(target=main)

def load_map(map_grid, file):
    tree = ET.parse(file)
    root = tree.getroot()
    mg_ = ft.Row(spacing=0, scroll = ft.ScrollMode.ADAPTIVE)
    map_grid.content = mg_

    mg_col = ft.Column(spacing=0)
    for row in root[0]:
        cell = ft.Container(
                                width= 200,
                                height= int(row.attrib['width']) * 100,
                                bgcolor=ft.colors.CYAN,
                                border_radius=0,
                                content = ft.Text(row.attrib['name']),
                                border = ft.border.all(1, ft.colors.BLACK),
                                alignment = ft.alignment.Alignment(0, 0)
                            )
        mg_col.controls.append(cell)
    map_grid.content.controls.append(mg_col)

    for i in range(int(root[0].attrib['cols'])):
        mg_col = ft.Column(spacing=0)
        for row in root[0]:
            cell_content = ft.Row(spacing=0)
            for j in range(60 // int(row[i].attrib['min_approx'])):
                cell_content.controls.append(ft.DragTarget(
                    content=ft.Container(
                        width=10,
                        height=int(row.attrib['width']) * 100,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border = ft.border.all(1, ft.colors.BLUE_GREY_200),
                        border_radius=0,
                    ),
                )
                                   )
            cell = ft.Container(
                                    width= 10 * 60 // int(row[i].attrib['min_approx']),
                                    height= 100,
                                    # bgcolor=ft.colors.CYAN,
                                    border_radius=0,
                                    content = cell_content,
                                    border = ft.border.all(1, ft.colors.BLACK),
                                    alignment = ft.alignment.Alignment(0, 0)
                                )
            mg_col.controls.append(cell)
        map_grid.content.controls.append(mg_col)




        # map_grid.content.controls.append(cell)
        # print(row[0])
    
    # for row in root[0]:
    #     mg_row = ft.Row(spacing=0)
    #     cell = ft.Container(
    #                             width= 200,
    #                             height= int(row.attrib['width']) * 100,
    #                             bgcolor=ft.colors.CYAN,
    #                             border_radius=0,
    #                             content = ft.Text(row.attrib['name']),
    #                             border = ft.border.all(1, ft.colors.BLACK),
    #                             alignment = ft.alignment.Alignment(0, 0)
    #                         )
    #     mg_row.controls.append(cell)
    #     # map_grid.content.controls.append(cell)
    #     # print(row[0])
    #     for column in row:
    #         cell = ft.Container(
    #                             width= 10 * 60 / int(column.attrib['min_approx']),
    #                             height= 100,
    #                             bgcolor=ft.colors.CYAN,
    #                             border_radius=0,
    #                             # content = ft.Text(row.attrib['name']),
    #                             border = ft.border.all(1, ft.colors.BLACK),
    #                             alignment = ft.alignment.Alignment(0, 0)
    #                         )
    #         mg_row.controls.append(cell)
    #     map_grid.content.controls.append(mg_row)

def open_file(page, map_grid):
    def pick_files_result(e: ft.FilePickerResultEvent):
        print(e)
        file = (" ,".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!")
        
        if file != "Cancelled!":
            load_map(map_grid, file)
            
        # map_grid.content = ft.Text(file)
        map_grid.update()
        
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    
    page.overlay.append(pick_files_dialog)
    page.update()
    
    pick_files_dialog.pick_files(allow_multiple=False)

def main(page: ft.Page):
    page.theme_mode = ft.types.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
 
    open = ft.FilledButton(text= "Open", on_click = lambda _: open_file(page, map_grid))
    page.controls.append(open)
    page.update()
    
    map_grid = ft.Container()
    page.add(map_grid)

ft.app(target=main)
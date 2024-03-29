import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="pyoneliner")
dpg.setup_dearpygui()
global selected
global for_selected
selected = None
for_selected = None


class Loop:
    def __init__(self, iterable):
        self.iterable = iterable
        self.statements = []

    def add_statement(self, statement):
        self.statements.append(statement)

    def generate_code(self):
        DE = ", "
        return f"[({DE.join(self.statements)}) for i in {self.iterable}]"

    def set_stat(self, stat):
        self.statements = stat

    @property
    def stat(self):
        return self.statements


global loops
loops = []


def for_lineup():
    global loops
    loop = loops[int(selected.split(" ")[1]) - 1]
    lst = loop.stat
    i = lst.index(dpg.get_value(looplist))
    if i ==0: return
    lst[i], lst[i - 1] = lst[i - 1], lst[i]
    loop.set_stat(lst)
    dpg.configure_item(looplist, items=lst)

def for_linedown():
    global loops
    loop = loops[int(selected.split(" ")[1]) - 1]
    lst = loop.stat
    i = lst.index(dpg.get_value(looplist))
    if i == len(lst)-1: return
    lst[i], lst[i +1] = lst[i + 1], lst[i]
    loop.set_stat(lst)
    dpg.configure_item(looplist, items=lst)

def for_linedelete():
    global loops
    loop = loops[int(selected.split(" ")[1]) - 1]
    lst = loop.stat
    i = lst.index(dpg.get_value(looplist))
    lst.pop(i)
    loop.set_stat(lst)
    dpg.configure_item(looplist, items=lst)


def lineup():
    i = linelist.index(dpg.get_value(listbox))
    if 0 == i:
        return
    linelist[i], linelist[i - 1] = linelist[i - 1], linelist[i]
    dpg.configure_item(listbox, items=linelist)


def linedown():
    i = linelist.index(dpg.get_value(listbox))
    if len(linelist) - 1 == i:
        return
    linelist[i], linelist[i + 1] = linelist[i + 1], linelist[i]
    dpg.configure_item(listbox, items=linelist)


def linedelete():
    linelist.remove(dpg.get_value(listbox))
    dpg.configure_item(listbox, items=linelist)


def load(img):
    width, height, channels, data = dpg.load_image(f"./{img}.png")
    with dpg.texture_registry():
        return dpg.add_static_texture(width, height, data)


def linecreate(value):
    global selected
    print(selected)
    if selected is not None and selected.startswith("for"):
        loop = loops[int(selected.split(" ")[1]) - 1]
        loop.add_statement(value)
        dpg.configure_item(looplist, items=loop.stat)
        return
    linelist.append(value)
    dpg.configure_item(listbox, items=linelist)


def show_menu():
    with dpg.window(label="Choose functionality", width=400, height=400) as win:
        dpg.set_item_pos(win, (500, 0))
        cvar = dpg.add_button(label="Create Variable")
        with dpg.popup(cvar, mousebutton=dpg.mvMouseButton_Left):
            name1 = dpg.add_input_text(label="Enter variable name")
            val = dpg.add_input_text(label="Enter default value")

            def callback():
                linecreate(dpg.get_value(name1) + " := " + dpg.get_value(val))
                dpg.set_value(name1, "")
                dpg.set_value(val, "")

            dpg.add_button(label="Create", callback=callback)
            # TODO - ADD EVENT LISTENER TO SUBMIT FORM
            # dpg.add_key_press_handler(dpg.mvKey_Return, callback=lambda:print("pressed"))
        pout = dpg.add_button(label="Print Output")
        with dpg.popup(pout, mousebutton=dpg.mvMouseButton_Left):
            pstr = dpg.add_input_text(label="Enter formatted string")

            def callback():
                linecreate(f"print(f\"{dpg.get_value(pstr)}\")")
                dpg.set_value(pstr, "")

            dpg.add_button(label="Create", callback=callback)
        elist = dpg.add_button(label="Edit List")
        with dpg.popup(elist, mousebutton=dpg.mvMouseButton_Left):
            name2 = dpg.add_input_text(label="Enter List Name")
            opts1 = ["append", "insert", "remove", "pop", "clear", "reverse"]
            bts1 = dpg.add_radio_button(opts1, default_value="append")
            p1_1 = dpg.add_input_text(label="Enter First parameter")
            p2_1 = dpg.add_input_text(label="Enter Second Parameter (if any)")

            def callback():
                print(dpg.get_value(bts1))
                if (dpg.get_value(p2_1)) == "":
                    linecreate(f"{dpg.get_value(name2)}.{dpg.get_value(bts1)}({dpg.get_value(p1_1)})")
                else:
                    linecreate(
                        f"{dpg.get_value(name2)}.{dpg.get_value(bts1)}({dpg.get_value(p1_1)}, {dpg.get_value(p2_1)})")
                dpg.set_value(name2, "")
                dpg.set_value(p1_1, "")
                dpg.set_value(p2_1, "")

            dpg.add_button(label="Create", callback=callback)
        dlist = dpg.add_button(label="Edit Dictionary")
        with dpg.popup(dlist, mousebutton=dpg.mvMouseButton_Left):
            name3 = dpg.add_input_text(label="Enter Dictionary Name")
            bts2 = dpg.add_radio_button(["clear", "pop", "popitem", "update"])
            p1_2 = dpg.add_input_text(label="Enter First parameter")
            p2_2 = dpg.add_input_text(label="Enter Second Parameter (if any)")

            def callback():
                if (dpg.get_value(p2_2)) == "":
                    linecreate(f"{dpg.get_value(name3)}.{dpg.get_value(bts2)}({dpg.get_value(p1_2)})")
                else:
                    linecreate(
                        f"{dpg.get_value(name3)}.{dpg.get_value(bts2)}({dpg.get_value(p1_2)}, {dpg.get_value(p2_2)})")
                dpg.set_value(name3, "")
                dpg.set_value(p1_2, "")
                dpg.set_value(p2_2, "")

            dpg.add_button(label="Create", callback=callback)
        inp = dpg.add_button(label="Take Input")
        with dpg.popup(inp, mousebutton=dpg.mvMouseButton_Left):
            name4 = dpg.add_input_text(label="Enter variable")
            typ = dpg.add_input_text(label="Type to be cast to")
            msg = dpg.add_input_text(label="Enter Message to display")

            def callback():
                linecreate(f"{dpg.get_value(name4)}:={dpg.get_value(typ)}(input(\"{dpg.get_value(msg)}\"))")
                dpg.set_value(name4, "")
                dpg.set_value(typ, "")

            dpg.add_button(label="Create", callback=callback)
        cus = dpg.add_button(label="Custom command")
        with dpg.popup(cus, mousebutton=dpg.mvMouseButton_Left):
            line = dpg.add_input_text(label="Enter the custom line")

            def callback():
                linecreate(dpg.get_value(line))
                dpg.set_value(line, "")

            dpg.add_button(label="Create", callback=callback)
        forl = dpg.add_button(label="For Loop")
        with dpg.popup(forl, mousebutton=dpg.mvMouseButton_Left):
            it = dpg.add_input_text(label="Enter Iterable")

            def callback():
                global loops
                linecreate(f"for {len(loops) + 1}")
                loops.append(Loop(dpg.get_value(it)))
                dpg.set_value(line, "")

            dpg.add_button(label="Create", callback=callback)
        #TODO- if conditions


up_texture = load("up")
down_texture = load("down")
del_texture = load("delete")

with dpg.window(label="Main Window", tag="Primary Window"):
    linelist = []
    listbox = dpg.add_listbox(linelist, num_items=15, width=400)
    with dpg.child_window(border=True, width=150, height=45) as childWindow1:
        with dpg.group(horizontal=True):
            dpg.add_image_button(up_texture, width=20, height=20, callback=lineup)
            dpg.add_image_button(down_texture, width=20, height=20, callback=linedown)
            dpg.add_image_button(del_texture, width=20, height=20, callback=linedelete)
    with dpg.group(pos=(10, dpg.get_viewport_height() - 350), height=200, width=400):
        looplist = dpg.add_listbox([], num_items=5)
    with dpg.child_window(border=True, width=150, height=45, pos=(10, dpg.get_viewport_height() - 250)) as childWindow:
        with dpg.group(horizontal=True):
            dpg.add_image_button(up_texture, width=20, height=20, callback=for_lineup)
            dpg.add_image_button(down_texture, width=20, height=20, callback=for_linedown)
            dpg.add_image_button(del_texture, width=20, height=20, callback=for_linedelete)


    def on_click():
        global selected
        selected = dpg.get_value(listbox)
        if selected.startswith("for"):
            global loops
            dpg.configure_item(looplist, items=loops[int(selected.split(" ")[1]) - 1].stat)


    dpg.set_item_callback(listbox, on_click)
    dpg.add_button(label="Add line", callback=show_menu, pos=(450, 10))
    DE = ", "


    def callback():
        val = "print(("
        for i in linelist:
            if i.startswith("for"):
                global loops
                val += loops[int(i.split(" ")[1]) - 1].generate_code() + ", "
            else:
                val += i + ", "
        dpg.set_value(output, val[:-2] + ")[-1])")


    dpg.add_button(label="Generate single liner", callback=callback, pos=(450, 40))
    output = dpg.add_input_text(pos=(450, 80), readonly=True)
    dpg.add_text(default_value="Selected Looping Statement contents", pos=(10, dpg.get_viewport_height() - 375))
dpg.set_primary_window("Primary Window", True, )
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

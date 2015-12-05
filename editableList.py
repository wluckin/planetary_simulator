import Tkinter

class EditableOptionMenu(Tkinter.OptionMenu):
    """OptionMenu which allows editing of menu items
    
    Differences between this and Tkinter.OptionMenu:
      1) insert_option() and delete_option() methods
      2) self.menu, self.variable, self.callback exposed (as we need them to add
         menu items later) (last 3 lines in __init__ )
      3) some names changed from foo to Tkinter.foo, in __init__
         as we do "import Tkinter"

    By Abel Daniel, under the same licence as Tkinter. (As code was
    copyed from there.)
    """
    def __init__(self, master, variable, value, *values, **kwargs):
        """copy-paste-modified from Tkinter.OptionMenu, works the same way"""
        kw = {"borderwidth": 2, "textvariable": variable,
              "indicatoron": 1, "relief": Tkinter.RAISED, "anchor": "c",
              "highlightthickness": 2}
        Tkinter.Widget.__init__(self, master, "menubutton", kw)
        self.widgetName = 'tk_optionMenu'
        menu = self.__menu = Tkinter.Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        # 'command' is the only supported keyword
        callback = kwargs.get('command')
        if kwargs.has_key('command'):
            del kwargs['command']
        if kwargs:
            raise TclError, 'unknown option -'+kwargs.keys()[0]
        menu.add_command(label=value,
                 command=Tkinter._setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v,
                     command=Tkinter._setit(variable, v, callback))
        self["menu"] = menu
        
        self.menu=menu
        self.variable=variable
        self.callback=callback
        
    def insert_option(self, index, text):
        """Insert an option to the menu.
        Handling of index is the same as in Tkinter.Menu.insert_command()
        """
        self.menu.insert_command(index, label=text,
            command=Tkinter._setit(self.variable, text, self.callback))

    def delete_option(self, index1, index2=None):
        """Delete options the same way as Tkinter.Menu.delete()"""
        self.menu.delete(index1, index2)

    def change_option(self, index, new_text):
        """Change to new_text
        Bug: doesn't change the selection if the currently selected option
        is changed, fixing this is left as an exercise to the reader"""
        self.menu.entryconfigure(index, label=new_text,
            command=Tkinter._setit(self.variable, new_text, self.callback))



if __name__ == '__main__':
    r=Tkinter.Tk()
    strvar = Tkinter.StringVar()
    test = ("none", "item1", "item2", "item3")
    strvar.set(test[0])
    om = EditableOptionMenu(r, strvar, *test)
    om.pack()

    om.insert_option(4, 'item4')
    om.delete_option(2)
    om.change_option(0, 'baz') # this nicely exposes the bug :)
    r.mainloop()

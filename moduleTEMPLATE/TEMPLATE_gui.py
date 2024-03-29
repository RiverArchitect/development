try:
    import os, sys
    import tkinter as tk
    from tkinter.messagebox import askokcancel, showinfo
    from tkinter.filedialog import *
    import webbrowser
    import logging
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, logging tkinter, webbrowser).")

try:
    # import own routines
    import cTEMPLATE
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\")
    import slave_gui as sg
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\.site_packages\\riverpy\\")
    # ALSO: add the new module path to the \.site_packages\riverpy\config.py
    # All 'vital' packages and functions are loaded and stored, respectivel from \.site_packages\riverpy\fGlobal.py
    from fGlobal import *  # this is the global functions file
except:
    print("ExceptionERROR: Cannot find package files (riverpy).")


class PopUpWindow(object):
    def __init__(self, master):
        """
        This creates a popup window to inquire particular user actions (e.g., "calculate / define parameter")
        Check usage in MainGui.set_value() function
        """
        config.dir2ra = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\"
        top = self.top = tk.Toplevel(master)
        self.l = tk.Label(top, text="Enter value:")
        self.l.pack()
        self.e = tk.Entry(top, width=10)
        self.e.pack()
        self.b = tk.Button(top, text='OK', command=self.cleanup)
        self.b.pack()
        self.top.iconbitmap(config.code_icon)

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


class MainGui(sg.RaModuleGui):
    def __init__(self, from_master):
        sg.RaModuleGui.__init__(self, from_master)
        self.ww = 800  # window width
        self.wh = 840  # window height
        self.title = "TEMPLATE"         # <---------------------- SET MODULE NAME HERE, BUT DO NOT CHANGE CLASS NAME
        self.set_geometry(self.ww, self.wh, self.title)

        # BUILD tkinter ENVIRONMENT - GOOD DOCUMENTATION: https://effbot.org/tkinterbook/
        # define tkinter - variables (changes when users input)
        self.apply_something = tk.BooleanVar()  # see usage with self.cb_name (checkbutton)

        # LABEL EXAMPLE
        self.l_name = tk.Label(self, text="", bg="white")
        self.l_name.grid(sticky=tk.W, row=0, rowspan=2, column=2, columnspan=3, padx=self.xd, pady=self.yd)

        # DROP DOWN ENTRIES (SCROLL BAR WITH LISTBOX)
        self.sb_name = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sb_name.grid(sticky=tk.W, row=2, column=2, padx=0, pady=self.yd)
        self.lb_name = tk.Listbox(self, height=3, width=15, yscrollcommand=self.sb_name.set)
        self.lb_name.grid(sticky=tk.E, row=2, column=1, padx=0, pady=self.yd)
        self.sb_name.config(command=self.lb_name.yview)

        # CHECK BUTTONS
        self.cb_name = tk.Checkbutton(self, text="Geometric mean", variable=self.apply_something,
                                      onvalue="On!", offvalue="Off!")
        self.cb_name.grid(sticky=tk.W, row=2, column=2, padx=self.xd, pady=self.yd)
        self.cb_name.select()

        # BUTTONS
        self.b_name = tk.Button(self, width=55, fg="RoyalBlue3", bg="white",
                                     text="Click to start calculation",
                                     command=lambda: self.run_calculation())
        self.b_name.grid(sticky=tk.EW, row=5, rowspan=1, column=0, columnspan=3, padx=self.xd, pady=self.yd)
        # self.b_name["state"] = "disabled"  # toggle to freeze button (or replace "disabled" with "normal")

        # DROP DOWN MENUS
        self.my_menu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="DROP DOWN MENU", menu=self.my_menu)  # attach it to the menubar
        self.my_menu.add_command(label="Select me", command=lambda: showinfo("Greetings from the menu"))
        self.my_menu.add_command(label="Pop up", command=lambda: self.set_value())

    def run_calculation(self):
        """
        Trigger a calculation with cTEMPLATE.TEMPLATE()
        """
        geo_calc_object = cTEMPLATE.TEMPLATE()

        # inquire input raster name
        dir2raster = askopenfilename(initialdir=".", title="Select input GeoTIFF raster",
                                     filetypes=[('GeoTIFF', '*.tif;*.tiff')])
        result = geo_calc_object.use_spatial_analyst_function(dir2raster)
        geo_calc_object.clear_cache()  # remove temporary calculation files

        if not(result == -1):
            showinfo("SUCCESS", "The result raster %s has been created." % result)
        else:
            showinfo("ERROR", "Something went wrong. Check the logfile and River Architect Troubleshooting Wiki.")

    def set_value(self):
        sub_frame = PopUpWindow(self.master)
        self.master.wait_window(sub_frame.top)
        value = float(sub_frame.value)
        showinfo("INFO", "You entered %s (whatever...)." % str(value))

    def __call__(self):
        self.mainloop()

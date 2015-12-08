""" Will Luckin <will@luckin.co.uk> """

import Tkinter as tk
import tkFileDialog
import tkMessageBox
import json
from orbiter import orbiter
import numpy as np
from numpy.random import rand
from editableList import EditableOptionMenu
from utils import is_number, convert
from tooltip import createToolTip

class mainWindow(tk.Frame):
    """ Represents the main entry point of the application """
    def __init__(self, master, orbiters, running, ax, system=None):
        tk.Frame.__init__(self, master)
        self.orbiters = orbiters
        self.running = running
        self.ax = ax
        self.system = system
        # Scale real-time to system-time. Needed for planetary scale!!
        self.timescale = 1
        
        self.inputFrame = tk.Frame(self)
        self.renderFrame = tk.Frame(self)
        
        self.renderInputs()

        self.grid(column=0, row=0)
        self.inputFrame.grid(column=0, row=0)
        self.renderFrame.grid(column=1, row=0)

    def renderInputs(self):
        # Register a validation command so that only numbers can be entered
        validateCommand = self.register(lambda x: is_number(x) or len(x) == 0)
        
        # ADD THE "TIME" CONTROLS

        timeBox = tk.LabelFrame(self.inputFrame, text="Time controls", padx=5, pady=5)
        timeBox.grid(column=0, row=0, sticky="news")
        timeInputs = []
        tk.Label(timeBox, text="Timescale \n (*10**5 s per real second)").grid(column=0, row=1)
        timeInputs.append(tk.Scale(timeBox, from_=1, to=100, orient="horizontal",
                                   command=self.updateTimescale))
        timeInputs[-1].grid(column=1, row=1, sticky="news")
        createToolTip(timeInputs[-1], "A scaling factor to render the simulation \n faster or slower.")
        timeInputs.append(tk.Button(timeBox, text="Pause the simulation",
                                    command=self.toggleRunning))
        timeInputs[-1].grid(column=0, row=0)
        createToolTip(timeInputs[-1], "Stop the simulation from advancing in time")

        self.timeInputs = timeInputs

        # ADD THE "CREATE NEW SYSTEM" CONTROLS

        systemBox = tk.LabelFrame(self.inputFrame, text="Create a new system", padx=5, pady=5)
        systemBox.grid(column=0, row=1, sticky="news")
        systemInputs = []
        tk.Label(systemBox, text="Number of initial orbiters").grid(column=0, row=0)
        systemInputs.append(tk.Scale(systemBox, from_=0, to=40, orient="horizontal"))
        systemInputs[-1].grid(column=1, row=0)
        createToolTip(systemInputs[-1], "If the system is randomly generated, generate" +
                      "this \n many orbiters.")
        systemInputs.append(tk.Button(systemBox, text="Restart system",
                                      command=self.restartSystem))
        systemInputs[-1].grid(column=0, row=1, sticky="news")
        createToolTip(systemInputs[-1], "Restart the simulation from initial time")
        self.loadButton = tk.Button(systemBox, text="Load an external config", command=self.loadSystem)
        self.loadButton.grid(column=0, row=2)
        createToolTip(self.loadButton, "Load an external configuration to describe the \n"+
                      " initial state of the system")
        self.discardButton = tk.Button(systemBox, text="Discard current config",
                                       command=self.deloadSystem, state=tk.DISABLED)
        self.discardButton.grid(column=0, row=3, sticky="news")
        createToolTip(self.discardButton, "Stop using an external config file.")
        self.systemInputs = systemInputs

        # ADD THE "CREATE NEW" CONTROLS
        
        # Create the master frame for wrapping the "create new" controls
        createBox = tk.LabelFrame(self.inputFrame, text="Add an orbiter", padx=5, pady=5)
        # Render that frame on the master inputs frame
        createBox.grid(column=0, row=2)
        # Create empty lists to hold the subframes and their elements
        createBoxes = []
        createInputs = []
        # Labels for the various subframes
        lf_labels = ["Position", "Velocity", "Acceleration"]
        # Add a wrapper frame to make everything aligned with only one column
        createBoxesWrapper = tk.Frame(createBox)
        createBoxesWrapper.grid(column=0, row=0)
        for i in range(0, 3):
            # Create a new subframe and render it
            createBoxes.append(tk.LabelFrame(createBoxesWrapper, text=lf_labels[i], padx=5, pady=5))
            createBoxes[i].grid(column=i, row=0)
            # Generate the labels
            tk.Label(createBoxes[i], text="x/m:").grid(column=0, row=0)
            tk.Label(createBoxes[i], text="y/m:").grid(column=0, row=1)
            tk.Label(createBoxes[i], text="z/m:").grid(column=0, row=2)
            # Append an empty dictionary to hold the inputs themselves
            createInputs.append({})
            # Generate and render the individual input widgets
            createInputs[i]["x"] = tk.Entry(createBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            createInputs[i]["x"].grid(column=1, row=0)
            createInputs[i]["y"] = tk.Entry(createBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            createInputs[i]["y"].grid(column=1, row=1)
            createInputs[i]["z"] = tk.Entry(createBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            createInputs[i]["z"].grid(column=1, row=2)
        # Create a wrapper frame for the second row. This is getting messy
        createBoxesWrapper2 = tk.Frame(createBox)
        createBoxesWrapper2.grid(column=0, row=1, sticky="W")
        # Create an input frame to hold the miscellanious "create new" inputs (mass, density)
        createBoxes.append(tk.LabelFrame(createBoxesWrapper2, text="Miscellaneous", padx=5, pady=5))
        createBoxes[-1].grid(column=0, row=1)
        # Add labels
        tk.Label(createBoxes[-1], text="Mass/kg:").grid(column=0, row=0)
        # Add input elements
        createInputs.append({})
        createInputs[-1]["mass"] = tk.Entry(createBoxes[-1], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
        createInputs[-1]["mass"].grid(column=1, row=0)
        # Add the "create" button
        createInputs.append({})
        createInputs[-1]["create"] = tk.Button(createBoxesWrapper2, text="Add orbiter",
                                               command = self.addOrbiter)
        createInputs[-1]["create"].grid(column=1, row=1, padx=5, pady=5, sticky="w e n s")

        self.createInputs = createInputs

        # ADD THE "MODIFY ORBITER" CONTROLS

        # Create master frame for holding the "modify" controls
        modifyBox = tk.LabelFrame(self.inputFrame,
                                  text="Modify an existing orbiter", padx=5, pady=5)
        modifyInputs = []
        modifyBox.grid(column=0, row=3, sticky="n e w s")
        tk.Label(modifyBox, text="Select an existing orbiter to modify in the simulation").grid(
            column=0, row=0, sticky="n e w s")
        modifyInputs.append({})
        self.selectedOrbiter = tk.StringVar(modifyBox)
        modifyInputs[0]["orbiter"] = EditableOptionMenu(modifyBox, self.selectedOrbiter, "memes",
                                                        command=self.selectOrbiter)
        modifyInputs[0]["orbiter"].grid(column=0, row=1, sticky="w e n")
        modifyBoxes = []
        modifyBoxesWrapper = tk.Frame(modifyBox)
        modifyBoxesWrapper.grid(column=0, row=2)
        for i in range(0, 3):
            # Create a new subframe and render it
            modifyBoxes.append(tk.LabelFrame(modifyBoxesWrapper, text=lf_labels[i], padx=5, pady=5))
            modifyBoxes[i].grid(column=i, row=0)
            # Generate the labels
            tk.Label(modifyBoxes[i], text="x/m:").grid(column=0, row=0)
            tk.Label(modifyBoxes[i], text="y/m:").grid(column=0, row=1)
            tk.Label(modifyBoxes[i], text="z/m:").grid(column=0, row=2)
            # Append an empty dictionary to hold the inputs themselves
            modifyInputs.append({})
            # Register a validation command so that only numbers can be entered
            validateCommand = self.register(lambda x: is_number(x) or len(x) == 0)
            # Generate and render the individual input widgets
            modifyInputs[i]["x"] = tk.Entry(modifyBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            modifyInputs[i]["x"].grid(column=1, row=0)
            modifyInputs[i]["y"] = tk.Entry(modifyBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            modifyInputs[i]["y"].grid(column=1, row=1)
            modifyInputs[i]["z"] = tk.Entry(modifyBoxes[i], vcmd=(validateCommand, "%P"),
                                            validate=tk.ALL, width=8)
            modifyInputs[i]["z"].grid(column=1, row=2)

        # Add the miscellaneous non-Cartesian bits on their own row
        modifyBoxesWrapper2 = tk.Frame(modifyBox)
        modifyBoxesWrapper2.grid(column=0, row=3, sticky="w")
        modifyBoxes.append(tk.LabelFrame(modifyBoxesWrapper2, text="Miscellaneous", padx=5, pady=5))
        modifyBoxes[-1].grid(column=0, row=0)
        modifyInputs.append({})
        tk.Label(modifyBoxes[-1], text="Mass/kg").grid(column=0, row=0)
        modifyInputs[-1]["mass"] =  tk.Entry(modifyBoxes[-1], vcmd=(validateCommand, "%P"),
                                             validate=tk.ALL, width=8)
        modifyInputs[-1]["mass"].grid(column=1, row=0)
        modifyInputs.append({})
        modifyInputs[-1]["create"] = tk.Button(modifyBoxesWrapper2, text="Commit changes",
                                               command = self.modifyOrbiter)
        modifyInputs[-1]["create"].grid(column=1, row=0, padx=5, pady=5, sticky="w e n s")
        self.modifyInputs = modifyInputs
        self.modifyError = tk.Label(modifyBoxesWrapper2, text="Some values were invalid. Please try again")
        
    def renderGraphs(self):
        pass

    def toggleRunning(self):
        """ Pause or unpause the animation dependant on current state """
        if self.running:
            self.timeInputs[1].config(text="Resume the simulation")
            self.running = False
        else:
            self.timeInputs[1].config(text="Pause the simulation")
            self.running = True

    def restartSystem(self):
        """ Regenerate a system at t=0 with the number of orbiters chosen. """
        self.orbiters = []
        self.ax.clear()
        if self.system == None:
            for i in range(0, self.systemInputs[0].get()):
                pos_ = (rand(3)*46e7)-23e7
                orbiter(pos=pos_,
                        vel=np.array([pos_[2]/200, pos_[1]/200,
                                      (np.random.ranf() - 0.5)*pos_[0]/20000]),
                        mass=10e27,
                        axis=self.ax,
                        orbiters=self.orbiters)
            orbiter(mass=1e30,
                    pos=np.array([0., 0., 0.]),
                    vel=np.array([0., 0., 0.]),
                    axis=self.ax,
                    orbiters=self.orbiters,
                    name="Big thing")
            self.ax.set_xlim(-1e9, 1e9)
            self.ax.set_ylim(-1e9, 1e9)
            self.ax.set_zlim(-1e9, 1e9)            
        else:
            for i in self.system:
                i = convert(i)
                i.update({"axis": self.ax, "orbiters": self.orbiters})
                orbiter(**i)
            x_max = np.amax(np.array([x.pos[0] for x in self.orbiters]))
            y_max = np.amax(np.array([x.pos[1] for x in self.orbiters]))
            z_max = np.amax(np.array([x.pos[2] for x in self.orbiters]))
            axis_max = max(x_max, y_max, z_max)
            self.ax.set_xlim(-axis_max, axis_max)
            self.ax.set_ylim(-axis_max, axis_max)
            self.ax.set_zlim(-axis_max, axis_max)
        self.updateList()


    def addOrbiter(self):
        """ Add a new orbiter to the system at current time """
        try:
            orbiter(pos=np.array([float(self.createInputs[0]["x"].get()),
                                  float(self.createInputs[0]["y"].get()),
                                  float(self.createInputs[0]["z"].get())]),
                    vel=np.array([float(self.createInputs[1]["x"].get()),
                                  float(self.createInputs[1]["y"].get()),
                                  float(self.createInputs[1]["z"].get())]),
                    acc=np.array([float(self.createInputs[2]["x"].get()),
                                  float(self.createInputs[2]["y"].get()),
                                  float(self.createInputs[2]["z"].get())]),
                    axis=self.ax,
                    mass=float(self.createInputs[3]["mass"].get()),
                    orbiters=self.orbiters)
            self.updateList()
        except ValueError:
            tkMessageBox.showerror("Invalid entry", "All fields must be populated" +
                                   " and valid numbers.")

    def updateList(self):
        """ Update the list of orbiters in the 'modify' dropdown to contain only
        the current orbiters. """
        self.modifyInputs[0]["orbiter"].delete_option(0, tk.END)
        for orb in self.orbiters:
            self.modifyInputs[0]["orbiter"].insert_option(0, str(orb))

    def selectOrbiter(self, selected):
        """ Modify the Entry boxes in the'modify' section to contain the
        current values of an orbiter. """
        try:
            orb = [x for x in self.orbiters if str(x) == selected][0]
            for x in self.orbiters:
                x.reset_color()
                orb.line.set_color((1, 0, 0))
                if not orb == None:
                    for i in range(0, 3):
                        q = [orb.pos, orb.vel, orb.acc][i]
                        for j in range(0, 3):
                            self.modifyInputs[i][["x", "y", "z"][j]].delete(0, tk.END)
                            self.modifyInputs[i][["x", "y", "z"][j]].insert(0, int(q[j]))
                    self.modifyInputs[-2]["mass"].delete(0, tk.END)
                    self.modifyInputs[-2]["mass"].insert(0, int(orb.mass))
        except IndexError:
            pass

    def modifyOrbiter(self):
        """ Commit the changes in the modify boxes to the state of the selected
        orbiter at current time. """
        try:
            selected = self.selectedOrbiter.get()
            orb = [x for x in self.orbiters if str(x) == selected][0]
            if not orb == None:
                pos_ = [float(self.modifyInputs[0][["x", "y", "z"][j]].get()) for j in range(0, 3)]
                vel_ = [float(self.modifyInputs[1][["x", "y", "z"][j]].get()) for j in range(0, 3)]
                acc_ = [float(self.modifyInputs[2][["x", "y", "z"][j]].get()) for j in range(0, 3)]
                mass_ = float(self.modifyInputs[-2]["mass"].get())
                if mass_ < 0.0001:
                    raise ValueError
                orb.pos = np.array(pos_)
                orb.vel = np.array(vel_)
                orb.acc = np.array(acc_)
                orb.mass = mass_
                self.modifyError.grid_forget()
        except IndexError:
            # Selected an orbiter that doesn't exist anymore
            if self.selectedOrbiter.get() == "":
                tkMessageBox.showerror("Invalid selection", "Please select an orbiter from" +
                                       " the dropdown menu.")
            self.updateList()
        except ValueError:
            # Entered invalid values
            tkMessageBox.showerror("Invalid values", "Some or more of the chosen values" +
                                   " are not valid. Please recify these values and try again.")

    def loadSystem(self):
        """ Use an external file to describe the initial state of the system """
        filename = tkFileDialog.askopenfilename()
        try:
            with open(filename) as f:
                self.system = json.load(f)
                self.restartSystem()
                self.discardButton.config(state=tk.NORMAL)
                self.systemInputs[0].config(state=tk.DISABLED)
        # I admit this is slightly nasty, but a myriad of errors are thrown based on
        # the different ways the JSON can be malformed, and providing different
        # error codes in this case is not particularly useful to the end user, seeing as I
        # wrote the JSON provided!
        except Exception:
            tkMessageBox.showwarning("Open file", "This file contains malformed JSON. (Error code 1A)")

    def deloadSystem(self):
        """ Stop using an external config file to describe the initial state """
        self.system = None
        self.discardButton.config(state=tk.DISABLED)
        self.systemInputs[0].config(state=tk.NORMAL)
        self.restartSystem()

    def updateTimescale(self, value):
        """ Mutate the self variable when the slider is moved """
        self.timescale = int(value)

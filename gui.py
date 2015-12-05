""" Will Luckin <will@luckin.co.uk> """

import Tkinter as tk
from orbiter import orbiter
import numpy as np
from numpy.random import rand

class mainWindow(tk.Frame):
    """ Represents the main entry point of the application """
    def __init__(self, master, orbiters, running, ax):
        tk.Frame.__init__(self, master)
        self.orbiters = orbiters
        self.running = running
        self.ax = ax
        self.grid(column=0, row=0)
        self.inputFrame = tk.Frame(self)
        self.renderFrame = tk.Frame(self)
        self.createInputs()
        self.inputFrame.grid(column=0, row=0)
        self.renderFrame.grid(column=1, row=0)

    def createInputs(self):

        # ADD THE "TIME" CONTROLS

        timeBox = tk.LabelFrame(self.inputFrame, text="Time controls", padx=5, pady=5)
        timeBox.grid(column=0, row=0, sticky="news")
        timeInputs = []
        timeInputs.append(tk.Button(timeBox, text="Pause the simulation",
                                    command=self.toggleRunning))
        timeInputs[-1].grid(column=0, row=0)

        self.timeInputs = timeInputs

        # ADD THE "CREATE NEW SYSTEM" CONTROLS

        systemBox = tk.LabelFrame(self.inputFrame, text="Create a new system", padx=5, pady=5)
        systemBox.grid(column=0, row=1, sticky="news")
        systemInputs = []
        tk.Label(systemBox, text="Number of initial orbiters").grid(column=0, row=0)
        systemInputs.append(tk.Scale(systemBox, from_=0, to=40, orient="horizontal"))
        systemInputs[-1].grid(column=1, row=0)
        systemInputs.append(tk.Button(systemBox, text="Restart system",
                                      command=self.restartSystem))
        systemInputs[-1].grid(column=0, row=1)

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
            # Register a validation command so that only numbers can be entered
            validateCommand = self.register(lambda x: x.isdigit() or len(x) == 0)
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
        modifyInputs[0]["orbiter"] = tk.OptionMenu(modifyBox, self.selectedOrbiter, "memes",
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
            validateCommand = self.register(lambda x: x.isdigit() or len(x) == 0)
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
                                               command = None)
        modifyInputs[-1]["create"].grid(column=1, row=0, padx=5, pady=5, sticky="w e n s")

        self.modifyInputs = modifyInputs

    def renderGraphs(self):
        pass

    def toggleRunning(self):
        self.running = True if self.running == False else False

    def restartSystem(self):
        self.orbiters = []
        self.ax.clear()
        for i in range(0, self.systemInputs[0].get()):
            pos_ = (rand(3)*1000)-400
            orbiter(pos=pos_,
                    vel=np.array([pos_[1]/2, -pos_[0]/2, (np.random.ranf() - 0.5)*pos_[2]/2]),
                    mass=np.random.ranf()*10000,
                    axis=self.ax,
                    orbiters=self.orbiters)
        orbiter(mass=7500000.,
                pos=np.array([0., 0., 0.]),
                vel=np.array([0., 0., 0.]),
                axis=self.ax,
                orbiters=self.orbiters)
        self.updateList()
        print self.orbiters

    def addOrbiter(self):
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

    def updateList(self):
        self.modifyInputs[0]["orbiter"]["menu"].delete(0, tk.END)
        for orb in self.orbiters:
            self.modifyInputs[0]["orbiter"]["menu"].add_command(label=str(orb),
                                                                command=tk._setit(self.selectedOrbiter,
                                                                                  str(orb)))

    def selectOrbiter(self):
        print "memes"
        orb = [x for x in self.orbiters if str(x) == self.selectedOrbiter.get()][0]
        print("Selected orbiter: {}".format(orb))
        for i in range(0, 3):
            for j in ["x", "y", "z"]:
                self.modifyInputs[i][j].delete(0, tk.END)
        for input in [self.modifyInputs[0][["x", "y", "z"][i]] for i in range(0, 3)]:
            input.insert(0, orb.pos[i])

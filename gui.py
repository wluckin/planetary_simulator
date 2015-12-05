""" Will Luckin <will@luckin.co.uk> """

import Tkinter as tk

class mainWindow(tk.Frame):
    """ Represents the main entry point of the application """
    def __init__(self, master, funcs=[None, None, None, None]):
        tk.Frame.__init__(self, master)
        self.grid(column=0, row=0)
        self.inputFrame = tk.Frame(self)
        self.renderFrame = tk.Frame(self)
        self.funcs = funcs
        self.createInputs()
        self.inputFrame.grid(column=0, row=0)
        self.renderFrame.grid(column=1, row=0)

    def createInputs(self):

        # ADD THE "TIME" CONTROLS

        timeBox = tk.LabelFrame(self.inputFrame, text="Time controls", padx=5, pady=5)
        timeBox.grid(column=0, row=0, sticky="news")
        timeInputs = []
        timeInputs.append(tk.Button(timeBox, text="Pause the simulation", command=self.funcs[0]))
        timeInputs[-1].grid(column=0, row=0)

        # ADD THE "CREATE NEW SYSTEM" CONTROLS

        systemBox = tk.LabelFrame(self.inputFrame, text="Create a new system", padx=5, pady=5)
        systemBox.grid(column=0, row=1, sticky="news")
        systemInputs = []
        systemInputs.append(tk.Label(systemBox, text="Number of initial orbiters"))
        systemInputs[-1].grid(column=0, row=0)
        systemInputs.append(tk.Scale(systemBox, from_=0, to=40, orient="horizontal"))
        systemInputs[-1].grid(column=1, row=0)
        systemInputs.append(tk.Button(systemBox, text="Restart system", command=self.funcs[1]))
        systemInputs[-1].grid(column=0, row=1)

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
                                               command = self.funcs[2])
        createInputs[-1]["create"].grid(column=1, row=1, padx=5, pady=5, sticky="w e n s")

        # ADD THE "MODIFY ORBITER" CONTROLS

        # Create master frame for holding the "modify" controls
        modifyBox = tk.LabelFrame(self.inputFrame,
                                  text="Modify an existing orbiter", padx=5, pady=5)
        modifyInputs = []
        modifyBox.grid(column=0, row=3, sticky="n e w s")
        tk.Label(modifyBox, text="Select an existing orbiter to modify in the simulation").grid(
            column=0, row=0, sticky="n e w s")
        modifyInputs.append({})
        modifyInputs[0]["orbiter"] = tk.Listbox(modifyBox, height=5)
        modifyInputs[0]["orbiter"].grid(column=0, row=1, sticky="w e n")
        for item in [str(i) for i in range(1, 15)]:
            modifyInputs[0]["orbiter"].insert(tk.END, item)

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
                                               command = self.funcs[3])
        modifyInputs[-1]["create"].grid(column=1, row=0, padx=5, pady=5, sticky="w e n s")

    def renderGraphs(self):
        pass

root = tk.Tk()
memes = mainWindow(root)
memes.mainloop()

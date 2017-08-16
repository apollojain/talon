import Tkinter
import tkFileDialog
import os, pickledb



class App:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.wm_title("Img Classify ")
        frame = Tkinter.Frame(self.root).pack()
        label = Tkinter.Label(text="Image Classify").pack()
        self.button = Tkinter.Button(frame, 
                            text="Choose", 
                            command=self.get_file_path, 
                            width=50)
        self.button.pack(side=Tkinter.LEFT)
        self.root.mainloop()

    def save_directory(self, directory_path):
        db = pickledb.load('example.db', False)
        db.set("directory", directory_path)
        filename = 'directory_path.txt'
        try:
            os.remove(filename)
        except OSError:
            pass
        f = open(filename, 'w')
        f.write(directory_path)
        f.close()

    def quit(self):
        print "DESTROYING"
        self.root.destroy()
        self.root.quit()

    def get_file_path(self): 
        local = Tkinter.Tk()
        local.withdraw() #use to hide tkinter window

        currdir = os.getcwd()
        tempdir = tkFileDialog.askdirectory(parent=local, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            self.save_directory(tempdir)
            self.quit()
            




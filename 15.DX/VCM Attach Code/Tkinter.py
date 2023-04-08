#tkinter GUI
from tkinter import *
from PIL import ImageTk,Image

#create window
root = Tk()
root.title("VCM") #set title
root.iconbitmap("D:/1.Image/Copy1.jpeg") #set icon for app

#import img as label
#my_img = ImageTk.PhotoImage(Image.open("D:/1.Image/qub0v52rls551.png"))
#my_label2 = Label(image=my_img)
#my_label2.pack()
#mylabel2.grid_forget() --- delete if there is a grid




#creating LABEL widget
myLabel = Label(root, text = "VCM Tool").pack()
myLabel1 = Label(root, text = "VCM Too1").pack()
    #myLabel.pack() #pack widget to root
    #myLabel.grid(row=0,column=0)
    #myLabel1.grid(row=1,column=0,columnspan= x-for later y-row with the same x colunmn)
    


#BUTTON Widget
myButton = Button(root, text= "Open file",fg ="blue",bg ="red" ).pack()  
    #myButton = Button(root, text= "Open file",state = DISABLE)---grey button can't click
    #padx= , pady= ----size of button
    #command = name of def, without ()
    #fg = color of text button (e.g "red","blue")
    #bg = color of background button
Button_quit = Button(root,text="Quit",fg="green",bg="lightskyblue1",command = root.quit)
Button_quit.pack()

#ENTRY widget-input text in a white box
Myentry = Entry(root,width=50).pack()
    #width = ,borderwidth = --- width of text box, thêm lề sụt xuống
    #bg, fg is availble as well
    #.get() get the value on text box 
    #.delete(start,end) -- delete on text box



#keep the app continue to run
root.mainloop()




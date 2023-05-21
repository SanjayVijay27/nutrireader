from tkinter import *
from analyze import *
from tkinter_webcam import webcam
import cv2 as cv
from PIL import Image, ImageTk
from mindee import Client, documents
import base64

#Init mindee client
mindee_client = Client(api_key="6162e2afb589929eba2d4ddfc5254369").add_endpoint(
    account_name="westfordjack",
    endpoint_name="nutrition_label",
)



#for field_name, field_values in result.document.fields.items():
   # print(field_name, "=", field_values)

#define colors
bg_color = "#121212"
level1_color = "#1e1e1e"
level2_color = "#242424"
level3_color = "#2c2c2c"
level4_color = "#333333"
level5_color = "#383838"
primary_color = "#03DAC6"
secondary_color = "#BB86FC"
tertiary_color = "#3700B3"
error_color = "#CF6679"

#define dimensions
width = 500
height = 500

#create main window
main_window = Tk()
main_window.title("Nutrireader")
main_window.geometry(str(width) + "x" + str(height))
main_window.config(bg=bg_color)
main_window.resizable(height=None, width=None)

#create title frame
title_frame = Frame(main_window, bg=level1_color, width=width, height = 50)
title_frame.grid(row=0, column=0)
title_frame.pack_propagate(False)

#create title label
title_label = Label(title_frame,text="Nutrireader",font=("Roboto", '30', 'bold'),bg=level1_color,fg="white")
title_label.pack()

#create frames, labels, and entries for ingredients
data_frame = Frame(main_window, bg=level1_color)
data_frame.grid(row=1, column=0)

#serving size input
serv_label1 = Label(data_frame, font=("Roboto", 10), text="Serving Size:", bg=level1_color, fg = 'white')
serv_label1.grid(row=0, column=0)
serv_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
serv_entry.grid(row=0, column=1)
serv_label2 = Label(data_frame, font=("Roboto", 10), text="g", bg=level1_color, fg = 'white')
serv_label2.grid(row=0, column=2)

#calories per serving
cal_label1 = Label(data_frame, font=("Roboto", 10), text="Calories Per Serving:", bg=level1_color, fg = 'white')
cal_label1.grid(row=1, column=0)
cal_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
cal_entry.grid(row=1, column=1)
cal_label2 = Label(data_frame, font=("Roboto", 10), text="cal", bg=level1_color, fg = 'white')
cal_label2.grid(row=1, column=2)

#saturated fat per serving
sat_fat_label1 = Label(data_frame, font=("Roboto", 10), text="Saturated Fat Per Serving:", bg=level1_color, fg = 'white')
sat_fat_label1.grid(row=2, column=0, sticky="E")
sat_fat_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sat_fat_entry.grid(row=2, column=1)
sat_fat_label2 = Label(data_frame, font=("Roboto", 10), text="g", bg=level1_color, fg = 'white')
sat_fat_label2.grid(row=2, column=2)

#sodium per serving
sodium_label1 = Label(data_frame, font=("Roboto", 10), text="Sodium Per Serving:", bg=level1_color, fg = 'white')
sodium_label1.grid(row=3, column=0)
sodium_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sodium_entry.grid(row=3, column=1)
sodium_label2 = Label(data_frame, font=("Roboto", 10), text="mg", bg=level1_color, fg = 'white')
sodium_label2.grid(row=3, column=2)

#fiber per serving
fiber_label1 = Label(data_frame, font=("Roboto", 10), text="Fiber Per Serving:", bg=level1_color, fg = 'white')
fiber_label1.grid(row=4, column=0)
fiber_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
fiber_entry.grid(row=4, column=1)
fiber_label2 = Label(data_frame, font=("Roboto", 10), text="g", bg=level1_color, fg = 'white')
fiber_label2.grid(row=4, column=2)

#sugar per serving
sugar_label1 = Label(data_frame, font=("Roboto", 10), text="Sugar Per Serving:", bg=level1_color, fg = 'white')
sugar_label1.grid(row=5, column=0)
sugar_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sugar_entry.grid(row=5, column=1)
sugar_label2 = Label(data_frame, font=("Roboto", 10), text="g", bg=level1_color, fg = 'white')
sugar_label2.grid(row=5, column=2)

#protein per serving
protein_label1 = Label(data_frame, font=("Roboto", 10), text="Protein Per Serving:", bg=level1_color, fg = 'white')
protein_label1.grid(row=6, column=0)
protein_entry = Entry(data_frame, font=("Roboto", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
protein_entry.grid(row=6, column=1)
protein_label2 = Label(data_frame, font=("Roboto", 10), text="g", bg=level1_color, fg = 'white')
protein_label2.grid(row=6, column=2)

#submit function
def submit():
    analyze(serv_entry.get(), cal_entry.get(), sat_fat_entry.get(), sodium_entry.get(), fiber_entry.get(), sugar_entry.get(), protein_entry.get())

#image vars
webcam = cv.VideoCapture(0)

#capture image function
def capture():
    result, raw_image = webcam.read()
    if result:
        #get and display image
        converted_image = cv.cvtColor(raw_image, cv.COLOR_BGR2RGB)
        selected_image = Image.fromarray(converted_image)
        final_image = ImageTk.PhotoImage(selected_image)
        display_window = Toplevel(main_window)
        capture_frame = Label(display_window, image=final_image, bg='red')
        capture_frame.pack()

        #OCR
        image_bytes = cv.imencode('.jpg', raw_image)[1].tobytes()
        result = mindee_client.doc_from_bytes(image_bytes, "file.jpg").parse(documents.TypeCustomV1, endpoint_name="nutrition_label")

        #clear fields
        serv_entry.delete(0, END)
        cal_entry.delete(0, END)
        fiber_entry.delete(0, END)
        protein_entry.delete(0, END)
        sat_fat_entry.delete(0, END)
        sodium_entry.delete(0, END)
        sugar_entry.delete(0, END)

        #populate fields
        result = list(result.document.fields.values())
        serv_entry.insert(0, result[2])
        cal_entry.insert(0, result[0])
        fiber_entry.insert(0, result[1])
        protein_entry.insert(0, result[3])
        sat_fat_entry.insert(0, result[4])
        sodium_entry.insert(0, result[5])
        sugar_entry.insert(0, result[6])

        #get rid of windows
        display_window.destroy()
    display_window.mainloop()

        
   


#open camera function
def open_cam():
    #show frames of camera
    def show_frames():
        result, raw_image = webcam.read()
        if result:
            converted_image = cv.cvtColor(raw_image, cv.COLOR_BGR2RGB)
            selected_image = Image.fromarray(converted_image)
            final_image = ImageTk.PhotoImage(selected_image)
            display_frame.imgtk = final_image
            display_frame.config(image=final_image)
            display_frame.config(bg='blue')
            #cam_window.destroy()

        display_frame.after(10, show_frames)
    #initialize frame
    cam_window = Toplevel(main_window)
    display_frame = Label(cam_window, bg='red')
    display_frame.pack()
    capture_button = Button(cam_window, text="Capture", bg=level4_color, fg='white', activebackground=level4_color, activeforeground=primary_color, command=capture)
    capture_button.pack()
    show_frames()
    cam_window.mainloop()
    
    

        
#submit button
submit_button = Button(data_frame, text="Submit", bg=level4_color, fg='white', activebackground=level4_color, activeforeground=primary_color, width=50, command=submit)
submit_button.grid(row=7, column=0, columnspan=3)

#Camera button
submit_button = Button(data_frame, text="Open Camera for Scanning", bg=level4_color, fg='white', activebackground=level4_color, activeforeground=primary_color, width=50, command=open_cam)
submit_button.grid(row=8, column=0, columnspan=3)


#display main window
main_window.mainloop()
from dotenv import load_dotenv
import os
import textwrap
from tkinter import *
from analyze import *
import cv2
from PIL import Image, ImageTk
from mindee import Client, documents

#Load .env
load_dotenv()

#Init mindee client
mindee_client = Client(api_key=os.getenv("API_KEY")).add_endpoint(
    account_name=os.getenv("ACCOUNT_NAME"),
    endpoint_name="nutrition_label",
)

#define colors
bg_color = "#121212"
level1_color = "#1e1e1e"
level2_color = "#242424"
level3_color = "#2c2c2c"
level4_color = "#333333"
level5_color = "#383838"
primary_color = "#03DAC6"
secondary_color = "#BB86FC"
tertiary_color = "#AEC6CF"
error_color = "#CF6679"

#define dimensions
width = 500
height = 500

#create main window
main_window = Tk()
main_window.title("Nutrireader")
main_window.geometry(str(width) + "x" + str(height))
main_window.config(bg=level1_color)
main_window.resizable(height=None, width=None)

#create title frame
title_frame = Frame(main_window, bg=level1_color, width=width, height = 100)
title_frame.grid(row=0, column=0, pady=20)
title_frame.pack_propagate(False)

#create title label
title_label = Label(title_frame,text="Nutrireader",font=("Satoshi", '30', 'bold'),bg=level1_color,fg=primary_color)
title_label.pack()

#create description label
desc_label = Label(title_frame,text="The Best Way to an A in your health",font=("Satoshi", '12', 'bold italic'),bg=level1_color,fg=tertiary_color)
desc_label.pack()

#create frames, labels, and entries for ingredients
data_frame = Frame(main_window, bg=level1_color)
data_frame.grid(row=1, column=0)

#serving size input
serv_label1 = Label(data_frame, font=("Satoshi", 10), text="Serving Size:", bg=level1_color, fg = 'white')
serv_label1.grid(row=0, column=0, sticky="E")
serv_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
serv_entry.grid(row=0, column=1)
serv_label2 = Label(data_frame, font=("Satoshi", 10), text="g", bg=level1_color, fg = 'white')
serv_label2.grid(row=0, column=2, sticky="W")

#calories per serving
cal_label1 = Label(data_frame, font=("Satoshi", 10), text="Calories Per Serving:", bg=level1_color, fg = 'white')
cal_label1.grid(row=1, column=0, sticky="E")
cal_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
cal_entry.grid(row=1, column=1)
cal_label2 = Label(data_frame, font=("Satoshi", 10), text="cal", bg=level1_color, fg = 'white')
cal_label2.grid(row=1, column=2, sticky="W")

#saturated fat per serving
sat_fat_label1 = Label(data_frame, font=("Satoshi", 10), text="Saturated Fat Per Serving:", bg=level1_color, fg = 'white')
sat_fat_label1.grid(row=2, column=0, sticky="E")
sat_fat_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sat_fat_entry.grid(row=2, column=1)
sat_fat_label2 = Label(data_frame, font=("Satoshi", 10), text="g", bg=level1_color, fg = 'white')
sat_fat_label2.grid(row=2, column=2, sticky="W")

#sodium per serving
sodium_label1 = Label(data_frame, font=("Satoshi", 10), text="Sodium Per Serving:", bg=level1_color, fg = 'white')
sodium_label1.grid(row=3, column=0, sticky="E")
sodium_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sodium_entry.grid(row=3, column=1)
sodium_label2 = Label(data_frame, font=("Satoshi", 10), text="mg", bg=level1_color, fg = 'white')
sodium_label2.grid(row=3, column=2, sticky="W")

#fiber per serving
fiber_label1 = Label(data_frame, font=("Satoshi", 10), text="Fiber Per Serving:", bg=level1_color, fg = 'white')
fiber_label1.grid(row=4, column=0, sticky="E")
fiber_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
fiber_entry.grid(row=4, column=1)
fiber_label2 = Label(data_frame, font=("Satoshi", 10), text="g", bg=level1_color, fg = 'white')
fiber_label2.grid(row=4, column=2, sticky="W")

#sugar per serving
sugar_label1 = Label(data_frame, font=("Satoshi", 10), text="Sugar Per Serving:", bg=level1_color, fg = 'white')
sugar_label1.grid(row=5, column=0, sticky="E")
sugar_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
sugar_entry.grid(row=5, column=1)
sugar_label2 = Label(data_frame, font=("Satoshi", 10), text="g", bg=level1_color, fg = 'white')
sugar_label2.grid(row=5, column=2, sticky="W")

#protein per serving
protein_label1 = Label(data_frame, font=("Satoshi", 10), text="Protein Per Serving:", bg=level1_color, fg = 'white')
protein_label1.grid(row=6, column=0, sticky="E")
protein_entry = Entry(data_frame, font=("Satoshi", 10), width=4, bg=level3_color, fg=secondary_color, insertbackground=secondary_color)
protein_entry.grid(row=6, column=1)
protein_label2 = Label(data_frame, font=("Satoshi", 10), text="g", bg=level1_color, fg = 'white')
protein_label2.grid(row=6, column=2, sticky="W")

#radio buttons for type of item
item_type = IntVar()
food_option_frame = Frame(data_frame, bg=level1_color)
food_option_frame.grid(row = 7, column=0, columnspan=3)
type_label = Label(food_option_frame, font=("Satoshi", 10), text="Item Type: ", fg = 'white', bg=level1_color)
type_label.grid(row=0,column=0,sticky="E")
food_button = Radiobutton(food_option_frame, text = "Food", variable=item_type, value = 0, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
food_button.grid(row=0,column=1)
drink_button = Radiobutton(food_option_frame, text = "Drink", variable=item_type, value = 1, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
drink_button.grid(row=0,column=2)

#radio buttons for verboseness
explanation_type = IntVar()
ex_option_frame = Frame(data_frame, bg=level1_color)
ex_option_frame.grid(row = 8, column=0, columnspan=3)
ex_label = Label(ex_option_frame, font=("Satoshi", 10), text="Explanation Length: ", bg=level1_color, fg = 'white')
ex_label.grid(row=0,column=0,sticky="E")
short_button = Radiobutton(ex_option_frame, text = "Short", variable=explanation_type, value = 0, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
short_button.grid(row=0,column=1)
med_button = Radiobutton(ex_option_frame, text = "Medium", variable=explanation_type, value = 1, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
med_button.grid(row=0,column=2)
long_button = Radiobutton(ex_option_frame, text = "Long", variable=explanation_type, value = 2, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
long_button.grid(row=0,column=3)

#submit function
def submit():
    #get results
    score, text = get_info(float(serv_entry.get()), float(cal_entry.get()), float(sat_fat_entry.get()), float(sodium_entry.get()), float(fiber_entry.get()), float(sugar_entry.get()), float(protein_entry.get()), beverage=item_type.get(), verboseness=explanation_type.get())

    #create window for summary
    summary_height = 600
    if explanation_type.get() == 0:
        summary_height = 400
    if explanation_type.get() == 2:
        summary_height = 1000

    summary_window = Toplevel(main_window)
    summary_window.title("Nutrireader Result")
    summary_window.geometry("600x" + str(summary_height))
    summary_window.config(bg=level1_color)
    summary_window.resizable(height=None, width=None)

    #format text
    text = '\n'.join(l for line in text.splitlines() for l in textwrap.wrap(line, width=80))

    #color for score
    score_color = primary_color
    if (score < 40):
        score_color = error_color
    elif (score < 60):
        score_color = secondary_color
    elif (score < 80):
        score_color = tertiary_color

    #Summary of results
    score_label = Label(summary_window, text="Your Score: " + str(score) +"/100",font=("Satoshi", '20', 'bold'),bg=level1_color,fg=score_color)
    score_label.pack(pady=(0, 50))
    summary_label = Label(summary_window, text=text, font=('Satoshi', '12', 'normal'), bg=level1_color, fg = tertiary_color)
    summary_label.pack()

#image vars
webcam = cv2.VideoCapture(0)

#capture image function
def capture():
    result, raw_image = webcam.read()
    if result:
        #get and display image
        converted_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
        selected_image = Image.fromarray(converted_image)
        final_image = ImageTk.PhotoImage(selected_image)
        display_window = Toplevel(main_window)
        capture_frame = Label(display_window, image=final_image, bg='red')
        capture_frame.pack()

        #OCR
        image_bytes = cv2.imencode('.jpg', raw_image)[1].tobytes()
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

        #add zeros
        if (serv_entry.get() == ""):
            serv_entry.insert(0, str(0))
        if (cal_entry.get() == ""):
            cal_entry.insert(0, str(0))
        if (fiber_entry.get() == ""):
            fiber_entry.insert(0, str(0))
        if (protein_entry.get() == ""):
            protein_entry.insert(0, str(0))
        if (sat_fat_entry.get() == ""):
            sat_fat_entry.insert(0, str(0))
        if (sodium_entry.get() == ""):
            sodium_entry.insert(0, str(0))
        if (sugar_entry.get() == ""):
            sugar_entry.insert(0, str(0))

        #get rid of windows
        display_window.destroy()
    display_window.mainloop()

#open camera function
def open_cam():
    #show frames of camera
    def show_frames():
        result, raw_image = webcam.read()
        if result:
            converted_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
            selected_image = Image.fromarray(converted_image)
            final_image = ImageTk.PhotoImage(selected_image)
            display_frame.imgtk = final_image
            display_frame.config(image=final_image)

        #animate frame
        display_frame.after(10, show_frames)
    #initialize frame
    cam_window = Toplevel(main_window)
    cam_window.config(bg=level1_color)
    display_frame = Label(cam_window)
    display_frame.pack()
    capture_button = Button(cam_window, font=('Satoshi', '12', 'normal'), text="Capture", bg=level4_color, fg=error_color, activebackground=level4_color, activeforeground=primary_color, width=50, command=capture)
    capture_button.pack()
    show_frames()
    cam_window.mainloop()
        
#submit button
submit_button = Button(data_frame, text="Submit", font=('Satoshi', '12', 'normal'), bg=level4_color, fg=primary_color, activebackground=level4_color, activeforeground=primary_color, width=50, command=submit)
submit_button.grid(row=9, column=0, columnspan=3, pady=(20,0))

#Camera button
submit_button = Button(data_frame, font=('Satoshi', '12', 'normal'), text="Open Camera for Scanning", bg=level4_color, fg=tertiary_color, activebackground=level4_color, activeforeground=primary_color, width=50, command=open_cam)
submit_button.grid(row=10, column=0, columnspan=3)

#Credits
credits_label = Label(main_window, text="Project for the 2023 Steel City Hacks Hackathon by Sanjay Vijay and Jack Whitman", font=('Satoshi', '10', 'italic'), bg = level1_color, fg = secondary_color, pady=20)
credits_label.grid(row=2, column=0)

#display main window
main_window.mainloop()
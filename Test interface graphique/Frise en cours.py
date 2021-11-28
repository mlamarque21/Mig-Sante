from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
from datetime import date, time, timedelta, datetime
#Récupération des noms des patients

globbing = Path('Liste_patient')
tuple_name = tuple(P.name for P in list(globbing.glob("*")))

#génération de l'interface graphique
window = Tk()
window.title('Projet Orbis amélioré')
window.geometry('1500x1200')
window.configure(bg='blue')
#Choix des données d'affichage
data_type = ['Type 1', 'Type 2', 'Type 3', 'Type 4', 'Type 5']#récupérer les types de données intéressantes

checked = [BooleanVar() for j in range(len(data_type))]
def check():
    """Initialise la liste des cases à cocher dans window"""
    checked = [BooleanVar() for j in range(len(data_type))]
    for i, c in enumerate(data_type):
        if i in [0, 2, 4]:#choix des types de données à afficher initialement
            checked[i].set(True)
        button_loc = Checkbutton(window, text=c, var=checked[i])
        button_loc.place(x=0, y=20*i +100)
    return checked

checked = check()

#Choix des paramètres d'affichage:

#Choix du patient
spin_patient = Spinbox(window, values=tuple_name, width=25, wrap=True)
spin_patient.place(x=0, y=0)

#Choix durée
spin_time = Spinbox(window, values=('6 mois', '1 an', '2 ans', '5 ans', '10 ans'), width=25, wrap=True)
spin_time.place(x=0, y=50)

#Affichage de la frise dans une nouvelle fenêtre
def affichage1():
    """affichage de la frise"""
    #Initialisation de la nouvelle fenêtre
    window_loc = Toplevel(window)
    window_loc.geometry('1500x1200')
    patient = spin_patient.get()
    window_loc.title(patient)

    #données importantes 
    beg_frise, end_frise = (130, 286), (1230, 286)
    current_date = date.today()
    choice_time = spin_time.get()
    if choice_time == '6 mois':
        beg_date = current_date - timedelta(days=180)
    elif choice_time == '1 an':
        beg_date = current_date - timedelta(days=365)
    elif choice_time == '2 ans':
        beg_date = current_date - timedelta(days=730)
    elif choice_time == '5 ans':
        beg_date = current_date - timedelta(days=1825)
    elif choice_time == '10 ans':
        beg_date = current_date - timedelta(days=3650)

    #Chargement des images
    load_frise = Image.open('C:\\Users\\lamar\\OneDrive\\Bureau\\Mines 1A\\MIG santé\\Test interface graphique\\image\\Frise en test.jpg')       
    render_frise = ImageTk.PhotoImage(load_frise)
    load_flag = Image.open('C:\\Users\\lamar\\OneDrive\\Bureau\\Mines 1A\\MIG santé\\Test interface graphique\\image\\drapeau.jpg').resize((100, 100), Image.ANTIALIAS)
    render_flag = ImageTk.PhotoImage(load_flag)
    load_cross = Image.open('C:\\Users\\lamar\\OneDrive\\Bureau\\Mines 1A\\MIG santé\\Test interface graphique\\image\\croix_rouge.jpg').resize((200, 200), Image.ANTIALIAS)
    render_cross = ImageTk.PhotoImage(load_cross)

    #Création du canva
    canvas = Canvas(window_loc, height=1200, width=1500)
    canvas.pack()

    #Affichage de la frise vierge
    frise = canvas.create_image(890, 400,anchor='center', image=render_frise)

    #Légende nom du patient
    legend = Label(window_loc, text=spin_patient.get(), font=("Arial Black", 20), bg='grey')
    legend.place(x=677, y=66, anchor='center')
    
    #Fonction d'affichage drapeau et date
    def mark(time, type):
        """Prend une date et le type d'un élément et l'affiche 
        sur la frise"""
        days_event = abs((time - beg_date).days)
        x_pos = (days_event/((current_date - beg_date).days)) * (end_frise[0] - beg_frise[0]) + beg_frise[0]

        #drapeau
        flag = canvas.create_image(x_pos - 10, beg_frise[1], anchor='center', image=render_flag)
        #date et type d'évènement

        text1 = canvas.create_text(x_pos-30, beg_frise[1]+30, anchor='center', text=time)
        text2 = canvas.create_text(x_pos-30, beg_frise[1]+40, anchor='center', text=type)

        return (flag, text1, text2, x_pos)

    #test de la fonction mark
    l = mark(date(2021, 4, 28), 'test')
    flag = l[0]
    x_pos = l[3]
    #Création des boutons de lecture si les cases ont été cochées, il faut encore créer des fonctions de lecture de fichier
    read_button = [] #liste qui stocke les boutons de lecture
    counter = 0 #permet d'évaluer le nombre de boutons à afficher
    for i, c in enumerate(checked):
        if c.get():
            counter = counter + 1
            print(counter)
            button_loc = Button(window_loc, text=data_type[i], font=('Arial Black', 10), bg='grey')
            button_loc.place(x=x_pos-60, y=beg_frise[1]+20 + 32*counter)
            read_button.append(button_loc)
        else:#permet de conserver les indices i de checked
            read_button.append('test')

    #Affichage date de début/fin 
    event_beg, event_current = mark(beg_date,''), mark(current_date, '')
    
    #Affichage de la croix rouge décorative
    cross_img = canvas.create_image(697, 656, anchor='center', image=render_cross)



    #Déplacement de object pour récupérer des coordonnées inutile pour le code final mais sympa pour coder
    object = flag 
    def left(event):
        x = -10
        y = 0
        canvas.move(object, x, y)
        print(canvas.coords(object))

    def right(event):
        x = 10
        y = 0
        canvas.move(object, x, y)
        print(canvas.coords(object))

    def down(event):
        x = 0
        y = 10
        canvas.move(object, x, y)
        print(canvas.coords(object))
    
    def up(event):
        x = 0
        y = -10
        canvas.move(object, x, y)
        print(canvas.coords(object))

    window_loc.bind("<Left>", left)
    window_loc.bind("<Right>", right)
    window_loc.bind("<Down>", down)
    window_loc.bind("<Up>", up)


    window_loc.mainloop()

#bouton affichage de la frise 
bouton1 = Button(window, text = 'Afficher frise', font=("Arial Black", 10), command=affichage1, bg='White')
bouton1.place(x=200, y=0)


window.mainloop()
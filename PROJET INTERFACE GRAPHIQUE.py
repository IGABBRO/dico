from tkinter import *
from tkinter.messagebox import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
import unicodedata
import sys

def remove_accents(word):
    nfkd_form = unicodedata.normalize('NFKD', word)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

##
def fenetre_erreur (msg):
    fenetre_erreur = Tk()
    fenetre_erreur.configure(background='#388E3C', cursor='tcross')
    fenetre_erreur.title("Selection des paramètres")
    fenetre_erreur.resizable(False, False)
    label = Label(fenetre_erreur, text="Erreur\n"+msg, fg='white', bg='#388E3C')
    label.grid()
    valider=Button(fenetre_erreur, background='#388E3C', highlightbackground='#2E7D32', activebackground='#2E7D32', text="Je comprend, retour", command=fenetre_erreur.destroy, fg='white')
    valider.grid(padx=3, pady=3)
    return


##
def creation_fenetre () :
    fenetre_debut = Tk()
    fenetre_debut.configure(background='#388E3C', cursor='tcross')
    fenetre_debut.title("Selection des paramètres")
    fenetre_debut.resizable(False, False)
    def enter(event = None):
        fenetre_debut.destroy()
        return

    label = Label(fenetre_debut, text="Recherche :",fg='white',bg='#388E3C')
    label.grid()
    word = StringVar()
    saisieword = Entry(fenetre_debut, textvariable=word, width=60, bg='#1B5E20', fg='white')
    saisieword.grid(padx=7, pady=7)

    valider=Button(fenetre_debut, background='#388E3C', highlightbackground='#2E7D32', activebackground='#2E7D32', text="Valider", command=fenetre_debut.destroy, fg='white')
    valider.grid(padx=3, pady=3)
    fenetre_debut.bind("<Return>", fenetre_debut.destroy)

    fenetre_debut.mainloop()

    word = word.get()

    return word

##
def definition (word):
    unaccented_word = remove_accents(word)
    def_final = ""
    def_page = "http://www.larousse.fr/dictionnaires/francais/"+unaccented_word+"/"
    page = urlopen(def_page)
    soup = BeautifulSoup(page, 'html.parser')
    def_brut = soup.findAll("li", attrs={"class": "DivisionDefinition"})
    for i in range(0,len(def_brut)):
        def_final = def_final + "-\n" + def_brut[i].text.strip()

    nom_brut = soup.find("h2", attrs={"class": "AdresseDefinition"})
    nom_final = nom_brut.text.strip()

    nature_brut = soup.find("p", attrs={"class": "CatgramDefinition"})
    nature_final = nature_brut.text.strip()

    return nom_final, nature_final, def_final
#
def synonyme(word):
    unaccented_word = remove_accents(word)
    syn_final = ""
    syn_page = "http://www.crisco.unicaen.fr/des/synonymes/"+unaccented_word
    page = urlopen(syn_page)
    soup = BeautifulSoup(page, 'html.parser')
    syn_brut = soup.findAll("tr", attrs={"style": "height:8px"})
    if len(syn_brut) > 4:
        for i in range(0,4):
            syn_final = syn_final + syn_brut[i].text.strip() + ", "
            syn_final = syn_final + syn_brut[4].text.strip()
    elif len(syn_brut) > 1 :
            for i in range(0,len(syn_brut)-1):
                syn_final = syn_final + syn_brut[i].text.strip() + ", "
                syn_final = syn_final + syn_brut[len(syn_brut)].text.strip()
    elif len(syn_brut) == 1:
        syn_final = syn_brut[0].text.strip()
    else:
        syn_final = "Aucun synonyme trouvé."

    return syn_final
##
def fenetre_resultat (nom_final, nature_final, def_final, syn_final):
    fenetre_resultat = Tk()
    fenetre_resultat.configure(background='#388E3C', cursor='tcross', bg='#388E3C')
    fenetre_resultat.title("Résultats")
    fenetre_resultat.resizable(False, False)
    Label(fenetre_resultat, text=nom_final.title(), width=20, bg='#388E3C', font=('Calibri', 20), fg='white').grid()
    Framebas = Frame(fenetre_resultat, width=75,bg='white').grid()
    Label(Framebas, text="Genre : "+nature_final, font=(None, 14), bg='white').grid(pady=2,padx=5)
    Label(Framebas, text=def_final, font=(None, 16), justify='left', bg='white').grid(padx=5)
    Label(Framebas, fg='#2196F3', text="Synonymes (du plus courant au moins courant) :\n "+syn_final, font=(None, 14), bg='white').grid(pady=2,padx=5)

    Button(fenetre_resultat, background='#388E3C', highlightbackground='#2E7D32', activebackground='#2E7D32', text="Retour", command=fenetre_resultat.destroy, fg='white').grid(padx=3, pady=3)


    fenetre_resultat.mainloop()
    return

##
def test_word(word):
    msg = "Pas de mot rentré !"
    while word=='':
        fenetre_erreur(msg)
        word = creation_fenetre()
    return
# word = '' <-- forcément si tu réinitialisait word a chaque fois ca risquait pas de marcher
#compteur = 0
#while compteur == 0 :
#    if word == '':
#        msg = "Pas de mot rentré !"
#        fenetre_erreur(msg)
#        word = creation_fenetre()
#        msg = ''
#    else : compteur = 1
# c'était une bonne idée le while mais ya plus simple
#msg = "Pas de mot rentré !"
#while word=='':
#    fenetre_erreur(msg)
#    word = creation_fenetre()
#    nom_final, nature_final, def_final = definition(word)
#syn_final = synonyme(word)
#fenetre_resultat(nom_final, nature_final, def_final, syn_final)
#
def main():
    word = creation_fenetre()
    test_word(word)

    nom_final, nature_final, def_final = definition(word)
    syn_final = synonyme(word)

    fenetre_resultat(nom_final, nature_final, def_final, syn_final)
    return

close = 0
if __name__ == "__main__":
    while close == 0:
        main()

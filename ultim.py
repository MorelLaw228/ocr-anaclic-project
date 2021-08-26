import re
import csv 
from spellchecker import SpellChecker


def convert2csv():
    header = ['Element','Unite','Valeur_obtenu', 'Valeur_reference', 'Anteriorite']
    with open('bilan.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f,delimiter = ";")
        writer.writerow(header)
        fichier2 = open("correction0.txt", "a")
        spell = SpellChecker(language=None,distance = 1)
        spell.word_frequency.load_dictionary('medicaleJson.json')
        with open('datasetDcp.txt') as f:
            dictionnary = [''+line.rstrip() for line in f]
        file = open('sortie0.txt', "r")
        #uniteBilan = open('uniteBilan.txt',"r")
        fichier = open("dataResult0.txt", "a")
        with open('uniteBilan.txt') as f:
            uniteBilan = [''+uniteB.rstrip() for uniteB in f]
        for line in file :
            correct_output = []
            output = ''+line.rstrip()
            listOutput = output.split()
            misspelled = spell.unknown(listOutput)
            for word in listOutput:
                correct_output.append(spell.correction(word))
            output = ' '.join(correct_output)
            fichier2.write(output+"\n")
            for element in dictionnary :
                correct_ligne = output if  element.lower() in output.lower() else None
                if correct_ligne is None :
                    pass
                else :
                    correct_ligne = re.sub('([^\\w^*^<^>^=]{3,}[A-Za-z]*)(\\s*[a-zA-Z])*', ' ', correct_ligne)
                    if re.search('([^\\d]+\\d+){2,}',correct_ligne) :
                        for unite in uniteBilan :
                            #print(correct_ligne)
                            #unite = ''+unit.rstrip()
                            #print(unite)
                            valeur = re.search('\\W+\\d+\\W?\\d*\\s'+unite+'\\s\\d+\\W?\\d*\\s\\w?\\s\\d+\\W?\\d*(\\s\\d+\\W?\\d*)?',correct_ligne)
                            #print(valeur)
                            if valeur :
                                valeurBilan = valeur.group(0)
                                #print("mdr")
                                print(" {} {} ".format(element,valeurBilan))
                                print("")
                                data = []
                                data.append(element)
                                data.append(unite)
                                valeurBilan = re.sub(unite, '####', valeurBilan)
                                valeur_obtenu = re.search(r'\d+\W?\s?\d+\s?####',valeurBilan)
                                valeurBilan = re.sub(r'\d+\W?\s?\d+\s?####', '' ,valeurBilan)
                                if valeur_obtenu :
                                    data.append(valeur_obtenu.group(0).rstrip('####'))

                                valeur_reference = re.search(r'\d+\W\d+\s?à\s?\d+\W\d+',valeurBilan)

                                if valeur_reference :
                                    data.append(valeur_reference.group(0))
                                valeurBilan = re.sub(r'\d+\W\d+\s?à\s?\d+\W\d+', '' ,valeurBilan)

                                anteriorite = re.search(r'\d+\W?\s?\d+\W?\d*',valeurBilan)

                                if anteriorite :
                                    data.append(anteriorite.group(0))

                                writer.writerow(data)
                                #fichier.write("\n\n"+correct_ligne+"\n\n")
                                break
                            else:
                                pass
                    else :
                        pass
    fichier.close()
    fichier2.close()

    return fichier,fichier2




    

#with open('ocr.txt') as f:
    #output = [''+line.rstrip() for line in f]

#Correct_ligne = [ output for word in  if dictionnary in output]

#\W?\s?\d+\W?\d*
#\d+\s?à\s?\d+

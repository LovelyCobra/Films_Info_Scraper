import os
import re
import shutil
from pathlib import Path

#Aggregating the content of txt files in the given directory in one txt file
def txt_aggr():
    global dir_path
    dir_path = input("\nThe full path to the folder where your txt files are located:\n\n")
    txt_list = os.listdir(dir_path)
    root =  os.path.join(str(Path.home()), "Videos")
   
    global output_file
    output_file = f"{root}/Full_List.txt"
    if os.path.exists(output_file): os.remove(output_file)
    output_txt = open(output_file, "+a", encoding="utf-8")

    for file in txt_list:
        if ".txt" in file:
            txt_file = open(f"{dir_path}/{file}", "r", encoding='utf-8')
            text = txt_file.read()
            output_txt.write(f"{file}:\n\n{text}\n\n")
            txt_file.close()

    output_txt.close()
    print(f"\nContent of all txt files have been aggregated and saved in \033[92m'{output_file}'\033[0m.\n")


#Counting numbered lines and listing of duplicates
def duplicates():
    with open(output_file, "+r", encoding="utf-8") as file:
        input_txt = file.readlines()
    clean_input = [item.rstrip('\n') for item in input_txt ]

    #Counting lines with titles of movies and number of groups
    count = 0
    groups_count = 0
    for line in clean_input:
        if re.findall("\A[0-9]", line):
            count += 1
        elif re.findall("\A[a-zA-Z]", line):
            groups_count += 1

    #Making a list of duplicates
    ready_input = []
    for item in clean_input:
        if "." in item and ".txt" not in item: 
            ready_input.append(item[item.index('.') + 2:]) #removal of initial numbering
        elif ".txt" in item:
            ready_input.append(item)

    duplicate_list = []
    for title in ready_input:
        n = ready_input.count(title)
        if  n > 1 and [title, n] not in duplicate_list and title != "":
            duplicate_list.append([title, n])

    #Location of duplicates:
    locations = []
    for film in duplicate_list:
        dupl_loc = [f"{film[0]}"]
        m = film[1]
        while m > 0:
            p = ready_input.index(film[0])
            while ".txt" not in ready_input[p]:
                p -= 1
            ready_input.remove(film[0])
            dupl_loc.append(ready_input[p].replace("_Movie_List.txt", ""))
            m -=1
        locations.append(dupl_loc)

    print(f"\nNumber of movies: \033[92m{count}\033[0m.\n") 
    print(f"Number of groups: \033[94m{groups_count}\033[0m\n")
    print("\033[91mList of duplicates:\033[0m\n")
    for item in duplicate_list:
        print(item)
    
    print("\n\nLOCATION OF DUPLICATES:\n")
    for i in range(len(locations)):
        print(f"\nThe film '{locations[i][0].upper()}' is located at:\n")
        for j in range(1, len(locations[i])):
            print(f'    {locations[i][j].replace(":", "")}')
    print('\n')


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    txt_aggr()
    duplicates()
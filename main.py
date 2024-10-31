'''
FILMS INFO WEB SCRAPER
The code goes through all the video files in a given directory or chosen subdirectories of a given
parent directory, collates basic quick info about each from Wikipedia and Rotten Tomatoes websites
if such info exists and saves the info in a separate file named after the videofile name itself in
the same directory.
Additional functionality constists of the option of:
    * Editing the video file names before scraping
    * Making a list of video file names, saved in a text file named after the directory and placed
      in that directory
    * Scraping of the basic quick info about a single film
'''
import os, shutil
import mechanicalsoup as ms
from tqdm import tqdm
from pathlib import Path
import helperfunctions as hf

# Creating list of films in one directory
#########################################

def film_list(dir_path):
    dir_path = dir_path.replace("\\", "/")
    
    try:
        dir_name = dir_path[dir_path.rindex('/')+1 : ]
    except:
        dir_name = dir_path
        
    item_list = os.listdir(dir_path)
    film_list = [item for item in item_list if ('.mp4' in item or '.avi' in item or '.mkv' in item or '.mpg' in item)]
    output_txt = f"{dir_path}/{dir_name}_Movie_List.txt"
    
    with open(output_txt, 'w', encoding='utf-8') as file:
        for n, title in enumerate(film_list):
            file.write(f"{n+1}. {title}\n")
            
    # Creating a new subdirectory 'Film_lists' in the curent user's Videos directory and saving the film list there too
    root_dir = os.path.join(str(Path.home()), "Videos")
    if "Film_lists" not in os.listdir(root_dir):
        os.mkdir(os.path.join(root_dir, 'Film_lists'), mode=0o777)
    root_dir = os.path.join(root_dir, "Film_lists")
            
    shutil.copy(output_txt, root_dir)
    
    return film_list, dir_name


def film_ls_print(fls, dn):
    for n, film in enumerate(fls):
        print(f"{n+1}. {film}")
    
    print(f"\nThe list of films in the named directory was saved in \033[92m{dn}_Movie_List.txt\033[0m file in the same directory.\nThe copy was also saved in \033[92mFilm_lists\033[0m folder in your native user 'Videos' folder.\n")


# Creating lists of films in subdirectories of a parent directory
#################################################################
    
def grand_listing(parent_dir_path):
    parent_dir = parent_dir_path.replace('\\', '/')
    dir_list = [item for item in os.listdir(parent_dir) if '.' not in item]
    
    for dir in dir_list:
        dir_path = os.path.join(parent_dir, dir)
        film_list(dir_path)
    return dir_list

def grand_ls_print(grls):
    for n, dir in enumerate(grls):
        print(f"{n+1}. {dir}")

    print(f"\nThe lists of films in the above directories were created and saved in txt files in the respective directories.\nThe copies were also saved in \033[92mFilm_lists\033[0m folder in your native user 'Videos' folder.\n")
    
    
# Films info SCRAPING limited to ONE chosen directory; info source: Wikipedia and Rotten Tomatoes websites
##########################################################################################################

# Helper function: A single film info Wikipedia SCRAPE
def wiki_single_scrap(film_title, release_year, path):
    wmiss = True
    def first_par_test(address):
        browser.open(address)
        par = browser.page.find_all('p', attrs={"class": None})
        return [value.text for value in par][0]
    
    def wiki_scrape(film_title, release_year, path, address):
        browser.open(address)
        
        th = browser.page.find_all("th", attrs={"class": "infobox-label"})  # Scraping the left side of the table, i.e. labels
        th_text = [value.text for value in th]                              # and extracting only textual content

        td = browser.page.find_all("td", attrs={"class": "infobox-data"})   # scraping the right side of the table, i.e. actual info
        td_text = [value.text for value in td]                              # and extracting only textual content
        
        txt_name = film_title + f'_({release_year})' + '.txt'
        txt_name = txt_name.replace(':', '')
        txt_full_path = os.path.join(path, txt_name)
        
        with open(txt_full_path, 'w', encoding='utf-8') as file:
            file.write(f"{film_title.upper()}\n\n")
            file.write(first_paragr)
            for index, line in enumerate(th_text):
                file.write(f"\n{line}: {td_text[index]}\n")
        browser.close()
        return False
    
    
    
    try:
        browser = ms.StatefulBrowser()
        wiki = hf.from_title_addresses(film_title, release_year)
        first_paragr = first_par_test(wiki[0])
        
        if 'film' in first_paragr and f'{release_year}' in first_paragr:
            wiki_scrape(film_title, release_year, path, wiki[0])
            wmiss = False
        
        else:
           try:
               first_paragr = first_par_test(wiki[1])
               if 'film' in first_paragr and f'{release_year}' in first_paragr:
                   wiki_scrape(film_title, release_year, path, wiki[1])
                   wmiss = False
               else:
                   try:
                       first_paragr = first_par_test(wiki[2])
                       if 'film' in first_paragr and f'{release_year}' in first_paragr:
                           wiki_scrape(film_title, release_year, path, wiki[2])
                           wmiss = False
                   except:
                       wmiss = True
           except:
               wmiss = True
            
    except:
        wmiss = True
    return wmiss
        
# Helper function: A single film info Rotten Tomatoes SCRAPE
def rotten_single_scrap(film_title, release_year, path):
    rmiss = True
    
    rot_address = hf.from_title_addresses(film_title, release_year)[3]
    
    def rot_scrape(film_title, release_year, path):
        browser.open(rot_address)
        
        scores = browser.page.find_all("rt-text", attrs={"size": "1.375", 'context': "label"})
        scores_text = [value.text for value in scores if value.text != '']
        
        txt_name = film_title + f'_({release_year})' + '.txt'
        txt_name = txt_name.replace(':', '')
        txt_full_path = os.path.join(path, txt_name)
        
        with open(txt_full_path, 'a', encoding='utf-8') as file:
            file.write(f"\nFilm Critics Score: {scores_text[0]}\nAudiences Score: {scores_text[1]}")
        return False
    
    browser = ms.StatefulBrowser()

    try:
        rmiss = rot_scrape(film_title, release_year, path)
    except:
        rot_address = rot_address + f"_{release_year}"
        try:
            rmiss = rot_scrape(film_title, release_year, path)
        except:
            rot_address = rot_address[4:]
            try:
                rmiss = rot_scrape(film_title, release_year, path)
            except:
                rmiss = True
        
    return rmiss


# Helper function: One film info SCRAPE
def film_info_scrap(film_title, release_year, path):

    # Wikipedia Quick info table scraping
    wmiss = wiki_single_scrap(film_title, release_year, path)

    # Extract Rotten Tomatoes scores
    rmiss = rotten_single_scrap(film_title, release_year, path)
    
    return [wmiss, rmiss]
        
        
# MAIN function 1: SCRAPING info for all films in a given directory
def subdir_scrap(dir_path, list_edit=True):
    
    #Enabling use of this function both with and without film list prior editing
    if list_edit:
        switch = hf.film_list_edit(dir_path)
    else: switch = 'P' # 'P' stands for 'Proceed'
    
    if switch == 'P':
    
        wiki_path = os.path.join(dir_path, 'wiki.txt')
        wikmiss = []
        rotmiss = []
        miss = []
        success = []
        
        with open(wiki_path, 'r', encoding='utf-8') as films:
            names = films.readlines()
            ind = 0
        
            for i in tqdm(range(len(names)), desc=f"Processing:", ascii=True, colour='green'):
                tails = hf.from_file_name_addresses(names[i])
                
                if len(tails) == 5:
                    releaseyear = tails[4]
                    end_index = names[i].index(' (')
                    film_title = names[i][:end_index].replace('--', ':')
                    
                    [w, r] = film_info_scrap(film_title, releaseyear, dir_path)
                    if w: wikmiss.append(names[i])
                    if r: rotmiss.append(names[i])
                    if not w and not r: success.append(names[i])
                    
                elif len(tails) == 1:
                    miss.append(names[i])
                ind += 1
        
        with open(wiki_path, 'w', encoding='utf-8') as file:
            for film in miss:
                file.write(f"{film}\n")
        with open(wiki_path, 'a', encoding='utf-8') as file:
            for film in wikmiss:
                if film not in miss:
                    file.write(film)
            for film in rotmiss:
                if (film not in miss) and (film not in wikmiss):
                    file.write(film) 
                    
        return miss, wikmiss, rotmiss, success
    
    elif switch == 'A':      # 'A' stands for 'Abort'
        print("\n\033[92mGOODBYE!\033[0M\n")
        return 'switch', 'switch', 'switch', 'switch'    

# MAIN function 2: Same as above, but for all films in chosen subdirectories in a parent directory
def parentdir_scrap(parent_path):
    subdir_list = [item for item in os.listdir(parent_path) if '.' not in item]
    subd_txt_path = os.path.join(parent_path, "subdir_list.txt")
    misses = {}
    print("\n\n\033[94mList of subdirectories in the choosen parent directory\033[0m:\n")
    
    with open(subd_txt_path, 'w', encoding='utf-8') as file:
        for dir in subdir_list:
            file.write(f"{dir}\n")
            print(dir)
            
    cont = input(f"\n\nIf you wish to remove some of the subdirectories to prevent them from being included in the process, you can do so in \033[92m{subd_txt_path}\033[0m text file.\nWhen you are finished with editing, \033[91mdo NOT forget\033[0m to save the edited file.\n\nWhen you are ready to proceed, type 'C' and press 'Enter' to continue.\n\n").upper()
    
    if cont == 'C':
        subds = open(subd_txt_path, 'r', encoding='utf-8')
        for sdir in subds:
            sdir = sdir.rstrip('\n')
            sdir_path = os.path.join(parent_path, sdir)
            print(f"\n\n{sdir}:\n")
            m, w, r = subdir_scrap(sdir_path)
            if m != [] or w != [] or r != []:
                misses[sdir] = [m, w, r]
                
        return misses
    else:
        print("\n\033[91mWrong input, DUMMY!\033[0m")
            
            
    
    
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n\n\033[95mGRAND FILM SCRAPER & PROCESSOR\033[0m\n")
    
    fork = input("\nChoose from these options:\n\n\033[91m1\033[0m. Making a list of films in a chosen directory\n\n\033[91m2\033[0m. Making lists of films in subdirectories of a chosen parent directory\n\n\033[91m3\033[0m. Generating txt files with basic info about each film in a chosen directory, scraped from \033[92mWikipedia\033[0m and \033[92mRotten Tomatoes\033[0m websites.\n\n\033[91m4\033[0m. As above, but this time done with ALL subdirectories in a chosen parent directory.\n\n\033[91m5\033[0m. Scrape quick info about a single film.\n\n")
    
    if fork == '1':
        dir = input("\nWhich directory are your films in?\n\n")
        fl, dn = film_list(dir)
        film_ls_print(fl, dn)
        
    elif fork == '2':
        pardir = input("\nWhich one is your chosen parent directory?\n\n")
        dirls = grand_listing(pardir)
        grand_ls_print(dirls)
        
    elif fork == '3':
        dir = input("\nWhich directory are your films in?\n\n")
        wrong_file_name, wikimiss, rotmiss, success = subdir_scrap(dir)
        
        if wrong_file_name != 'switch':
            fork = 'Y'
            
            while fork == 'Y':
                
                print("\n\nThe films in the chosen directory or subdirectory have been processed.\n\n")
                if success != []:
                    print("\n\nThe info scraping from BOTH Wiki AND Rotten Tomatoes succeeded for these films:\n\n")
                    for item in success:
                        print(item)
                if wrong_file_name != [] or wikimiss != [] or rotmiss != []:
                    print("\033[91mThe process failed for these films\033[0m:\n\n")
                if wrong_file_name != []:
                    print("On \033[92mBOTH\033[0m sites, due to wrongly named file (missing ' (ReleaseYear)' string):")
                    for item in wrong_file_name: print(item)
                if wikimiss != []:
                    print("\nOn \033[92mWIKIPEDIA\033[0m:")
                    for item in wikimiss: print(item)
                if rotmiss != []:
                    print("On \033[92mRotten Tomatoes\033[0m:")
                    for item in rotmiss: print(item)
                
                
                
                print(f"\n\nAll the films for which a failure has occured were saved as a list in '{dir}/wiki.txt' text file.\n\n")
                fork = input("Do you wish to go to that file, do the required edits, SAVE the edited file and try the info scraping again? (Y/N)\n\n\033[91mN O T E\033[0m: If it is the case that only scraping on Rotten Tomatoes fails, it can be corrected only by processing those films individually.\n\n").upper()
                if fork == 'Y': wrong_file_name, wikimiss, rotmiss, success = subdir_scrap(dir, False)
            
            
                    
    elif fork == '4':
        dir = input("\nType in your chosen parent directory:\n\n")
        misses = parentdir_scrap(dir)
        
        for key in misses.keys():
            print(f"\033[95m{key}\033[0m:\n")
            print(f"Wikipedia:\n{misses[key][1]}\n\nRotten Tomatoes:\n{misses[key][2]}\n\nBoth:\n{misses[key][0]}")
    
        print("\n\nText files containing quick info about films in subdirectories of your chosen parent directory have been created, whenever the information has been found. Info scraping may have failed in the cases listed above:\n")
        
    elif fork == '5':
        filmtitle = input("\nType in these three pieces of information:\n\n1. The exact film title (either 'Film_Name' or 'Film Name'):\n\n")
        dir_path = input("\n2. The whole path to the directory where the film info should be saved:\n\n")
        releaseyear = input("\n3. The film's release year:\n\n")
        
        miss = film_info_scrap(filmtitle, releaseyear, dir_path)
        
        if miss == [False, False]:
            print(f"\n\n\033[94mS U C C E S S !!\033[0m\n\nBasic quick info about the given film was scraped from Wikipedia and Rotten Tomatoes website\nand saved as \033[92m{filmtitle}_({releaseyear}).txt\033[0m in the directory: \033[92m{dir_path}\033[0m\n\n")
        elif miss == [False, True]:
            print(f"\n\n\033[94mP A R T I A L  Success !!\033[0m\n\nBasic quick info about the given film was scraped from \033[92mWikipedia\033[0m and saved as \033[92m{filmtitle}_({releaseyear}).txt\033[0m in the directory: \033[92m{dir_path}\033[0m\n\n\033[91mH O W E V E R\033[0m, scraping failed on Rotten Tomatoes site due to the subpage's naming idiosyncrasy.\n\n")
            fork = input("Do you wish to check the Rotten Tomatoes website to add the missing information? (Y/N)\n\n").upper()
            if fork == 'Y':
                rottitle = input("\nWhat is the exact final part of the Rotten Tomatoes website address that contains the scores for your chosen film?:\n\n")
                rmiss = rotten_single_scrap(rottitle, releaseyear, dir_path)
                if rmiss == False:
                    txt_name = filmtitle + f'_({releaseyear})' + '.txt'
                    txt_name = txt_name.replace(':', '')
                    txt_full_path = os.path.join(dir_path, txt_name)
                    rot_full_path = os.path.join(dir_path, rottitle + f'_({releaseyear})' + '.txt')
        
                    with open(txt_full_path, 'a', encoding='utf-8') as file:
                        scores = open(rot_full_path, 'r', encoding='utf-8')
                        add = scores.readlines()
                        for line in add:
                            file.write(f'{line}\n')
                        scores.close()
                        os.remove(rot_full_path)
                        
                    print("\n\n\033[94mB I N G O !!\033[0m\n\nThe scores from the Rotten Tomatoes Website were successfully added. Congratulation!\n\n")
        elif miss == [True, False]:
            print(f"\nScraping info about the film from Wikipedia failed, probably due to a problem with the address. However, at least the Film Critics and Audiences Scores from Rotten Tomatoes were saved in \033[92m{filmtitle}_({releaseyear}).txt\033[0m text file in the directory: \033[92m{dir_path}\033[0m\n\nIf you wish to add info from Wiki, check the exact film title there and try again.\n\n")
        else:
            print(f"\nScraping quick info about the film \033[91mfailed!!\033[0m on both Wikipedia and Rotten Tomatoes. Check the film title on Wiki and try again.\n\n")
       
    
    # w = "https://en.wikipedia.org/wiki"
    # rt = "https://www.rottentomatoes.com/m"
    
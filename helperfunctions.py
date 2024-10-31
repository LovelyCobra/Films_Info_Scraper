import mechanicalsoup as ms
import pandas as pd
import sqlite3, os
from tqdm import tqdm
from main import film_list 

# Helper function: cleaning up film titles in wiki.txt so that they can serve as probable web addresses

def film_list_edit(dir_path):
    film_ls, dir_name = film_list(dir_path)
    sugest_edit = []
    txt_path = os.path.join(dir_path, 'wiki.txt')
    
    with open(txt_path, 'w', encoding='utf-8') as file:
        for n, line in enumerate(film_ls):
            line = line.replace(' ', '_')
            line = line.replace('_(', ' (')
            
            if ' (' not in line:
                sugest_edit.append(n+1)
            
            file.write(f"{n+1}. {line}\n")
            print(f"{n+1}. {line}")
    
    if sugest_edit != []:    
        print(f"""
            \n            The video-names numbered \033[92m{sugest_edit}\033[0m do not contain the required '\033[94m (ReleaseYear)\033[0m' string.
            If you wish, you can open the \033[92m{txt_path}\033[0m file to perform any edit you choose
            (adding the above missing string right after the film's title, removing some of the files etc.)
            When you are finished with editing, \033[91mD O    N O T   F O R G E T !!\033[0m to save the edited txt file!
            You can also proceed without any editing. Info for films with incorrect path-names will not be created.\n
            """)
    else:
        print(f"\nThe above list of movie titles have been created.\nIf you wish to edit it, you can do so by opening the \033[92m{txt_path}\033[0m file.\nWhen you are done with editing, \033[91mD O   N O T   F O R G E T !!t\033[0m to save the edited file!\n\n")
        
    fork = input("When you are ready, choose one of these options:\n\n\033[91mP\033[0m - Proceed!\n\n\033[91mA\033[0m - Abort!\n\n").upper()
    
    if fork == 'P':
        webtails = os.path.join(dir_path, 'webtails.txt')
        with open(webtails, 'w', encoding='utf-8') as file:
            wiki = open(txt_path, 'r', encoding='utf-8')
            lines = wiki.readlines()
            
            for line in lines:
                start = line.index('. ') + 2
                line = line[start:]
                file.write(f"{line}")
            wiki.close()
                
        os.remove(txt_path)
        os.rename(webtails, txt_path)
        
    elif fork == 'A':
        print("\n\nProcess aborted.\n")
        
    return fork
           

def web_address_cleaning(root_site, sub_site_extension):
    final = os.path.join(root_site, sub_site_extension)
    final = final.replace("\\", "/")
    final = final.replace("\n", '')
    return final
    
'''Creating a list of probable web addresses of Wiki and Rotten Tomatoes pages that show movies info.
Video files' names should start with exact names of the films in question with words separated by '_';
the last word of each movie title should be followed by ' (1997)' - one space followed by the release year in round brackets.
If a movie official title contains ':', in the movie file name it should be represented by "--" double dash'''

# Generating a list of possible Wiki and Rotten Tomatoes addresses from a film's official title and release year
def from_title_addresses(film_title, release_year):
    film_title = film_title.replace(' ', '_')
    first = web_address_cleaning("https://en.wikipedia.org/wiki", film_title)
    second = first + '_(film)'
    third = first + f'_({release_year}_film)'
    film_title = film_title.replace('_-', '')
    film_title = film_title.replace(':', '')
    rot = web_address_cleaning("https://www.rottentomatoes.com/m", film_title)
    return [first, second, third, rot.lower(), release_year]

# Generating a list of possible Wiki and Rotten Tomatoes addresses from video file name;
# For it to work, the video file name must be either in the form of "Official_Film_Title (ReleaseYear)..." or "Official Film Title (ReleaseYear)..."
# If the official film's title contains ':', in the video file name it should be replaced with '--'

def from_file_name_addresses(video_file_name):
    if ' (' not in video_file_name:
        return [video_file_name]
    else:
        end_index = video_file_name.index(' (')
        film_title = video_file_name[:end_index].replace('--', ':')
        release_year = video_file_name[end_index+2:end_index+6]
        
        result = from_title_addresses(film_title, release_year)
        
        return result
    
    
if __name__ == '__main__':
    
    wiki_http = "https://en.wikipedia.org/wiki/Inside_Man"
    rotten_http = "https://www.rottentomatoes.com/m/inside_man"
    filmfname = "Inside_Man_(2006) vosmovies.org.mkv"
    dir_path = "T:\Videos\ABSOLUTE_FAVOURITES"
    name = "X-Men--_Days_of_Future_Past_(2014)_subt.mkv"
    
    # result = web_tails(name)
    # result = web_address_cleaning("https:\\en.wikipedia.org\\wiki", "Inside_Man\n")
    # print(result)
    # film_info_scrap(wiki_http, rotten_http, filmfname, dir_path)
    # subdir_scrap(dir_path)



# During conversion of file names to web addresses the '-' character needs to be changed to ':'
# (i.e. Dune-_Part_Two  ->  Dune:_Part_Two etc.
# ['', '', '86%', '85%']
# ['', '', '96%', '79%']
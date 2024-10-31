import os
import Video_listings as vl



# Automation of the creating the lists of videos and their copies called 'rename.txt' in all the subdirectorie of a given parent directory

def grand_listing(parent_dir):
    parent_dir = parent_dir.replace('\\', '/')
    dir_list = [item for item in os.listdir(parent_dir) if '.' not in item]
    
    for dir in dir_list:
        dir_path = os.path.join(parent_dir, dir)
        rename_txt = os.path.join(dir_path, 'rename.txt')
        content = vl.film_list(dir_path)
        n = 0
        with open(rename_txt, 'w', encoding='utf-8') as rename:
            for title in content:
                x = title.replace(' ', '_')
                y = x.replace('_(', ' (', 1)
                n += 1
                rename.write(f"{n}. {y}\n")

# Renaming video files in 'dir_path' directory using a chosen text file as a template
    
def film_rename(dir_path):
    item_list = os.listdir(dir_path)
    txt_files = [item for item in item_list if '.txt' in item]
    film_list = [item for item in item_list if ('.mp4' in item or '.avi' in item or '.mkv' in item or '.mpg' in item)]
    
    if len(txt_files) != 1:
        print(f"\nThe folder {dir_path} contains these '.txt' files:\n")
        for ind, file in enumerate(txt_files): print(f"{ind}. {file}")
        i = int(input("\nWhich one should be used as a template for renaming?\n"))
        txt_file = txt_files[i]
    else: txt_file = txt_files[0]
    
    with open(os.path.join(dir_path, txt_file), 'r', encoding='utf-8') as f_list:
        src_list = []
        dest_list = []
        for i, line in enumerate(f_list):
            indx = line.index(' ') + 1
            cl_line = line[indx:]
            clean_line = cl_line.rstrip('\n')
            src_list.append(os.path.join(dir_path, film_list[i]))
            dest_list.append(os.path.join(dir_path, clean_line))
            print(src_list[-1])
            print(f"{dest_list[-1]}\n")
            
        print(("\n\nCheck whether old and new names are correctly paired:\n").upper())    
        fork = input("Do you wish to proceed with renaming? (Y/N)\n").upper()
        
        if fork == 'Y':
            for index, item in enumerate(src_list):
                os.rename(item, dest_list[index])
        else:
            print("The Process was terminated.\n")
    

if __name__ == '__main__':
    fork = input("\nChoose the step you wish to undertake:\n\n\033[91m1\033[0m. Creating lists of videos and their 'rename.txt' copies in all subdirectories of a chosen parent directory \n\n\033[91m2\033[0m. Renaming videos in a chosen directory using 'rename.txt' file as a template\n\n")
    
    if fork == '1':
        par_dir = input("\nYour chosen parent directory?:\n\n")
        grand_listing(par_dir)
        print(f"\n\n\033[91mSUCCESS!!\033[0m\n\nLists of movies and their copies in all the subdirectories of the parent directory \033[92m{par_dir}\033[0m have been created.\n\n\033[95mProcessing COMPLETED!\033[0m\n\n")
    elif fork == '2':
        parentdir = input("\nThe directory in which movie collections are to be renamed:\n")
        #grand_listing(parentdir)
        film_rename(parentdir)
    
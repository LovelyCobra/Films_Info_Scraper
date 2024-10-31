Films Quick Info Scraper
------------------------
<i>Automatic Collating of Films Info from Wikipedia and Rotten Tomatoes</i>


A Python code that scrapes a basic quick information about a film/films from <b>Wikipedia</b> and <b>Rotten Tomatoes</b> websites and saves it in a text file/files. The additional functionality also includes creating a list/lists of video files in a chosen directory or subdirectories of a chosen directory and saving them in txt files located. The code was created because, at one point, the author had unmanagable number of film previews scattered in number of subdirectories on an external drive and needed to make the collection managable.

When running the code, one can choose from five options corresponding to five possible tasks.
1. Creating a list of video files in a chosen directory and saving it in a txt file in the same directory and copy of it in the directory named <b>Film_lists</b> located in the "Videos" folder in the current user's root directory. The text file is named after the name of the chosed directory where the video files in question are placed.
2. The same as above, this time doing it for all video files in all subdirectories of a chosen parent directory.
3. Scraping basic quick information about all films in a chosen directory from Wikipedia and Rotten Tomatoes websites and saving that info in txt files placed in the same directory. For the automatic collation of the information to work, the video files have to be named correctly with right film titles and years of release (examples: "Titanic (1999)...anything here....avi", "Harry Potter and the Philosopher's Stone (2001)...anything....mkv; if an official film title contains colon (:), it should be replaced with double hyphen (--) in the video file name: "The Lord of the Rings-- The Fellowship of the Ring (2001)....mp4"). Before proceeding with the scraping action the program shows the list of all video files in the chosen directory, says which file names do not contain the obligatory " (ReleaseYear)" substring and offers the option of editting the list within a given text file before proceeding.
4. Doing the same as above, but this time for all the video files contained in all the subdirectories of a chosen parent directory
5. Scraping the same basic info about a single chosen film from Wikipedia and Rotten Tomatoes and saving it in a txt file named after the film and placed in the same directory.

From Wikipedia, the program scrapes the first paragraph of the main article and quick info in the initial table. From Rotten Tomatoes it scrapes the Critics' and Audiences' scores.



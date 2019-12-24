# goodreads_list_crawler
Depends on beautifulsoup4, lxml, and goodreads. Use pip (or pip3) to install.

```
pip3 install beautifulsoup4
pip3 install lxml
pip3 install goodreads
```

Made for Python 3

This script goes over every list linked to in fantasylists.txt. Remove '?page=x' if the url ends on that. The program will automatically add that and go over each page of the given list. Outputs an sqlite file with the name 'fantasy.db', containing all the books found and info on ratings for that book. The code double checks if the book is actually fantasy, by checking if 'fantasy' is among the books popular shelves. Just in case someone confuses historic fiction with fantasy or something.

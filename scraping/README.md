This script uses the Python Selenium web browser automation package to run a scraping process via Chrome.

Scraping Process:
1. Log into Crunchbase with specified credentials
2. Scrape the 'investors' page as a csv and save to 'cb_csv' directory
3. Save the top n investors on the page to scrape their investments individually (currently set at n=10)
4. Scrape each of those investors and get a csv for each detailing their investments based on a specified custom search query

To-do list:
1. Be able to rename the downloaded csv's appropriately (using os and sys I assume)
2. Come up with a custom search that addresses what data we actually need to pull (current one is kind of arbitrary and was just to test)
3. Probably once we get it working well it would be worthwhile to move to headless Chrome or PhantomJS for efficiency purposes since the overhead and graphics loaded in the browser can really slow it down
4. Consider trying to get it working via HTTP requests or maybe mechanize? Will be a lot of work and I don't think it will work since most of CB is dynamic
5. Foolproof the script with error handling which I have semi-done but not extensively
6. Be able to concatenate downloaded csv's (write a shell script using 'copy *.csv new_csv.csv') 
7. Write a script for saving the csv data into SQL tables using SQLalchemy package and Postgres database
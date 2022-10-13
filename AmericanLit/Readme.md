This is a two part project to crawl a series of short stories from Americanliterature.com. They're a pretty cool website with a collection of the 'dying' art of the short story, so please go check them out if you have a chance.
Base Crawled Link: https://americanliterature.com/100-great-short-stories

The project was split into two scripts so as to scrape the links, author, body text, etc. into an intermediary database first with sqlite. This way after the first script 'SSScraper' one may perform quality control, select wanted stories, etc. first before moving on with 'To_PDF' and downloading the total as a pdf.
Sample database and pdf included.
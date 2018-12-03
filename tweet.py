import re

# Class to display and format the data
class Tweet:

    def __init__(self, data):
        self.data = data

    # Creates a link to the user's twitter page
    def user_link(self):
        return f"http://twitter.com/{self.data['username']}" # string formatting
        #return "http://twitter.com/{}".format(self.data['username'])

    # Runs two other methods (filter_brands and filter_urls) and makes links clickable and highlights the brands in the tweet
    def filtered_text(self):
        return self.filter_brands(self.filter_urls(self.data['text']))

    # If key word is in the text replace text with html mark tag. Creates a highlight.
    def filter_brands(self, text):
        brands = ["@BBC", "@CBS", "@CNN", "@FoxNews", "@nytimes"]

        for brand in brands:
            if (brand in text):
                text = text.replace(brand, "<mark>{}</mark>".format(brand))
            else:
                continue

        return text

    # Finds links and replaces with a html <a tag so we can have a clickable link in html
    def filter_urls(self, text):
        return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)", r'<a href="\1" target="_blank">\1</a>', text)

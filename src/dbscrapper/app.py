"""
Web Scrapping App for www.delaniblog.com
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from dbscrapper.scrapper import get_url, get_max_page_number, get_data
import pandas as pd
from dbscrapper.pageContent import homepage,page


class DBScrapper(toga.App):

    def startup(self):

        self.editor = toga.MultilineTextInput(style=Pack(
            flex=1), placeholder="Click on 'Get posts' to fetch blog posts")

        main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        image = toga.ImageView(
            image="./resources/DELANIBLOGPNG.png", style=Pack(width=200, height=75, flex=1, alignment="left", padding=(10, 100, 10, 100)))
        imageBox = toga.Box(style=Pack(
            alignment="right", direction=COLUMN))
        imageBox.add(image)

        info_Box = toga.Box(style=Pack(
            padding=(5, 20), alignment="center", direction=COLUMN, text_align="center"))
        app_description = toga.Label(
            'Get Blog posts on the click of one button',
            style=Pack(padding=(0, 5,5,5), text_align="center")
        )
        self.info = toga.Label(
            '',
            style=Pack(padding=(0, 5), text_align="center")
        )

        info_Box.add(app_description)
        info_Box.add(self.info)

        select_Box = toga.Box(style=Pack(
            padding=(5, 20), direction=COLUMN, alignment="center", text_align="center"))
        self.select = toga.Selection(items=["Latest Posts", "Home", "Music", "Entertainment", "Videos",
                                            "Album & EP", "Lyrics", "Mixtape", "Trending"],
                                     style=Pack(alignment="center", flex=1, text_align="center", padding_top=10, height=30), on_select=self.change_max_number)

        self.page_number = toga.NumberInput(
            min_value=1, style=Pack(padding_top=30, height=30))

        submit_button = toga.Button(
            "Get Posts", on_press=self.get_posts, style=Pack(padding_top=30, height=50))

        select_Box.add(self.select)
        select_Box.add(self.page_number)
        select_Box.add(submit_button)

        credit_Box = toga.Box(style=Pack(
            padding=(90, 20, 0, 20), alignment="center", direction=COLUMN, text_align="center"))

        editor_button = toga.Button(
            "Open Text Editor", on_press=self.text_editor, style=Pack(height=30))
        credit = toga.Label(
            "Developed by Johnson Cooper",
            style=Pack(padding=(0, 5), text_align="center")
        )
        phone = toga.Label(
            "08139002724",
            style=Pack(padding=(0, 5), text_align="center")
        )
        credit_Box.add(editor_button)
        credit_Box.add(credit)
        credit_Box.add(phone)

        main_box.add(imageBox)
        main_box.add(info_Box)
        main_box.add(select_Box)
        main_box.add(credit_Box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        self.main_window.size = (400, 500)

    def text_editor(self, *args, **kwargs):
        store = self.editor.value
        self.editor = toga.MultilineTextInput(style=Pack(
            flex=1), placeholder="Click on 'Get posts' to fetch blog posts")
        self.editor.value = store
        box = toga.Box(style=Pack(direction=COLUMN))
        copy_button = toga.Button(
            "Copy Text", on_press=self.copy_text, style=Pack(height=30))
        box.add(self.editor)
        box.add(copy_button)
        self.window = toga.Window(
            'Text Editor', title='Scrapper Text Editor', closeable=False, minimizable=False)
        self.window.content = box
        self.window.show()
    

    def copy_text(self, *args, **kwargs):
        text = self.editor.value
        df = pd.DataFrame([text])
        df.to_clipboard(index=False, header=False)

    def change_max_number(self, widget, *args, **kwargs):
        select = self.select.value
        try:
            max_page_number = get_max_page_number(select)
            self.page_number.max_value = max_page_number
        except :
            self.info.text = "Error occured: Connection Failed"

    def get_posts(self, widget, *args, **kwargs):
        self.editor = toga.MultilineTextInput(style=Pack(
            flex=1), placeholder="Click on 'Get posts' to fetch blog posts")
        select = self.select.value
        page_number = self.page_number.value

        try:
            posts = get_data(select, page_number)

            string = ""
            for post in range(len(posts)):
                string += posts.headings[post] + \
                    "\n" + posts.links[post] + "\n\n"
            self.editor.value = string

            self.copy_text()

            self.main_window.info_dialog(
                'Info', "Posts successfullly copied to clipboard")
            self.info.text = "Posts successfullly copied to clipboard"
            
        except:
            self.info.text = "Error occured: Connection Failed"


def main():
    return DBScrapper()

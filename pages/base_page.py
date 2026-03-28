class BasePage:
    PATH = ''

    def __init__(self, page):
        self.page = page

    def open(self, base_url):
        self.page.goto(f'{base_url}{self.PATH}')

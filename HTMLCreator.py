class HTMLPage:
    def __init__(self):
        self.page_content = ""
        self.css_code = """
                        body {
                            background-color: #f2f2f2;
                        }
                        .titolo_paragrafo {
                            color: blue;
                        }
                        .testo_paragrafo {
                            font-size: 14px;
                        }
                        """

    def create_empty_page(self, title):
        self.page_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style></style>
        </head>
        <body>
        </body>
        </html>
        """

    def add_css(self, css=""):
        # if no css has been passed: use the default
        if css == "":
            css_code = self.css_code

        css_tag = f"<style>{css_code}</style>"
        self.page_content = self.page_content.replace("<style></style>", css_tag)

    def add_content(self, title, text):
        content = f"""
        <div class="item">
            <h2 class="titolo_paragrafo">{title}</h2>
            <p class="testo_paragrafo">{text}</p>
        </div>
        """
        self.page_content = self.page_content.replace("</body>", f"{content}\n</body>")

    def save_to_file(self, filename):
        with open("HTML_Reports/"+filename, "w") as file:
            file.write(self.page_content)
class Index:
    def __init__(self, articles):
        """
        初始化Index类，接受一个包含(文章名, 文章地址)的列表。
        :param articles: 一个包含(文章名, 文章地址)的列表
        """
        self.articles = articles

    def generateIndex(self, output_file):
        """
        生成一个index.html文件，包含文章名和对应的链接。
        :param output_file: 输出的HTML文件名，默认为'index.html'
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html><meta charset="UTF-8">\n')
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("    <title>文章索引</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("    <h1>文章索引</h1>\n")
            f.write("    <ul>\n")
            for title, url in self.articles:
                f.write(f'        <li><a href="{url}">{title}</a></li>\n')
            f.write("    </ul>\n")
            f.write("</body>\n")
            f.write("</html>\n")

        print(f"Index file '{output_file}' has been generated successfully.")


class Index:
    def __init__(self, articles):
        """
        初始化Index类，接受一个包含(文章名, 文章地址)的列表。
        :param articles: 一个包含(文章名, 文章地址)的列表
        """
        self.articles = articles

    def generateIndex(self, output_file, template=lambda x:x):
        """
        生成一个index.html文件，包含文章名和对应的链接。
        :param output_file: 输出的HTML文件名，默认为'index.html'
        """
        content = "<h1>文章目录</h1>"
        for title, url in self.articles:
            content += (f'<li><a href="{url}">{title}</a></li>\n')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template(content))
            

        print(f"Index file '{output_file}' has been generated successfully.")


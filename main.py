import markdown
import os
import sys
import shutil
import pygments

from pygments.formatters import HtmlFormatter
from index import Index
from l2m4m import LaTeX2MathMLExtension

def getPkgResourcePath():
    return os.module
class Repository:
    def __init__(self, directory, charset="UTF-8"):
        self.dir = directory
        self.charset = charset
        # check if the dir exists
        if not Repository.isDirExist(directory):
            raise Exception("Directory not exists!")
        
        # keep the realpath
        self.dir = os.path.realpath(self.dir)
        
        
    
    def isDirExist(directory):
        return os.path.exists(directory) and os.path.isdir(directory)
    
    def getHtmlRootPath(self):
        """ get the path htmls to be stored """
        return os.path.join(self.dir, "htmls")

    def getCssPath(self):
        return os.path.join(self.getHtmlRootPath(), "css")
        
    def getCodeStyleCssName(self):
        return "styles.css"
    
    def getPageStyleCssName(self):
        return "github-markdown-light.css"
    
    def getPageStyleSetting(self):
        return """
        <style>
            .markdown-body {
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }

            @media (max-width: 767px) {
                .markdown-body {
                    padding: 15px;
                }
            }
        </style>
        """
    
    def getCssFilePath(self, cssname):
        return os.path.join(self.getCssPath(),cssname)
    
    def localPathToNetPath(self, lpath):
        """convert local path to net realpath. i.e:<dir>/a/b -> /a/b"""
        relpath = os.path.relpath(lpath, self.getHtmlRootPath())
        if relpath.startswith(".."):
            raise Exception("Not a child dir")
        return os.path.join("/",relpath)
    
    def generateMdHtmlTemplate(self):
        return lambda content: f"""
        <meta charset={self.charset}>
        <link rel="stylesheet" href="{self.localPathToNetPath(self.getCssFilePath(self.getCodeStyleCssName()))}">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{self.localPathToNetPath(self.getCssFilePath(self.getPageStyleCssName()))}">
        {self.getPageStyleSetting()}
        <article class="markdown-body">
        {content}
        </article>
        """
    
    def generateBase(self):
        with Repository.openFileToWrite(self.getCssFilePath(self.getCodeStyleCssName())) as f:
            f.write("w")
            f.write(HtmlFormatter().get_style_defs(".codehilite"))
            
        pageStyleCssSourcePath = os.path.join(os.path.join(os.path.join(os.path.split(__file__)[0],"resource"),"css"),self.getPageStyleCssName())
        pageStyleCssDestPath = self.getCssFilePath(self.getPageStyleCssName())
        
        shutil.copy(pageStyleCssSourcePath, pageStyleCssDestPath)
        
    def generateIndex(self, blogs):
        index = Index(blogs)
        index.generateIndex(os.path.join(self.getHtmlRootPath(),"index.html"))
    
    def convertMd2Html(self, md):
        extensions = ["extra",
                      "codehilite",
                      LaTeX2MathMLExtension(),
                      ]
        t = self.generateMdHtmlTemplate()
        html = t(markdown.markdown(md, extensions=extensions))
        return html
    
    def clean(self):
        if not Repository.isDirExist(self.getHtmlRootPath()):
            return
        shutil.rmtree(self.getHtmlRootPath())
        
    def openFileToWrite(path):
        """open a file for writing. if the file not exists, create it.
           create corresponding directorys if needed"""
        directory = os.path.dirname(path)
        if not Repository.isDirExist(directory):
            os.makedirs(directory)
        f = open(path, "w")
        return f
    
    def convertAll(self):
        """ convert all markdowns in dir to html
            htmls are saved in dir/htmls
            keep the directory struct"""
        blogs = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if not file.endswith(".md"):
                    continue
                realpath = os.path.join(root,file)
                relpath = os.path.relpath(realpath, self.dir)
                
                with open(realpath, "r") as f:
                    md = f.read()
                    html = self.convertMd2Html(md)
                    
                relHtmlPath = relpath.removesuffix(".md")+".html"
                htmlPath = os.path.join(self.getHtmlRootPath(), relHtmlPath)
                with Repository.openFileToWrite(htmlPath) as f:
                    f.write(html)
                blogs.append((file.removesuffix(".md"), relHtmlPath))
        return blogs

    def generate(self):
        """generate all the things"""
        self.generateBase()
        self.generateIndex(repo.convertAll())
        
                    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: [dir]")
        exit(0)
    repo = Repository(sys.argv[1])
    # repo.clean()
    repo.generate()
            
import markdown
import os
import sys
import shutil
import pygments

from pygments.formatters import HtmlFormatter
from index import Index
from l2m4m import LaTeX2MathMLExtension
from style import CodeStyle
from style import PageStyle

def getPkgResourcePath():
    return os.module
class Repository:
    def __init__(self, directory, styles = [], charset="UTF-8",  ignoreDirs = ["private","log"]):
        self.dir = directory
        self.charset = charset
        self.styles = styles
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
        
    def getCssFilePath(self, cssname):
        return os.path.join(self.getCssPath(),cssname)
    
    def localPathToNetPath(self, lpath):
        """convert local path to net realpath. i.e:<dir>/a/b -> /a/b"""
        relpath = os.path.relpath(lpath, self.getHtmlRootPath())
        if relpath.startswith(".."):
            raise Exception("Not a child dir")
        return os.path.join("/",relpath)
    
    def generateMdHtmlTemplate(self):
        styleHeaders = ''.join([style.header(self.localPathToNetPath(self.getCssFilePath(style.getName()))) for style in self.styles])
        return lambda content: f"""
        <meta charset={self.charset}>
        {styleHeaders}
        <article class="markdown-body">
        {content}
        </article>
        """
    def generateBase(self):
        for style in self.styles:
            sourcePath = os.path.join(os.path.split(__file__)[0], style.getLocalPath())
            destPath   = self.getCssFilePath(style.getName())
            with Repository.openFileToWrite(destPath) as f:
                pass
            shutil.copy(sourcePath, destPath)
        
    def generateIndex(self, blogs):
        index = Index(blogs)
        index.generateIndex(os.path.join(self.getHtmlRootPath(),"index.html"), self.generateMdHtmlTemplate())
    
    def convertMd2Html(self, md):
        extensions = ["extra",
                      "codehilite",
                      LaTeX2MathMLExtension(),
                      ]
        t = self.generateMdHtmlTemplate()
        html = t(markdown.markdown(md, extensions=extensions))
        return html
    
    def clean(self):
        # TODO: not remove .git dir
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
            if root in self.ignoreDirs:
                continue
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
    argc = len(sys.argv)
    if len(sys.argv) < 2:
        print("usage: [dir] <ignore dir>")
        exit(0)
    if argc == 2:
        repo = Repository(sys.argv[1], [CodeStyle('resource/css/styles.css'), PageStyle('resource/css/github-markdown-light.css')])
    else:
        repo =  Repository(sys.argv[1], [CodeStyle('resource/css/styles.css'), PageStyle('resource/css/github-markdown-light.css')], ignoreDirs=sys.argv[2])
    # repo.clean()
    repo.generate()
            
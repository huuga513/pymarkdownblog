import os
class Element:
    def __init__(self):
        pass
    def header(self):
        return ""

class MathJaxScript(Element):
    def __init__(self, url):
        self.url = url
        return
    def header(self):
        return f'<script id="MathJax-script" async src="{self.url}"></script>'
class Style(Element):
    def __init__(self, localpath):
        self.filename = os.path.basename(localpath)
        self.filepath = localpath
        self.remotepath = None
        
    def setRemotePath(self, remotepath):
        self.remotepath = remotepath
        
    def header(self):
        return ""

    def getLocalPath(self):
        return self.filepath

    def getName(self):
        return self.filename
    
class CodeStyle(Style):
    def header(self):
        return f"""<link rel="stylesheet" href="{self.remotepath}">"""
    
class PageStyle(Style):
    def header(self):
        return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{self.remotepath}">
        <style>
            .markdown-body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}

            @media (max-width: 767px) {{
                .markdown-body {{
                    padding: 15px;
                }}
            }}
        </style>
        """
import os
class Style:
    def __init__(self, localpath):
        self.filename = os.path.basename(localpath)
        self.filepath = localpath
        
    def header(self, remotepath):
        return ""

    def getLocalPath(self):
        return self.filepath

    def getName(self):
        return self.filename
    
class CodeStyle(Style):
    def header(self, remotepath):
        return f"""<link rel="stylesheet" href="{remotepath}">"""
    
class PageStyle(Style):
    def header(self, remotepath):
        return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{remotepath}">
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
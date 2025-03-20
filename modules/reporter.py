#!/usr/bin/env python3

from jinja2 import Template

class HTMLreporter:
    def __init__(self, templateFileName="templates/report.htm"):
        with open(templateFileName, encoding="utf-8") as templateFile:  # Specify encoding for reading
            self._template = Template(templateFile.read())
        
    def report(self, rows, reportFileName=None):
        if reportFileName is None:
            reportFileName = "output.html"
        with open(reportFileName, "wt", encoding="utf-8") as reportFile:  # Specify encoding for writing
            reportFile.write(self._template.render(rows=rows))  # Write the string directly

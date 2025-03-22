#!/usr/bin/env python3

from jinja2 import Template
import json

class HTMLreporter:
    def __init__(self, templateFileName="templates/report.htm"):
        with open(templateFileName, encoding="utf-8") as templateFile:
            self._template = Template(templateFile.read())
        
    def report(self, rows, reportFileName=None):
        if reportFileName is None:
            reportFileName = "output.html"
        with open(reportFileName, "wt", encoding="utf-8") as reportFile:
            reportFile.write(self._template.render(rows=rows))

class JSONreporter:
    def report(self, rows, reportFileName=None):
        if reportFileName is None:
            reportFileName = "output.json"
        with open(reportFileName, "w", encoding="utf-8") as reportFile:
            json.dump(rows, reportFile, ensure_ascii=False, indent=2)

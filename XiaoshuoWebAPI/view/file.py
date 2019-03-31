
import os
import pandas as pd

from django.http import HttpResponse
from pydocx import PyDocX
import base64


def upload(request):
    if request.method == 'POST':  # 获取对象
        file = request.FILES.get("file", None)
        print(file.name)
        bs = base64.b64decode(file.name)
        filename = str(bs, 'ISO-8859-1')
        print(filename)
        extension = fileExtension(filename)
        print(extension)
        html = None
        if (extension == '.docx' or extension == '.doc'):
            html = PyDocX.to_html(file)
        if (extension == '.xls' or extension == '.xlsx'):
            xd = pd.ExcelFile(file)
            df = xd.parse()
            html = df.to_html(header=True, index=False)
    return HttpResponse(html)


def fileExtension(filename):
    return os.path.splitext(filename)[1]

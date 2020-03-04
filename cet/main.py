import requests
import re
import base64
import zipfile
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os
import uuid
from .models import CetIdCookies
from person.models import Person


def read_pdf(file):
    pdf_wb = open(file, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf_wb)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    pdf_wb.close()
    return content


def un_zip(file_name):
    file = None
    with zipfile.ZipFile(file_name) as zip_file:
        name = zip_file.namelist()[0]
        file = zip_file.extract(name)
    os.remove(file_name)  # 删除文件，本地不进行保存
    return file


def down(sid):
    r = requests.get("http://cet-bm.neea.edu.cn/Home/DownTestTicket?SID=" + sid)
    data = r.content
    name = str(uuid.uuid4())
    with open(name + ".zip", "wb") as f:
        f.write(data)
    return name + ".zip"


def cet_number(person: Person, verify_code):
    jar = requests.cookies.RequestsCookieJar()
    cet_model = CetIdCookies.objects.get(person=person)
    cookie = cet_model.cookies.split("分")
    jar.set('ASP.NET_SessionId', cookie[0], domain='cet-bm.neea.edu.cn', path='/')
    jar.set('BIGipServercet_pool', cookie[1], domain='cet-bm.neea.edu.cn', path='/')
    param = dict(provinceCode=11, IDTypeCode=1, IDNumber=person.id_card, Name=person.name, verificationCode=verify_code)
    response = requests.post("http://cet-bm.neea.edu.cn/Home/ToQuickPrintTestTicket", param, cookies=jar).json(
        encoding='utf-8')
    if response.get("ExceuteResultType") == 1:
        sid = re.findall('SID":"(.+)","SubjectName"', response.get("Message"))
        if sid:
            zip_file_path = down(sid[0])
            file_path = un_zip(zip_file_path)
            text = read_pdf(file_path)
            os.remove(file_path)
            number = re.findall(r"准考证号：(\d+)", text)
            if number:
                cet_model.number = number[0]
                cet_model.save()
                return int(number[0])
        else:
            return '系统错误'
    else:
        return response['Message']


def verify_code(person):
    response = requests.get("http://cet-bm.neea.edu.cn/Home/VerifyCodeImg")
    cookies = response.cookies['ASP.NET_SessionId'] + "分" + response.cookies['BIGipServercet_pool']
    cet_cookies = CetIdCookies.objects.get_or_create(person=person)[0]
    cet_cookies.cookies = cookies
    cet_cookies.save()
    image = base64.b64encode(response.content).decode()
    return image

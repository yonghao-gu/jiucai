# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage


import copy
import types
import global_obj
import log




class CMailMessage(object):
    def __init__(self, parent):
        self.m_parent = parent
        self.m_sender = None
        self.m_receive = []
        self.m_title = None
        self.m_context = None
    
    def _Check_args(self, wkg):
        if "receive" in wkg:
            if type(wkg["receive"]) is str:
                self.m_receive.append(wkg["receive"])
            else:
                self.m_receive = wkg["receive"]
        else:
            self.m_receive = self.m_parent.Receive()
        
        if "sender" in wkg:
            self.m_sender = wkg["sender"]
        else:
            self.m_sender = self.m_parent.Sender()

    def SendMessage(self, title, text, **wkg):
        self._Check_args(wkg)
        self.m_title = title
        self.m_context = text
        return self._send()
    
    def _send(self):
        try:
            message = self._MakeMessage()
            smtpObj = self.m_parent.Login()
            smtpObj.sendmail(self.m_sender, self.m_receive, message.as_string())
            smtpObj.quit()
        except smtplib.SMTPException as e:
            log.Error("send mail false", e)
            return False
        except BaseException as e:
            log.Error("sned mail false by other reason",e)
            return False
        return True

    def _MakeMessage(self):
        message = MIMEText(self.m_context,'plain','utf-8')
        message['Subject'] = self.m_title
        message['From'] = self.m_sender
        message["To"] = ",".join(self.m_receive)
        return message



class CHtmlMailMessage(CMailMessage):

    def __init__(self, parent):
        super().__init__(parent)
        self.m_imgs = {}

    def _Check_args(self, wkg):
        super()._Check_args(wkg)
        if "imgs" in wkg:
            self.m_imgs = wkg["imgs"]

 
    def _MakeMessage(self):
        message = MIMEMultipart('related')
        mail_body = MIMEText(self.m_context, _subtype='html', _charset='utf-8')
        message['Subject'] = Header(self.m_title, 'utf-8')
        message.attach(mail_body)
        for k,v in self.m_imgs.items():
            fp = open(v, 'rb')
            image_data = fp.read()
            fp.close()
            images = MIMEImage(image_data)
            images.add_header('Content-ID', k)
            message.attach(images)
        
        message['Subject'] = self.m_title
        message['From'] = self.m_sender
        message["To"] = ",".join(self.m_receive)
        return message



class CMailBox(object):
    def __init__(self, user, password, mailhost, port):
        self.m_user = user
        self.m_pwd = password
        self.m_host = mailhost
        self.m_sender = None
        self.m_receive = []
    
    def Login(self):
        smtpObj = smtplib.SMTP(timeout = 60) 
        smtpObj.connect(self.m_host,465)
        smtpObj.login(self.m_user,self.m_pwd)
        return smtpObj

    def SetSender(self, name):
        self.m_sender = name
    
    def SetReceive(self, name):
        self.m_receive.append(name)

    def Sender(self):
        return self.m_sender
    
    def Receive(self):
        return copy.copy(self.m_receive)

    def MailMessage(self):
        return CMailMessage(self)

    def HtmlMailMessage(self):
        return CHtmlMailMessage(self)



def init_mail():
    config = global_obj.get_obj("config")
    mail_data = config["mail"]
    obj = CMailBox(mail_data["user"], mail_data["password"], mail_data["host"], mail_data["port"])
    obj.SetSender(mail_data["user"])
    for name in mail_data["to"]:
        obj.SetReceive(name)
    global_obj.set_obj("mail", obj)



def test():

    boby = """
<h3>Hi，all</h3>
<p>附件为本次FM_自动化测试报告。</p>
<p>请解压zip，并使用Firefox打开index.html查看本次自动化测试报告结果。</p>
<p>
<br><img src="cid:image1"></br> 
<br><img src="cid:image2"></br> 
</p>
<p>
""" 
    


    mailobj = global_obj.get_obj("mail")

    message = mailobj.HtmlMailMessage()
    if message.SendMessage("这是标题", boby):
        print("发送成功")


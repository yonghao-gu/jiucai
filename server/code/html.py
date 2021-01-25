# -*- coding: utf-8 -*-

class CHtml(object):
    __context = '''
<!Doctype html>
<html>
<head>
	<title>%s </title>
</head>
<body>
%s
</body>
'''

    def __init__(self, title):
        self.m_title = title
        self.m_Context = ""
        self.AddLine(title)
    
    def Add(self, text):
        self.m_Context+=text
     
    def AddLine(self,text):
        self.Add("<p>%s<br>"%(text))


    def AddDict2Table(self, data_list):
        v0 = data_list[0]
        head_list = v0.keys()
        tblist = []
        for data in data_list:
            trlist = [ str(data.get(key, "NULL")) for key in head_list]
            tblist.append(trlist)
        self.AddTable(tblist, head_list)



    def AddTable(self, ls, head = None):
        '''
            ls = [[行1], [行2]]
        '''
        text = ""
        if head:
            text+="<tr>"
            for s in head:
                text+="<th>%s</th>"%(s)
            text+="</tr>"
        
        for l in ls:
            text+="<tr>"
            for s in l:
                text+="<td>%s</td>"%(s)
            text+="</tr>"
        
        text = '<table border= "1" cellspacing="5">%s</table>'%(text)
        self.Add(text)
    
    def GetHtml(self):
        return CHtml.__context%(self.m_title, self.m_Context)
    
    def SaveHtml(self, filename):
        with open(filename,"w") as fp:
            fp.write(self.GetHtml())


if __name__ == "__main__":
    ls = []
    for i in range(10):
        data= {
            "key":i,
            "val": "love*%s"%(i),
            "TapTap":"OF",
        }
        ls.append(data)

    htmobj = CHtml("测试")
    htmobj.AddDict2Table(ls)
    htmobj.save_html("./test.html")







from flask import Flask, render_template,redirect, request
import json
import requests


class LeadScoreClassifier:
    
    def __init__(self,data):
        self.score_name =0
        self.score_email =0
        self.score_addr =0
        self.score_brows =0
        self.score_ip =0
        self.tot_score = 0
        self.data = data
        
    def name(self):
        name = self.data['first_name'] + self.data['last_name']
        
        for i in name:
            if (i.isalpha()==0):
                self.score_name-= 0.8
                break
                
        if self.score_name == 0:
            self.score_name += 0.8
            
        if len(name)> 100:
            self.score_name-= 0.2
            
        else:
            self.score_name+= 0.2
        
        return self.score_name
    
    
    
    def email(self):

        domains =[ "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com", "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com", "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk", "email.com", "fastmail.fm", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "iname.com", "inbox.com", "lavabit.com", "love.com", "outlook.com", "pobox.com", "protonmail.ch", "protonmail.com", "tutanota.de", "tutanota.com", "tutamail.com", "tuta.io",\
              "keemail.me", "rocketmail.com", "safe-mail.net", "wow.com", "ygm.com",\
              "ymail.com", "zoho.com", "yandex.com", "bellsouth.net", "charter.net", "cox.net", "earthlink.net", "juno.com",\
               "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",\
               "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",\
               "virgin.net", "wanadoo.co.uk", "bt.com",\
               "sina.com", "sina.cn", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph", "163.com", "yeah.net", "126.com", "21cn.com", "aliyun.com", "foxmail.com",\
               "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr",\
               "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de",\
                  "libero.it", "virgilio.it", "hotmail.it", "aol.it", "tiscali.it", "alice.it", "live.it", "yahoo.it", "email.it", "tin.it", "poste.it", "teletu.it",\
                 "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru",\
                "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be",\
                 "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",\
                 "yahoo.com.mx", "live.com.mx", "hotmail.es", "hotmail.com.mx", "prodigy.net.mx",\
                "yahoo.ca", "hotmail.ca", "bell.net", "shaw.ca", "sympatico.ca", "rogers.com",\
                "yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br", "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br"]\
        
        address=['com','net','co','fm','ch','de','io','me','cn','jp','kr','id','sg','ph','fr','it','ru','be','ar','mx','es','ca','br']
        addr_special=['uk','in']

 

        websites= [x.split(".")[0] for x in domains]

 

        websites= list(set(websites))

        email = self.data['email'].lower()

 

        comp_name= self.data['company'].lower()
        splitt = email.split('@')
        domain = splitt[1]
        domain = domain.split('.')

 

        if comp_name in domain[0]:
            self.score_email+=0.8
        elif domain[0] in websites:
            self.score_email+=0.8
        else:
            self.score_email-=0.8

        # print(domain)

        flag1=False
        flag2=True
        for x in domain[1:]:
            if x in address:
                self.score_email+=0.1
                flag1=True
                flag2= False
            elif x in addr_special:
                if(flag1):
                    self.score_email+=0.1
                else:
                    self.score_email+=0.2
                flag2=False
                break
        if(flag2):
            self.score_email-=0.2    
        return self.score_email
        
#     def addr(self):
#         addr = self.data['address'].lower()
#         if 'uk' in addr:
#             self.score_addr += 1.0
#         elif 'united' in addr:
#             self.score_addr += 1.0
#         elif 'u.k' in addr:
#             self.score_addr += 1.0
#         elif 'kingdom' in addr:
#             self.score_addr += 1.0
#         else:
#             self.score_addr -= 1.0

#         return self.score_addr
    
    
        
    def brows(self):
        brows = self.data['browser']
        brows = brows.split('/')
        if any(x.lower() in ['chrome', 'safari', 'firefox', 'samsung internet','uc','opera','edge','ie','aosp'] for x in brows):
             self.score_brows += 1.0
        else:
            self.score_brows -= 1.0    
            
        return self.score_brows
    
    
        
    def ip(self):
        
        ip= self.data['ip_address']
        url = "https://tony11-blacklist-ip-v1.p.rapidapi.com/ipv4/" + ip
        headers = {'x-rapidapi-host': "tony11-blacklist-ip-v1.p.rapidapi.com", 'x-rapidapi-key': "6350f9a380msh77e1b7f71166e09p169206jsn45bf3dc73018"}
        response2 = requests.request("GET", url, headers=headers)
        res2= response2.text
        dictt2= json.loads(res2)

        flag3=True
        if(dictt2['content']['blacklisted']==1):
            flag3= False
            self.score_ip-= 0.8
        if(dictt2['status']!= 'OK'):
            flag3= False
            self.score_ip-= 0.2
        if(flag3):
            self.score_ip+=1.0
            
#         print("IP Score =",self.score_ip)
        return self.score_ip

    
    
    def predict(self):
        
        name_score = self.name()
        email_score = self.email()
#         addr_score = self.addr()
        brows_score  = self.brows()
        ip_score = self.ip()
        
        self.tot_score = (name_score + email_score + brows_score + ip_score)/4
        return self.tot_score





app = Flask(__name__)


@app.route("/")

def hello():
	return render_template("index.html")

@app.route('/',methods=['POST'])
def marks():
	if request.method== 'POST':
		try:
			result=request.form
			data= dict(result)
			user = LeadScoreClassifier(data)
			
			scorre= user.predict()	
		except:
			scorre= "Invalid Input"

	return render_template("index.html", score= scorre)


if __name__ == '__main__':
	app.run(debug=True)
	


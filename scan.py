import json
import requests
import html
import schedule
import time
import smtplib
from email.mime.text import MIMEText

#---------------Fill in your data---------------

send_mail=True
'''
2729: AKTION .de-Domain 14 Cent OST21
2730: AKTION .ch-Domain OST21
2731: AKTION .li-Domain OST21
2732: AKTION .eu-Domain OST21
2733: AKTION .at-Domain OST21
2734: VPS Ostern S OST21
2735: VPS Ostern M OST21
2736: VPS Ostern L OST21
2737: VPS Ostern XL OST21
2738: VPS Funny Bunny OST21
2739: Webhosting 1000 SE OST21
2740: Webhosting 2000 SE OST21
2741: Webhosting 4000 SE OST21
2742: Webhosting Power Egg OST21
2743: RS Ostern S OST21
2744: RS Ostern M OST21
2745: RS Ostern L OST21
2746: RS Ostern XL OST21
2747: RS Ostern XXL OST21
2749: Cloud vLAN Giga OST21
2750: Cloud vLAN 2,5 Gbit/s OST21
2751: Reseller Level B OST21
2752: Zusätzliche IPv4 OST21
2753: Failover IPv4-Adresse OST21
2754: netcup Twinbook OST21
'''
ids=[2744,2738] # fill in the desired Product ids
me="sender@email.de"
you="receiver@email.de"
mail_user="user"
mail_pw="pw"
smtp_ssl_server="email.de"


#----------------------------------

urls = ["/",
"/ausbildung/",
"/ausbildung/bachelor-of-engineering-studiengang-informationstechnik-mwd",
"/ausbildung/fachinformatik-anwendungsentwicklung-mwd",
"/ausbildung/fachinformatik-systemintegration-mwd",
"/bestellen/agb.php",
"/bestellen/domainangebote.php",
"/bestellen/softwareangebote.php",
"/bestellen/warenkorb.php",
"/groupware/",
"/hosting/",
"/hosting/qualitaetsgarantien.php",
"/hosting/webhosting-application-hosting.php",
"/hosting/webhosting-testaccount.php",
"/jobs/",
"/jobs/junior-php-developer-mwd",
"/jobs/software-engineer-mwd-faoer-rd-go-python",
"/jobs/supportmitarbeiter-mwd",
"/jobs/systemadministrator-mit-fokus-auf-linux-und-3rd-level-support-mwd",
"/kontakt/",
"/kontakt/datenschutzerklaerung.php",
"/kontakt/impressum.php",
"/kontakt/postanschrift.php",
"/kontakt/telefonsupport.php",
"/professional/",
"/professional/dedizierte-server/",
"/professional/dedizierte-server/perc_raid_controller.php",
"/professional/dedizierte-server/remote_management.php",
"/professional/individuelle-loesungen/",
"/professional/individuelle-loesungen/penetrationtesting.php",
"/professional/individuelle-loesungen/preise.php",
"/professional/individuelle-loesungen/servermanagement.php",
"/professional/individuelle-loesungen/software-installationen.php",
"/professional/managed-server/managed-cloud-cluster.php",
"/professional/managed-server/managed-privateserver.php",
"/professional/managed-server/managed-server.php",
"/ssl-zertifikate/",
"/ssl-zertifikate/geotrust.php",
"/ssl-zertifikate/globe.php",
"/ssl-zertifikate/rapid.php",
"/ssl-zertifikate/thawte.php",
"/support/",
"/ueber-netcup/",
"/ueber-netcup/auszeichnungen.php",
"/ueber-netcup/ddos-schutz-filter.php",
"/ueber-netcup/hardware-infrastruktur.php",
"/ueber-netcup/kundenmeinungen-netcup.php",
"/ueber-netcup/merchandising.php",
"/ueber-netcup/oekostrom.php",
"/ueber-netcup/partner.php",
"/ueber-netcup/public-relations.php",
"/ueber-netcup/rechenzentrum.php",
"/ueber-netcup/referenzen.php",
"/vserver/",
"/vserver/reseller_angebote_vserver.php",
"/vserver/root-server-erweiterungen.php",
"/vserver/storagespace.php",
"/vserver/uebersicht_vserver_angebote.php",
"/vserver/vergleich-linux-vserver-kvm.php",
"/vserver/vergleich-root-server-vps.php",
"/vserver/vps.php",
"/vserver/vserver_guenstig_qualitaet.php",
"/vserver/vserver_images.php",
"/vserver/vstorage.php"
]

def scan():
    eggs=[]
    for u in urls:
      api = "https://www.netcup.de/api/eggs"
      data = {"requrl": u}
      response = requests.post(api, data).text
      response_json = json.loads(response)
      if response_json["eggs"] != False:
        if int(response_json["eggs"][0]["product_id"]) in ids:
            eggs.append([html.unescape(response_json["eggs"][0]["title"]),"https://www.netcup.de/bestellen/produkt.php?produkt=" + str(response_json["eggs"][0]["product_id"]) + "&hiddenkey="+ str(response_json["eggs"][0]["product_key"])],"https://netcup.de" + u)
        print("Gefunden auf:", "https://netcup.de" + u)
        print(html.unescape(response_json["eggs"][0]["title"]), "( Produkt ", str(response_json["eggs"][0]["product_id"]) ,") für", html.unescape(response_json["eggs"][0]["price"]))
        #Geht nur lokal:
        print("https://www.netcup.de/bestellen/produkt.php?produkt=" + str(response_json["eggs"][0]["product_id"]) + "&hiddenkey="+ str(response_json["eggs"][0]["product_key"]))
        print("----------")
    print("DONE!")
    if len(eggs) > 0 and send_mail:
        print("SENDING MAIL")
        msg="Found {} Netcup Eggs:\n".format(len(eggs))
        for egg in eggs:
            msg+="{}: {} on {}\n".format(*egg)
        msg = MIMEText(msg)
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'Found Netcup Eggs'
        msg['From'] = me
        msg['To'] = you

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP_SSL(smtp_ssl_server)
        s.login(mail_user,mail_pw)
        s.sendmail(me, [you], msg.as_string())
        s.quit()
        print("MAIL SENT!")
    print("===========================")

schedule.every().hour.at("00:10").do(scan)
schedule.every().hour.at("10:10").do(scan)
schedule.every().hour.at("20:10").do(scan)
schedule.every().hour.at("30:10").do(scan)
schedule.every().hour.at("40:10").do(scan)
schedule.every().hour.at("50:10").do(scan)
scan()
while True:
    schedule.run_pending()
    time.sleep(1)

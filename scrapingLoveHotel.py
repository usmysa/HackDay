# -*- coding: utf-8 -*-

import json
import base64
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def getLatLng(_json, address):
    lat = 0
    lng = 0
    try:
        lat = _json["results"][0]["geometry"]["location"]["lat"]
        lng = _json["results"][0]["geometry"]["location"]["lng"]
    except IndexError:
        query = "http://www.geocoding.jp/api/?v=1.1&q=" + address
        address_xml = BeautifulSoup(urllib2.urlopen(query.replace(" ", "").encode("utf-8")), "html.parser")
        lat = address_xml.find("lat").text
        lng = address_xml.find("lng").text

    return (lat, lng)


if __name__ == "__main__":
    hostname = "localhost"
    dbname = "HackDay"
    username = "root"
    password = base64.b64decode( open('pass.dat', 'r').read().strip() )
    connector = MySQLdb.connect(host=hostname, db=dbname, user=username, passwd=password, charset="utf8")
    cursor = connector.cursor()

    url = 'http://www.love-hotels.jp/t/?q=tokyo,toshima.tokyo,shinjuku.tokyo,taito.tokyo,shibuya.tokyo,hachioji.tokyo,adachi.tokyo,shinagawa.tokyo,ota.tokyo,sumida.tokyo,edogawa.tokyo,minato.tokyo,bunkyo.tokyo,machida.tokyo,arakawa.tokyo,tachikawa.tokyo,katsushika.tokyo,suginami.tokyo,mizuho.tokyo,kita.tokyo,chiyoda.tokyo,akishima.tokyo,kokubunji.tokyo,kunitachi.tokyo,higashimurayama.tokyo,higashiyamato.tokyo,akiruno.tokyo,koto.tokyo,setagaya.tokyo,fuchu.tokyo,ome.tokyo,meguro.tokyo,chuo.tokyo,musashino.tokyo,tama.tokyo,chofu.tokyo,itabashi.tokyo,nakano.tokyo,nerima.tokyo,nishitokyo.tokyo,kodaira.tokyo,higashikurume.tokyo,fussa.tokyo,musashimurayama.tokyo,koganei.saitama,saitama_iwatsuki.saitama,saitama_omiya.saitama,saitama_kita.saitama,saitama_minami.saitama,saitama_midori.saitama,saitama_urawa.saitama,saitama_sakura.saitama,saitama_chuo.saitama,kawaguchi.saitama,honjo.saitama,kawagoe.saitama,koshigaya.saitama,tokorozawa.saitama,kuki.saitama,gyoda.saitama,fukaya.saitama,toda.saitama,higashimatsuyama.saitama,kumagaya.saitama,sayama.saitama,iruma.saitama,niiza.saitama,kitamoto.saitama,kasukabe.saitama,misato.saitama,tsurugashima.saitama,hidaka.saitama,sakado.saitama,yashio.saitama,hasuda.saitama,nagatoro.saitama,miyoshi.saitama,namegawa.saitama,fujimi.saitama,konosu.saitama,shiki.saitama,warabi.saitama,soka.saitama,hanyu.saitama,ina.saitama,hanno.saitama,okegawa.saitama,miyashiro.saitama,shiraoka.saitama,kazo.saitama,yorii.saitama,wako.saitama,satte.saitama,matsubushi.saitama,asaka.saitama,minano.kanagawa,hadano.kanagawa,hiratsuka.kanagawa,hayama.kanagawa,ebina.kanagawa,oi.kanagawa,miura.kanagawa,matsuda.kanagawa,kamakura.kanagawa,ayase.kanagawa,manatsuru.kanagawa,ninomiya.kanagawa,yugawara.kanagawa,samukawa.kanagawa,zama.chiba,isumi.chiba,sakura.chiba,yotsukaido.chiba,shiroi.chiba,nagara.chiba,kamogawa.chiba,katsura.chiba,oamishirasato.chiba,shisui.chiba,otaki.chiba,tonosho.chiba,minamiboso.chiba,shibayama.chiba,mutsuzawa.tochigi,utsunomiya.tochigi,ashikaga.tochigi,nasushiobara.tochigi,tochigi.tochigi,sano.tochigi,nasu.tochigi,oyama.tochigi,kanuma.tochigi,nikko.tochigi,yaita.tochigi,shimotsuke.tochigi,mashiko.tochigi,nasukarasuyama.tochigi,otawara.tochigi,moka.tochigi,takanezawa.tochigi,mibu.tochigi,nogi.tochigi,haga.tochigi,sakura.tochigi,shioya.ibaraki,tsuchiura.ibaraki,tsukuba.ibaraki,kasama.ibaraki,kamisu.ibaraki,koga.ibaraki,hitachi.ibaraki,bando.ibaraki,chikusei.ibaraki,inashiki.ibaraki,shimotsuma.ibaraki,hokota.ibaraki,naka.ibaraki,kashima.ibaraki,hitachinaka.ibaraki,toride.ibaraki,ibaraki.ibaraki,omitama.ibaraki,ryugasaki.ibaraki,oarai.ibaraki,sakuragawa.ibaraki,kasumigaura.ibaraki,tsukubamirai.ibaraki,kitaibaraki.ibaraki,miho.ibaraki,joso.ibaraki,ami.ibaraki,yuki.ibaraki,tokai.ibaraki,yachiyo.ibaraki,itako.ibaraki,ushiku.ibaraki,namegata.ibaraki,daigo.ibaraki,ishioka.gunma,isesaki.gunma,takasaki.gunma,yoshioka.gunma,maebashi.gunma,ota.gunma,fujioka.gunma,annaka.gunma,ora.gunma,shibukawa.gunma,numata.gunma,tatebayashi.gunma,kiryu.gunma,midori.gunma,meiwa&color=000000&border=000000&bg=ffffff"'
    page = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    hotel_record = page.find_all("tr")[1:]
    for record in hotel_record:
        table_data = record.find_all("td")
        reviews = record.find("span", {"class": "star"}).text
        name = table_data[1].text
        address = table_data[2].text.strip()

        query = u"http://maps.google.com/maps/api/geocode/json?address=" + address + u"&sensor=false"
        address_json = json.load(urllib2.urlopen(query.replace(" ", "").encode("utf-8")))

        lat, lng = getLatLng(address_json, address)
        print name, address, lat, lng
        cursor.execute('INSERT INTO love_hotel (name, address, lat, lng) VALUES (%s, %s, %s, %s)' , (name, address, str(lat), str(lng)))
        connector.commit()

    connector.close()

# encoding: shift_jis
import urllib2
import sys
import os
import json

usage = """GoogleSpeechRecog.py

���g����
 GoogleSpeechRecog.py test.flac
 �ȉ���flac.exe���g�p�����wav����flac�֊ȒP�ɕϊ����邱�Ƃ��ł��܂��D
    http://sourceforge.net/projects/flac/files/flac-win/
 �f�t�H���g�ł�10best�̔F�����ʂ��o�͂��܂��D
"""

def RecogFlac( filename , nbest=1 ):
    if not os.path.exists( filename ):
        return []

    try:
        recogRes = []
        url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=%d" % nbest;

        data = open( filename , "rb" ).read()
        req = urllib2.Request( url , data )
        req.add_header( "Content-Type" , "audio/x-flac; rate=16000" )

        result = urllib2.urlopen(req).read().decode( "utf_8" )

        data = json.loads(result)
        #print "status:%d"%data["status"]
        for u in data["hypotheses"]:
            if "confidence" in u:
                recogRes.append( (u["utterance"].encode("sjis"),u["confidence"]) )
            else:
                recogRes.append( (u["utterance"].encode("sjis"),0.0) )
        return recogRes
    except:
        return []

if __name__ == '__main__':
    if len(sys.argv)==2:
        for r in RecogFlac( sys.argv[1] , 10 ):
            print "%s:%lf" %( r[0] , r[1] )
    else:
        print usage

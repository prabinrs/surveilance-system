import json

from django.http import HttpResponse

from sms_handler.SmsParser import SmsParser


sample_sms = "J1!test_form_2!uuid#ce546ca8b4c44c329685cffccb7c90c8\
#Question_1#option_3#Question_2#option_2 option_3 option_5\
#Question_3#Bdhud\#\#\#\#hbxbc#Question_4#8451#Question_5#469464.349\
#question_6#2016-01-18#Question_7#16:20:00.000+05:45#Question_8\
#27.7111128 85.318415 0.0 36.0#Question_9#1453113337876.jpg#Question_10\
#1453113348755.amr#Question_11#1453113368638.mp4#start\
#2016-01-18T16:19:38.539+05:45#end#2016-01-18T16:21:15.762+05:45\
#instanceID#uuid:9eea2d7d-8091-4d22-8472-bbbe3395b25f#"


def sms_data_api(request):
    sms_parser = SmsParser(sample_sms)
    return HttpResponse(json.dumps(sms_parser.parameters))

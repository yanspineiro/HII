from serializers import ApiFromSFSerializer
from models import APIFromSF
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from xmlrpcclient import XMLRPCClient
import xml.etree.ElementTree as Et
import urllib2
import httplib
from  sf_bridge.utils.generatedictxml import XMLRenderer
from models import ProductDictionary
import datetime


# Create your views here.
@api_view(['POST'])
def sf_bridge_list(request):
    if request.method == 'POST':
        serializer = ApiFromSFSerializer(data=request.DATA)
        if serializer.is_valid():
            rpc_client = XMLRPCClient()
            array_map = request.DATA['full_post'].split(",")
            obj_dict = {}
            xml_quote = ''
            try:
                dict_gen = ProductDictionary(array_map)
                for obj in array_map:
                    xml_quote = obj
                    key_value = obj.split(":")
                    obj_dict[key_value[0].strip()] = key_value[1].strip()
                plan_id = ''

                response_question = ''
                url_quote = 'http://test1.hiiquote.com/webservice/quote_service.php'
                url_process = 'http://test1.hiiquote.com/webservice/process.php'
                url_question = 'http://test1.hiiquote.com/webservice/quote_service.php'
                if obj_dict.get('Health_Plan_Type__c') is not None:

                    if obj_dict.get('Health_Plan_Type__c') == 'Guaranteed Issue':
                        plan_id = '54'
                        dic_quot = dict_gen.gen_principle_adventage_quote_dic(request.DATA['user_name'], plan_id)
                        dic_quot = XMLRenderer().render(dic_quot,'QuoteRequest')
                        xml_quote = rpc_client.send_quote(url_quote,dic_quot)

                    if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and '1st Med STM Health' in  str(obj_dict.get('STM_Type__c')):
                        plan_id = '19'
                        xml_quote = rpc_client.send_quote_1_SMT(url_quote,obj_dict, request.DATA['user_name'], plan_id)
                    if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and 'HealtheMed STM Health' in str(obj_dict.get('STM_Type__c')):
                        plan_id = '56'
                        xml_quote = rpc_client.send_quote_healthemed_SMT(url_quote,obj_dict, request.DATA['user_name'], plan_id)

                    root = Et.fromstring(xml_quote)
                    dict_quote_data = {}
                    if obj_dict.get('Health_Plan_Type__c') == 'Guaranteed Issue':
                        dict_quote_data = get_quote_toke_add_ons(xml_quote, 'Principle Advantage')

                    if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and '1st Med STM Health' in str(obj_dict.get('STM_Type__c')):
                        dict_quote_data = get_quote_toke_add_ons(xml_quote, 'STM')

                    if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and 'HealtheMed STM Health' in  str(obj_dict.get('STM_Type__c')):
                         dict_quote_data = get_quote_toke_add_ons(xml_quote, 'STM')



                    error = dict_quote_data.get('Error')
                    token = dict_quote_data.get('Token')
                    quote_id = dict_quote_data.get('Quote')
                    add_ons_list = dict_quote_data.get('Add-ons')

                    if error != '':
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if obj_dict.get('Health_Plan_Type__c') == 'Guaranteed Issue':

                            enroll_data = dict_gen.get_principle_adventage_enrollment_dic(request.DATA['user_name'], plan_id,quote_id,token,xml_quote,'192.168.1.1',datetime.date.today())
                            enroll_data = XMLRenderer().render(enroll_data,'NewBusiness')
                            question =  rpc_client.post_xml(url_process, enroll_data)
                            # question =  rpc_client.send_enrollment(url_process, obj_dict,request.DATA['user_name'], plan_id, quote_id, token, root)
                            response_question = Et.fromstring(question)

                        if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and str(obj_dict.get('STM_Type__c')).__contains__('1st Med STM Health'):
                            question = rpc_client.get_question(url_question ,quote_id,request.DATA['user_name'],add_ons_list )
                            question_xml = Et.fromstring(question)

                            if len(question_xml.findall('Error')) == 0 :
                                question =  rpc_client.send_enrollment_STM(url_process, obj_dict,request.DATA['user_name'], plan_id, quote_id, token, root,question_xml )
                                return Response(question, status=status.HTTP_400_BAD_REQUEST)
                                response_question = Et.fromstring(question)
                                question_xml = response_question

                            if question_xml.findall('Error') is not None:
                                for child in question_xml:
                                    if child.tag == 'Error':
                                        for sub in child:
                                            error = error + ' ' + sub.text
                                return Response(error, status=status.HTTP_400_BAD_REQUEST)

                        if obj_dict.get('Health_Plan_Type__c') == 'Short Term Medical' and str(obj_dict.get('STM_Type__c')).__contains__('HealtheMed STM Health'):
                            question = rpc_client.get_question_healthemed_SMT(url_question ,quote_id,request.DATA['user_name'],add_ons_list )
                            question_xml = Et.fromstring(question)
                            if len(question_xml.findall('Error')) == 0 :
                                question =  rpc_client.send_enrollment_heathMed(url_process, obj_dict,request.DATA['user_name'], plan_id, quote_id, token, root,question_xml )
                                response_question = Et.fromstring(question)
                                question_xml = response_question

                            if question_xml.findall('Error') is not None:
                                for child in question_xml:
                                    if child.tag == 'Error':
                                        for sub in child:
                                            error = error + ' ' + sub.text
                                return Response(error, status=status.HTTP_400_BAD_REQUEST)

                #if obj_dict.get('Dental_Plan__c') is not None :
                 #      repo = rpc_client.send_quote_principal(url_quote, obj_dict, request.DATA['user_name'],plan_id)





            except urllib2.HTTPError, e:

                return Response(str(e.code), status=status.HTTP_406_NOT_ACCEPTABLE)
            except urllib2.URLError, e:

                return Response(str(e.reason), status=status.HTTP_406_NOT_ACCEPTABLE)
            except httplib.HTTPException, e:

                return Response('HTTPException', status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception , e:
                return Response(e.message, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(response_question, status=status.HTTP_410_GONE)
                # adata= (JSONParser).parse(serializer)
                # serializer.save()
                # return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sf_bridge_detail(request, pk):
    """
    Get, udpate, or delete a specific task
    """
    try:
        task = APIFromSF .objects.get(pk=pk)
    except APIFromSF.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApiFromSFSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApiFromSFSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # queryset = APIFromSF.objects.all()
        # serializer_class = ApiFromSFSerializer


def get_quote_toke_add_ons(xml_quote_request, product_type):
    error = ''
    token = ''
    quote_id = ''
    root = Et.fromstring(xml_quote_request)
    add_ons_list = list()
    quote_tag=''
    if product_type == 'STM':
        quote_tag = 'Quote_ID'
    else :
        quote_tag = 'Quote'


    for child in root:
        if child.tag == 'Error':
            for sub in child:
                error = error + ' ' + sub.text
            break

        if child.tag == 'Access_Token':
            token = child.text
        if child.tag == quote_tag:
            quote_id = child.text
        if child.tag == 'Add-ons':
            for sub in child:
                add_ons_list.append(sub.tag)
    dict_quote_data = {}
    dict_quote_data['Quote'] = quote_id
    dict_quote_data['Token'] = token
    dict_quote_data['Add-ons'] = add_ons_list
    dict_quote_data['Error'] = error

    return dict_quote_data


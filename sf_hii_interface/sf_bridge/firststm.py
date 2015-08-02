import xmlrpclib
import urllib2, urllib
import re
import HTMLParser
import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from sf_bridge.models import QuestionAnswer


class First_STM():
    def __init__(self):
        pass

    @staticmethod
    def send_quote_1_SMT(endpoint, dict_values, user_id, plan_id):
        root = Element('QuoteRequest')
        SubElement(root, 'User_ID').text = user_id
        SubElement(root, 'State').text = dict_values.get('Mailing_State__c')
        SubElement(root, 'Zip_Code').text = dict_values.get('Mailing_Zip_Code__c')

        if dict_values.get('Primary_Sex__c') == 'M':
            SubElement(root, 'Applicant_Gender').text = 'Male'
        else:
            SubElement(root, 'Applicant_Gender').text = 'Female'

        SubElement(root, 'Applicant_Age').text = dict_values.get('Primary_Age__c')
        SubElement(root, 'Applicant_DOB').text = dict_values.get('Primary_Date_of_Birth__c')

        if dict_values.get('Spouse_First_Name__c') is not None and dict_values.get('Spouse_First_Name__c') != '':
            SubElement(root, 'Include_Spouse').text = 'Yes'
        else:
            SubElement(root, 'Include_Spouse').text = 'No'

        if dict_values.get('Spouse_First_Name__c') is not None and dict_values.get('Spouse_First_Name__c') != '':
            SubElement(root, 'Spouse_Age').text = dict_values.get('Spouse_Age__c')
            SubElement(root, 'Spouse_DOB').text = dict_values.get('Spouse_Date_of_Birth__c')

        count_child = 0

        if dict_values.get('Child1_First_Name__c') is not None and dict_values.get('Child1_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child2_First_Name__c') is not None and dict_values.get('Child2_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child3_First_Name__c') is not None and dict_values.get('Child3_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child4_First_Name__c') is not None and dict_values.get('Child4_First_Name__c') != '':
            count_child += 1

        SubElement(root, 'Children_Count').text = str(count_child)
        SubElement(root, 'Payment_Option').text = '1'
        SubElement(root, 'Coinsurance_Limit').text = '$5,000'
        SubElement(root, 'Coinsurance_Percentage').text = '80_20'
        SubElement(root, 'Coverage_Days').text = '50'

        if dict_values.get('Tobacco_Use__c') == 'Yes':
            SubElement(root, 'Tobacco').text = 'Y'
        else:
            SubElement(root, 'Tobacco').text = 'N'

        SubElement(root, 'Plan_ID').text = plan_id

        if count_child > 0:

            dependents = SubElement(root, 'Dependents')
            if dict_values.get('Child1_First_Name__c') is not None and dict_values.get('Child1_First_Name__c') != '':
                dependent1 = SubElement(dependents, 'Dependent')

                if str(dict_values.get('Child1_Sex__c')).strip() == 'F':
                    SubElement(dependent1, 'Gender').text = 'Female'
                else:
                    SubElement(dependent1, 'Gender').text = 'Male'

                date_dob = datetime.date.strftime(dict_values.get('Child1_Date_of_Birth__c'))
                date_object = datetime.strptime(date_dob, "%Y-%m-%d")
                SubElement(dependent1, 'DOB').text = date_object.strftime("%m-%d-%Y")
                SubElement(dependent1, 'Age').text = dict_values.get('Child1_Age__c')

            if dict_values.get('Child2_First_Name__c') is not None and dict_values.get('Child2_First_Name__c') != '':
                dependent2 = SubElement(dependents, 'Dependent')

                if str(dict_values.get('Child2_Sex__c')).strip() == 'F':
                    SubElement(dependent2, 'Gender').text = 'Female'
                else:
                    SubElement(dependent2, 'Gender').text = 'Male'

                date_dob = datetime.date.strftime(dict_values.get('Child2_Date_of_Birth__c'))
                date_object = datetime.strptime(date_dob, "%Y-%m-%d")
                SubElement(dependent2, 'DOB').text = date_object.strftime("%m-%d-%Y")
                SubElement(dependent2, 'Age').text = dict_values.get('Child2_Age__c')

            if dict_values.get('Child3_First_Name__c') is not None and dict_values.get('Child3_First_Name__c') != '':
                dependent3 = SubElement(dependents, 'Dependent')

                if str(dict_values.get('Child3_Sex__c')).strip() == 'F':
                    SubElement(dependent3, 'Gender').text = 'Female'
                else:
                    SubElement(dependent3, 'Gender').text = 'Male'

                date_dob = datetime.date.strftime(dict_values.get('Child3_Date_of_Birth__c'))
                date_object = datetime.strptime(date_dob, "%Y-%m-%d")
                SubElement(dependent3, 'DOB').text = date_object.strftime("%m-%d-%Y")
                SubElement(dependent3, 'Age').text = dict_values.get('Child3_Age__c')

            if dict_values.get('Child4_First_Name__c') is not None and dict_values.get('Child4_First_Name__c') != '':
                dependent4 = SubElement(dependents, 'Dependent')

                if str(dict_values.get('Child4_Sex__c')).strip() == 'F':
                    SubElement(dependent4, 'Gender').text = 'Female'
                else:
                    SubElement(dependent4, 'Gender').text = 'Male'

                date_dob = datetime.date.strftime(dict_values.get('Child4_Date_of_Birth__c'))
                date_object = datetime.strptime(date_dob, "%Y-%m-%d")
                SubElement(dependent4, 'DOB').text = date_object.strftime("%m-%d-%Y")
                SubElement(dependent4, 'Age').text = dict_values.get('Child4_Age__c')

        xml_value = '<?xml version="1.0" encoding="iso-8859-1"?>' + tostring(root)

        server = xmlrpclib.ServerProxy(endpoint)
        result = server.QuoteRequest(xml_value)
        xml_value = result
        htm_parser = HTMLParser.HTMLParser()
        xml_value = htm_parser.unescape(xml_value)

        return xml_value

    @staticmethod
    def pp(dict_values, root):
        if dict_values.get('Plan_Size__c') == 'Individual':
            SubElement(root, 'Plan_Type').text = 'Single Member'
        if dict_values.get('Plan_Size__c') == 'Individual + Spouse':
            SubElement(root, 'Plan_Type').text = 'Member+1'
        if dict_values.get('Plan_Size__c') == 'Individual + Child':
            SubElement(root, 'Plan_Type').text = 'Member+1'
        if dict_values.get('Plan_Size__c') == 'Family':
            SubElement(root, 'Plan_Type').text = 'Family'
        if dict_values.get('Plan_Size__c') == 'Child Only':
            SubElement(root, 'Plan_Type').text = 'Individual'

    @staticmethod
    def send_enrollment_STM(host, dict_values, user_id, plan_id, quote_id, access_token, xml_quote, stm_questions):
        question_answer = QuestionAnswer()
        root = Element('NewBusiness')
        SubElement(root, 'Plan_ID').text = plan_id
        SubElement(root, 'User_ID').text = user_id
        SubElement(root, 'Quote_ID').text = quote_id
        SubElement(root, 'Access_Token').text = access_token

        if dict_values.get('Plan_Size__c') == 'Child Only':
            SubElement(root, 'Parent_First_Name').text = dict_values.get('Primary_First_Name__c')
            SubElement(root, 'Parent_Middle_Name').text = dict_values.get('Primary_Middle_Name__c')
            SubElement(root, 'Parent_Last_Name').text = dict_values.get('Primary_Last_Name__c')
            if dict_values.get('Primary_Sex__c') == 'M':
                SubElement(root, 'Parent_Gender').text = 'Male'
            else:
                SubElement(root, 'Parent_Gender').text = 'Female'
            SubElement(root, 'Parent_DOB').text = dict_values.get('Primary_Date_of_Birth__c')
            SubElement(root, 'Parent_Address').text = dict_values.get('Mailing_Address__c')
            SubElement(root, 'Parent_City').text = dict_values.get('Mailing_City__c')
            SubElement(root, 'Parent_State').text = dict_values.get('Mailing_State__c')
            SubElement(root, 'Parent_ZipCode').text = dict_values.get('Mailing_Zip_Code__c')
            ##SubElement(root, 'Parent_Email')
            phone = re.sub(r'\D', '', dict_values.get('Contact_Phone__c'))
            phone = phone.lstrip('1')
            SubElement(root, 'Parent_DayPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

            if dict_values.get('Contact_Alt_Phone__c') is not None or dict_values.get('Contact_Alt_Phone__c') != '':
                phone_a = re.sub(r'\D', '', dict_values.get('Contact_Alt_Phone__c'))
                phone_a = phone_a.lstrip('1')
                SubElement(root, 'Parent_EveningPhone').text = '{}-{}-{}'.format(phone_a[0:3], phone_a[3:6],
                                                                                 phone_a[6:])
            else:
                SubElement(root, 'Parent_EveningPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

        SubElement(root, 'First_Name').text = dict_values.get('Primary_First_Name__c')
        SubElement(root, 'Middle_Name').text = dict_values.get('Primary_Middle_Name__c')
        SubElement(root, 'Last_Name').text = dict_values.get('Primary_Last_Name__c')

        if dict_values.get('Primary_Sex__c') == 'M':
            SubElement(root, 'Gender').text = 'Male'
        else:
            SubElement(root, 'Gender').text = 'Female'

        SubElement(root, 'DOB').text = dict_values.get('Primary_Date_of_Birth__c')
        SubElement(root, 'Age').text = dict_values.get('Primary_Age__c')
        SubElement(root, 'Occupation').text = dict_values.get('Primary_Occupation__c')

        SubElement(root, 'Feet').text = ''
        SubElement(root, 'Inch').text = ''
        # Primary_Height__c
        SubElement(root, 'Weight').text = dict_values.get('Primary_Weight__c')

        SubElement(root, 'Address').text = dict_values.get('Mailing_Address__c')
        SubElement(root, 'City').text = dict_values.get('Mailing_City__c')
        SubElement(root, 'State').text = dict_values.get('Mailing_State__c')
        SubElement(root, 'ZipCode').text = dict_values.get('Mailing_Zip_Code__c')
        #SubElement(root, 'Email').text = dict_values.get('Contact_Email__c')

        phone = re.sub(r'\D', '', dict_values.get('Contact_Phone__c'))
        phone = phone.lstrip('1')
        SubElement(root, 'DayPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

        if dict_values.get('Contact_Alt_Phone__c') is not None or dict_values.get('Contact_Alt_Phone__c') != '':
            phone_a = re.sub(r'\D', '', dict_values.get('Contact_Alt_Phone__c'))
            phone_a = phone_a.lstrip('1')
            SubElement(root, 'EveningPhone').text = '{}-{}-{}'.format(phone_a[0:3], phone_a[3:6], phone_a[6:])
        else:
            SubElement(root, 'EveningPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

        SubElement(root, 'Mailing_Name').text = dict_values.get('Primary_Full_Name__c')
        SubElement(root, 'Mailing_Address').text = dict_values.get('Mailing_Address__c')
        SubElement(root, 'Mailing_City').text = dict_values.get('Mailing_City__c')
        SubElement(root, 'Mailing_State').text = dict_values.get('Mailing_State__c')
        SubElement(root, 'Mailing_ZipCode').text = dict_values.get('Mailing_Zip_Code__c')

        SubElement(root, 'Beneficiary_First_Name')
        SubElement(root, 'Beneficiary_Last_Name')
        SubElement(root, 'Beneficiary_Relationship')
        SubElement(root, 'Contingent_First_Name')
        SubElement(root, 'Contingent_Last_Name')
        SubElement(root, 'Contingent_Relationship')
        SubElement(root, 'Estate_Flag').text = '1'
        SubElement(root, 'Estate_Detail').text = 'ESTATE'

        First_STM.pp(dict_values, root)

        SubElement(root, 'Payment_Option').text = '1'

        if str(dict_values.get('Product_Name')).__contains__('6 months'):
            SubElement(root, 'Duration_Coverage').text = '6'
        if str(dict_values.get('Product_Name')).__contains__('12 months'):
            SubElement(root, 'Duration_Coverage').text = '12'

        SubElement(root, 'Coinsurance_Limit').text = '$5,000'
        SubElement(root, 'Coinsurance_Percentage').text = '80_20'
        SubElement(root, 'Deductible_Option').text = dict_values.get('STM_Deductable_Amounts__c')
        SubElement(root, 'Effective_Date').text = dict_values.get('Effective_Date__c')
        SubElement(root, 'EffectiveDate_Ack').text = 'Agree'

        if str(dict_values.get('Product_Name')).__contains__('6 months'):
            sub_tree_sixmonth = xml_quote.findall('SixMonth')[0]
            option_srt = str(dict_values.get('STM_Deductable_Amounts__c'))
            option_srt = 'Option' + option_srt.replace('$', '')
            option_text = sub_tree_sixmonth.findall(option_srt)[0].text
            SubElement(root, 'Premium').text = option_text
            SubElement(root, 'Enrollment_Fee').text = sub_tree_sixmonth.findall('EnrollmentFe')[0]
            SubElement(root, 'Administrative_Fee').text = sub_tree_sixmonth.findall('AdministrativeFee')[0]

        if str(dict_values.get('Product_Name')).__contains__('12 months'):
            sub_tree_TwelveMonth = xml_quote.findall('TwelveMonth')[0]
            option_srt = str(dict_values.get('STM_Deductable_Amounts__c'))
            option_srt = 'Option' + option_srt.replace('$', '')
            option_text = sub_tree_TwelveMonth.findall(option_srt)[0].text
            SubElement(root, 'Premium').text = option_text
            SubElement(root, 'Enrollment_Fee').text = sub_tree_TwelveMonth.findall('EnrollmentFe')[0]
            SubElement(root, 'Administrative_Fee').text = sub_tree_TwelveMonth.findall('AdministrativeFee')[0]

        STMHealthQuestion = SubElement(root, 'STMHealthQuestion')
        for que in stm_questions.findall('Que'):
            que_id = que.findall('ID')[0].text
            answer = question_answer.get(que_id)
            question = SubElement(STMHealthQuestion, 'Que')
            SubElement(question, 'ID').text = que_id
            SubElement(question, 'Answer').text = answer

        if str(dict_values.get('Payment_Method')).strip() == 'CreditCard':
            SubElement(root, 'Payment_Method').text = 'CreditCard'
            SubElement(root, 'Card_Type').text = str(dict_values.get('Card_Type')).strip()
            SubElement(root, 'Card_Number').text = str(dict_values.get('Card_Number')).strip()
            SubElement(root, 'Card_ExpirationMonth').text = str(dict_values.get('Card_ExpirationMonth')).strip()
            SubElement(root, 'Card_ExpirationYear').text = str(dict_values.get('Card_ExpirationYear')).strip()
            SubElement(root, 'CardHolder_Name').text = str(dict_values.get('CardHolder_Name')).strip()
        else:
            SubElement(root, 'Payment_Method').text = 'BankDraft'
            SubElement(root, 'Bank_Account_Name').text = str(dict_values.get('Bank_Account_Name')).strip()
            SubElement(root, 'Bank_Account_Class').text = str(dict_values.get('Bank_Account_Class')).strip()
            SubElement(root, 'Bank_Account_Type').text = str(dict_values.get('Bank_Account_Type')).strip()
            SubElement(root, 'Bank_Name').text = str(dict_values.get('Bank_Name')).strip()
            SubElement(root, 'Bank_Location').text = str(dict_values.get('Bank_Location')).strip()
            SubElement(root, 'Bank_Routing_Number').text = str(dict_values.get('Bank_Routing_Number')).strip()
            SubElement(root, 'Bank_Account_Number').text = str(dict_values.get('Bank_Account_Number')).strip()
            SubElement(root, 'Bank_Check_Number').text = str(dict_values.get('Bank_Check_Number')).strip()

        SubElement(root, 'Billing_Address').text = str(dict_values.get('Billing_Address')).strip()
        SubElement(root, 'Billing_City').text = str(dict_values.get('Billing_City')).strip()
        SubElement(root, 'Billing_State').text = str(dict_values.get('Billing_State')).strip()
        SubElement(root, 'Billing_ZipCode').text = str(dict_values.get('Billing_ZipCode')).strip()
        SubElement(root, 'Payment_Agree').text = '1'
        SubElement(root, 'Medsense_Agree').text = '1'
        SubElement(root, 'Termscondition_Agree').text = '1'
        SubElement(root, 'MedCare_Agree').text = '1'
        SubElement(root, 'Careington_Agree').text = '1'

        SubElement(root, 'Name_Enroll').text = str(dict_values.get('Primary_Full_Name__c')).strip()
        SubElement(root, 'Name_Auth').text = str(dict_values.get('Primary_Full_Name__c')).strip()
        SubElement(root, 'Date_Signed').text = '2015-07-21'
        SubElement(root, 'IP_Address').text = '192.168.1.19'

        dependes = SubElement(root, 'Dependents')

        if dict_values.get('Spouse_First_Name__c') is not None and dict_values.get('Spouse_First_Name__c') != '':
            spouse_depent = SubElement(dependes, 'Dependent')
            SubElement(spouse_depent, 'Relation').text = 'Spouse'
            SubElement(spouse_depent, 'First_Name').text = dict_values.get('Spouse_First_Name__c')
            SubElement(spouse_depent, 'Middle_Name').text = dict_values.get('Spouse_Middle_Name__c')
            SubElement(spouse_depent, 'Last_Name').text = dict_values.get('Spouse_Last_Name__c')

            if str(dict_values.get('Spouse_Sex__c')).strip() == 'F':
                SubElement(spouse_depent, 'Gender').text = 'Female'
            else:
                SubElement(spouse_depent, 'Gender').text = 'Male'

            SubElement(spouse_depent, 'DOB').text = dict_values.get('Spouse_Date_of_Birth__c')
            SubElement(spouse_depent, 'Age').text = dict_values.get('Spouse_Age__c')

        if dict_values.get('Child1_First_Name__c') is not None and dict_values.get('Child1_First_Name__c') != '':
            child_depent = SubElement(dependes, 'Dependent')
            SubElement(child_depent, 'Relation').text = 'Child'
            SubElement(child_depent, 'First_Name').text = dict_values.get('Child1_First_Name__c')
            SubElement(child_depent, 'Middle_Name').text = dict_values.get('Child1_Middle__c')
            SubElement(child_depent, 'Last_Name').text = dict_values.get('Child1_Last_Name__c')

            if str(dict_values.get('Child1_Sex__c')).strip() == 'F':
                SubElement(child_depent, 'Gender').text = 'Female'
            else:
                SubElement(child_depent, 'Gender').text = 'Male'

            SubElement(child_depent, 'DOB').text = dict_values.get('Child1_Date_of_Birth__c')
            SubElement(child_depent, 'Age').text = dict_values.get('Child1_Age__c')

        if dict_values.get('Child2_First_Name__c') is not None and dict_values.get('Child2_First_Name__c') != '':
            child_depent = SubElement(dependes, 'Dependent')
            SubElement(child_depent, 'Relation').text = 'Child'
            SubElement(child_depent, 'First_Name').text = dict_values.get('Child2_First_Name__c')
            SubElement(child_depent, 'Middle_Name').text = dict_values.get('Child2_Middle__c')
            SubElement(child_depent, 'Last_Name').text = dict_values.get('Child2_Last_Name__c')

            if str(dict_values.get('Child2_Sex__c')).strip() == 'F':
                SubElement(child_depent, 'Gender').text = 'Female'
            else:
                SubElement(child_depent, 'Gender').text = 'Male'

            SubElement(child_depent, 'DOB').text = dict_values.get('Child2_Date_of_Birth__c')
            SubElement(child_depent, 'Age').text = dict_values.get('Child2_Age__c')

        if dict_values.get('Child3_First_Name__c') is not None and dict_values.get('Child3_First_Name__c') != '':
            child_depent = SubElement(dependes, 'Dependent')
            SubElement(child_depent, 'Relation').text = 'Child'
            SubElement(child_depent, 'First_Name').text = dict_values.get('Child3_First_Name__c')
            SubElement(child_depent, 'Middle_Name').text = dict_values.get('Child3_Middle__c')
            SubElement(child_depent, 'Last_Name').text = dict_values.get('Child3_Last_Name__c')

            if str(dict_values.get('Child3_Sex__c')).strip() == 'F':
                SubElement(child_depent, 'Gender').text = 'Female'
            else:
                SubElement(child_depent, 'Gender').text = 'Male'

            SubElement(child_depent, 'DOB').text = dict_values.get('Child3_Date_of_Birth__c')
            SubElement(child_depent, 'Age').text = dict_values.get('Child3_Age__c')

        if dict_values.get('Child4_First_Name__c') is not None and dict_values.get('Child4_First_Name__c') != '':
            child_depent = SubElement(dependes, 'Dependent')
            SubElement(child_depent, 'Relation').text = 'Child'
            SubElement(child_depent, 'First_Name').text = dict_values.get('Child4_First_Name__c')
            SubElement(child_depent, 'Middle_Name').text = dict_values.get('Child4_Middle__c')
            SubElement(child_depent, 'Last_Name').text = dict_values.get('Child4_Last_Name__c')

            if str(dict_values.get('Child4_Sex__c')).strip() == 'F':
                SubElement(child_depent, 'Gender').text = 'Female'
            else:
                SubElement(child_depent, 'Gender').text = 'Male'

            SubElement(child_depent, 'DOB').text = dict_values.get('Child4_Date_of_Birth__c')
            SubElement(child_depent, 'Age').text = dict_values.get('Child4_Age__c')

        add_ons = SubElement(root, 'Add-ons')
        add_on_tree = xml_quote.findall('Add-ons')[0]

        if dict_values.get('Additional_Product_1') is not None and dict_values.get('Additional_Product_1') != '':
            freedom_tree = add_on_tree.findall(dict_values.get('Additional_Product_1_ID'))[0]
            if freedom_tree is not None:
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == dict_values.get('Additional_Product_1_Price'):
                        plan_add_on = SubElement(add_on_tree, 'Plan')
                        SubElement(plan_add_on, 'Name').text = plan_child.findall('Name')[0].text
                        SubElement(plan_add_on, 'Premium').text = plan_child.findall('Premium')[0].text
                        SubElement(plan_add_on, 'AdministrativeFee').text = plan_child.findall('AdministrativeFee')[
                            0].text
                        SubElement(plan_add_on, 'EnrollmentFee').text = plan_child.findall('EnrollmentFee')[0].text

        if dict_values.get('Additional_Product_2') is not None and dict_values.get('Additional_Product_2') != '':
            freedom_tree = add_on_tree.findall(dict_values.get('Additional_Product_2_ID'))[0]
            if freedom_tree is not None:
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == dict_values.get('Additional_Product_2_Price'):
                        plan_add_on = SubElement(add_on_tree, 'Plan')
                        SubElement(plan_add_on, 'Name').text = plan_child.findall('Name')[0].text
                        SubElement(plan_add_on, 'Premium').text = plan_child.findall('Premium')[0].text
                        SubElement(plan_add_on, 'AdministrativeFee').text = plan_child.findall('AdministrativeFee')[
                            0].text
                        SubElement(plan_add_on, 'EnrollmentFee').text = plan_child.findall('EnrollmentFee')[0].text

        if dict_values.get('Additional_Product_3') is not None and dict_values.get('Additional_Product_3') != '':
            freedom_tree = add_on_tree.findall(dict_values.get('Additional_Product_3_ID'))[0]
            if freedom_tree is not None:
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == dict_values.get('Additional_Product_3_Price'):
                        plan_add_on = SubElement(add_on_tree, 'Plan')
                        SubElement(plan_add_on, 'Name').text = plan_child.findall('Name')[0].text
                        SubElement(plan_add_on, 'Premium').text = plan_child.findall('Premium')[0].text
                        SubElement(plan_add_on, 'AdministrativeFee').text = plan_child.findall('AdministrativeFee')[
                            0].text
                        SubElement(plan_add_on, 'EnrollmentFee').text = plan_child.findall('EnrollmentFee')[0].text

        if dict_values.get('Additional_Product_3') is not None and dict_values.get('Additional_Product_3') != '':
            freedom_tree = add_on_tree.findall(dict_values.get('Additional_Product_3_ID'))[0]
            if freedom_tree is not None:
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == dict_values.get('Additional_Product_3_Price'):
                        plan_add_on = SubElement(add_on_tree, 'Plan')
                        SubElement(plan_add_on, 'Name').text = plan_child.findall('Name')[0].text
                        SubElement(plan_add_on, 'Premium').text = plan_child.findall('Premium')[0].text
                        SubElement(plan_add_on, 'AdministrativeFee').text = plan_child.findall('AdministrativeFee')[
                            0].text
                        SubElement(plan_add_on, 'EnrollmentFee').text = plan_child.findall('EnrollmentFee')[0].text

        SubElement(root, 'Email').text = dict_values.get('Contact_Email__c')
        if dict_values.get('Plan_Size__c') == 'Child Only':
            SubElement(root, 'Parent_Email').text = dict_values.get('Contact_Email__c')

        xml_value = '<?xml version="1.0" encoding="iso-8859-1"?>' + tostring(root)
        #xml_value = xml_value.replace('<Parent_Email />', '<Parent_Email>' + dict_values.get('Contact_Email__c') + '</Parent_Email>')
        #xml_value = xml_value.replace('<Email />', '<Email>' + dict_values.get('Contact_Email__c') + '</Email>')
        return xml_value
        # , headers={'Content-Type': 'text/xml; charset=utf-8'}
        da = { 'HII_New_Business' : xml_value}
        data = urllib .urlencode(da)
        req = urllib2.Request(host, data )
        req.add_header('Content-Length', len(xml_value))

        urlopen = urllib2.urlopen(req)

        response = urlopen.read()
        return response

    @staticmethod
    def get_question(endpoint, quote_id, user_id, add_ons_list):
        root = Element('HealthQuestion')
        user_id_child = SubElement(root, 'User_ID')
        user_id_child.text = user_id
        quote_id_child = SubElement(root, 'Quote_ID')
        quote_id_child.text = quote_id
        add_ons_child = SubElement(root, 'Add-ons')

        for item in add_ons_list:
           sub_child = SubElement(add_ons_child, 'ID')
           if item.startswith('ID'):
               sub_child.text = item[len('ID'):]
           else:
               sub_child.text = item


        xml_value = '<?xml version="1.0" encoding="iso-8859-1"?>' + tostring(root)
        #return  xml_value
        server = xmlrpclib.ServerProxy(endpoint)
        result = server.STMHealthQuestion(xml_value)
        xml_value = result
        htm_parser = HTMLParser.HTMLParser()
        xml_value = htm_parser.unescape(xml_value)

        return xml_value









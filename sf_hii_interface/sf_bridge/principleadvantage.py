import xmlrpclib
import urllib2
import re
import HTMLParser
from xml.etree.ElementTree import Element, SubElement, tostring
import json
import urllib



class Principle_Advantage():
    def __init__(self):
        pass
    @staticmethod
    def send_quote_principal(endpoint, dict_values, user_id,plan_id):
        root = Element('QuoteRequest')

        user_id_child = SubElement(root, 'User_ID')
        user_id_child.text = user_id

        state_child = SubElement(root, 'State')
        state_child.text = dict_values.get('Mailing_State__c')

        zipcode_child = SubElement(root, 'Zip_Code')
        zipcode_child.text = dict_values.get('Mailing_Zip_Code__c')

        gender_child = SubElement(root, 'Applicant_Gender')
        if dict_values.get('Primary_Sex__c') == 'M':
            gender_child.text = 'Male'
        else:
            gender_child.text = 'Female'

        age_child = SubElement(root, 'Applicant_Age')
        age_child.text = dict_values.get('Primary_Age__c')

        spouse_child = SubElement(root, 'Include_Spouse')
        if dict_values.get('Spouse_First_Name__c') is not None and dict_values.get('Spouse_First_Name__c') != '':
            spouse_child.text = 'Yes'
        else:
            spouse_child.text = 'No'

        spouse_age_child = SubElement(root, 'Spouse_Age')
        if dict_values.get('Spouse_First_Name__c') is not None and dict_values.get('Spouse_First_Name__c') != '':
            spouse_age_child.text = dict_values.get('Spouse_Age__c')
        count_child = 0
        if dict_values.get('Child1_First_Name__c') is not None and dict_values.get('Child1_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child2_First_Name__c') is not None and dict_values.get('Child2_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child3_First_Name__c') is not None and dict_values.get('Child3_First_Name__c') != '':
            count_child += 1
        if dict_values.get('Child4_First_Name__c') is not None and dict_values.get('Child4_First_Name__c') != '':
            count_child += 1
        age_child = SubElement(root, 'Children_Count')
        age_child.text = str(count_child)

        tobacco_child = SubElement(root, 'Tobacco')
        if dict_values.get('Tobacco_Use__c') == 'Yes':
            tobacco_child.text = 'Y'
        else:
            tobacco_child.text = 'N'
        age_child = SubElement(root, 'Plan_ID')
        age_child.text = plan_id

        xml_value = '<?xml version="1.0" encoding="iso-8859-1"?>' + tostring(root)


        server = xmlrpclib.ServerProxy(endpoint)

        result = server.QuoteRequest(xml_value)

        # xml_value="&lt;?xml version=&quot;1.0&quot; encoding=&quot;iso-8859-1&quot;?&gt;&lt;QuoteResult&gt;&lt;Plan_Cost&gt;&lt;Plan_1&gt;&lt;Premium&gt;275.59&lt;/Premium&gt;&lt;TelaDocFee&gt;26.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_1&gt;&lt;Plan_2&gt;&lt;Premium&gt;192.90&lt;/Premium&gt;&lt;TelaDocFee&gt;26.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_2&gt;&lt;Plan_3&gt;&lt;Premium&gt;451.86&lt;/Premium&gt;&lt;TelaDocFee&gt;26.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_3&gt;&lt;Plan_4&gt;&lt;Premium&gt;566.11&lt;/Premium&gt;&lt;TelaDocFee&gt;26.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_4&gt;&lt;Plan_8&gt;&lt;Premium&gt;112.74&lt;/Premium&gt;&lt;TelaDocFee&gt;22.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_8&gt;&lt;Plan_9&gt;&lt;Premium&gt;130.08&lt;/Premium&gt;&lt;TelaDocFee&gt;22.50&lt;/TelaDocFee&gt;&lt;EnrollmentFee&gt;125.00&lt;/EnrollmentFee&gt;&lt;/Plan_9&gt;&lt;/Plan_Cost&gt;&lt;Add-ons&gt;&lt;ID25&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$1,000&lt;/Name&gt;&lt;Premium&gt;29.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$2,000&lt;/Name&gt;&lt;Premium&gt;34.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$3,000&lt;/Name&gt;&lt;Premium&gt;39.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$4,000&lt;/Name&gt;&lt;Premium&gt;44.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$5,000&lt;/Name&gt;&lt;Premium&gt;49.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Accident Insurance~~$10,000&lt;/Name&gt;&lt;Premium&gt;59.95&lt;/Premium&gt;&lt;AdministrativeFee&gt;7.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;/ID25&gt;&lt;ID24&gt;&lt;Plan&gt;&lt;Name&gt;Agile Copay Rx~~Agile Copay Rx&lt;/Name&gt;&lt;Premium&gt;30.69&lt;/Premium&gt;&lt;AdministrativeFee&gt;6.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;/ID24&gt;&lt;ID12&gt;&lt;Plan&gt;&lt;Name&gt;Foundation Dental~~Protector III&lt;/Name&gt;&lt;Premium&gt;22.78&lt;/Premium&gt;&lt;AdministrativeFee&gt;25.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;/ID12&gt;&lt;ID21&gt;&lt;Plan&gt;&lt;Name&gt;Freedom Spirit Plus~~50,000&lt;/Name&gt;&lt;Premium&gt;22.45&lt;/Premium&gt;&lt;AdministrativeFee&gt;16.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0.0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;Plan&gt;&lt;Name&gt;Freedom Spirit Plus~~100,000&lt;/Name&gt;&lt;Premium&gt;48.45&lt;/Premium&gt;&lt;AdministrativeFee&gt;16.00&lt;/AdministrativeFee&gt;&lt;EnrollmentFee&gt;0.0&lt;/EnrollmentFee&gt;&lt;MedsenseFee&gt;0&lt;/MedsenseFee&gt;&lt;Embeded&gt;No&lt;/Embeded&gt;&lt;/Plan&gt;&lt;/ID21&gt;&lt;/Add-ons&gt;&lt;Quote&gt;11348656&lt;/Quote&gt;&lt;Access_Token&gt;2015071710415555a9143360c78&lt;/Access_Token&gt;&lt;/QuoteResult&gt;"
        xml_value = result
        htm_parser = HTMLParser.HTMLParser()
        xml_value = htm_parser.unescape(xml_value)

        return xml_value



    @staticmethod
    def send_enrollment(host,  dict_values, user_id, plan_id, quote_id, access_token, xml_quote):
        root = Element('NewBusiness')
        SubElement(root, 'Plan_ID').text = plan_id
        SubElement(root, 'User_ID').text = user_id
        SubElement(root, 'Quote_ID').text = quote_id
        SubElement(root, 'Access_Token').text = access_token
        SubElement(root, 'First_Name').text = dict_values.get('Primary_First_Name__c')
        SubElement(root, 'Middle_Name').text = dict_values.get('Primary_Middle_Name__c')
        SubElement(root, 'Last_Name').text = dict_values.get('Primary_Last_Name__c')

        if  dict_values.get('Primary_Sex__c') == 'M':
            SubElement(root, 'Gender').text = 'Male'
        else:
            SubElement(root, 'Gender').text = 'Female'

        SubElement(root, 'DOB').text = dict_values.get('Primary_Date_of_Birth__c')
        SubElement(root, 'Age').text = dict_values.get('Primary_Age__c')
        SubElement(root, 'Occupation').text = dict_values.get('Primary_Occupation__c')
        SubElement(root, 'Address').text = dict_values.get('Mailing_Address__c')
        SubElement(root, 'City').text = dict_values.get('Mailing_City__c')
        SubElement(root, 'State').text = dict_values.get('Mailing_State__c')
        SubElement(root, 'ZipCode').text = dict_values.get('Mailing_Zip_Code__c')

        #SubElement(root, 'Email')
        phone = re.sub(r'\D', '', dict_values.get('Contact_Phone__c'))
        phone = phone.lstrip('1')
        SubElement(root, 'DayPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

        if dict_values.get('Contact_Alt_Phone__c') is not None or dict_values.get('Contact_Alt_Phone__c') != '':
            phone_a = re.sub(r'\D', '', dict_values.get('Contact_Alt_Phone__c'))
            phone_a = phone_a.lstrip('1')
            SubElement(root, 'EveningPhone').text = '{}-{}-{}'.format(phone_a[0:3], phone_a[3:6], phone_a[6:])
        else:
            SubElement(root, 'EveningPhone').text = '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

        SubElement(root, 'Beneficiary_First_Name')
        SubElement(root, 'Beneficiary_Last_Name')
        SubElement(root, 'Beneficiary_Relationship')
        SubElement(root, 'Contingent_First_Name')
        SubElement(root, 'Contingent_Last_Name')
        SubElement(root, 'Contingent_Relationship')
        SubElement(root, 'Estate_Flag').text = '1'
        SubElement(root, 'Estate_Detail').text = 'ESTATE'
        SubElement(root, 'Mailing_Name').text = dict_values.get('Primary_Full_Name__c')
        SubElement(root, 'Mailing_Address').text = dict_values.get('Mailing_Address__c')
        SubElement(root, 'Mailing_City').text = dict_values.get('Mailing_City__c')
        SubElement(root, 'Mailing_State').text = dict_values.get('Mailing_State__c')
        SubElement(root, 'Mailing_ZipCode').text = dict_values.get('Mailing_Zip_Code__c')

        if dict_values.get('Plan_Size__c')== 'Individual':
            SubElement(root, 'Plan_Type').text ='Single Member'
        if dict_values.get('Plan_Size__c')== 'Individual + Spouse':
            SubElement(root, 'Plan_Type').text ='Member+1'
        if dict_values.get('Plan_Size__c')== 'Individual + Child':
            SubElement(root, 'Plan_Type').text ='Member+1'
        if dict_values.get('Plan_Size__c')== 'Family':
            SubElement(root, 'Plan_Type').text ='Family'
        if dict_values.get('Plan_Size__c')== 'Child Only':
            SubElement(root, 'Plan_Type').text ='Individual'


        SubElement(root, 'Effective_Date').text = dict_values.get('Effective_Date__c')
        SubElement(root, 'EffectiveDate_Ack').text = 'Agree'

        name_plan=str(dict_values.get('Product_Name')).split('(')
        name_plan=name_plan[1].split(')')
        name_value = name_plan[0].strip()
        name_value = name_value.replace(' ', '_')
        SubElement(root, 'Plan_Name').text = name_value

        sub_tree_plan_cost = xml_quote.findall('Plan_Cost')[0]
        plan_tree = sub_tree_plan_cost.findall(name_value)[0]
        for child in plan_tree:
            if child.tag == 'Premium':
                SubElement(root, 'Premium').text = child.text
            if child.tag == 'EnrollmentFee':
                SubElement(root, 'Enrollment_Fee').text = child.text
            if child.tag == 'TelaDocFee':
                SubElement(root, 'TelaDoc_Fee').text = child.text
        if  str(dict_values.get('Payment_Method')).strip() == 'CreditCard':
            SubElement(root, 'Payment_Method').text = 'CreditCard'
            SubElement(root, 'Card_Type').text = str(dict_values.get('Card_Type')).strip()
            SubElement(root, 'Card_Number').text = str(dict_values.get('Card_Number')).strip()
            SubElement(root, 'Card_ExpirationMonth').text = str(dict_values.get('Card_ExpirationMonth')).strip()
            SubElement(root, 'Card_ExpirationYear').text = str(dict_values.get('Card_ExpirationYear')).strip()
            SubElement(root, 'CardHolder_Name').text = str(dict_values.get('CardHolder_Name')).strip()
        else :
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
        SubElement(root, 'Applicant_Agree').text = '1'
        SubElement(root, 'Member_Agree').text = '1'
        SubElement(root, 'Name_Enroll').text = str(dict_values.get('Primary_Full_Name__c')).strip()
        SubElement(root, 'Name_Auth').text = str(dict_values.get('Primary_Full_Name__c')).strip()
        SubElement(root, 'Date_Signed').text = '2015-07-21'
        SubElement(root, 'IP_Address').text = '192.168.1.19'
        dependes = SubElement(root, 'Dependents')

        if dict_values.get('Spouse_First_Name__c'):
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

        if dict_values.get('Child1_First_Name__c'):
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

        if dict_values.get('Child2_First_Name__c') :
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

        if dict_values.get('Child3_First_Name__c'):
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

        if dict_values.get('Child4_First_Name__c'):
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
        if dict_values.get('Additional_Product_1'):
            freedom_tree = add_on_tree.findall(dict_values.get('Additional_Product_1_ID'))[0]
            if freedom_tree is not None:
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == dict_values.get('Additional_Product_1_Price'):
                        plan_add_on = SubElement(add_on_tree, 'Plan')
                        SubElement(plan_add_on, 'Name').text = plan_child.findall('Name')[0].text
                        SubElement(plan_add_on, 'Premium').text = plan_child.findall('Premium')[0].text
                        SubElement(plan_add_on, 'AdministrativeFee').text = plan_child.findall('AdministrativeFee')[0].text
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
        xml_value = '<?xml version="1.0" encoding="iso-8859-1"?>' + tostring(root)
        #xml_value = xml_value.replace('<Email />', '<Email>' + dict_values.get('Contact_Email__c') + '</Email>')
        #return xml_value
        # xml_value = '<?xml version="1.0" encoding="iso-8859-1"?><NewBusiness><Plan_ID>54</Plan_ID><User_ID>A10000560000002</User_ID><Quote_ID>1309909</Quote_ID><Access_Token>2015072418324255b2bd0a69305</Access_Token><First_Name>Test</First_Name><Middle_Name>M</Middle_Name><Last_Name>BimSym</Last_Name><Gender>Male</Gender><DOB>1979-01-01</DOB><Age>35</Age><Occupation>Business</Occupation><Address>12, Square Road</Address><City>Akron</City><State>AL</State><ZipCode>35201</ZipCode><Email>testmail@bimsym.com</Email><DayPhone>123-456-8963</DayPhone><EveningPhone>132-869-8963</EveningPhone><Beneficiary_First_Name></Beneficiary_First_Name><Beneficiary_Last_Name></Beneficiary_Last_Name><Beneficiary_Relationship></Beneficiary_Relationship><Contingent_First_Name></Contingent_First_Name><Contingent_Last_Name></Contingent_Last_Name><Contingent_Relationship></Contingent_Relationship><Estate_Flag>1</Estate_Flag><Estate_Detail>ESTATE</Estate_Detail><Mailing_Name>TestFTestL</Mailing_Name><Mailing_Address>Test A</Mailing_Address><Mailing_City>Akron</Mailing_City><Mailing_State>AL</Mailing_State><Mailing_ZipCode>35201</Mailing_ZipCode><Plan_Type>Family</Plan_Type><Effective_Date>2014-07-31</Effective_Date><EffectiveDate_Ack>Agree</EffectiveDate_Ack><Plan_Name>Plan_4</Plan_Name><Premium>96.17</Premium><Enrollment_Fee>10.00</Enrollment_Fee><TelaDoc_Fee>15.00</TelaDoc_Fee><Payment_Method>CreditCard</Payment_Method><Card_Type>VISA</Card_Type><Card_Number>4111111111111111</Card_Number><Card_ExpirationMonth>12</Card_ExpirationMonth><Card_ExpirationYear>2012</Card_ExpirationYear><CardHolder_Name>Test BimSym</CardHolder_Name><Billing_Address>12,Square Road</Billing_Address><Billing_City>Texas</Billing_City><Billing_State>CA</Billing_State><Billing_ZipCode>12345</Billing_ZipCode><Payment_Agree>1</Payment_Agree><Applicant_Agree>1</Applicant_Agree><Member_Agree>1</Member_Agree><Name_Enroll>Test M BimSym</Name_Enroll><Name_Auth>Test M BimSym</Name_Auth><Date_Signed>2012-12-14</Date_Signed><IP_Address>174.168.20.20</IP_Address><Dependents><Dependent><Relation>Spouse</Relation><First_Name>Test</First_Name><Middle_Name></Middle_Name><Last_Name>Spouse</Last_Name><Gender>Female</Gender><DOB>1980-01-01</DOB><Age>34</Age></Dependent><Dependent><Relation>Child</Relation>	<First_Name>Test</First_Name>	<Middle_Name></Middle_Name><Last_Name>Child</Last_Name><Gender>Male</Gender><DOB>2005-01-01</DOB><Age>9</Age></Dependent></Dependents>'

        da = { 'HII_New_Business' : xml_value}
        data = urllib .urlencode(da)
        req = urllib2.Request(host, data )
        req.add_header('Content-Length', len(xml_value))
        urlopen = urllib2.urlopen(req)
        response = urlopen.read()
        return response

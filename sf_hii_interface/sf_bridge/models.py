from django.db import models
import datetime
from utils import utils_tool
import xml.etree.ElementTree as Et


class APIFromSF(models.Model):

    user_name = models.CharField(max_length=100, blank=True, default='')
    full_post = models.TextField(blank=True, default='')
    url_quote = models.TextField(blank=True, default='')
    url_Question = models.TextField(blank=True, default='')
    url_Enrrollment = models.TextField(blank=True, default='')
    product = models.CharField(max_length=100, blank=True, default='')
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __srt__(self):
        return self.name


class StripDictValue(object):
    def __init__(self, dict_values={}):
        self.dict_values = dict_values

    def get(self, key):
        if self.dict_values.get(key):
            return str(self.dict_values.get(key)).strip()
        else:
            return ''


class QuestionAnswer:
    def __init__(self):
        self.yes_list = [5, 9, 13]

    def get(self, key):
        key = int(key)
        d = {'True': 'Yes', 'False': 'No'}
        return d[str(key in self.yes_list)]


class ProductDictionary(StripDictValue):

    def __init__(self, array_map):
        super(ProductDictionary, self).__init__()
        for obj in array_map:
            key_value = obj.split(":")
            self.dict_values[key_value[0].strip()] = key_value[1].strip()

        self.gender_dict = {'M': 'Male', 'F': 'Female'}
        self.yes_no = {'Yes': 'Y', 'No': 'N'}
        self.plan_size = {'Individual': 'Single Member', 'Individual + Spouse': 'Member+1',
                          'Individual + Child': 'Member+1', 'Family': 'Family', 'Child Only': 'Individual'}

    def calc_child(self):
        count_child = 0
        if self.get('Child1_First_Name__c'):
            count_child += 1
        if self.get('Child2_First_Name__c'):
            count_child += 1
        if self.get('Child3_First_Name__c'):
            count_child += 1
        if self.dict_values.get('Child4_First_Name__c'):
            count_child += 1
        return count_child

    def gen_principle_adventage_quote_dic(self, user_id, plan_id):
        quote_dict = {
            'User_ID': user_id,
            'State': self.get('Mailing_State__c'),
            'Zip_Code': self.get('Mailing_Zip_Code__c'),
            'Applicant_Gender': self.gender_dict.get(self.get('Primary_Sex__c')),
            'Applicant_Age': self.get('Primary_Age__c'),
            'Children_Count':  self.calc_child(),
            'Tobacco': self.yes_no.get(self.dict_values.get('Tobacco_Use__c')),
            'Plan_ID': plan_id
        }
        quote_dict.append(self.have_spouse())
        return quote_dict

    def gen_payment(self):
        if str(self.get('Payment_Method')).strip() == 'CreditCard':
            payment = {
                'Payment_Method': 'CreditCard',
                'Card_Type': self.get('Card_Type'),
                'Card_Number': self.get('Card_Number'),
                'Card_ExpirationMonth': self.get('Card_ExpirationMonth'),
                'Card_ExpirationYear': self.get('Card_ExpirationYear'),
                'CardHolder_Name': self.get('CardHolder_Name'),
            }
        else:
            payment = {
                'Payment_Method': 'BankDraft',
                'Bank_Account_Name': self.get('Bank_Account_Name'),
                'Bank_Account_Class': self.get('Bank_Account_Class'),
                'Bank_Account_Type': self.get('Bank_Account_Type'),
                'Bank_Name': self.get('Bank_Name'),
                'Bank_Location': self.get('Bank_Location'),
                'Bank_Routing_Number': self.get('Bank_Routing_Number'),
                'Bank_Account_Number': self.get('Bank_Account_Number'),
                'Bank_Check_Number': self.get('Bank_Check_Number'),
            }
        return payment

    def get_principle_adventage_enrollment_dic(self, user_id, plan_id, quote_id, access_token, xml_quote, ip_address, s_date):

        xml_quote = Et.fromstring(xml_quote)

        enroll_quote = {
            'Plan_ID': plan_id,
            'User_ID': user_id,
            'Quote_ID': quote_id,
            'Access_Token': access_token,
            'First_Name': self.get('Primary_First_Name__c'),
            'Middle_Name': self.get('Primary_Middle_Name__c'),
            'Last_Name': self.get('Primary_Last_Name__c'),
            'Gender':  self.gender_dict.get(self.get('Primary_Sex__c')),
            'DOB': self.get('Primary_Date_of_Birth__c'),
            'Age': self.get('Primary_Age__c'),
            'Occupation': self.get('Primary_Occupation__c'),
            'Address': self.get('Mailing_Address__c'),
            'City': self.get('Mailing_City__c'),
            'State': self.get('Mailing_State__c'),
            'ZipCode': self.get('Mailing_Zip_Code__c'),
            'Email': self.get('Contact_Email__c'),
            'DayPhone': utils_tool.format_phone(self.get('Contact_Phone__c')),
            'Beneficiary_First_Name': '',
            'Beneficiary_Last_Name': '',
            'Beneficiary_Relationship': '',
            'Contingent_First_Name': '',
            'Contingent_Last_Name': '',
            'Contingent_Relationship': '',
            'Estate_Flag': '1',
            'Estate_Detail': 'ESTATE',
            'Mailing_Name': self.get('Primary_Full_Name__c'),
            'Mailing_Address': self.get('Mailing_Address__c'),
            'Mailing_City': self.get('Mailing_City__c'),
            'Mailing_State': self.get('Mailing_State__c'),
            'Mailing_ZipCode': self.get('Mailing_Zip_Code__c'),
            'Plan_Type': self.plan_size.get(self.get('Plan_Size__c')),
            'Effective_Date': self.get('Effective_Date__c'),
            'EffectiveDate_Ack': 'Agree',
            'Billing_Address': self.get('Mailing_Address__c'),
            'Billing_City': self.get('Mailing_City__c'),
            'Billing_State': self.get('Mailing_State__c'),
            'Billing_ZipCode': self.get('Mailing_Zip_Code__c'),
            'Payment_Agree': '1',
            'Applicant_Agree': '1',
            'Member_Agree': '1',
            'Name_Enroll':  self.get('Primary_Full_Name__c'),
            'Name_Auth': self.get('Primary_Full_Name__c'),
            'Date_Signed': s_date,
            'IP_Address': ip_address

            }

        if self.dict_values.get('Contact_Alt_Phone__c'):
            enroll_quote['EveningPhone'] = utils_tool.format_phone(self.get('Contact_Alt_Phone__c'))
        else:
            enroll_quote['EveningPhone'] = enroll_quote['DayPhone']

        name_plan = str(self.get('Product_Name')).split('(')
        name_plan = name_plan[1].split(')')
        name_value = name_plan[0].strip()
        name_value = name_value.replace(' ', '_')
        enroll_quote['Plan_Name'] = name_value

        sub_tree_plan_cost = xml_quote.findall('Plan_Cost')[0]
        plan_tree = sub_tree_plan_cost.findall(name_value)[0]
        for child in plan_tree:
            if child.tag == 'Premium':
                enroll_quote['Premium'] = child.text
            if child.tag == 'EnrollmentFee':
                enroll_quote['Enrollment_Fee'] = child.text
            if child.tag == 'TelaDocFee':
                enroll_quote['TelaDoc_Fee'] = child.text

        enroll_quote['Dependents'] = self.get_depend_dict()
        enroll_quote['Add-ons'] = self.get_addons_pa_dict(xml_quote)
        enroll_quote.update(self.gen_payment())
        return enroll_quote

    def get_depend_dict(self):
        list_dict_dep = []
        if self.dict_values.get('Spouse_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Spouse'
            dependents['First_Name'] = self.get('Spouse_First_Name__c')
            dependents['Middle_Name'] = self.get('Spouse_Middle_Name__c')
            dependents['Last_Name'] = self.get('Spouse_Last_Name__c')
            dependents['Gender'] = self.gender_dict.get(self.get('Spouse_Sex__c'))
            dependents['DOB'] = self.get('Spouse_Date_of_Birth__c')
            dependents['Age'] = self.get('Spouse_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child1_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Child'
            dependents['First_Name'] = self.get('Child1_First_Name__c')
            dependents['Middle_Name'] = self.get('Child1_Middle__c')
            dependents['Last_Name'] = self.get('Child1_Last_Name__c')
            dependents['Gender'] = self.gender_dict.get(self.get('Child1_Sex__c'))
            dependents['DOB'] = self.get('Child1_Date_of_Birth__c')
            dependents['Age'] = self.get('Child1_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child2_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Child'
            dependents['First_Name'] = self.get('Child2_First_Name__c')
            dependents['Middle_Name'] =  self.get('Child2_Middle__c')
            dependents['Last_Name'] = self.get('Child2_Last_Name__c')
            dependents['Gender'] = self.gender_dict.get(self.get('Child2_Sex__c'))
            dependents['DOB'] = self.get('Child2_Date_of_Birth__c')
            dependents['Age'] = self.get('Child2_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child3_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Child'
            dependents['First_Name'] = self.get('Child3_First_Name__c')
            dependents['Middle_Name'] =  self.get('Child3_Middle__c')
            dependents['Last_Name'] = self.get('Child3_Last_Name__c')
            dependents['Gender'] = self.gender_dict.get(self.get('Child3_Sex__c'))
            dependents['DOB'] = self.get('Child3_Date_of_Birth__c')
            dependents['Age'] = self.get('Child3_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child4_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Child'
            dependents['First_Name'] = self.get('Child4_First_Name__c')
            dependents['Middle_Name'] =  self.get('Child4_Middle__c')
            dependents['Last_Name'] = self.get('Child4_Last_Name__c')
            dependents['Gender'] = self.gender_dict.get(self.get('Child4_Sex__c'))
            dependents['DOB'] = self.get('Child4_Date_of_Birth__c')
            dependents['Age'] = self.get('Child4_Age__c')
            list_dict_dep.append(dependents)

        return list_dict_dep

    def get_addons_pa_dict(self, xml_quote):
        list_dict_addon = {}
        add_on_tree = xml_quote.findall('Add-ons')[0]

        if self.dict_values.get('Additional_Product_1'):
            freedom_tree = add_on_tree.findall(self.get('Additional_Product_1_ID'))[0]
            if freedom_tree is not None:
                plan = {}
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == self.get('Additional_Product_1_Price'):
                        plan['Name'] = plan_child.findall('Name')[0].text
                        plan['Premium'] = plan_child.findall('Premium')[0].text
                        plan['AdministrativeFee'] = plan_child.findall('AdministrativeFee')[0].text
                        plan['EnrollmentFee'] = plan_child.findall('EnrollmentFee')[0].text
                addon_id = {'Plan': plan}
                list_dict_addon[self.get('Additional_Product_1_ID')] = addon_id

        if self.dict_values.get('Additional_Product_2'):
            freedom_tree = add_on_tree.findall(self.get('Additional_Product_2_ID'))[0]
            if freedom_tree is not None:
                plan = {}
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == self.get('Additional_Product_2_Price'):
                        plan['Name'] = plan_child.findall('Name')[0].text
                        plan['Premium'] = plan_child.findall('Premium')[0].text
                        plan['AdministrativeFee'] = plan_child.findall('AdministrativeFee')[0].text
                        plan['EnrollmentFee'] = plan_child.findall('EnrollmentFee')[0].text
                addon_id = {'Plan': plan}
                list_dict_addon[self.get('Additional_Product_2_ID')] = addon_id
        if self.dict_values.get('Additional_Product3'):
            freedom_tree = add_on_tree.findall(self.get('Additional_Product_3_ID'))[0]
            if freedom_tree is not None:
                plan = {}
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == self.get('Additional_Product_3_Price'):
                        plan['Name'] = plan_child.findall('Name')[0].text
                        plan['Premium'] = plan_child.findall('Premium')[0].text
                        plan['AdministrativeFee'] = plan_child.findall('AdministrativeFee')[0].text
                        plan['EnrollmentFee'] = plan_child.findall('EnrollmentFee')[0].text
                addon_id = {'Plan': plan}
                list_dict_addon[self.get('Additional_Product_3_ID')] = addon_id
        if self.dict_values.get('Additional_Product_4'):
            freedom_tree = add_on_tree.findall(self.get('Additional_Product_4_ID'))[0]
            if freedom_tree is not None:
                plan = {}
                for plan_child in freedom_tree.findall('Plan'):
                    if plan_child.findall('Premium')[0].text == self.get('Additional_Product_4_Price'):
                        plan['Name'] = plan_child.findall('Name')[0].text
                        plan['Premium'] = plan_child.findall('Premium')[0].text
                        plan['AdministrativeFee'] = plan_child.findall('AdministrativeFee')[0].text
                        plan['EnrollmentFee'] = plan_child.findall('EnrollmentFee')[0].text
                addon_id = {'Plan': plan}
                list_dict_addon[self.get('Additional_Product_4_ID')] = addon_id
        return  list_dict_addon

    def have_spouse(self, is_stm= False):
        is_spouse = {}
        if self.get('Spouse_First_Name__c'):
            is_spouse['Include_Spouse'] = 'Yes'
            is_spouse['Spouse_Age'] = self.get('Spouse_Age__c')
            is_spouse['Spouse_DOB'] = self.get('Spouse_Date_of_Birth__c')
        else:
            is_spouse['Include_Spouse'] = 'No'
            is_spouse['Spouse_Age'] = ''
        return is_spouse

    def gen_1_stm_quote_dic(self, user_id, plan_id):
        quote_dict = {
            'User_ID': user_id,
            'State': self.get('Mailing_State__c'),
            'Zip_Code': self.get('Mailing_Zip_Code__c'),
            'Applicant_Gender': self.gender_dict.get(self.get('Primary_Sex__c')),
            'Applicant_Age': self.get('Primary_Age__c'),
            'Applicant_DOB': self.get('Primary_Date_of_Birth__c'),
            'Children_Count':  self.calc_child(),
            'Tobacco': self.yes_no.get(self.dict_values.get('Tobacco_Use__c')),
            'Plan_ID': plan_id,
            'Payment_Option': '1',
            'Coinsurance_Limit': '$5,000',
            'Coinsurance_Percentage': '80_20',
            'Coverage_Days': '50'

        }
        quote_dict.append(self.have_spouse())
        quote_dict['Dependents'] = self.get_depend_stm_quote_dict()
        return quote_dict

    def get_depend_stm_quote_dict(self):
        list_dict_dep = []
        if self.dict_values.get('Child1_First_Name__c'):
            dependents = {}
            date_dob = datetime.date.strftime(self.get('Child1_Date_of_Birth__c'))
            date_object = datetime.strptime(date_dob, "%Y-%m-%d")
            dependents['Gender'] = self.gender_dict.get(self.get('Child1_Sex__c'))
            dependents['DOB'] = date_object.strftime("%m-%d-%Y")
            dependents['Age'].text = self.get('Child1_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child2_First_Name__c'):
            dependents = {}
            date_dob = datetime.date.strftime(self.get('Child2_Date_of_Birth__c'))
            date_object = datetime.strptime(date_dob, "%Y-%m-%d")
            dependents['Gender'] = self.gender_dict.get(self.get('Child2_Sex__c'))
            dependents['DOB'] = date_object.strftime("%m-%d-%Y")
            dependents['Age'].text = self.get('Child2_Age__c')
            list_dict_dep.append(dependents)


        if self.dict_values.get('Child3_First_Name__c'):
            dependents = {}
            date_dob = datetime.date.strftime(self.get('Child3_Date_of_Birth__c'))
            date_object = datetime.strptime(date_dob, "%Y-%m-%d")
            dependents['Gender'] = self.gender_dict.get(self.get('Child3_Sex__c'))
            dependents['DOB'] = date_object.strftime("%m-%d-%Y")
            dependents['Age'].text = self.get('Child3_Age__c')
            list_dict_dep.append(dependents)

        if self.dict_values.get('Child4_First_Name__c'):
            dependents = {}
            dependents['Relation'] = 'Child'
            date_dob = datetime.date.strftime(self.get('Child4_Date_of_Birth__c'))
            date_object = datetime.strptime(date_dob, "%Y-%m-%d")
            dependents['Gender'] = self.gender_dict.get(self.get('Child4_Sex__c'))
            dependents['DOB'] = date_object.strftime("%m-%d-%Y")
            dependents['Age'].text = self.get('Child4_Age__c')
            list_dict_dep.append(dependents)

        return list_dict_dep



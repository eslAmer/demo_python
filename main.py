from flask import Flask, redirect, request
from flask_restful import Resource, Api
import ast
import json

event_registration_app = Flask(__name__)

#Contact entity
class Contact():
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

#Lead entity
class Lead():
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


class Helper():
    @staticmethod
    def clean_number(phone_number):
        characters = " []{}()-"

        for character in characters:
            phone_number = phone_number.replace(character, "")

        return phone_number

    @staticmethod
    def update_changes(original_user_data, recived_user_data):
        if(not recived_user_data.name and recived_user_data.name != original_user_data.name):
            original_user_data.name = user.name
        if(not recived_user_data.email and recived_user_data.email != original_user_data.email):
            original_user_data.email = user.email
        if(not recived_user_data.phone and recived_user_data.phone != original_user_data.phone):
            original_user_data.phone = user.phone

        return original_user_data

    @staticmethod
    def contacts_data_source():
        contacts = []

        contacts.append(Contact("Alice Brown", None, "1231112223"))
        contacts.append(Contact("Bob Crown", "bob@crowns.com", None))
        contacts.append(Contact("Carlos Drew", "carl@drewess.com", "3453334445"))
        contacts.append(Contact("Doug Emerty", None, "4564445556"))
        contacts.append(Contact("Egan Fair", "eg@fairness.com", "5675556667"))

        return contacts

    @staticmethod
    def leads_data_source():
        leads = []

        leads.append(Lead(None, "kevin@keith.com", None))
        leads.append(Lead("Lucy", "lucy@liu.com", "3210001112"))
        leads.append(Lead("Mary Middle", "mary@middle.com", "3331112223"))
        leads.append(Lead(None, None, "4442223334"))
        leads.append(Lead(None, "ole@olson.com", None))

        return leads


#preparing initial data
contacts_list = Helper.contacts_data_source()
leads_list = Helper.leads_data_source()

@event_registration_app.route('/', methods=['POST', 'GET'])
def register():
    #Check if the request is a POST request
    if request.method == 'POST':
    
        #Cleaning the phone number and removing any non-digit characters
        phone_number = Helper.clean_number(request.json['registrant']['phone'])
        
        #Checking the phone number length
        if (len(phone_number) < 10):
            return "Phone Number less than 10 digits."

        else:
            #Constructing a Contact object from recived data
            user = Contact(request.json['registrant']['name'],
                           request.json['registrant']['email'], phone_number)

            #Checking if the Contact in already in the Contatcs
            contacts_result = list(filter(lambda x: x.email ==
                                          user.email or x.phone == user.phone, contacts_list))
            #Checking if the Contact in already in the Leads
            leads_result = list(filter(lambda x: x.email ==
                                    user.email or x.phone == user.phone, leads_list))

            if (len(contacts_result)):
                #updating the contact from incoming data
                contacts_result[0] = Helper.update_changes(
                    contacts_result[0], user)

                return contacts_result[0].__dict__

            elif (len(leads_result)):
                #updating the contact from incoming data
                leads_result[0] = Helper.update_changes(leads_result[0], user)

                #adding the contact from contacts list
                contacts_list.append(leads_result[0])
                #removing the contact from leads list
                leads_list.remove(leads_result[0])

                return leads_result[0].__dict__

            #if the incoming contact is not in the contacts list or leads list
            else:
                contacts_list.append(user)
                return user.__dict__

    #Check if the request is not a POST request
    else:
        contacts_dict = list(map(lambda x: x.__dict__, ContactsList))
        resp = json.dumps(contacts_dict)
        print(contacts_dict)

        return resp


if __name__ == '__main__':
    event_registration_app.run(debug=True, port=9900)

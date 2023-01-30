from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import random , string
from . models import Account


def generate_account():
    # function to generate an account number and check if account number exists in db
    return ''.join(random.choice(string.digits) for _ in range(5))
    
def is_valid(name):
    # function to check weather name is valid or not
    special_char="#@%&^*()!~`:;/,><{}[]|\-_'"
    if len(name)<=3:
        return False
    for i in special_char :
        if i in name:
            return False
    return True

# api to fetch all the data

@api_view(['GET'])
def all_account(request):
    account = Account.objects.all().values()
    return Response(account)

# fetch a particular account

@api_view(['POST'])
def get_account(request):
    data=request.data
    try:
        account = Account.objects.get(acc_no=data['acc_no'])
        acc_details={}
        acc_details['name']=account.name
        acc_details['acc_no']=account.acc_no
        acc_details['balance']=account.balance

        return JsonResponse(acc_details)

    except Exception as e :
        return JsonResponse({
            'message':str(e),
            'success':False
        })

#api to create single account

@api_view(['POST'])
def create_account(request):
    #storing json data in dictionary
    data = request.data
    # check name length and if string is valid
    if (is_valid(str(data['name']))):
        # create a dictionary to store the details and generated acc_no
        new_acc = {}
        new_acc['name']=data['name']

        #set a variable gen to check weather generation is valid or not
        gen=False
        while(gen==False):
            new_acc['acc_no']=generate_account()
            try :
                Account.objects.get(acc_no=new_acc['acc_no'])
                gen = False
            except:
                gen = True
                break
        # check if balance entred else set to 0
        if 'balance' in data and float(data['balance'])>0:    
            new_acc['balance'] = data['balance']
        else:
            new_acc['balance']=0.00
        #create an object of Account class and store details in database
        account = Account()
        account.name=new_acc['name']
        account.acc_no=new_acc['acc_no']
        account.balance=new_acc['balance']
        account.save()
        return JsonResponse(new_acc)

    else:
        return JsonResponse({
            'message':'Invalid Name!',
            'success':False
        })

# api to update name 

@api_view(['POST'])
def update_name(request):
    data = request.data
    if (is_valid(str(data['name']))):
        try :
            account=Account.objects.get(acc_no=data['acc_no'])
        except:
            return JsonResponse({
                'message':'No match found !',
                'success':False
            })
        account.name= data['name']
        account.save()

        return JsonResponse(account.values())
    else:
        return JsonResponse({
            'message':'Invalid Name!',
            'success':False
        })


# api to deposit money

@api_view(['POST'])
def deposit(request):
    data = request.data
    if float(data['amount'])<=0.00 :
        return JsonResponse({
            'message':'Enter Valid Ammount!',
            'success':False
        })
    else:
        try :
            account=Account.objects.get(acc_no=data['acc_no'])
        except:
            return JsonResponse({
                'message':'No match found !',
                'success':False
            })
        account.balance= float(account.balance) + float(data['amount'])
        account.save()

        return JsonResponse(account.values())

# api to withdraw money

@api_view(['POST'])
def debit(request):
    data = request.data
    if float(data['amount'])<=0.00 :
        return JsonResponse({
            'message':'Enter Valid Ammount!',
            'success':False
        })
    else:
        try :
            account=Account.objects.get(acc_no=data['acc_no'])
        except:
            return JsonResponse({
                'message':'No match found !',
                'success':False
            })
        if(float(account.balance)<float(data['amount'])):

            return JsonResponse({
                'message':'Insufficient Balance!',
                'success':False
                })

        else:
            account.balance=float(account.balance)-(data['amount'])
            account.save()
            return JsonResponse(account.values())
        
        
        

# api to delete an account 

@api_view(['POST'])
def delete_account(request):

    data=request.data
    try:
        account = Account.objects.get(acc_no=data['acc_no'])
        account.delete()
        return JsonResponse({
            'message':'Deletion Successful',
            'success': True
        })
    except:
        return JsonResponse({
            'message':'No match found !',
            'success':False
        })

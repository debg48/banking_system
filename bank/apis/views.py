from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import random , string
from . models import Account,Loan
import datetime

intrest_bank = 10

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

def get_intrest(amount):
    # function to calculate intrest
    # amount = float(amount)
    return (amount*intrest_bank)/100

# api to fetch all the data

@api_view(['GET'])
def all_account(request):
    try :
        account = Account.objects.all().values()
        return Response(account)
    except Exception as e :
        return JsonResponse({
            "message" : str(e),
            "success" : False
        })
# fetch a particular account

@api_view(['POST'])
def get_account(request):
    try:
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
    except :
        return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })
#api to create single account

@api_view(['POST'])
def create_account(request):
    #storing json data in dictionary
    try:
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
    except:
        return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to create multiple accounts

@api_view(['POST'])
def create_multi(request):
    try:
        data = request.data
        sucessfull=[]
        unsucessfull=[]
        for i in range(len(data)):
            #check if name is valid or not
            if (is_valid(str(data[str(i+1)]['name']))):
                #create a new dictionary to store name
                new_acc = {}
                new_acc['name']=data[str(i+1)]['name']
                # generae account no and check if smae is present in db
                gen=False
                while(gen==False):
                    new_acc['acc_no']=generate_account()
                    try :
                        Account.objects.get(acc_no=new_acc['acc_no'])
                    except:
                        gen = True
                        break
                if 'balance' in data[str(i+1)] and float(data[str(i+1)]['balance'])>0:    
                    new_acc['balance'] = data[str(i+1)]['balance']
                else:
                    new_acc['balance']=0.00
                account = Account()
                account.name=new_acc['name']
                account.acc_no=new_acc['acc_no']
                account.balance=new_acc['balance']
                account.save()
                sucessfull.append(i+1)
                
            else:
                unsucessfull.append(i+1)

        return JsonResponse({
                    'sucessfull':sucessfull,
                    'unsuccessfull':unsucessfull
                })

    except :

         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })


# api to update name 

@api_view(['POST'])
def update_name(request):
    try:
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
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to update multiple account.name 

@api_view(['POST'])
def update_name_multi(request):
    try:
        data = request.data
        sucessfull=[]
        unsucessfull=[]
        for i in range(len(data)):
            if (is_valid(str(data[str(i+1)]['name']))):
                try :
                    account=Account.objects.get(acc_no=data[str(i+1)]['acc_no'])
                    sucessfull.append(i+1)
                    account.name= data[str(i+1)]['name']
                    account.save()
                except:
                    unsucessfull.append(i+1)
                            
            else:
                unsucessfull.append(i+1)
        return JsonResponse({
                    'sucessfull':sucessfull,
                    'unsuccessfull':unsucessfull
                })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to deposit money

@api_view(['POST'])
def deposit(request):
    try:
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
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api for mutiple deposit 

@api_view(['POST'])
def deposit_multi(request):
    try:
        data = request.data
        sucessfull=[]
        unsucessfull=[]
        for i in range(len(data)):
            if float(data[str(i+1)]['amount'])<=0.00 :
                unsucessfull.append(i+1)
            else:
                try :
                    account=Account.objects.get(acc_no=data[str(i+1)]['acc_no'])
                    account.balance= float(account.balance) + float(data[str(i+1)]['amount'])
                    account.save()
                    sucessfull.append(i+1)
                except:
                    unsucessfull.append(i+1)
                    
        return JsonResponse({
                    'sucessfull':sucessfull,
                    'unsuccessfull':unsucessfull
                })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to withdraw money

@api_view(['POST'])
def debit(request):
    try:
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
            
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to do multiple withdrawal

@api_view(['POST'])
def debit_multi(request):
    try:
        data = request.data
        sucessfull=[]
        unsucessfull=[]
        for i in range(len(data)):
            if float(data[str(i+1)]['amount'])<=0.00 :
                unsucessfull.append(i+1)
            else:
                try :
                    account=Account.objects.get(acc_no=data[str(i+1)]['acc_no'])
                    account.balance= float(account.balance) - float(data[str(i+1)]['amount'])
                    account.save()
                    sucessfull.append(i+1)
                except:
                    unsucessfull.append(i+1)
                    
        return JsonResponse({
                    'sucessfull':sucessfull,
                    'unsuccessfull':unsucessfull
                })
    except:  
        return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to delete an account 

@api_view(['POST'])
def delete_account(request):
    try:
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
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to delete multiple accounts

@api_view(['POST'])
def delete_acc_multi(request):
    try:
        data = request.data
        sucessfull=[]
        unsucessfull=[]
        for i in range(len(data)):
            try:
                account = Account.objects.get(acc_no=data[str(i+1)]['acc_no'])
                account.delete()
                sucessfull.append(i+1)
            except:
                unsucessfull.append(i+1)
        
        return JsonResponse({
                    'sucessfull':sucessfull,
                    'unsuccessfull':unsucessfull
                })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })


# api to delete all the accounts

@api_view(['GET'])
def del_all_account(request):
    try:
        account = Account.objects.all()
        account.delete()
        return JsonResponse({
            'message':'Deletion Successful',
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'message':str(e),
            'success':False
        })

# api to take loan (single  account)

@api_view(['POST'])
def get_loan(request):
    try:
        data=request.data
        if data['amount']<=50000 or data['amount']>100000000:
            return JsonResponse({
                        'message':'Enter Valid Amount',
                        'success': False
                    })
        else:
            try:
                check =  Loan.objects.get(acc_no=data['acc_no'])
                return JsonResponse({
                        'message':'Previous Loan not cleared!',
                        'success': False
                    })
            except:
                try:
                    account = Account.objects.get(acc_no=data['acc_no'])
                    loan = Loan()
                    loan.name=account.name
                    loan.balance=account.balance
                    loan.acc_no=account.acc_no
                    loan.loan=data['amount']
                    loan.date=datetime.date.today()
                    loan.save()
                    return JsonResponse({
                        'message':'Loan Granted',
                        'success': True
                    })
                except Exception as e:
                    return JsonResponse({
                        'message':str(e),
                        'success':False
                    })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

#api to view all loans

@api_view(['GET'])
def loan_all(request):
    try:
        loan =  Loan.objects.all().values()
        return Response(loan)
    except Exception as e :
        return JsonResponse({
            'message':str(e),
            'success': False
            })

#api to check status of loan of a particular account

@api_view(['POST'])
def status_loan(request):
    try:
        data=request.data
        try:
            loan =  Loan.objects.get(acc_no=data['acc_no'])
            acc_details={}
            acc_details['name']=loan.name
            acc_details['acc_no']=loan.acc_no
            acc_details['balance']=loan.balance
            acc_details['loan']=loan.loan
            acc_details['date']=loan.date

            return JsonResponse(acc_details)
            

        except Exception as e:
                return JsonResponse({
                    'message':str(e),
                    'success':False
                })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

#api to return loan (single)

@api_view(['POST'])
def return_loan(request):
    try:
        data=request.data
        if data['amount']<=0:
            return JsonResponse({
                        'message':'Enter Valid Amount',
                        'success': False
                    })
        else:
            try:
                loan =  Loan.objects.get(acc_no=data['acc_no'])
                if loan.loan < data['amount']:
                    return JsonResponse({
                        'message':'Enter Valid Amount,amount exceeds loan',
                        'success': False
                    })
                else:
                    loan.loan=loan.loan - data['amount']
                    loan.save()
                    return JsonResponse({
                        'message':'Return Accepted !',
                        'success': True
                    })

            except Exception as e:
                    return JsonResponse({
                        'message':str(e),
                        'success':False
                    })
    except:
         return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })

# api to update yearly intrest

@api_view(['POST'])
def intrest(request):
    try:
        data=request.data
        try:
            loan =  Loan.objects.get(acc_no=data['acc_no'])
            date_today = datetime.date(2043,1,31) #datetime.date.today()
            #check if a yea has competed or not
            if date_today.year-loan.date.year>=1 and loan.date.month == date_today.month and loan.date.day == date_today.day:
                loan.loan = loan.loan + get_intrest(loan.loan)
                loan.save()
                return JsonResponse({
                            'message': "after intresed your loan is " + str(loan.loan),
                            'success':True
                        })
            else:
                return JsonResponse({
                            'message': "The next increment has time !",
                            'success': False
                        })                

        except Exception as e:
                    return JsonResponse({
                        'message': str(e),
                        'success':False
                    })

    except:
        return JsonResponse({
                'message': "Please send valid response!",
                'success':False
            })
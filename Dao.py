import json
from dbHandeling import validateHeader,getCUSTOMERID,getACCOUNTBALANCE
from utility import readPropertyFile,writeLog

def getCustomerID(jsonstring):#sessionName):
    writeLog('getCustomerID-1-',str(jsonstring))
    bool = False
    messageID=''
    connectionID=''
    connectionPassword=''
    errpoint='.00'
    returnjson={}
    
    try:
        paramdict={}
        paramdict=json.loads(jsonstring)
        parameterinfo=paramdict["pageInfo"]["formInfo"]["parameterInfo"]
        print(str(parameterinfo))
        for i in parameterinfo:
          if i["displayName"]== "APIUserName":
            connectionID=i["value"]
          elif i["displayName"]== "APIPassword":
            connectionPassword=i["value"]
          elif i["displayName"]== "CustMobNo":
            DBparamdict={}
            DBparamdict['MOBILENUMBER']=i["value"] 
          
          
        #paramdict=json.loads(jsonstring)
        #print(paramdict)
        paramdict=jsonstring#json.dumps(jsonstring)
        print(111)
        connectionID=paramdict[ 'APIUserName']
        print(222)
        connectionPassword=paramdict['APIPassword']
        print(333)
        #sessionName=jsonstring['queryResult']['outputContexts'][0]['name'];
        bool =True
    except Exception as er:
        print("The parameters are not valid or they are missing.-----",str(er))
        retstr= {'header':{'messageID':messageID,'statusCode':'400','statusDescription':'The parameters are not valid or they are missing.'+str(errpoint)}}
    if bool==True :
        try:
            errpoint='.081111'
            vd=validateHeader(connectionID,connectionPassword)
            errpoint=vd['RESPCODE']
            if vd['RESPCODE']==0:
                conn=vd['CONNECTION']
            else:
                conn=None
                writeLog('getCustomerID-1.1-',str(vd['RESPDESC']))
            print(conn)
            if conn!=None:
                
                retstr= getCUSTOMERID(conn,str(DBparamdict))
                print(retstr)
                writeLog('getCustomerID-2',str(retstr))
                retstrjson={}
                retstrjson=json.loads(retstr)
                respcode=retstrjson['RESPCODE']
                errpoint='.02'

                if respcode==0:
                    respdesc={}
                    respdesc=json.loads(retstrjson['RESPDESC'])
                    custname=respdesc['CUSTOMERNAME']
                    #returnjson={'fulfillmentText':'Welcome '+custname,"outputContexts":[{"name": sessionName,"parameters": {"CustomerId": respdesc['CUSTOMERID']}}]}
                    returnjson={"fulfillment_response": {"messages": [{"text": {"text": ['Welcome '+custname]}}]}}
                elif respcode==1:
                    returnjson= {'header':{'messageID':messageID,'statusCode':'404','statusDescription':'The task/operation does not exist.'}}
                else:
                    returnjson= {'header':{'messageID':messageID,'statusCode':'405','statusDescription':'A severe problem has occurred.'}}
            else:
                print('The caller is not authorized for this request.')
                returnjson= {'header':{'messageID':messageID,'statusCode':'401','statusDescription':'The caller is not authorized for this request.'+str(errpoint)}}
            #retstr= {'header':{'messageID':messageID,'statusCode':'200','statusDescription':'Successfully validated student'},'response': { 'TransactionReferenceCode': 'EDA/1140/13', 'TransactionDate': '2018-07-23T18:24:00.195+03:00', 'TotalAmount': 0.0,'Currency': '', 'AdditionalInfo': 'Wanyama Jostine Anyango', 'AccountNumber': 'EDA/1140/13', 'AccountName': 'Wanyama Jostine Anyango', 'InstitutionCode': '2100082', 'InstitutionName': 'Eldoret University '}}
        except Exception as e:
            print("A severe problem has occurred.",e)
            returnjson= {'header':{'messageID':messageID,'statusCode':'405','statusDescription':'A severe problem has occurred.'+str(errpoint)+str(e)}}

    else:
        print("A severe problem has occurred."+str(errpoint))
        returnjson= {'header':{'messageID':messageID,'statusCode':'405','statusDescription':'A severe problem has occurred.'+str(errpoint)}}
    writeLog('getCustomerID-3-',str(returnjson))
    return returnjson


def getAccountBalance(jsonstring):
    writeLog('getAccountList-1-',str(jsonstring))
    bool = False
    messageID=''
    connectionID=''
    connectionPassword=''
    errpoint='.00'
    defaultDict=readPropertyFile('defaultvalues.properties')
    returnjson={}
    try:
        paramdict={}
        paramdict=jsonstring#json.loads(jsonstring)
        connectionID=paramdict['APIUserName']
        connectionPassword=paramdict['APIPassword']

        bool =True
    except Exception as er:
        print("The parameters are not valid or they are missing.")
        return {'header':{'messageID':messageID,'statusCode':'400'+errpoint,'statusDescription':'The parameters are not valid or they are missing.'}}
    if bool==True :
        try:
            vd=validateHeader(connectionID,connectionPassword)
            if vd['RESPCODE']==0:
                conn=vd['CONNECTION']
            else:
                conn=None
            errpoint='.25'
            if conn!=None:
                #print(str(paramdict))
                DBparamdict={}
                DBparamdict['ACCOUNTNUMBER']=paramdict['AccountNumber']
                DBparamdict['CUSTOMERID']=paramdict['CustomerId']

                print(DBparamdict)
                retstr= getACCOUNTBALANCE(conn,str(DBparamdict))
                writeLog('getAccountList-3-',str(retstr));
                if retstr.find("ERROR")>-1:
                    retstr= {'header':{'messageID':messageID,'statusCode':'405'+errpoint,'statusDescription':'A severe problem has occurred.'}}
                else:
                    print(retstr)
                    retstrjson={}
                    retstrjson=json.loads(retstr)
                    respcode=retstrjson['RESPCODE']
                    errpoint='.02'
                    if respcode==0:
                        respdesc={}
                        respdesc=json.loads(retstrjson['RESPDESC'])
                        returnjson={'fulfillmentText':respdesc['BALANCE']}
                    elif respcode==1:
                        returnjson= {'header':{'messageID':messageID,'statusCode':'404'+errpoint,'statusDescription':'The task/operation does not exist.'}}
                    elif respcode==3:
                        returnjson= {'header':{'messageID':messageID,'statusCode':'402'+errpoint,'statusDescription':'Duplicate transaction detected.'}}
                    else:
                        returnjson= {'header':{'messageID':messageID,'statusCode':'405'+errpoint,'statusDescription':'A severe problem has occurred.'}}
            else:
                print('The caller is not authorized for this request.')
                returnjson= {'header':{'messageID':messageID,'statusCode':'401'+errpoint,'statusDescription':'The caller is not authorized for this request.'}}
            #retstr= {'header':{'messageID':messageID,'statusCode':'200','statusDescription':'Successfully validated student'},'response': { 'TransactionReferenceCode': 'EDA/1140/13', 'TransactionDate': '2018-07-23T18:24:00.195+03:00', 'TotalAmount': 0.0,'Currency': '', 'AdditionalInfo': 'Wanyama Jostine Anyango', 'AccountNumber': 'EDA/1140/13', 'AccountName': 'Wanyama Jostine Anyango', 'InstitutionCode': '2100082', 'InstitutionName': 'Eldoret University '}}
        except Exception as e:
            print("A severe problem has occurred.",e)
            returnjson= {'header':{'messageID':messageID,'statusCode':'405'+errpoint,'statusDescription':'A severe problem has occurred.'}}

    else:
        print("A severe problem has occurred.")
        returnjson= {'header':{'messageID':messageID,'statusCode':'405'+errpoint,'statusDescription':'A severe problem has occurred.'}}

    writeLog('getAccountList-4-',str(returnjson));
    return returnjson

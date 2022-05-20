from builtins import len, print
from django.http import HttpResponse
import asyncio
from hfc.fabric import Client
import os
import json
from django.http import JsonResponse
from pkg_resources import BINARY_DIST
# -*- coding:utf-8 -*-
import logging
 
 
class HttpCode(object):
    success = 0
    error = 1
 
 
def result(code=HttpCode.success, message='', data=None, kwargs=None):
    json_dict = {'data': data, 'code': code, 'message': message}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})
 
 
def success(data=None):
    if data is not None:
        data=data.encode("utf-8").decode("latin1")
    return result(code=HttpCode.success, message='OK', data=data)
 
 
def error(message='', data=None):
    if data is not None:
        data=data.encode("utf-8").decode("latin1")
    return result(code=HttpCode.error, message=message, data=data)

loop = asyncio.get_event_loop()
cli = Client(net_profile="/home/user/fabric/fabric-sdk-py/test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')
cli.new_channel('businesschannel')
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
                      os.path.dirname(os.path.realpath('__file__')),
                      '/home/user/fabric/fabric-sdk-py/test/fixtures/chaincode'
                     ))
os.environ['GOPATH'] = os.path.abspath(gopath)
 
def hello(request):
    return HttpResponse("Hello world ! ")

policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0},
        ]
    }
}

# 医嘱上链
def writeMedicalAdvice(request):
    print(request)
    args = []
    # args.append(request.GET.get("adviceId",default='xxx'))
    # args.append(request.GET.get("adviceNum",default='xxx'))
    # args.append(request.GET.get("diseaseClass",default='xxx'))
    # args.append(request.GET.get("treatmentId",default='xxx'))
    # args.append(request.GET.get("chargeId",default='xxx'))
    # args.append(request.GET.get("day",default='xxx'))
    # args.append(request.GET.get("content",default='xxx'))
    # args.append(request.GET.get("firstUse",default='xxx'))
    # args.append(request.GET.get("everyUse",default='xxx'))
    # args.append(request.GET.get("totalUse",default='xxx'))
    # args.append(request.GET.get("specimenPart",default='xxx'))
    # args.append(request.GET.get("checkMethod",default='xxx'))
    # args.append(request.GET.get("entrust",default='xxx'))
    # args.append(request.GET.get("execFreq",default='xxx'))
    # args.append(request.GET.get("freqTime",default='xxx'))
    # args.append(request.GET.get("freqInterval",default='xxx'))
    # args.append(request.GET.get("intervalUnit",default='xxx'))
    # args.append(request.GET.get("execTimeScheme",default='xxx'))
    # args.append(request.GET.get("execNature",default='xxx'))
    # args.append(request.GET.get("deptId",default='xxx'))
    # args.append(request.GET.get("execMark",default='xxx'))
    # args.append(request.GET.get("execMark",default='xxx'))
    # args.append(request.GET.get("execMark",default='xxx'))
    # args.append(request.GET.get("execMark",default='xxx'))
    args = request.GET.getlist("args",default='xxx')
    for i in range(len(args)):
        args[i] = args[i].encode("utf-8").decode("latin1")
    logger = logging.getLogger('django')
    logger.info(args)
    logger.info(len(args))
    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='writeMedicalAdvice',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 根据医嘱id读取医嘱信息
def queryMedicalAdvice(request):
    print(request)
    
    args = []
    args.append(request.GET.get("adviceId",default='xxx'))
    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='queryMedicalAdvice',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 数据溯源：溯源病人最新的医嘱或某次医嘱前的一次医嘱
def traceBackward(request):
    print(request)
    args = request.GET.getlist("args",default='xxx')
    print(args)
    for i in range(len(args)):
        args[i] = str(args[i].encode("utf-8").decode("latin1"))

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='traceBackward',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    logger = logging.getLogger('django')
    logger.info(response)
    print(response)
    if (response == True):
        return success(response)
    else:
        return error(response)

# 数据追踪：追踪目标病人最初的医嘱或某医嘱后的一次医嘱
def traceForward(request):
    print(request)
    args = []
    args = request.GET.getlist("args",default='xxx')

    # args.append(request.GET.get("patientId",default='xxx'))
    # if (request.GET.get("adviceId") != NULL) :
    #     args.append(request.GET.get("adviceId",default='xxx'))

    print(args)
 
    print(12)
    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='traceForward',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# cp-track

# 入院记录上链
def writeAdmissionRecord(request):
    print(request)
    args = []
    # args.append(request.GET.get("idNum",default='xxx'))
    # args.append(request.GET.get("patientId",default='xxx'))
    # args.append(request.GET.get("enterTime",default='xxx'))
    # args.append(request.GET.get("leaveTime",default='xxx'))
    # args.append(request.GET.get("diseaseClass",default='xxx'))
    # args.append(request.GET.get("adviceId",default='xxx'))
    args = request.GET.getlist("args",default='xxx')
    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='cp_track',
                fcn='writeAdmissionRecord',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 模板医嘱上链
def writeAdtmpRecord(request):
    logger = logging.getLogger('django')
    logger.info(request)
    print(request)
    args = []
    # args.append(request.GET.get("idNum",default='xxx'))
    # args.append(request.GET.get("patientId",default='xxx'))
    # args.append(request.GET.get("enterTime",default='xxx'))
    # args.append(request.GET.get("leaveTime",default='xxx'))
    # args.append(request.GET.get("diseaseClass",default='xxx'))
    # args.append(request.GET.get("adviceId",default='xxx'))
    args = request.GET.getlist("args",default='xxx')
    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='adtmp',
                fcn='writeAdtmpRecord',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 入院记录溯源
def traceAdmissionRecord(request):
    print(request)
    args = []
    args = request.GET.getlist("args",default='xxx')

    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='cp_track',
                fcn='traceAdmissionRecord',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 判断是否二次入院
def judgeRepeatedAdmission(request):
    print(request)
    args = []
    args = request.GET.getlist("args",default='xxx')

    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='cp_track',
                fcn='judgeRepeatedAdmission',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 判断是否存在费用异常
def judgeFeeErr(request):
    print(request)
    args = []
    args = request.GET.getlist("args",default='xxx')

    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='judgeFeeErr',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)

# 判断是否存在费用异常
def judgePathSeqError(request):
    print(request)
    args = []
    args = request.GET.getlist("args",default='xxx')

    print(args)

    # The response should be true if succeed
    response = loop.run_until_complete(cli.chaincode_invoke(
                requestor=org1_admin,
                channel_name='businesschannel',
                peers=['peer0.org1.example.com'],
                args=args,
                cc_name='advice',
                fcn='judgePathSeqError',
                transient_map=None, # optional, for private data
                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
    if (response == True):
        return success(response)
    else:
        return error(response)


#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import re
from public import api
import logging


base_url = api.get_config('base_info', 'base_url')
logger = logging.getLogger(__file__)


def get_response(url, data):
    # 定义全局请求包头
    headers = {
        "Content-Type": "application/json",
        "Client-Version": "2.7.3"
    }
    # 从请求url中获取接口名
    interface_name = re.match(r'.*experts.(.*?)&v=', url).group(1)
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    request_json = json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ':'))
    logging.debug('【Interface {} Request data】：\n {}'.format(interface_name, request_json))
    response_json = json.dumps(response, indent=4, ensure_ascii=False, separators=(',', ':'))
    logging.debug('【Interface {} Response data】：\n {}'.format(interface_name, response_json))
    hasError = response.get('hasError')
    if hasError:
        logging.error('Error %s ' % response.get('errorDesc'))
    return response


# 用户登录拿到sessionId
def login_get_sessionid(nickname, passwd):
    url = base_url + "/call?id=experts.login&v="
    data = {
        "nickname": nickname,
        "passwd": passwd
    }
    logger.debug('User %s login' % data.get('nickname'))
    response = get_response(url, data)
    sessionid = response.get('data').get('sessionId')
    logger.debug('sessionid = %s' % sessionid)
    logger.debug('User %s login complete !!! \n' % data.get('nickname'))
    return sessionid


# 添加权限分组
def AddAuthGroup(sessionid, groupname):
    url = base_url + "/call?id=experts.AddAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "groupname": groupname
    }
    logger.debug('AddAuthGroup %s ' % data.get('groupname'))
    response = get_response(url, data)
    logger.debug('AddAuthGroup %s complete !!! \n' % data.get('groupname'))
    return response


# 获取权限分组列表,拿到新分组groupid
def GetAuthGroupList(sessionid):
    url = base_url + "/call?id=experts.GetAuthGroupList&v="
    data = {
        "sessionid": sessionid
    }
    logger.debug('GetAuthGroupList')
    response = get_response(url, data)
    return response


# 修改权限分组
def UpdateAuthGroup(sessionid, groupid):
    url = base_url + "/call?id=experts.UpdateAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "groupid": groupid,
        "authlist": {
            'AuthCreateCase': True,
            'AuthDeleteCase': True,
            'AuthGiveCase': True,
            'AuthManageUser': True,
            'AuthOverCase': True,
            'AuthRenameCase': True
        }
    }
    logger.debug('UpdateAuthGroup groupid : %s authlist : %s ' % (data.get('groupid'), data.get('authlist')))
    response = get_response(url, data)
    logger.debug(
        'UpdateAuthGroup groupid : %s authlist : %s complete !!! \n' % (data.get('groupid'), data.get('authlist')))
    return response


# 添加权限分组用户
def AddUserAuthGroup(sessionid, groupid, username):
    url = base_url + "/call?id=experts.AddUserAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "groupid": groupid,
        "username": username
    }
    response = get_response(url, data)
    return response


# 新建案件
def newCriminalCase(sessionid, caseName, privateCase=True):
    url = base_url + "/call?id=experts.newCriminalCase&v="
    data = {
        "sessionId": sessionid,
        "caseName": caseName,
        "privateCase": privateCase
    }
    logger.debug('newCriminalCase caseName : %s ' % data.get('caseName'))
    response = get_response(url, data)
    logger.debug('newCriminalCase caseName : %s  complete !!! \n' % data.get('caseName'))
    return response


# 列出案件
def listCriminalCase(sessionid, offset=0, limit=999, removeType=0, key_word=[''], type=1):
    url = base_url + "/call?id=experts.listCriminalCase&v="
    data = {
        "sessionid": sessionid,
        "offset": offset,
        "limit": limit,
        "removeType": removeType,
        "key_word": key_word,
        "type": type
    }
    response = get_response(url, data)
    return response


# 打开案件
def openCriminalCase(sessionid, criminalCaseId):
    url = base_url + "/call?id=experts.openCriminalCase&v="
    data = {
        "sessionId": sessionid,
        "criminalCaseId": criminalCaseId
    }
    response = get_response(url, data)
    return response


# 上传文件
def voiceFileUpload(sessionid, newFile):
    url = base_url + "/file?id=experts.voiceFileUpload&v=&sessionId=" + sessionid
    uploaded_fileList = []
    for i in range(len(newFile)):
        with open(newFile[i], "rb") as f:
            data = f.read()
        multiple_files = [
            (newFile[i], (newFile[i], data, 'audio/wav'))
        ]
        response = json.loads(requests.post(url, files=multiple_files).content)
        logger.debug('response %s ' % response)
        logger.debug('voiceFileUpload  %s  complete !!! \n' % newFile[i])
        uploaded_fileList.append(response.get('data').get('fileList')[0])
    return uploaded_fileList


# 列出语音
def listVoice(sessionid, cateGory='MATERIAL', **kwargs):
    url = base_url + "/call?id=experts.listVoice&v="
    data = {
        "sessionId": sessionid,
        "cateGory": cateGory,
        "criminalCaseId": kwargs["criminalCaseId"],
        "offset": 0,
        "limit": 30
    }

    logger.debug('listVoice')
    response = get_response(url, data)

    for k in kwargs.keys():

        if k == 'verifyFile':
            uploaded_voiceList = []
            voiceList = response.get('data').get('voiceList')
            for file in voiceList:
                for i in range(len(kwargs['verifyFile'])):
                    if file['voiceFileName'] == kwargs['verifyFile'][i]:
                        uploaded_voiceList.append(file)
            logger.debug('uploaded_voiceList %s' % uploaded_voiceList)
            return uploaded_voiceList

        elif k == 'compareFile':
            if not len(kwargs['compareFile']) == 2:
                logger.error('Error： compareFile can only contain 2 files ...')
                raise ValueError('Error： compareFile can only contain 2 files ...')

            compare_voiceList = []
            voiceList = response.get('data').get('voiceList')
            for file in voiceList:
                for i in range(len(kwargs['compareFile'])):
                    if file['voiceFileName'] == kwargs['compareFile'][i]:
                        compare_voiceList.append(file)
            logger.debug('compare_voiceList %s' % compare_voiceList)
            return compare_voiceList

    return response


# 增加语音
def addVoice(sessionid, criminalCaseId, uploaded_fileList):
    url = base_url + "/call?id=experts.addVoice&v="
    file_list = []
    for file in uploaded_fileList:
        data = {
            "sessionId": sessionid,
            "criminalCaseId": criminalCaseId,
            "voiceFileName": file['name'],
            "voiceFileId": file['fileId'],
            "cateGory": "MATERIAL"
        }
        response = get_response(url, data)
        file_list.append(response)
        logger.debug('addVoice name: %s , fileId: %s complete !!!  \n ' % (file['name'], file['fileId']))
    return file_list


# 新增语音和重命名语音文件都可以用该接口
def addVoice2(sessionId, criminalCaseId, voiceFileId, voiceFileName, cateGory='MATERIAL'):
    url = base_url + '/call?id=experts.addVoice&v='
    data = {
        'sessionId': sessionId,
        'criminalCaseId': criminalCaseId,
        'voiceFileId': voiceFileId,
        'voiceFileName': voiceFileName,
        'cateGory': cateGory
    }
    response = get_response(url, data)
    return response


# 获取文件mos和snr
def getmossnr(sessionid, voiceid):
    url = base_url + "/call?id=experts.getmossnr&v="
    data = {
        "sessionid": sessionid,
        "voiceid": voiceid
    }
    logger.debug('getmossnr %s ' % data)
    response = get_response(url, data)
    logger.debug('getmossnr of %s complete : %s !!!  \n ' % (voiceid, response.get('data')))
    return response


# 开始人声分离和有效人声分离
def startdiarizationspeech(sessionid, uploaded_voiceList):
    url = base_url + "/call?id=experts.startdiarizationspeech&v="
    for voice in uploaded_voiceList:
        data = {
            "sessionId": sessionid,
            "voiceid": voice['voiceInfoId'],
            "speech": False,
            "diarization": False,
            "peoplenum": 0,
            "noisemin": 0
        }
        logger.debug('startdiarizationspeech')
        response = get_response(url, data)
        logger.debug('startdiarizationspeech complete !!!  \n ')


# 人声分离和有效人声分离
def getdiarizationspeech(sessionid, uploaded_voiceList):
    url = base_url + "/call?id=experts.getdiarizationspeech&v="
    for voice in uploaded_voiceList:
        data = {
            "sessionId": sessionid,
            "voiceid": voice['voiceInfoId'],
            "speech": False,
            "diarization": False,
            "peoplenum": 0,
            "noisemin": 0
        }
        logger.debug('getdiarizationspeech')
        response = get_response(url, data)
        logger.debug('getdiarizationspeech complete !!!  \n ')


# 开始查找语音文件的音素
def startfindphoneme(sessionid, uploaded_voiceList):
    url = base_url + "/call?id=experts.startfindphoneme&v="
    for voice in uploaded_voiceList:
        data = {
            "sessionId": sessionid,
            "voiceFileId": voice['voiceInfoId']
        }
        logger.debug('startfindphoneme')
        response = get_response(url, data)
        logger.debug('startfindphoneme complete !!!  \n ')


# 列出音素
def listPhoneme(sessionId, voiceFileId, listType='UNFILTERED', limit=100000, offset=0, reGenPhoneme=False):
    url = base_url + '/call?id=experts.listPhoneme&v='
    data = {
        'sessionId': sessionId,
        'voiceFileId': voiceFileId,
        'listType': listType,
        'limit': limit,
        'offset': offset,
        'reGenPhoneme': reGenPhoneme
    }
    response = get_response(url, data)
    return response


# 声纹对比
def VoiceCompare(sessionid, filelist, filerate=8000):
    url = base_url + "/call?id=experts.VoiceCompare&v="
    data = {
        "sessionId": sessionid,
        "filerate": filerate,
        "filelist": filelist
    }
    response = get_response(url, data)
    return response


# 增加标记
def addVoiceTag(sessionId, criminalCaseId, beginTime, endTime, voiceFileId, voiceTagName, phonemeId='', comment=''):
    url = base_url + "/call?id=experts.addVoiceTag&v="
    data = {
        'sessionId': sessionId,
        'criminalCaseId': criminalCaseId,
        'beginTime': beginTime,
        'endTime': endTime,
        'voiceFileId': voiceFileId,
        'voiceTagName': voiceTagName,
        'phonemeId': phonemeId,
        'comment': comment
    }
    response = get_response(url, data)
    return response


# 列出标记
def listVoiceTag(sessionId, criminalCaseId, voiceFileId, limit=1000, offset=0):
    url = base_url + "/call?id=experts.listVoiceTag&v="
    data = {
        'sessionId': sessionId,
        'criminalCaseId': criminalCaseId,
        'voiceFileId': voiceFileId,
        'limit': limit,
        'offset': offset
    }
    response = get_response(url, data)
    return response


# 删除标记
def removeVoiceTag(sessionId, voiceTagId):
    url = base_url + "/call?id=experts.removeVoiceTag&v="
    data = {
        'sessionId': sessionId,
        'voiceTagId': voiceTagId
    }
    response = get_response(url, data)
    return response


# 删除语音
def removeVoice(sessionid, voiceFileId, cateGory='MATERIAL'):
    url = base_url + "/call?id=experts.removeVoice&v="
    data = {
        "sessionId": sessionid,
        "voiceFileId": voiceFileId,
        "cateGory": cateGory
    }
    response = get_response(url, data)
    return response


# 删除案件
def removeCriminalCase(sessionid, criminalCaseId, removeType=10):
    # removeType：10-放到案件回收站，20-从案件回收站删除
    url = base_url + "/call?id=experts.removeCriminalCase&v="
    data = {
        "sessionId": sessionid,
        "criminalCaseId": criminalCaseId,
        "removeType": removeType
    }
    logger.debug('removeCriminalCase: %s ' % criminalCaseId)
    response = get_response(url, data)
    logger.debug('removeCriminalCase: %s  complete !!! \n' % criminalCaseId)
    return response


# 获取权限分组用户列表
def GetAuthGroupUserList(sessionid, groupid):
    url = base_url + "/call?id=experts.GetAuthGroupUserList&v="
    data = {
        "sessionid": sessionid,
        "groupid": groupid
    }
    logger.debug('GetAuthGroupUserList')
    response = get_response(url, data)
    logger.debug('GetAuthGroupUserList complete !!! \n')
    return response


# 删除权限分组用户
def DelUserAuthGroup(sessionid, groupid, userid):
    url = base_url + "/call?id=experts.DelUserAuthGroup&v="
    data = {
        "sessionId": sessionid,
        "groupid": groupid,
        "userid": userid
    }
    response = get_response(url, data)
    return response


# 删除权限分组
def DelAuthGroup(sessionid, groupid):
    url = base_url + "/call?id=experts.DelAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "groupid": groupid
    }
    response = get_response(url, data)
    return response


# 修改用户所属分组
def UpdateUserAuthGroup(sessionid, togroupid, userid, username):
    url = base_url + "/call?id=experts.UpdateUserAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "togroupid": togroupid,
        "userid": userid,
        "username": username
    }
    response = get_response(url, data)
    return response


# 修改权限分组名称
def UpdateNameAuthGroup(sessionid, groupname, groupid):
    url = base_url + "/call?id=experts.UpdateNameAuthGroup&v="
    data = {
        "sessionid": sessionid,
        "groupname": groupname,
        "groupid": groupid
    }
    response = get_response(url, data)
    logger.debug("UpdateNameAuthGroup：AuthGroup update name to '{}'".format(groupname))
    return response


# 鉴定报告保存
def saveidentifyreport(**kwargs):
    url = base_url + "/call?id=experts.saveidentifyreport&v="
    data = {
        "analysiscontext": kwargs["analysiscontext"],  # 分析内容
        "analysistitle": kwargs["analysistitle"],  # 分析标题
        "casecontext": kwargs["casecontext"],  # 案件内容
        "casedesc": kwargs["casedesc"],  # 案件简介
        "caseid": kwargs["caseid"],  # 案件id
        "identifier": kwargs["identifier"],  # 鉴定
        "identifycontext": kwargs["identifycontext"],  # 鉴定内容
        "identifytime": kwargs["identifytime"],  # 鉴定时间
        "identifytitle": kwargs["identifytitle"],  # 鉴定标题
        "sessionId": kwargs["sessionId"],
        "title": kwargs["title"]
    }
    response = get_response(url, data)
    return response


# 鉴定报告获取
def getidentifyreport(sessionId, caseid):
    url = base_url + "/call?id=experts.getidentifyreport&v="
    data = {
        "caseid": caseid,
        "sessionId": sessionId
    }
    response = get_response(url, data)
    return response


# 重命名图片
def renameCriminalCaseImage(sessionId, ImageName, ImageId):
    url = base_url + "/call?id=experts.renameCriminalCaseImage&v="
    data = {
        "sessionId": sessionId,
        "ImageName": ImageName,
        "ImageId": ImageId
    }
    response = get_response(url, data)


# 列出案件图片
def listImage(sessionId, criminalCaseId, limit, offset):
    url = base_url + "/call?id=experts.listImage&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "limit": limit,
        "offset": offset
    }
    response = get_response(url, data)
    return response


# 删除图片
def removeImage(sessionId, imageId):
    url = base_url + "/call?id=experts.removeImage&v="
    data = {
        "sessionId": sessionId,
        "imageId": imageId
    }
    response = get_response(url, data)
    return response


# 保存图片
def addImage(sessionId, criminalCaseId, imageFileId, imageFileName):
    url = base_url + "/call?id=experts.addImage&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "imageFileId": imageFileId,
        "imageFileName": imageFileName
    }
    response = get_response(url, data)
    return response


# 获取存档
def getCriminalCaseSave(sessionId, criminalCaseSaveId):
    url = base_url + "/call?id=experts.getCriminalCaseSave&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseSaveId": criminalCaseSaveId
    }
    response = get_response(url, data)
    return response


# 列出存档
def listCriminalCaseSave(sessionId, criminalCaseId, limit, offset):
    url = base_url + "/call?id=experts.listCriminalCaseSave&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "limit": limit,
        "offset": offset
    }
    response = get_response(url, data)
    return response


# 重命名存档
def renameCriminalCaseSave(sessionId, caseSaveId, criminalCaseSaveName):
    url = base_url + "/call?id=experts.renameCriminalCaseSave&v="
    data = {
        "sessionId": sessionId,
        "caseSaveId": caseSaveId,
        "criminalCaseSaveName": criminalCaseSaveName
    }
    response = get_response(url, data)
    return response


# 设置存档
def setCriminalCaseSave(sessionId, caseSaveId, criminalCaseId, criminalCaseSaveName, newCaseSave, sonogramSettingList):
    url = base_url + "/call?id=experts.setCriminalCaseSave&v="
    data = {
        "sessionId": sessionId,
        "caseSaveId": caseSaveId,
        "criminalCaseId": criminalCaseId,
        "criminalCaseSaveName": criminalCaseSaveName,
        "newCaseSave": newCaseSave,
        "sonogramSettingList": sonogramSettingList
    }
    response = get_response(url, data)
    return response


# 移除存档
def removeCriminalCaseSave(sessionId, caseSaveId):
    url = base_url + "/call?id=experts.removeCriminalCaseSave&v="
    data = {
        "sessionId": sessionId,
        "caseSaveId": caseSaveId
    }
    response = get_response(url, data)
    return response


# 上传日志
def uploadlog(ip, desc, version):
    url = base_url + "/call?id=experts.uploadlog&v="
    data = {
        "ip": ip,
        "desc": desc,
        "version": version
    }
    response = get_response(url, data)
    return response


# 分配案件
def alloctCriminalCase(sessionId, criminalCaseId, isDelMyself, userIdList):
    url = base_url + "/call?id=experts.alloctCriminalCase&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "isDelMyself": isDelMyself,
        "userIdList": userIdList
    }
    response = get_response(url, data)
    return response


# 案件重命名
def renameCriminalCase(sessionId, criminalCaseName, criminalCaseId):
    url = base_url + "/call?id=experts.renameCriminalCase&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseName": criminalCaseName,
        "criminalCaseId": criminalCaseId
    }
    response = get_response(url, data)
    return response


# 添加语音并返回新文件名
def addVoiceAndReturnNewName(sessionId, criminalCaseId, voiceFileId, cateGory):
    url = base_url + "/call?id=experts.addVoiceAndReturnNewName&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "voiceFileId": voiceFileId,
        "cateGory": cateGory
    }
    response = get_response(url, data)
    return response


# 替换语音
def replaceVoice(sessionId, newVoiceFileId, oldVoiceFileId):
    url = base_url + "/call?id=experts.replaceVoice&v="
    data = {
        "sessionId": sessionId,
        "newVoiceFileId": newVoiceFileId,
        "oldVoiceFileId": oldVoiceFileId
    }
    response = get_response(url, data)
    return response


# 列出过滤的音素
def addPhonemeFilter(sessionId, phonemeId):
    url = base_url + "/call?id=experts.addPhonemeFilter&v="
    data = {
        "sessionId": sessionId,
        "phonemeId": phonemeId
    }
    response = get_response(url, data)
    return response


# 标记音素
def markPhoneme(sessionId, phonemeId, marked=True):
    url = base_url + "/call?id=experts.markPhoneme&v="
    data = {
        "sessionId": sessionId,
        "phonemeId": phonemeId,
        "marked": marked
    }
    response = get_response(url, data)
    return response


# 撤销音素移除
def removePhonemeFilter(sessionId, voiceFileId):
    url = base_url + "/call?id=experts.removePhonemeFilter&v="
    data = {
        "sessionId": sessionId,
        "voiceFileId": voiceFileId
    }
    response = get_response(url, data)
    return response


# 修改音素名
def UpdatePhonemeName(sessionId, phonemeId, phonemeName):
    url = base_url + "/call?id=experts.UpdatePhonemeName&v="
    data = {
        "sessionId": sessionId,
        "phonemeId": phonemeId,
        "phonemeName": phonemeName
    }
    response = get_response(url, data)
    return response


# 检查服务状态
def getserverstatus():
    url = base_url + "/call?id=experts.getserverstatus&v="
    data = {}
    response = get_response(url, data)
    return response


# 同步
def sync(userName, userToken, remoteAddr):
    url = base_url + "/call?id=experts.sync&v="
    data = {
        "userName": userName,
        "userToken": userToken,
        "remoteAddr": remoteAddr
    }
    response = get_response(url, data)
    return response


# 显示服务端版本号
def ListVersion(source):
    url = base_url + "/call?id=experts.ListVersion&v="
    data = {
        "source": source
    }
    response = get_response(url, data)
    return response


# upload上传操作日志
def UploadOprationLog(sessionid, caseid, log):
    url = base_url + "/call?id=experts.UploadOprationLog&v="
    data = {
        "sessionid": sessionid,
        "caseid": caseid,
        "log": log
    }
    response = get_response(url, data)
    return response


# 列出操作日志
def ListOprationLog(sessionid, caseid):
    url = base_url + "/call?id=experts.ListOprationLog&v="
    data = {
        "sessionid": sessionid,
        "caseid": caseid
    }
    response = get_response(url, data)
    return response


# 增加lpc标记
def addlpctag(sessionId, remark, caseId, changevalue, imgdata, list):
    url = base_url + "/call?id=experts.addlpctag&v="
    data = {
        "sessionId": sessionId,
        "remark": remark,
        "caseId": caseId,
        "changevalue": changevalue,
        "imgdata": imgdata,
        "list": list,
    }
    response = get_response(url, data)
    return response


# 获取lpc标记
def getlpctag(sessionId, id):
    url = base_url + "/call?id=experts.getlpctag&v="
    data = {
        "sessionId": sessionId,
        "id": id
    }
    response = get_response(url, data)
    return response


# 列出lpc标记
def listlpctag(sessionId, caseId):
    url = base_url + "/call?id=experts.listlpctag&v="
    data = {
        "sessionId": sessionId,
        "caseId": caseId
    }
    response = get_response(url, data)
    return response


# 修改lpc标记
def updatelpctag(sessionId, id, remark, changevalue, imgdata, list):
    url = base_url + "/call?id=experts.updatelpctag&v="
    data = {
        "sessionId": sessionId,
        "id": id,
        "remark": remark,
        "changevalue": changevalue,
        "imgdata": imgdata,
        "list": list
    }
    response = get_response(url, data)
    return response


# 删除lpc标记
def dellpctag(sessionId, id):
    url = base_url + "/call?id=experts.dellpctag&v="
    data = {
        "sessionId": sessionId,
        "id": id
    }
    response = get_response(url, data)
    return response


# 修改用户密码
def changePasswd(userId, oldPasswd, newPasswd):
    url = base_url + "/call?id=experts.changePasswd&v="
    data = {
        "userId": userId,
        "oldPasswd": oldPasswd,
        "newPasswd": newPasswd
    }
    response = get_response(url, data)
    return response


# 列出用户
def listUser(sessionId, offset, Limit):
    url = base_url + "/call?id=experts.listUser&v="
    data = {
        "sessionId": sessionId,
        "offset": offset,
        "Limit": Limit
    }
    response = get_response(url, data)
    return response


# 注销（退出登录）
def logout(sessionId):
    url = base_url + "/call?id=experts.logout&v="
    data = {
        "sessionId": sessionId
    }
    response = get_response(url, data)
    return response


# 批量增加标记
def addVoiceTagbatch(sessionId, taglist):
    url = base_url + "/call?id=experts.addVoiceTagbatch&v="
    data = {
        "sessionId": sessionId,
        "taglist": taglist
    }
    response = get_response(url, data)
    return response


# 更新标记
def updateVoiceTag(sessionId, beginTime, comment, criminalCaseId, endTime, phonemeId, voiceFileId, voiceTagId,
                   voiceTagName, wavId=0, type='normalTag'):
    url = base_url + "/call?id=experts.updateVoiceTag&v="
    data = {
        'sessionId': sessionId,
        'beginTime': beginTime,
        'comment': comment,
        'criminalCaseId': criminalCaseId,
        'endTime': endTime,
        'phonemeId': phonemeId,
        'voiceFileId': voiceFileId,
        'voiceTagId': voiceTagId,
        'voiceTagName': voiceTagName,
        'wavId': wavId,
        'type': type
    }
    response = get_response(url, data)
    return response


# 储存标记
def saveVoiceTag(sessionId, criminalCaseId, voiceTagList):
    url = base_url + "/call?id=experts.saveVoiceTag&v="
    data = {
        "sessionId": sessionId,
        "criminalCaseId": criminalCaseId,
        "voiceTagList": voiceTagList
    }
    response = get_response(url, data)
    return response


# 获取文件信息
def GetFileInfo(sessionId, voiceid):
    url = base_url + "/call?id=experts.GetFileInfo&v="
    data = {
        "sessionId": sessionId,
        "voiceid": voiceid
    }
    response = get_response(url, data)
    return response


# 文件下载
def voiceFileDownload(sessionId, fileId):
    url = base_url + "/file?id=experts.voiceFileDownload&v=&sessionId={}&fileId={}".format(sessionId, fileId)
    response = requests.get(url)
    return response


# 开始音素检索
def startfindphoneme(sessionId, voiceFileId):
    url = base_url + '/call?id=experts.startfindphoneme&v='
    data = {
        'sessionId': sessionId,
        'voiceFileId': voiceFileId
    }
    response = get_response(url, data)
    return response


username = api.get_config('base_info', 'user_name')
password = api.get_config('base_info', 'user_password')
start_name = api.get_config('base_info', 'case_name_prefix')


# 清空回收站案件
def clear_recycle_bin(session_id):
    case_list_res = listCriminalCase(session_id, type=1, removeType=10)
    case_list = case_list_res.get('data').get('caseList')
    for case in case_list:
        if case.get('caseName').startswith(start_name):
            case_id = case.get('criminalCaseId')
            removeCriminalCase(session_id, case_id, removeType=20)
        else:
            pass


# 清空案件列表
def clear_case_list(session_id):
    case_list_res = listCriminalCase(session_id, type=1, removeType=0)
    case_list = case_list_res.get('data').get('caseList')
    for case in case_list:
        if case.get('caseName').startswith(start_name):
            case_id = case.get('criminalCaseId')
            removeCriminalCase(session_id, case_id, removeType=10)
        else:
            pass


# 因服务器等不可控原因，测试用例执行不下去的时候案件不会被成功删除，该方法在模块用例执行完后遍历案件列表，删除所有auto开头的案件
def del_all_case():
    session_id = login_get_sessionid(username, password)
    clear_case_list(session_id)
    clear_recycle_bin(session_id)


if __name__ == '__main__':
    # session_id = login_get_sessionid('yaocheng', '123456')
    # print(session_id)
    del_all_case()

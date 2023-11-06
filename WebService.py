from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import suds
import base64
import ssl
#import syslogger 
import datetime
import requests
import cv2
import os

def qqCheckOnline(telCode):
  url = "http://www.webxml.com.cn/webservices/qqOnlineWebService.asmx?wsdl"
  #log = syslogger.logger().log
  #log.info("Web Service Start...")

  if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context

  client = Client(url)
  result = client.service.qqCheckOnline(telCode)
  #log.info(result)
  #ret = client.service.InsertEventMain("")

def DetectEventLog(log, config, sensorID, locationID, detectImg):
  url= config["DetectEventLogWS"]["url"]
  #log = syslogger.logger().log
  log.info("DetectEventLog Web Service Start...")

  # cv2.imwrite("TempDetectImg.jpg", detectImg)
  # with open(os.getcwd() + "\\" + "TempDetectImg.jpg", "rb") as image_file:
  #   base64_img1 = base64.b64encode(image_file.read())

  image_bytes = cv2.imencode(".jpg", detectImg)[1].tobytes()
  base64_img1 = base64.b64encode(image_bytes)

  finalPic = base64_img1

  NVR_CurTime = CallNxWebAPI(log, config["NVR"]["CallNxWebAPIUrl"])
  NVRLinkPath = config["NVR"]["NVRLinkPath"]

  if(NVR_CurTime != ""):
    NVRLinkPath += NVR_CurTime
    log.info("NVRLinkPath = %s", NVRLinkPath)

  if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context
  client = Client(url)
  result = client.service.InsertEventMain("MFGAiEdge", datetime.datetime.now(), config["DetectEventLogWS"]["WSEventID"], sensorID, locationID, 
                                          config["DetectEventLogWS"]["WSMemo"], finalPic, NVRLinkPath, '1')
  log.info("result = %s" ,result)
  log.info("DetectEventLog Web Service End...")
  
def CallNxWebAPI(log, url):
  #log = syslogger.logger().log
  log.info("CallNxWebAPI Start!")
  result = ""
  
  response = requests.get("", verify=False)
  decoded_result = response.json()
  if(decoded_result["reply"]["vmsTime"] != ""):
    result = decoded_result["reply"]["vmsTime"]
  
  log.info("CallNxWebAPI End!")
  log.info("CallNxWebAPI , result is = %s", result)
  return result
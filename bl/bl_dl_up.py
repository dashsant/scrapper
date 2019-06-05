import boto3_wasabi
import os
import subprocess
import time


def upload_to_wasabi(f , file_key):

    WASABI_ACCESS_KEY = ''
    WASABI_SECRET_KEY = ''
    WASABI_BUCKET = 'nithya.bl'
    # Open the file as readable
    body = open(f, 'rb')

    # Start the boto3 client that points to Wasabi's S3 endpoints.
    s3 = boto3_wasabi.client('s3', region_name='us-east-1' ,aws_access_key_id=WASABI_ACCESS_KEY, aws_secret_access_key=WASABI_SECRET_KEY)
    # Upload your file
    upload_data = s3.put_object(Bucket=WASABI_BUCKET, Key=file_key, Body=body, ContentType='image/jpg')
    # Close the file; just a good practice.
    body.close()
    tmp = upload_data["ResponseMetadata"]
    sc = tmp["HTTPStatusCode"]
    if sc == 200:
        return True
    else:
        return False

def process(eaps):
    bf = "/home/ec2-user/britishLib/"
    for item in eaps:
        fn = bf + "eap_links/" + item
        f = open(fn , "r")
        #skip the header
        skip = True
        cmd = "node  " + bf + "dezoomify/node-app/dezoomify-node.js "
        baseFolder = bf + "eap_data/"
        for line in f:
            if skip == True:
                skip = False
                continue
            l = line.strip()
            t = l.split(",")
            if len(t) < 3:
                continue
            jsonUrl = t[1].replace('"' , '')
			imageUrl = jsonUrl.replace("info.json" , "full/full/0/default.jpg")
            folder = (t[2].replace('"' , '')).split("/")[0]
            print(imageUrl)
            page = (t[2].replace('"','')).split("/")[1]
            imgFolder = baseFolder + folder + "/"
            if not os.path.isdir(imgFolder):
                os.mkdir(imgFolder)
            outImgPath = imgFolder + page + ".jpg"
            if not os.path.isfile(outImgPath)  :
                wgetCmdStr = "wget " + imageUrl + " -O " + outImgPath
				cmdStr = cmd + '"' + jsonUrl + '"' + " " + outImgPath
                print( wgetCmdStr )
                ret = subprocess.call(wgetCmdStr , shell=True)
                # This handles the scenario where dezoomify is not able to get the file
                if not os.path.isfile(outImgPath)  :
                    continue
                if ret == 0:
                    file_key = get_key(folder , page)
                    if upload_to_wasabi(outImgPath,file_key):
                        rmCmdStr = "rm " + outImgPath
                        subprocess.call(rmCmdStr , shell=True)
                    else:
                        print "Upload to Wasabi Failed"
                else:
                    print "FAILED TO DEZOOMIFY"

def get_key(folder , page):
    tmp = folder.split("_")
    k = ""
    cnt = 0
    for i in tmp:
        if cnt:
            l = ""
            for p in range(0 , cnt+1):
                l = l + tmp[p]
                if p != cnt:
                    l = l + "_"
            k = k+"/"+l
        else:
            k = i
        cnt = cnt + 1
    k = k + "/" + page + ".jpg"
    return k


def main():
    tmp = [ 'EAP683I.csv' ,   'EAP692I.csv' , \
    'EAP636I.csv' ,  'EAP676I.csv' ,  'EAP689I.csv']

    #tmp = ['EAP609I.csv' ,  'EAP673I.csv' ,   'EAP683I.csv' ,   'EAP692I.csv' , \
    #'EAP636I.csv' ,  'EAP676I.csv' ,  'EAP689I.csv']
    process(tmp)

main()


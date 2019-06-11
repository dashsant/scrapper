import boto3_wasabi
import os
import subprocess
import time


def get_client( ):

    WASABI_ACCESS_KEY = 'XDD3268UILFWROHD11Q8'
    WASABI_SECRET_KEY = 'fCQATKvQwheleOZJ5FTW0gvMHOyNzwb8bk4YYLve'
    WASABI_BUCKET = 'nithya.bl'
    s3 = boto3_wasabi.client('s3', region_name='us-east-1' ,aws_access_key_id=WASABI_ACCESS_KEY, aws_secret_access_key=WASABI_SECRET_KEY)
    return s3
    # Close the file; just a good practice.

def process(eaps):
    bf = "/home/ec2-user/britishLib/"
    WASABI_BUCKET = 'nithya.bl'
    s3c = get_client()
    mf = open("EAP3XXIM.csv" , "w+")
    mf.write("Heading")
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
            folder = (t[2].replace('"' , '')).split("/")[0]
            page = (t[2].replace('"','')).split("/")[1]
            imgFolder = baseFolder + folder + "/"
            outImgPath = imgFolder + page + ".jpg"
            fileKey = get_key(folder , page)
            response = s3c.list_objects(Bucket=WASABI_BUCKET, Prefix=fileKey)
            obj = response.get("Contents" , None)
            if not obj:
                mf.write(line)
        f.close()
    mf.close()


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
    tmp = ['EAP3XXIM.csv']
    #tmp = ['EAP3XXIM.csv']
    #tmp = ['EAP310I.csv' , 'EAP314I.csv' , 'EAP329I.csv' , 'EAP341I.csv' , 'EAP365I.csv' , 'EAP373I.csv']
    #tmp = ['EAP201I.csv' , 'EAP209I.csv' , 'EAP217I.csv' ,'EAP261I.csv' ,'EAP272I.csv' , 'EAP281I.csv', \
#'EAP205I.csv' ,  'EAP211I.csv' ,  'EAP229I.csv' ,  'EAP262I.csv' ,  'EAP276I.csv' , \
#'EAP208I.csv' ,  'EAP212I.csv' ,  'EAP248I.csv' ,  'EAP264I.csv' ,  'EAP280I.csv']
    #tmp = ['EAP6XXIM.csv']
    #tmp = ['EAP6XXIM.csv']
    #tmp = ['EAP609I.csv' ,  'EAP676I.csv' , 'EAP692I.csv' , 'EAP636I.csv' , 'EAP683I.csv' , 'EAP673I.csv' , 'EAP689I.csv']
    process(tmp)

main()



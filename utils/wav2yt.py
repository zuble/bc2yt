# https://en.wikipedia.org/wiki/Comparison_of_video_container_formats

# FFMPEG-CHEATCODE
# https://gist.github.com/hasantayyar/5277357
# https://gist.github.com/protrolium/e0dbd4bb0f1a396fcb55?permalink_comment_id=3796114

# GH-EXAMPLES
# https://github.com/zkhan93/tb-yt-uploader/blob/fe590c12ed0d4d32ea5102c861604012992535d1/app/utils/a2v.py

import PySimpleGUI as sg
import ffmpeg 
import os, sys

def folderdat():
    folderdat = []

    if len(sys.argv) == 1:
        sg.theme("DarkGreen1")
        layout = [  [sg.Input(key="fldpth" ,change_submits=True), sg.FolderBrowse(key="browse")],
                    [sg.Button("folderdat")]  # identify the multiline via key option]
                ]
        ###Building Window
        window = sg.Window('bc2yt', layout, size=(400,250))

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event=="Exit":
                break
            elif event == "folderdat":
                if values["fldpth"]!="" and values["fldpth"] not in folderdat: #if not values["path"] or :
                    folderdat.append(values["fldpth"])
                    print(values["fldpth"])
    else:
        for i in range(1,len(sys.argv)):
            if sys.argv[i] not in folderdat:
                folderdat.append(sys.argv[i])
    print("folderdat\n",folderdat,"\n")
    return folderdat

def gen_mkv():

    def get_wavnimg(folderdat):
        wav_paths,wav_names,img=[],[],[]
        for file in os.listdir(folderdat):
            fname, fext = os.path.splitext(file)
            path=os.path.join(folderdat, file)
            if fext in [".png",".jpg"]: img = str(path)
            if fext in [".wav",".flac"]:
                wav_paths.append(path)
                wav_names.append(fname.replace('-', '~'))

        return img,sorted(wav_names),sorted(wav_paths)
    
    for i in range(len(folderdat)):
        img, wav_names, wav_paths=get_wavnimg(folderdat[i])

        #SCALE https://trac.ffmpeg.org/wiki/Scaling
        img = ffmpeg.input(img , r=1 , loop=1)\
                    .filter("scale",1080,1080)
                    #.drawbox(0, 0, -1, -1, color="black", t="3")
                    #.pad=(width,(ceil(iw/2)*2),height,(ceil(ih/2)*2))

        for wavi in range(len(wav_paths)):
            print(wavi,"\n")

            #FFPROBE
            #https://ottverse.com/ffprobe-comprehensive-tutorial-with-examples/
            #https://ffmpeg.org/ffprobe.html
            os.system('ffprobe -hide_banner '+str('"'+wav_paths[wavi]+'"'))


            #FFMPEG
            #https://ffmpeg.org/ffmpeg.html + https://github.com/kkroening/ffmpeg-python
            wav = ffmpeg.input(wav_paths[wavi]) 
            (
                ffmpeg
                .output(img, wav, folderdat[i]+"/"+wav_names[wavi]+".mkv" , vcodec="libx264", crf="18" , acodec="copy" , shortest=None , movflags="faststart" )
                .global_args('-loglevel','warning','-stats','-hide_banner') #'-report' = https://stackoverflow.com/questions/68382868/how-can-i-convert-an-ffmpeg-command-line-to-ffmpeg-python-code
                .run(overwrite_output=True)
            )

            print("\nGLUED IN2\n")
            os.system('ffprobe -hide_banner '+str('"'+folderdat[i]+"/"+wav_names[wavi]+".mkv"+'"'))
            print("\n------------------ :) --------------------\n")



def sel_mkv():
    tubedat = []
    sg.theme("DarkGreen1")
    layout = [  [sg.Input(key="videopth" ,change_submits=True), sg.FileBrowse(key="browse")],
                [sg.Button("tubedat")]  # identify the multiline via key option]
            ]
    ###Building Window
    window = sg.Window('bc2yt', layout, size=(400,250))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "tubedat":
            if values["videopth"]!="" and values["videopth"] not in tubedat and os.path.splitext(values["videopth"])[1] == ".mkv": #if not values["path"] or :
                tubedat.append(values["videopth"])
                print(values["videopth"])
    print(tubedat)
    return tubedat

def snd_mkv():

    def get_desc(folder):
        for file in os.listdir(folder):
            fname, fext = os.path.splitext(file)
            if(fext == '.txt' or fext == '.TXT'):
                path=os.path.join(folder, file)
                f=open(path,"r");d=f.read();f.close();
                #print(d)
                return '"'+d+'"'
        return None
        
    for i in range(len(tubedat)):
        tubedat_org_dir,tubedat_org_mkv = os.path.split(tubedat[i])
        #print(tubedat_org_dir,"\n",tubedat_org_mkv)

        tubedat_upl_mkv = '"'+tubedat_org_dir+"/"+tubedat_org_mkv+'"'
        title = str('"'+os.path.splitext(tubedat_org_mkv)[0]+'"')
        desc = get_desc(tubedat_org_dir)
        kw = ""
        cat = 28 # https://gist.github.com/dgp/1b24bf2961521bd75d6c
        status = "private"

        print(i,"\nsending 2da UNIVERSE\
              \n\t --file",tubedat_upl_mkv,\
              "\n\t --title", title,\
              "\n\t --description\n", desc,\
              "\n\t --category", cat,\
              "\n\t --privacyStatus", status,)
    
        cmd = f"python3 up.py --file {tubedat_upl_mkv}\
                                    --title {title}\
                                    --description {desc}\
                                    --category {cat}\
                                    --privacyStatus {status}"
        os.system(cmd)
        print("\n*************************---------------------------\n")


if __name__ == "__main__":
    
    '''
    SELELECT FOLDER  
        either by th gui or passing wanted folders as arguments
        eg. python3 bc2yt.py /home/kkkk/TheOrbLeeScratchPerry–MoreTalesFromTheOrbservatory
    '''
    folderdat = folderdat()

    '''
    GENERATE a .mkv per .wav in each selected folder with cover.png as img
    '''
    gen_mkv()


    '''
    SELELECT .mkv && SEND2DAUNIVERSE
        descritpion in .txt in same folder as the selected mkv
    '''
    tubedat = sel_mkv()
    snd_mkv()
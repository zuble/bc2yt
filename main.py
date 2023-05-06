import PySimpleGUI as sg
import ffmpeg 
import os, sys , argparse

def bc_dl():
'''            
  usage: bandcamp-downloader.py [-h]
                                [--browser {firefox,chrome,chromium,brave,opera,edge}]
                                [--cookies /path/to/cookies.txt]
                                [--directory DIRECTORY]
                                [--filename-format FILENAME_FORMAT]
                                [--format {aac-hi,aiff-lossless,alac,flac,mp3-320,mp3-v0,vorbis,wav}]
                                [--parallel-downloads PARALLEL_DOWNLOADS]
                                [--force]
                                [--wait-after-download WAIT_AFTER_DOWNLOAD]
                                [--max-download-attempts MAX_DOWNLOAD_ATTEMPTS]
                                [--retry-wait RETRY_WAIT] [--verbose]
                                username

  Download your collection from bandcamp. Requires a logged in session in a
  supported browser so that the browser cookies can be used to authenticate with
  bandcamp. Albums are saved into directories named after their artist. Already
  existing albums will have their file size compared to what is expected and re-
  downloaded if the sizes differ. Otherwise already existing albums will not be
  re-downloaded.

  positional arguments:
    username              Your bandcamp username

  optional arguments:
    -h, --help            show this help message and exit
    --browser {firefox,chrome,chromium,brave,opera,edge}, -b {firefox,chrome,chromium,brave,opera,edge}
                          The browser whose cookies to use for accessing
                          bandcamp. Defaults to "firefox"
    --cookies PATH        Specifies a path to a Netscape/Mozilla format cookies file. Takes precedence
                          over --browser option
    --directory DIRECTORY, -d DIRECTORY
                          The directory to download albums to. Defaults to the
                          current directory.
    --filename-format FILENAME_FORMAT
                          The filename format for downloaded tracks. Default is
                          '{artist}/{artist} - {title}'.
                          All placeholders: item_id, artist, title
    --format {aac-hi,aiff-lossless,alac,flac,mp3-320,mp3-v0,vorbis,wav}, -f {aac-hi,aiff-lossless,alac,flac,mp3-320,mp3-v0,vorbis,wav}
                          What format do download the songs in. Default is
                          'mp3-320'.
    --parallel-downloads PARALLEL_DOWNLOADS, -p PARALLEL_DOWNLOADS
                          How many threads to use for parallel downloads. Set to
                          '1' to disable parallelism. Default is 5. Must be
                          between 1 and 32
    --force               Always re-download existing albums, even if they
                          already exist.
    --wait-after-download WAIT_AFTER_DOWNLOAD
                          How long, in seconds, to wait after successfully
                          completing a download before downloading the next
                          file. Defaults to '1'.
    --max-download-attempts MAX_DOWNLOAD_ATTEMPTS
                          How many times to try downloading any individual files
                          before giving up on it. Defaults to '5'.
    --retry-wait RETRY_WAIT
                          How long, in seconds, to wait before trying to
                          download a file again after a failure. Defaults to
                          '5'.
    --verbose, -v
'''
  os.system(f'bandcamp-downloader.py  --browser firefox\
                                      --directory "{dest_path}"\
                                      --format wav    \
                                      diginn')   

######################
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
    
        cmd = f"python3 utils/up.py --file {tubedat_upl_mkv}\
                                    --title {title}\
                                    --description {desc}\
                                    --category {cat}\
                                    --privacyStatus {status}"
        os.system(cmd)
        print("\n*************************---------------------------\n")

  
if __name__ == "__main__":
  
  #parser = argparse.ArgumentParser(description='')
  #parser.add_argument('urls', metavar='URL', type=str, nargs='+', help='++ URLs')
  #args = parser.parse_args()
  #dest_path = args[1]
  bc_dl()
  
  
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
       

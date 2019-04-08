
import vlc
n = 'C:/Users/oraant/AppData/Local/Temp/tmpyw5dl9_8.mp3'
p = vlc.MediaPlayer(n)
p.play()




exit()

# ------------------------------------------------------------------------------------------------------------------


from playsound import playsound
import tempfile

#playsound('C:\Users\oraant\AppData\Local\Temp\tmpybz_qxnt.mp3')
n = 'C:/Users/oraant/AppData/Local/Temp/tmpyw5dl9_8.mp3'
#n = r'C:\Users\oraant\AppData\Local\Temp\tmpyw5dl9_8.mp3'
print(n)
playsound(n)

exit()
# ------------------------------------------------------------------------------------------------------------------

#playsound("%r" % s)

s1 = "welcome\tto\tPython"
raw_s1 = "%r"%s1
print(raw_s1)


exit()

# ------------------------------------------------------------------------------------------------------------------


from sys import getfilesystemencoding
a = getfilesystemencoding()
print(a)

exit()

# ------------------------------------------------------------------------------------------------------------------

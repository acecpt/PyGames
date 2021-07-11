import winsound  #https://www.programcreek.com/python/example/74090/winsound.SND_FILENAME
from playsound import playsound
# If full Dir String, location independent
# FartArmy formatted for Windows Dir String
playsound('C:\\Users\\dczel\\Desktop\\Examples\\PY-CSV-Graph\\PYGames\\Sounds\\FartArmy.wav')
# Pong formatted for Windows Dir String
playsound('C:\\Users\\dczel\\Desktop\\Examples\\PY-CSV-Graph\\PYGames\\Sounds\\Pong.wav')


winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
winsound.PlaySound("C:\\Users\\dczel\\Desktop\\Examples\\PY-CSV-Graph\\PyGames\\Sounds\\FartArmy.wav", winsound.SND_FILENAME)


winsound.PlaySound("This is the real me", winsound.SND_FILENAME)
SetTitleMatchMode, 2
WinGetActiveTitle, Title
if WinExist("ahk_class screenClass")
    SplashTextOn 200,200,, Video Reproduzindo. Ctrl J pra cancelar.
    WinActivate ; Use the window found by WinExist.
    Sleep 30000
    SplashTextOff
    ExitApp

^j::
   WinActivate, %Title%
   SplashTextOff
   ExitApp
return
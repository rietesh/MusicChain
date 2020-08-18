# MusicChain

Steps to Create a package for Android:

1. pip install --user buildozer
2. git clone https://github.com/rietesh/MusicChain.git
3. cd MusicChain
4. cd kivy-app
5. (optional) Plug in your android device and Turn on the USB debugging in Devloper options
6. buildozer -v android debug deploy run logcat
buildozer.spec file provides all the requirements to successfully create a package. 
Note: You can change the Android architecture to suit your needs in buildozer.spec line:222
After succesfull completion the apk can be found in ./bin/

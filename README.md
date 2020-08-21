# MusicChain

A cross-platform Blockchain app developed on top of Hyperledger Iroha using Kivy library.    

Install Kivy: https://kivy.org/doc/stable/gettingstarted/installation.html
* **Note:** Tested on python 3.6

### Steps to Create a package for Android
> Install dependencies:
> * sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
> * pip3 install --user --upgrade Cython==0.29.19 virtualenv 

1. pip install --user buildozer
2. git clone https://github.com/rietesh/MusicChain.git
3. cd MusicChain
4. cd kivy-app
5. buildozer init
6. cp ../android/buildozer.spec ./  (Replace the buildozer.spec file with the one in android directory and change the 
5. (optional) Plug in your android device and Turn on the USB debugging in Devloper options
6. buildozer -v android debug deploy run logcat

* buildozer.spec file provides all the requirements to successfully create a package such as permissions, name etc. 
* **Note:** You can change the Android architecture to suit your needs in buildozer.spec line:222
* After succesfull completion the apk can be found in ./bin/

A screenshot of the app running on arm64-v8a architecture:

![Image screenshot](/images/Screenshot_A.jpg)

### Steps to Create Windows application

1. pip install pyinstaller
2. git clone https://github.com/rietesh/MusicChain.git
3. cd MusicChain
4. mkdir app 
5. cd app 
6. python -m PyInstaller --name musicchain your\path\musicchain\kivy-app\main.py
7. cp ../windows/musicchain.spec ./ (Replace the spec file and edit it to add your path)
8. python -m PyInstaller musicchain.spec

* The compiled package will be in the app\dist\musicchain directory

A screenshot:

![Image windows](/images/Screenshot_W.PNG)

**Detailed Blog**: at this link

Working:

![image gif](/images/MusicChian_gif.gif)


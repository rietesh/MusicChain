# MusicChain

A crossplatform Blockchain app devloped on top of Hyperledger Iroha using Kivy library.    

### Steps to Create a package for Android
> Install dependencies:
> * sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
> * pip3 install --user --upgrade Cython==0.29.19 virtualenv 

1. pip install --user buildozer
2. git clone https://github.com/rietesh/MusicChain.git
3. cd MusicChain
4. cd kivy-app
5. (optional) Plug in your android device and Turn on the USB debugging in Devloper options
6. buildozer -v android debug deploy run logcat

* buildozer.spec file provides all the requirements to successfully create a package such as permissions, name etc. 
* **Note:** You can change the Android architecture to suit your needs in buildozer.spec line:222
* After succesfull completion the apk can be found in ./bin/

**Detailed Blog**: 

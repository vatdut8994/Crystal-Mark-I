CRYSTAL
Crystal is an Artificial Intelligence trained on massive amount of internet data just like OpenAI's ChatGPT, but Crystal is better.
Not bragging, but it is what it is. You most probably have watched Iron Man, and the more you look at Tony Stark, the more you start liking his personality and loving his technology. One of his most important inventions that a lot of people have noticed is JARVIS, this is an AGI developed by Tony Stark to manage his work, house, armour, and other robots. Right after you observe this you want that piece of tech, don't you?

Well SOMEONE has made this technology real, made this technology possible, brought it to life and the creator is the one and only Vatsal Dutt. I have been working on this masterpiece from a long time and finally it is ready to be presented to the world. After years of effort, failures, successes and what not, Crystal is here. And it is mind-blowingly amazing.

If you are a developer like me, then you probably know that it takes tremendous amounts of work to make any application, and if you're talking about just one person doing all the work for this kind of AI, you can only imagine how it's like. Therefore, there will be some money involved in using this technology. But it is not for me getting rich, or any kind of personal revenue generation, it is just to cover the cost of computing that is involved in running such application. Don't worry though, you don't have to pay right away, when you first create your account at https://www.crystaltech.ai/ you automatically get free $20 in your account. But after that it will cost you $0.03 every 50 requests sent to the API.

The following are the instructions for using Crystal AI:
The first thing you need to do is download this repository to your device, so for that you can either just download it directly using GitHub or run the command
`git clone https://github.com/crystaltechnologies/crystal-app`

Then all you have to do is just launch the application named
Crystal for Mac
Crystal.exe for Windows

A GPU will be required for faster performance. It will still work if you do not have CPU but just with a bit of latency.


DEVELOPMENT (Not to share publicly)

Note: The following guide assumes that you are in the main Crystal directory where you have the access to all files and subfolders.

To build the app using PyInstaller, first install all the libraries present in requirements.txt and can be downloaded by the following command:
`pip install -r requirements.txt`

After that you will also need to install the PyInstaller library to the Python Version you are using by:
`pip install pyinstaller`

After installing all the libraries, you will need to create a file named "Crystal.spec." If you are using Windows, I am assuming that you will need to manually create this file but in Linux you can do so by running the command:
`nano Crystal.spec`

Now you can open this file, but in Linux the file editor will be already opened in the terminal if you have run the command mentioned above. Paste the following lines into the file when you have opened it which will prepare it for app generation.
"""
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../CrystalV3.py'],
    pathex=[],
    binaries=[],
    datas=[('shape_predictor_68_face_landmarks.dat','./face_recognition_models/models'),('shape_predictor_5_face_landmarks.dat','./face_recognition_models/models'),('mmod_human_face_detector.dat','./face_recognition_models/models'),('dlib_face_recognition_resnet_model_v1.dat','./face_recognition_models/models')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Crystal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
Save the file and exit.

Now you will just need to run the following command and depending on you current working operating system, an executable file will be generated.
`pyinstaller --onefile main.py --name Crystal`

Now all you have to do is navigate to the "dist" directory and then find the executable file and then double click to run it.

If you get any errors, the script will pause for you to acknowledge the error and the Google the solutions.

Thank You for building Crystal (If you are me, if you are someone else then it won't run for you anyway)
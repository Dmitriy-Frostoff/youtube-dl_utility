## Description

### Download videos and audios from a [range of sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

### How to use

### **Caution!**

- `Python 3.12`+ required!
- `ffmpeg binary` required!
  Download actual release binary from [Download FFmpeg binary from official source](https://ffmpeg.org/download.html).  
  Use the actual `release builds` archive! Than unzip the archive to get structure like this (cwd relative):  
  `libs/ffmpeg` and especially with `libs/ffmpeg/bin/ffmpeg.exe`

---

- fork the repo

- install dependencies from requirements.txt
  If in the file `requirements.txt` dependencies are listed, you can install them all with a single command:

```bash
pip install -r requirements.txt
```

- to run code use

```bash
python ./src/main.py
```

or

```bash
npm run download
```

- check the terminale, you ' ll have got the message like:

```bash
Enter URL of the video for downloading:
URL: >>> ...
```

Enter the video url without quotation marks! Just address starting with `https://` (e.g. https://www.youtube.com/watch?v=abcdefg,
but not the ! 'https://www.youtube.com/watch?v=abcdefg' !)

- wait for downloading the video and audio files (video is prefered to be in the `1080p` (if is)
  or less otherwise but with the best possible quality)

- if one want to stop the process - make the terminal active and press `Ctrl + C` (possibly a few times
  or far less possible - quickly `Ctrl + C` and type `exit` emediately into terminal).

- after all, check the `./downloads` folder for video file and check that it's fine (video and audio present)

- done!)

### Step by step description (prune one)

to install all the libraries locally do the next steps (actual `Python`(3+) required!):  
(**briefly** - install in a local environment this libraries

```bash
pip install yt-dlp curl_cffi
```

)

- create virtual `Python`'s environment:

```bash
python -m venv env
```

- activate the virtual environment:

```bash
source env/Scripts/activate  # for Windows
# or
source env/bin/activate  # for Linux/Mac

```

- **optional:** if uninstall for library required, do this one:

```bash
pip uninstall yt-dlp
```

- **optional:** if updating of `pip` required:

```bash
python -m pip install --upgrade pip
```

and then check

```bash
pip --version
```

to get something like this

```bash
pip 24.0 from .../env/lib/site-packages/pip (python 3.12)
```

- install `yt-dlp` into the virtual environment:

```bash
pip install yt-dlp
```

- check the

```bash
pip list
```

to include `yt-dlp`

### **notice**:

**Caution!**
**Checking for video and audio availability**  
To check if the video has an audio track, you can use the `--dump-json` option. This option outputs
metadata about the video, including information about available audio tracks.

Here is an example of a command that will give you this information:

```bash
yt-dlp --dump-json "VIDEO_URL"
```

The output will contain the formats field, which lists all available formats, including video and audio. This way you can see if both video and audio are available before you start downloading.

---

**Checking formats before uploading:**  
To avoid downloading incorrect formats, you can check the available formats in advance
using the `yt-dlp --list-formats` command.

```bash
yt-dlp -F "link/to/video"

```

This will show a list of available formats for video and audio, which will help you choose
the correct format_id to download.

**Downloading video manually via video (or video and audio ID):**  
For downloading video manually via video (or video and audio ID) use this command

```bash
yt-dlp -f <video_id> htts://link/to/video
```

or if there're separated video and audio files (checked via previous step) download best video via its id, than best audio same way and merge them via `ffmpeg.exe`
(**notice:** ffmpeg.exe required!)

```bash
path/to/bin/ffmpeg.exe -i path/to/video -c:v <video_codec> -i path/to/audio -c:a <audio_codec> output.mkv
```

where <video_codec> and <audio_codec> are e.g. `libaom-av1` for best `AV1` video codec,
and `alac` or `flac` for best audio codec,

`output.mkv` - rename `output` as you wish, and use `.mkv` or `.mp4` as you like (check
[`ffmpeg docs`](https://www.ffmpeg.org/ffmpeg.html) for details and supported formats!)

**notice:** if there's downloading problems (too low speed) try to use `--concurrent-fragments N`,
as for example `--concurrent-fragments 5` (make a few experiments with that to reach optimum speed! default is: `--concurrent-fragments 1`)

**Example of the downloaded video info (via `yt-dlp -F link/to/video`)**

| ID  | EXT | RESOLUTION | FPS | CH  | FILESIZE | TBR  | PROTO | VCODEC        | VBR  | ACODEC     | ABR | ASR | MORE | INFO |
| --- | --- | ---------- | --- | --- | -------- | ---- | ----- | ------------- | ---- | ---------- | --- | --- | ---- | ---- |
| 602 | mp4 | 256x144    | 15  | --  | ~8.70MiB | 103k | m3u8  | vp09.00.10.08 | 103k | video only | --- | --- | ---- | ---- |

for more details about the table's head abbreviations check the [docs](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template) or use net search))

**Explanation of `python -m venv`**  
`-m`: This option tells `Python` to run the module as a script. In this case, venv is a module that is used to create virtual environments.
`venv`: A module for creating virtual environments in Python. Virtual environments allow you to isolate project dependencies, avoiding conflicts with globally installed packages.

---

**How to create and use the configuration file `yt-dlp.conf`**

1. **Create a configuration file**:

- In the root of the project (prefer the `configs/yt-dlp.conf`) create a file named `yt-dlp.conf`
  (or `yt-dlp.video.conf` and `yt-dlp.audio.conf` for more detailed preference and flexibility).

2. **Add the settings to the file**:

- Inside `yt-dlp.conf` add the necessary parameters. For example:

  ```plaintext
  --verbose
  --impersonate "Chrome-116:Windows-10"
  --continue
  --retries 100
  --fragment-retries 100
  --http-chunk-size 10M
  --concurrent-fragments 5
  -f bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]
  -o ./downloads/%(title).10s/%(title)s.%(ext)s
  --ffmpeg-location ./ffmpeg/ffmpeg-7.0.1-full_build/bin/
  ```

3. **Update the script `main.py `**:
   - Now, in order to use the configuration, you will not need to duplicate the parameters in the code.  
     Just add the `--config-location` option to specify the configuration file:

```python
# main.py
import subprocess
from typing import List

# current file dirname
current_dir = os.path.dirname(__file__)

# activating virtual surrounding
activate_env: str = os.path.join(current_dir, "..", "env", "Scripts", "activate.bat")
subprocess.call([activate_env], shell=True)

# URL video from youtube
video_url: str = 'url/of/the/video'

# download command
command: List[str] = ['yt-dlp', '--config-location', 'yt-dlp.conf', video_url]

#command execution
subprocess.run(command)
```

**Folder for the configuration file**

If you prefer to keep the configuration file in a separate folder, you can create a folder, for example, `configs`, and put the `yt-dlp.conf` file there. Then the path to the file will need to be specified in '--config-location`:

```python
command = ['yt-dlp', '--config-location', 'configs/yt-dlp.conf', video_url]
```

---

**What is `subprocess` and `os.system` in Python.**

1. **subprocess**

The `subprocess` module is used to create new processes, connect to their I/O streams, and get their results. It is more flexible and powerful than the old `os.system` module, which just executed commands in the shell.

**Main functions and methods:**

- **`subprocess.run()`**: Runs the command and waits for it to complete. Allows you to get the return code and the output of the command.

  ```python
  result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
  print(result.stdout) # outputs the result of executing the command
  ```

- **`subprocess.call()`**: Executes the command and returns the return code. This is an easier option than `run()` if you don't need to process the output.

  ```python
  return_code = subprocess.call(['ls', '-l'])
  ```

- **`subprocess.Popen()`**: Allows more complex interaction with processes. This allows you to run processes, read their I/O in real time, and do many other things.

  ```python
  process = subprocess.Popen(['ping', 'google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, error = process.communicate()
  ```

2. **os.system**

The `os.module` provides many functions for interacting with the operating system.`os.system()`is used to execute a
command in the shell. However, it is less flexible than`subprocess'.

**Usage example:**

```python
import os
os.system('ls -l') # executes the command and outputs the result to the console
```

**Differences between `subprocess` and `os.system`:**

- **Flexibility**: `subprocess` allows for more customization of interaction with running processes, including I/O processing.
- **Security**: `subprocess` avoids problems with executing commands containing special characters or arguments.
- **Information Return**: Using `subprocess` you can receive command output, return code and other data, which is not possible with `os.system`.

**Conclusion**

If you need to execute commands in the terminal and interact with their output, I would recommend using `subprocess'. It is more powerful and convenient for complex scenarios.

---

**Create a file requirements.txt to manage libs:**

```bash
pip freeze > requirements.txt
```

### configs/yt-dlp.conf details

`configs/yt-dlp.conf`

```bash
# to show details via script run
--verbose
# to simulate Google Chrome browser on Windows 10
--impersonate "Chrome-116:Windows-10"
# to continue download (*.part files) even in a time
--continue
# attemps to download entire file
--retries 100
# attemps to download *.part of the entire file
--fragment-retries 100
# max chunk size for download (far better to use it! Default: 10M === 10 Mb)
--http-chunk-size 10M
# ! the most important option!!! Current one mean that simultaneously will be downloaded 10 *.part files!
# check the opt one N of --concurrent-fragments N experimentally (default: N = 1) checking the number
# of errors and downloaded speed value
--concurrent-fragments 10
# download file option! This one means:
# download 1080p or less height video (best is 1080p currently)
# with .mp4 extension
# and video must have video codec
# with video bitrate more than 1000kbps
# and best audio with audio codec present
# with audio birate more than 120kbps
# with audio sample rate (asr) equal or more than 44000 Hz (44kHz)
# never the less best of all in a .mp4 format with at least 1080 pixels height
-f 'bestvideo[vcodec!=none][height<=1080][vbr>1000][ext=mp4]+bestaudio[acodec!=none][abr>120][asr>=44000]/best[height<=1080][ext=mp4]'
# set the dowloaded file's path and details (verbose description is below)
# notice: template %(title).10s will limit the name up to 10 symblos
# e.g. file name is "VeryLongVideoTitle"
# output => downloads/VeryLongVi/VeryLongVideoTitle.mp4 (VeryLongVi is a folder name limited to 10 symbols)
-o ./downloads/%(title).10s/%(title)s.%(ext)s
# ffmpeg is strongly required! Details below
--ffmpeg-location ../ffmpeg/ffmpeg-7.0.1-full_build/bin/ffmpeg.exe
# output format of the file after merge
--merge-output-format mkv
# ffmpeg options for preserving original codecs or
# --postprocessor-args "-c:v libaom-av1 -c:a alac"
# that is ffmpeg options for preserving AV1 codec for video and alac (m4a) for audio
# (or as you prefer *.flac to *.m4a, use flac)
--postprocessor-args '-c:v copy -c:a copy'
```

---

to change directory for downloading use

**configs/yt-dlp.conf**

```bash
-o ./downloads/%(title)s.%(ext)s
```

where `%()s` is a python ' s template string,  
`title` - save the original file's name,  
`ext` - save the original file's extension extension

---

to set cookies, just copy required from the browser ' s devTools/Application/cookies  
(`Ctrl+A` => `Shift + Right Click` => `Copy` or `Ctrl + C`)

```bash
--cookies ./cookies/cookies.txt
```

---

`ffmpeg` is **strongly required**. Download ffmpeg `Release stable version` archive from
[ffmpeg.org](https://www.ffmpeg.org/download.html) and copy it to `./libs/ffmpeg`and then use `ffmpeg-location`
to set relative path to the ffmpeg binary

**configs/yt-dlp.conf**

```bash
--ffmpeg-location ./libs/ffmpeg/bin/ffmpeg.exe
```

---

**--impersonate CLIENT' option**
install `curl_cffi` to emulate the browsers

```bash
pip install curl_cffi
```

then run

```bash
yt-dlp --list-impersonate-targets
```

to get something like this

```bash

[info] Available impersonate targets
Client        OS           Source
------------------------------------
Chrome-124    Macos-14     curl_cffi
Chrome-123    Macos-14     curl_cffi
Chrome-120    Macos-14     curl_cffi
Chrome-119    Macos-14     curl_cffi
Chrome-116    Windows-10   curl_cffi
Chrome-110    Windows-10   curl_cffi
Chrome-107    Windows-10   curl_cffi
Chrome-104    Windows-10   curl_cffi
Chrome-101    Windows-10   curl_cffi
Chrome-100    Windows-10   curl_cffi
Chrome-99     Windows-10   curl_cffi
Edge-101      Windows-10   curl_cffi
Edge-99       Windows-10   curl_cffi
Safari-17.0   Macos-14     curl_cffi
Safari-15.5   Macos-12     curl_cffi
Safari-15.3   Macos-11     curl_cffi
Chrome-99     Android-12   curl_cffi
Safari-17.2   Ios-17.2     curl_cffi
(env)
```

The `--impersonate CLIENT' option[:OS]` in `yt-dlp` allows you to emulate requests on behalf of another client to try to circumvent restrictions or locks set on the server side. This can help if the server reacts differently to different User-Agents or if it applies restrictions to certain clients.

#### Syntax:

- **`CLIENT`**: Specifies the type of client you want to emulate. For example, it can be a browser (Chrome, Firefox, etc.) or a mobile application (for example, YouTube App).
- **`OS`** (optional): Specifies the operating system from which the client is emulated.

**Usage examples:**

1. Chrome emulation on Windows:

   ```
   yt-dlp --impersonate "Chrome-116:Windows-10"
   ```

2. YouTube App Emulation on Android:
   ```
   yt-dlp --impersonate "Chrome-99:Android-12"
   ```

**Impact on download speed:**

This option will not necessarily increase the download speed, but it can help to avoid problems with video access that may be caused by client-based restrictions. If the server thinks that you are using an "unavailable" client, it can limit the speed or block access to the video altogether.

**How to use it in the config:**

If you want to add this option to your `yt-dlp.conf` configuration file, just add it to a new line:

```plaintext
--impersonate "Chrome-116:Windows-10"
```

And remember that changing the client may lead to differences in video availability or quality. Try different parameters to find the most suitable one for your needs.

## Links

- [Git Large File Storage docs](https://git-lfs.com/);
- [Git Large File Storage official GitHub repo and docs](https://github.com/git-lfs/git-lfs?utm_source=gitlfs_site&utm_medium=source_link&utm_campaign=gitlfs);
- [yt-dlp GitHub official repo and docs](https://github.com/yt-dlp/yt-dlp);
- [curl_cffi GitHub official repo and docs](https://github.com/yifeikong/curl_cffi);
- [FFmpeg official website and docs](https://www.ffmpeg.org/);
- [FFmpeg GitHub official repo and docs](https://github.com/FFmpeg/FFmpeg);
- [youtube-dl GitHub official repo and docs (inactive tool now)](https://github.com/ytdl-org/youtube-dl);

### Recommended tutorials all over the Python

- [Automate the Boring Stuff with Python by Al Sweigart](https://automatetheboringstuff.com/);
- [Python Crash Course by Eric Matthes](https://ehmatthes.github.io/pcc/);
- [Real Python](https://realpython.com/);
- [Python for Everybody by Charles Severance](https://www.py4e.com/);
- [Learn Python the Hard Way by Zed Shaw](https://learnpythonthehardway.org/);
- [The Hitchhiker’s Guide to Python](https://docs.python-guide.org/);
- [Python Cheatsheet](https://www.pythoncheatsheet.org/);
- [devhints.io Python Cheatsheet](https://devhints.io/python);

### All about paths usage in the Python

- [os.path — Common pathname manipulations](https://docs.python.org/3/library/os.path.html);
- [os — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html);
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html);

### Documenting and Docstring for Python usage

- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/);
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/);
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html);
- [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html);
- [Google style Python docstrings](https://docs.idmod.org/projects/doc-guidance/en/latest/docstrings.html);
- [What are the most common Python docstring formats? [closed]](https://stackoverflow.com/a/24385103/20705648);

### Typization in Python (v3.5+)

- [typing — Support for type hints](https://docs.python.org/3/library/typing.html);

**done:**
31.07.2024

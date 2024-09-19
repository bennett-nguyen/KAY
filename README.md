![KAY logo](./github-assets/img/Logo.jpg)

# KÂY 

## Locale: [Tiếng Việt](./README-vn.md)

KÂY (English: KAY, read either as /kaɪ/ in "kayak" or /keɪ/ in "okay") is a Python application that visualizes the segment tree as well as its properties.
<br>
<br>
The tree is drawn using the modification version of the Reingold-Tilford algorithm for drawing perfect binary trees.

# Installation

Requirements:
- Python 3.10+
- Pygame Community Edition 2.1.4+
- pygame-gui 0.6.9+
- OpenCV 4.10.0.84+
- Numpy 2.1.1+

Go to the [release page](https://github.com/bennett-nguyen/KAY/releases) and download the latest version. Otherwise you can clone this repository or click on download as ZIP.

It is recommended that you create a Python virtual environment and activate it before install and run the program. To install the requirements, change directory into the project and install all of them listed out in `requirements.txt`.

Linux:

```bash
$ cd KAY/                         # change dir into the program folder
$ python3 -m venv .venv                   # create virtual environment
$ source .venv/bin/activate               # activate environment
(.venv) $ pip install -r requirements.txt # install requirements
(.venv) $ python entry.py                 # to run the program
```

Windows:

```ps
C:\...> cd KAY/                   # change dir into the program folder
C:\...\KAY> python -m venv .venv       #  create virtual environment
C:\...\KAY> .venv\Scripts\activate.bat # activate environment
(.venv) C:\...\KAY> pip install -r requirements.txt # install requirements
(.venv) C:\...\KAY> python3 entry.py   # to run the program
```

if you already had created an environment then just activate it and run the program.

# License

This application is licensed under the [GNU General Public License version 3](./LICENSE).
```
Copyright (C) 2023 Nguyen Vinh Phu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Email: bennett-contact-me-github.magnify754@simplelogin.com
```

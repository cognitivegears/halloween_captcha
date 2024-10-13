# Spooky Halloween CAPTCHA

This is an example of an alternate CAPTCHA system, all dressed up for Halloween. As the world moves forward with Generative AI and improved machine learning, existing CAPTCHA systems will be less and less effective. This is downright _spooky_.

This repo is an example of a thought experiment about what else we could use that would be difficult for a machine to defeat. In this case, we are taking advantage of the fact that humans are inherently analog.

Have you ever thought about how weird it is that you can catch a ball? Calculating the curve of a ball to find the landing spot involves both physics and advanced math. Yet just about everyone can do it without thinking about it.

I propose that it is much harder for a machine to do. Generative AI is (at least currently) not very good at general math. And while computers in general are *great* at it, they would have to be taught the specific problem. Machine learning, likewise, would be an effective attack on this, but would need to be trained on the specific problem. And this (admittedly silly) CAPTCHA system took less than a day to create.

The existing CAPTCHA systems are based around our ability to perform pattern recognition, which machines have gotten really good at. We'll need to find new methods if we are to stay one step ahead.

![captcha_animation](https://github.com/user-attachments/assets/b41646f3-9d20-4358-b3d4-961d6ec0e812)

## Building ##

### Run with Python ###

Requires a modern Python (tested against Python 3.12)

1. Clone the repository
2. Install with venv

_Windows_:

```
    python -m venv .venv
    .\.venv\Scripts\activate
```

_Linux/Mac_

```
    python -m venv .venv
    source .venv/bin/activate
```

3. Install dependencies

```
    pip install -r requirements.txt
```

4. Run captcha with python

```
    python captcha.py
```

### Compile ###

Follow steps 1-3 above, then:

```
    pip install nuitka
    python -m nuitka --standalone --windows-console-mode=disable --noinclude-unittest-mode=nofollow --include-data-files="assets\*=assets\" captcha.py
```

## Contest ##

This came about as a result of a Halloween contest run on the YouTube channel LaurieWired: [LauriWired Halloween Programming Challenge 2024](https://github.com/LaurieWired/Halloween_2024_Programming_Challenge) - Video: [Programming Challenge Video](https://www.youtube.com/shorts/AAT1LVece0A). Do your worst Asuka!

## License ##

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

For more details, see [LICENSE.md](LICENSE.md).

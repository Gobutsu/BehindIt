![Alt text](https://files.catbox.moe/ubz2ae.png)

# 📸 BehindIt - Revealing the Source Behind Links

## 🤔 What is it?
This tool is designed to uncover the identity of a person who sends you an **Instagram reel** or a **TikTok post** by exploiting the tracking parameters in the URL. For instance, links like `https://vm.tiktok.com/********/` or `https://www.instagram.com/reel/C7gx9yMySJr/?igsh=***********` can be traced back to the sender. Anyone who shares such a link without knowing about this can potentially be identified.

## 📦 Installation
You can either install it from Github (recommended):
```
git clone https://github.com/Gobutsu/BehindIt
cd BehindIt
python setup.py install
```
Or from Pypi:
```
pip install behindit
```
Installation can be confirmed by typing `behindit` in a terminal.

## 🚀 How to use it?
```
behindit [-h] [-i INSTAGRAM] [-t TIKTOK]
```
"i" and "t" being either the full link, or the tracking ID

## 🤷‍♂️ Why isn't it finding anything?
Several factors could cause this issue:

- The ID is invalid.
- The ID has expired, meaning it can't find the profile anymore or has reached its maximum usage.
- The user has disabled the feature on their profile.

## 🛡️ How can I protect myself from this tool?
The simplest way to protect yourself is to remove the tracking parameter from any URL you send. For TikTok, you can copy the URL it redirects you to and send that instead. Additionally, you can disable the ability to find you via these links in your TikTok account settings.

Unfortunately, for Instagram, this level of protection is not available.
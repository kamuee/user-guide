
# Kamuee User's Guide

setup build env
```
sudo pip3 install sphinx sphinx_rtd_theme
sudo apt install -y texlive-fonts-recommended \
		texlive-latex-recommended texlive-latex-extra \
		texlive-lang-japanese latexmk texlive-latex-base
```

clone and build documentation
```
git clone <this-repo> <repo-name> && cd $_
make html
ls _build/html/index.html
```


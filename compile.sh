FILE=main/main.tex
CHAPTER=theBasics
SECTION=linearTrans

latexmk -pdflua -shell-escape -jobname=main/wip -pretex="\def\wipchapter{$CHAPTER}\def\wipsection{$SECTION}" -usepretex ${FILE}
# cp main/main.pdf pdfs/main.pdf

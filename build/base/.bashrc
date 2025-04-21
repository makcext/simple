source /opt/venv/bin/activate
export LS_OPTIONS='--color=auto'
alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'

force_color_prompt=yes
export PS1="\n[\T][${CONTAINER_NAME}(\h):/\W]>\n# "

HISTCONTROL=ignoreboth
shopt -s histappend
shopt -s checkwinsize
HISTSIZE=10000
HISTFILESIZE=20000

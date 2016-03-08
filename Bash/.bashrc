# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000000
HISTFILESIZE=2000000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;34m\]\w\[\033[00m\]\$ '
    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\w\$ '
    #PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias vi='vim'
alias juniper_bak='sudo touch /etc/jnpr-nc-hosts.bak'
alias juniper_res='sudo touch /etc/jnpr-nc-resolv.conf'
alias gettit='sudo apt-get install -y'
alias Grep='grep'
alias sss='sudo !!'
alias checkJ='python -mjson.tool'
alias startsyn='synergys --config ~/tools/tools/Synergy/synergy.conf'
alias cdb='cd /home/scott/GitRepos/Bock'
alias cdt='cd ~/tools/tools'
alias sb='source ~/.bashrc && echo source bashrc'
alias vb='vi ~/.bashrc'
alias pd='pushd $PWD'
alias findbig='sudo du -hsx * | sort -rh | head -10'
alias upMaster='git fetch --all && git checkout master && git merge --ff-only origin/master'
alias c.="cd .."
alias ..="cd ../.."
alias ...="cd ../../.."
alias lr="ls -altr"
alias gpu="git push -u origin"
alias buildIt="./build_bock.bash --version auto --no-c --no-sys --no-kmods --dist precise --no-unit-tests"
alias buildItExtras="./build_bock.bash --version auto --no-c --no-sys --no-kmods --dist precise --no-unit-tests --extras"
alias AuthFix="git commit --amend --reset-author -C HEAD"
alias sshe="echo eVolmon0004RndE"
alias cdn="cd ~/tools/tools/HPcloud/Nova/"
alias cinder="cinder --insecure"
alias nova="nova --insecure"
alias neutron="neutron --insecure"
alias swift="swift --insecure"
alias sc="vi ~/.ssh/config"
alias g="git"
alias nvrc="cd /home/scott/tools/tools/HPcloud/NovaRC"
alias sss="set |grep OS_"
alias startVPN="sudo openvpn --config /etc/openvpn/hp-client.ovpn"
alias tm="®"

set -o vi

if [ -f ~/.git-completion.bash ]; then
    . ~/.git-completion.bash
fi

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

export PATH=${PATH}:~/bin

#for packer
export PATH=${PATH}:~/packer


export DEBEMAIL="scott.dangelo@hp.com"
export DEBFULLNAME="Scott DAngelo"

export GPGKEY=05A9E408

export LAST_PROMPT=0
#Below changes to blue color. fix this
function tp() {
    if [ "$LAST_PROMPT" -eq "0" ]; then
        export PS1='$';
        LAST_PROMPT="1";
    else
        if [ "$color_prompt" = yes ]; then
            export PS1='${debian_chroot:+($debian_chroot)}\[\033[01;34m\]\w\[\033[00m\]\$ '
        else
            export PS1='${debian_chroot:+($debian_chroot)}\w\$ '
        fi
        unset color_prompt force_color_prompt
        #export PS1='${debian_chroot:+($debian_chroot)}\[\033[01;34m\]\w\[\033[00m\]\$';
        LAST_PROMPT="0";
    fi

}
export EDITOR=vim
# Add Tab-completion for SSH host aliases
#complete -o default -o nospace -W "$(/usr/bin/env ruby -ne 'puts $_.split(/[,s]+/)[1..-1].reject{|host| host.match(/*|?/)} if $_.match(/^s*Hosts+/);' < $HOME/.ssh/config)" scp sftp ssh
#export PS1=">"
complete -W "$(echo $(grep '^ssh ' ~/.bash_history | sort -u | sed 's/^ssh //'))" ssh

PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting
[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm" #Load RVM function
#[[ -s '/usr/local/lib/rvm' ]] && source '/usr/local/lib/rvm'

export LESS='-R'
export LESSOPEN='|~/.lessfilter %s'

#export NOVA_USERNAME=scott.dangelo
#export NOVA_PASSWORD=irwt50b!!
#export NOVA_PROJECT_ID=scott_cinder_test
#export NOVA_URL=https://region-b.geo-1.identity.hpcloudsvc.com:35357/v2.0/
#export NOVA_VERSION=1.1
#export NOVA_REGION_NAME=region-b.geo-1
#export OS_USERNAME=scott.dangelo
#export OS_PASSWORD=irwt50b!!
#export OS_PROJECT_ID=scott_cinder_test
#export OS_AUTH_URL=https://region-b.geo-1.identity.hpcloudsvc.com:35357/v2.0/
#export OS_REGION_NAME=region-b.geo-1
#export OS_TENANT_NAME="scott_cinder_project"
export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

#export PS1="\[$(tput bold)$(tput setb 4)$(tput setaf 7)\]\u@\h:\w $ \[$(tput sgr0)\]"

#keychain --nocolor --nogui id_rsa
#. ~/.keychain/`uname -n` -sh

#export HTTP_PROXY=http://web-proxy.fc.hp.com/
#export HTTPS_PROXY=https://web-proxy.fc.hp.com/
# ssh scott@76.120.120.93
export VAGRANT_DEFAULT_PROVIDER=libvirt

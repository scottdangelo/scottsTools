set nobackup
set nowritebackup
set noswapfile
set lines=40
set columns=80
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set smartindent
set expandtab
set smarttab
set background=light
set pastetoggle=<F12>
filetype indent on
filetype on
syntax on
filetype plugin on

:highlight ExtraWhitespace ctermbg=red guibg=red
:highlight AnyTab ctermbg=red guibg=red
:match ExtraWhitespace /\s\+$/
:match AnyTab /\t/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()


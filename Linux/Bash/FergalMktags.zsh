#!/bin/zsh
mktags()
{
    local grep_cmd="" ptn

    if [[ -d src/libswift ]]
    then
        set -- "$@" --exclude=src/BUILD_OUTPUT --exclude=src/LAST_
    elif [[ -d fs/ipfs1_old ]]
    then
        set -- "$@" --exclude="fs/ipfs0" --exclude="fs/ipfs1" --exclude="fs/Win2kXp"
    elif [[ -d build_rpm ]] || [[ -d build_deb ]]
    then
        set -- "$@" --exclude="build_rpm" --exclude="build_deb" --exclude="testing"
    fi

    ctags --recurse=yes --sort=yes --excmd=pattern --totals --links=no "$@"

    for excl in ${(M)@:#--exclude=*}
    do
        ptn="${excl#*=}"
        case "${ptn}" in
        fs/ipfs1)
            ptn="${ptn}/"
            ;;
        esac
        grep_cmd="${grep_cmd:-grep -v} -e '${ptn}'"
    done

    find . \
        \( \
            -name "*.[chs]" -o \
            -name "*.py" -o \
            -name "*[Mm]akefile" -o \
            -name "*.mk" -o \
            -name "*.in" \
        \) -print | \
        (
            if [[ -n "${grep_cmd}" ]]
            then
                eval "${grep_cmd}"
            else
                cat -
            fi
        ) | sed -e 's,^[.]/,,' | cscope -i- -bkqRUuv
}

${0##*/} "$@"
# vim:expandtab:shiftwidth=4:tabstop=4:autoindent:showmatch:nohlsearch


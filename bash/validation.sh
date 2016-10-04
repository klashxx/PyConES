
function  mail {
  local mail=$1

  if [[ ! $mail =~ ^[A-Za-z0-9._%+-]+@cajamar.es$ ]]; then
     echo "Email address $mail is invalid."
    return 5
  fi

  return 0
} >&2


function filesystem {
  local fs=$1
  [[ ! -d $1 ]] && echo "Not a FS" >&2 && return 5
  echo $fs
  return 0
}


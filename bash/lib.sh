

function avaliable_space {

  local fs=$1
  local host=${2:-none}

  if [ $host = "none" ]; then
    local_free=$(df -P -B 1 $fs 2>/dev/null|awk 'NR==2{print $4+0}')
  else
    local_free=$(ssh  $host \
                        -o BatchMode=yes \
                        -o UserKnownHostsFile=/dev/null \
                        -o StrictHostKeyChecking=no \
                        -o ConnectionAttempts=5 \
                        -o CheckHostIP=no \
                        "df -P -B 1 $fs" 2>/dev/null | \
                        awk 'NR==2{print $4+0}' 2>/dev/null)
  fi

  if [ -z $local_free ]; then
    return 2
  fi

  free=$local_free

  return 0
}


function  decode_pass {
  local fpass=$1
  local fpriv=$2

  openssl rsautl -decrypt -inkey $fpriv -in $fpass
}

readonly USER="pycones"
readonly SECRET="./keys/pass.ssl"
readonly PRIV="./keys/pycones.priv"

function avaliable_db_space {
  local host=$1
  password="$(decode_pass $SECRET $PRIV)"
  mysql -h $host --user=$USER --password=$password <<-EOF 2>/dev/null | awk 'NR>1'
      SELECT
      table_schema as "Database",
      table_name AS "Table",
      round(((data_length + index_length) / 1024 / 1024), 2) AS "MB"
        FROM information_schema.TABLES
        WHERE data_length > 0
        ORDER BY (data_length + index_length) DESC
EOF
  if [ $? -ne 0 ];then
  	echo "No se pudede conectar contra $host"
  fi

}


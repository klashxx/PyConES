
source ./auth.sh



readonly USER="pycones"
readonly HOST="pymysql"
readonly SECRET="./keys/pass.ssl"
readonly PRIV="./keys/pycones.priv"



function avaliable_space {
	password="$(decode_pass $SECRET $PRIV)"

	mysql -h $HOST --user=$USER --password=$password <<-EOF 2>/dev/null
     SELECT
     table_schema as "Database",
     table_name AS "Table",
     round(((data_length + index_length) / 1024 / 1024), 2) AS "MB"
       FROM information_schema.TABLES
       WHERE data_length > 0
       ORDER BY (data_length + index_length) DESC
EOF
}


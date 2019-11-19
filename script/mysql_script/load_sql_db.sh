start=`date +%s`

# Get kindle_reviews.csv
# estimated running time: 8s on EC2
echo "Downloading data ..."
wget https://database-project-50043.s3-us-west-2.amazonaws.com/kindle_reviews.csv
wget https://database-project-50043.s3-us-west-2.amazonaws.com/bookinfo.csv
echo "Downloading SQL script"
wget https://database-project-50043.s3-us-west-2.amazonaws.com/load_sql_db.sh
wget https://database-project-50043.s3-us-west-2.amazonaws.com/create_additional_tables.sql
wget https://database-project-50043.s3-us-west-2.amazonaws.com/load_data_sql.sql
wget https://database-project-50043.s3-us-west-2.amazonaws.com/store_user_information.sql


# Load all the tables 
# estimated running time: 21s
echo "Loading data into database ..."
echo "1.Load review db:"
mysql -u root < load_data_sql.sql
rm -rf load_data_sql.sql

echo "2.Load User management db:"
mysql -u root < store_user_information.sql
rm -rf store_user_information.sql

echo "3.Load addtional tables:"
mysql -u root < create_additional_tables.sql
rm -rf create_additional_tables.sql

end=`date +%s`

runtime=$((end-start))

echo "Finish set up"


# Print the running time
echo "Runtime was $runtime"




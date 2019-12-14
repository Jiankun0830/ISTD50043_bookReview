start=`date +%s`

# Get kindle_reviews.csv
# estimated running time: 8s on EC2
echo "Downloading data ..."
wget https://database-project-50043.s3-us-west-2.amazonaws.com/kindle_reviews.csv
wget https://database-project-50043.s3-us-west-2.amazonaws.com/bookinfo.csv

echo "Downloading SQL script"
wget --output-document=create_additional_tables.sql https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mysql_script/create_additional_tables.sql?token=AKWIWQQBW6ON6T4GCN7VX7C55T74U
wget --output-document=load_data_sql.sql https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mysql_script/load_data_sql.sql?token=AKWIWQXHCVSQSFJLIDKGL3255T77E
wget --output-document=store_user_information.sql https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mysql_script/store_user_information.sql?token=AKWIWQWIV37GVLLMNJ44WSS55UABU

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

# Delete the origninal data
rm -rf kindle_reviews.csv
rm -rf bookinfo.csv

end=`date +%s`

runtime=$((end-start))

echo "Finish set up"


# Print the running time
echo "Runtime was $runtime"




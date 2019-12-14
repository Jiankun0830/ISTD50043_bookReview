use admin
db.createUser({
      user: "admin",
      pwd: "myadminpassword",
      roles: [
                { role: "userAdminAnyDatabase", db: "admin" },
                { role: "readWriteAnyDatabase", db: "admin" },
                { role: "dbAdminAnyDatabase",   db: "admin" }
             ]
  });
use book_log
db.createUser({user:'db_grp7_test',pwd:'1234567',roles:[{role:'readWrite',db:'book_metadata'},{role:'readWrite',db:'book_log'}]})

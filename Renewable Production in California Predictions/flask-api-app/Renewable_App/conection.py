####################################################################
# This script is to be used as a module to create a general connection to 
# renewable database
####################################################################

# import needed libaries for creating connection to APDN
import sqlalchemy
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv
from os.path import join, dirname


####################
# need to tell load_dotenv
#what env file to load
# prod.env -> live app tables
#test.env -> testing database in prod server
#########################

class Connection():
    """
    Class to Create a connection to local postgres db
    """
    def __init__(self, ENV_FILE):
        """
        @param envFile - string for the name of the env file to use
        @param MORE - could add more params to define the connection cofig here too 
        """
        self.ENV_FILE = ENV_FILE + '.env'
        dotenv_path = join(dirname(__file__),'env', self.ENV_FILE)
        load_dotenv(dotenv_path=dotenv_path, override=True)
        self.db_config = {
            # [START cloud_sql_mysql_sqlalchemy_limit]
            # Pool size is the maximum number of permanent connections to keep.
            "pool_size": 5,
            # Temporarily exceeds the set pool_size if no connections are available.
            "max_overflow": 2,
            # The total number of concurrent connections for your application will be
            # a total of pool_size and max_overflow.
            # [END cloud_sql_mysql_sqlalchemy_limit]
            # [START cloud_sql_mysql_sqlalchemy_backoff]
            # SQLAlchemy automatically uses delays between failed connection attempts,
            # but provides no arguments for configuration.
            # [END cloud_sql_mysql_sqlalchemy_backoff]
            # [START cloud_sql_mysql_sqlalchemy_timeout]
            # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
            # new connection from the pool. After the specified amount of time, an
            # exception will be thrown.
            "pool_timeout": 30,  # 30 seconds
            # [END cloud_sql_mysql_sqlalchemy_timeout]
            # [START cloud_sql_mysql_sqlalchemy_lifetime]
            # 'pool_recycle' is the maximum number of seconds a connection can persist.
            # Connections that live longer than the specified amount of time will be
            # reestablished
            "pool_recycle": 3600,  # 30 minutes
            # [END cloud_sql_mysql_sqlalchemy_lifetime]
            "pool_pre_ping":True
        }
    # create connection to database 
    def init_connection_engine(self):
        """
       @returns connection pool to be used to query database
        """
        # Catch for either connecting to proxy TCP connection
        # or connecting to cloud sql
        if os.environ.get("DB_HOST"):
            db_user = os.environ["DB_USER"]
            db_pass = os.environ["DB_PASS"]
            db_name = os.environ["DB"]
            print('DATABASE NAME ######################')
            print(db_name)
            db_host = os.environ["DB_HOST"]
            # Extract host and port from db_host
            host_args = db_host.split(":")
            db_hostname, db_port = host_args[0], int(host_args[1])

            pool = create_engine(
                # Equivalent URL:
                # postgres+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
                sqlalchemy.engine.url.URL(
                    drivername="postgres+pg8000",
                    username=db_user,  # e.g. "my-database-user"
                    password=db_pass,  # e.g. "my-database-password"
                    host=db_hostname,  # e.g. "127.0.0.1"
                    port=db_port,  # e.g. 5432
                    database=db_name  # e.g. "my-database-name"
                ),
                # ... Specify additional properties here.
                # [END cloud_sql_postgres_sqlalchemy_create_tcp]
                **self.db_config
                # [START cloud_sql_postgres_sqlalchemy_create_tcp]
            )
            # [END cloud_sql_postgres_sqlalchemy_create_tcp]

            return pool
         
        else:
            #this method is how a cloud function connects to a Cloud SQL instance 
            db_user = os.environ["DB_USER"]
            db_pass = os.environ["DB_PASS"]
            db_name = os.environ["DB"]
            db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
            cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

            pool = sqlalchemy.create_engine(
                # Equivalent URL:
                # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
                #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
                sqlalchemy.engine.url.URL(
                    drivername="postgres+pg8000",
                    username=db_user,  # e.g. "my-database-user"
                    password=db_pass,  # e.g. "my-database-password"
                    database=db_name,  # e.g. "my-database-name"
                    query={
                        "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                            db_socket_dir,  # e.g. "/cloudsql"  LITERALLY "/cloudsql"
                            cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
                    }
                ),
                # ... Specify additional properties here.
                # [END cloud_sql_postgres_sqlalchemy_create_socket]
                **self.db_config
                # [START cloud_sql_postgres_sqlalchemy_create_socket]
            )
            # [END cloud_sql_postgres_sqlalchemy_create_socket]

            return pool

   
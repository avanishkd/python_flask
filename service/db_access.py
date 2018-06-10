from .db_util import DBConnect
import logging

class DBAccess():
    def validate_login(self, username, password):
        """
        Method to validate if user is valid; if his credentials exist in DB-
        True is returnrd, else False
        """
        result = False
        try:
            conn = DBConnect.getConnection()
        except Exception as e:
            logging.error("Connection Error ->" + str(e))
            print("Connection Error ->", e)

        try:
            # print("In db class "+username+" "+password)
            sql = "select username,password from users where username='" + username + "' and password ='" + password + "'";
            logging.debug("SQL query to login ->" + sql)
            conn.query(sql)
            all_recs = conn.store_result()
            logging.info("No of records fetched: "+str(all_recs.num_rows()))
            # print ("Number of Records Retrieved ->", all_recs.num_rows())
            if (1 <= all_recs.num_rows()):        
                result = True
            else:
                result = False


        except Exception as e:
            logging.error("Database error, " + str(e))
            result = False
        finally:
            conn.close()
            # print("Result is :",result)
        return result

    def fetch_account_detail(self,username):
        sql = "select firstname,lastname,account_number,account_balance,bank_name from users,accounts where users.user_id = accounts.user_id and users.username='"+username+"'"
        logging.debug("SQL query to fetch account detail is ->"+sql)
        try:
          conn = DBConnect.getConnection()      
        except Exception as e:
          logging.error("Connection Error ->"+str(e))
      
        try:
          conn.query(sql)
          #print("Query to fetch user profile ->"+sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print("Number of elements in the record is:",len(rec))
          for firstname, lastname,account_no, account_balance,bank_name in rec:
            fname= str(firstname,'utf-8')
            lname = str(lastname,'utf-8')
            #print(fname,lname,account_no,account_balance,sep='->')
            logging.info("Account detail fetched is:"+str((fname,lname,account_no,account_balance,bank_name)))
          return (fname,lname,account_no,account_balance,bank_name)
      
        except Exception as e:
          logging.error("Database error, "+str(e))
        finally:
          conn.close()

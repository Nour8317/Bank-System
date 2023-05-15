using System;
using System.Data.SqlClient;

namespace Database.SystemMethods
{
    public class Methods
    {
        static String Sql = "Data Source = DESKTOP-B8CIKIV ; Initial Catalog = Data-base;Integrated Security =True; User ID =''; Password = ''";
        SQlConnection con = new SqlConnection(Sql);//error type SqlConnection not found , check the link may have a solution https://stackoverflow.com/questions/29733221/the-type-or-namespace-name-sqlconnection-could-not-be-found

        private string name = "noor";// just for testing

        public Methods(){}
        public void print(){
            System.Console.WriteLine(name);
        }
    }
}
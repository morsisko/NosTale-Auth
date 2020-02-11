using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using Newtonsoft.Json.Linq; // install this using NuGet https://www.newtonsoft.com/json

namespace NostaleTest
{
    class ntAuth
    {
        string locale, gfLang, installation_id;
        string token = null, platformUserId = null;

        public ntAuth(string _locale="pl_PL", string _gfLang="pl", string _installation_id = "5ea61643-b22a-4ad6-89dd-175b0be2c9d9") {
            locale = _locale;
            gfLang = _gfLang;
            installation_id = _installation_id;
        }

        public bool auth(string _username, string _password) {
            string username = _username;
            string password = _password;
            string URL = "https://spark.gameforge.com/api/v1/auth/thin/sessions";
            try
            {
                var webRequest = System.Net.WebRequest.Create(URL);
                if(webRequest != null)
                {
                    string reqString = "{\"gfLang\": \"{gfLang}\", \"identity\": \"{username}\", \"locale\": \"{locale}\", \"password\": \"{password}\", \"platformGameId\": \"dd4e22d6-00d1-44b9-8126-d8b40e0cd7c9\"}";
                    reqString = reqString.Replace("{gfLang}", gfLang);
                    reqString = reqString.Replace("{username}", username);
                    reqString = reqString.Replace("{locale}", locale);
                    reqString = reqString.Replace("{password}", password);

                    webRequest.Method = "POST";
                    webRequest.ContentType = "application/json";
                    webRequest.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36");
                    webRequest.Headers.Add("TNT-Installation-Id", installation_id);
                    webRequest.Headers.Add("Origin", "spark://www.gameforge.com");

                    byte[] requestData = Encoding.UTF8.GetBytes(reqString);
                    webRequest.ContentLength = requestData.Length;
                    using (var stream = webRequest.GetRequestStream())
                    {
                        stream.Write(requestData, 0, requestData.Length);
                    }

                    System.Net.WebResponse response;
                    try
                    {
                        response = webRequest.GetResponse();
                    }
                    catch (Exception ex)
                    {
                        return false;
                    }
                    
                    var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
                    dynamic stuff = JObject.Parse(responseString);
                    token = stuff.token;
                    platformUserId = stuff.platformUserId;
                    return true;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                throw;
            }
            return false;
        }
    
        public List<string> getAccounts()
        {
            if((token == null) || (platformUserId == null)) {
                throw new System.ArgumentException("First use auth", "original");
            }
            string URL = "https://spark.gameforge.com/api/v1/user/accounts";
            try
            {
                var webRequest = System.Net.WebRequest.Create(URL);
                if (webRequest != null)
                {
                    webRequest.Method = "GET";
                    webRequest.ContentType = "application/json";
                    webRequest.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36");
                    webRequest.Headers.Add("TNT-Installation-Id", installation_id);
                    webRequest.Headers.Add("Origin", "spark://www.gameforge.com");
                    webRequest.Headers.Add("Authorization", "Bearer " + token);
                    webRequest.Headers.Add("Connection", "Keep-Alive");

                    System.Net.WebResponse response;
                    response = webRequest.GetResponse();

                    var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
                    JObject stuff = JObject.Parse(responseString);
                    List<string> acc = new List<string>(new string[] { });
                    foreach (JProperty property in stuff.Properties())
                    {
                        acc.Add(property.Name);
                    }
                    return acc;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                throw;
            }
            List<string> accx = new List<string>(new string[] { });
            return accx;
        }

        private string _convertToken(string code)
        {
            byte[] ba = Encoding.Default.GetBytes(code);
            var hexString = BitConverter.ToString(ba);
            hexString = hexString.Replace("-", "");
            return hexString;
        }
        public string getToken(string account)
        {
            if ((token == null) || (platformUserId == null))
            {
                throw new System.ArgumentException("First use auth", "original");
            }
            string URL = "https://spark.gameforge.com/api/v1/auth/thin/codes";
            try
            {
                var webRequest = System.Net.WebRequest.Create(URL);
                if (webRequest != null)
                {
                    webRequest.Method = "POST";
                    webRequest.ContentType = "application/json";
                    webRequest.Headers.Add("User-Agent", "GameforgeClient/2.0.48");
                    webRequest.Headers.Add("TNT-Installation-Id", installation_id);
                    webRequest.Headers.Add("Origin", "spark://www.gameforge.com");
                    webRequest.Headers.Add("Authorization", "Bearer " + token);
                    webRequest.Headers.Add("Connection", "Keep-Alive");

                    string reqString = "{\"platformGameAccountId\": \"{account}\"}";
                    reqString = reqString.Replace("{account}", account);
                    byte[] requestData = Encoding.UTF8.GetBytes(reqString);
                    webRequest.ContentLength = requestData.Length;
                    using (var stream = webRequest.GetRequestStream())
                    {
                        stream.Write(requestData, 0, requestData.Length);
                    }

                    System.Net.WebResponse response = webRequest.GetResponse();

                    var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
                    dynamic stuff = JObject.Parse(responseString);
                    string code = stuff.code;
                    return _convertToken(code);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
                throw;
            }
            return null;
        }
    }
}

using System;
using System.Collections.Generic;
using System.Globalization;

namespace NostaleTest
{
    class Program
    {
        static void Main(string[] args)
        {
            var api = new ntAuth("pl_PL", "pl", "5ea61643-b22a-4ad6-89dd-175b0be2c9d9");
            if (api.auth("emailOrNickname", "SuperDuperSecretPassword") == false)
            {
                Console.WriteLine("Couldn't auth!");
                Console.ReadKey();
                return;
            }
            List<string> accounts = api.getAccounts();
            string token = api.getToken(accounts[0]);
            Console.WriteLine(token); // this is your SESSION_TOKEN used to generate login packet
            Console.ReadKey();
        }
    }
}
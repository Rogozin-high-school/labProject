using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Drawing;
namespace WindowsFormsApp1
{
    class Server
    {
        static Color[] colors = { Color.Green, Color.Red, Color.Brown };
        const int CLIENTS_COUNT= 3;
        static List<Thread> threads = new List<Thread>();
        /// <summary>
        /// Constructor of server (should be on secondary thread)
        /// </summary>
        /// <param name="port">the port server needs to listen to</param>
        /// <param name="form">the parent form</param>
        public Server(int port,Form1 form)
        {
            //establish local end point for the server socket
            IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
            IPAddress ipAddr = ipHostInfo.AddressList[0];
            IPEndPoint localEP = new IPEndPoint(ipAddr, port);
            //creare the tcp server socket
            Socket listener = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            listener.Bind(localEP);
            listener.Listen(CLIENTS_COUNT);
            while(true)
            {
                Socket clientSoc = listener.Accept();
                Thread thread = new Thread(Handle(clientSoc ,form));
                thread.Start();
                threads.Add(thread);

            }
            
        }
        public static ThreadStart Handle(Socket clientSoc,Form1 form)
        {
            Color color = colors[threads.IndexOf(Thread.CurrentThread)];
            while (true)
            {
                int[] vector = Parse_Vector(Recieve(clientSoc));
                form.Print_Vector(vector,color);
            }
        }
        public static string Recieve(Socket soc)
        {
            byte[] buff = new byte[4];
            soc.Receive(buff);
            int len = int.Parse(Encoding.ASCII.GetString(buff));
            buff = new byte[len];
            soc.Receive(buff);
            return Encoding.ASCII.GetString(buff);
        }
        public static int[] Parse_Vector(string msg)
        {
            List<int> items = new List<int>();
            string[] temp = msg.Split(",".ToCharArray());
            foreach(string i in temp)
            {
                items.Add(int.Parse(i));
            }
            return items.ToArray();
        }
    }
}

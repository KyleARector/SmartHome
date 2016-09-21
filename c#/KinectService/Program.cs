using System;
using System.Collections.Generic;
using System.Net;
using System.ServiceProcess;
using System.Text;

namespace KinectService
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        static void Main()
        {
            ServiceBase[] ServicesToRun;
            ServicesToRun = new ServiceBase[]
            {
                new KinectVoiceService()
            };
            ServiceBase.Run(ServicesToRun);
        }
    }
}

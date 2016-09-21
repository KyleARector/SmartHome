using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace KinectHomeService
{
    class ProcessIcon : IDisposable
    {
        NotifyIcon notiIcon;

        public ProcessIcon()
        {
            notiIcon = new NotifyIcon();
        }

        public void Display()
        {
            //notiIcon.Icon = new System.Drawing.Icon("kinect.ico");
            notiIcon.Text = "Kinect Pseudo Service";
            notiIcon.Visible = true;
        }

        public void Dispose()
        {
            throw new NotImplementedException();
        }
    }
}
